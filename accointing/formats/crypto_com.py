from __future__ import annotations
from enum import Enum
from pathlib import Path
import csv
import typer
import attrs
from datetime import datetime
from typing import List
import cattrs
from itertools import islice
from typing import Union
from collections import namedtuple
from ..types import Unset, UNSET
from ..template.transaction import Order, Withdraw, Deposit
from ..template.classification import WithdrawClassification, DepositClassification

CONVERTER = cattrs.GenConverter()
CONVERTER.register_structure_hook(
    datetime, lambda value, _: datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
)


CONVERTER.register_structure_hook(
    Union[Unset, float], lambda value, _: float(value) if value else UNSET
)


CONVERTER.register_structure_hook(
    Union[Unset, str], lambda value, _: str(value) if value else UNSET
)

HEADER = {
    "Timestamp (UTC)": "timestamp",
    "Transaction Description": "description",
    "Currency": "currency",
    "Amount": "amount",
    "To Currency": "to_currency",
    "To Amount": "to_amount",
    "Native Currency": "native_currency",
    "Native Amount": "native_amount",
    "Native Amount (in USD)": "native_amount_usd",
    "Transaction Kind": "transaction_type",
}


class TransactionType(str, Enum):
    CRYPTO_EXCHANGE = "crypto_exchange"
    CRYPTO_WITHDRAWAL = "crypto_withdrawal"
    CRYPTO_DEPOSIT = "crypto_deposit"
    CRYPTO_PURCHASE = "crypto_purchase"  # e.g. Credit-Card
    VIBAN_DEPOSIT = "viban_deposit"  # FIAT Wallet
    VIBAN_PURCHASE = "viban_purchase"  # FIAT Wallet
    CRYPTO_PAYMENT = "crypto_payment"
    DUST_CONVERSION_DEBITED = "dust_conversion_debited"
    DUST_CONVERSION_CREDITED = "dust_conversion_credited"
    CRYPTO_EARN_INTEREST_PAID = "crypto_earn_interest_paid"


Mapper = namedtuple("Mapper", ["transaction", "classification"])

TRANSACTION = {
    TransactionType.CRYPTO_EXCHANGE: Mapper(Order, UNSET),
    TransactionType.CRYPTO_WITHDRAWAL: Mapper(Withdraw, UNSET),
    TransactionType.CRYPTO_DEPOSIT: Mapper(Deposit, UNSET),
    TransactionType.CRYPTO_PURCHASE: Mapper(Order, UNSET),
    TransactionType.VIBAN_PURCHASE: Mapper(Order, UNSET),
    TransactionType.VIBAN_DEPOSIT: Mapper(Deposit, DepositClassification.ADD_FUNDS),
    TransactionType.CRYPTO_PAYMENT: Mapper(Withdraw, WithdrawClassification.PAYMENT),
    TransactionType.DUST_CONVERSION_DEBITED: Mapper(None, UNSET),
    TransactionType.DUST_CONVERSION_CREDITED: Mapper(None, UNSET),
    TransactionType.CRYPTO_EARN_INTEREST_PAID: Mapper(
        Deposit, DepositClassification.INCOME
    ),
}


@attrs.define()
class Transaction:
    timestamp: datetime
    description: str
    currency: str
    amount: float
    to_currency: Union[Unset, str]
    to_amount: Union[Unset, float]
    native_currency: str
    native_amount: float
    native_amount_usd: float
    transaction_type: TransactionType

    def is_convertible(self) -> bool:
        mapper = TRANSACTION[self.transaction_type]
        return mapper.transaction is not None

    def to_template(self) -> Union[None, Order, Withdraw, Deposit]:
        mapper = TRANSACTION[self.transaction_type]

        if mapper.transaction is None:
            return None
        elif mapper.transaction is Order:
            if self.transaction_type == TransactionType.CRYPTO_PURCHASE:
                return Order(
                    timestamp=self.timestamp,
                    in_buy_amount=self.amount,
                    in_buy_asset=self.currency,
                    out_sell_amount=abs(self.native_amount),
                    out_sell_asset=self.native_currency,
                    comments=self.description,
                )
            else:
                return Order(
                    timestamp=self.timestamp,
                    in_buy_amount=self.to_amount,
                    in_buy_asset=self.to_currency,
                    out_sell_amount=abs(self.amount),
                    out_sell_asset=self.currency,
                    comments=self.description,
                )
        elif mapper.transaction is Withdraw:
            return Withdraw(
                timestamp=self.timestamp,
                out_sell_amount=abs(self.amount),
                out_sell_asset=self.currency,
                classification=mapper.classification,
                comments=self.description,
            )
        elif mapper.transaction is Deposit:
            return Deposit(
                timestamp=self.timestamp,
                in_buy_amount=self.amount,
                in_buy_asset=self.currency,
                classification=mapper.classification,
                comments=self.description,
            )


@attrs.define()
class CryptoCom:
    transactions: List[Transaction]

    @classmethod
    def loader(cls, path: Path) -> CryptoCom:
        transactions = list()
        with open(path) as f:
            content = f.read()
            f.seek(0)

            dialect = csv.Sniffer().sniff(content)
            header = csv.Sniffer().has_header(content)
            if not header:
                typer.echo(
                    "Cannot read a crypto.com CSV-File without a header. Sure format is correct?"
                )
                typer.Exit()

            reader = csv.DictReader(f, fieldnames=HEADER.values(), dialect=dialect)
            for row in islice(reader, 1, None):
                transaction = CONVERTER.structure(row, Transaction)
                transactions.append(transaction)

        return cls(transactions=transactions)
