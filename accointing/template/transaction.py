from __future__ import annotations
import attrs
import cattrs
from enum import Enum
from datetime import datetime
from typing import Union, Dict
from ..types import Unset, UNSET
from .classification import DepositClassification, WithdrawClassification
from .header import OVERRIDE


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    ORDER = "order"


@attrs.define(kw_only=True)
class Transaction:
    timestamp: datetime
    fee_amount: Union[Unset, float] = UNSET
    fee_asset: Union[Unset, str] = UNSET
    classification: Union[Unset, DepositClassification, WithdrawClassification] = UNSET
    operation_id: Union[Unset, str] = UNSET
    comments: Union[Unset, str] = UNSET

    def converter(self, t) -> cattrs.Converter:
        c = cattrs.GenConverter()

        c.register_unstructure_hook(Unset, lambda _: "")
        c.register_unstructure_hook(datetime, lambda v: v.strftime("%m/%d/%Y %H:%M:%S"))

        unst_hook = cattrs.gen.make_dict_unstructure_fn(t, c, **OVERRIDE)
        c.register_unstructure_hook(t, unst_hook)
        return c


@attrs.define(kw_only=True)
class Deposit(Transaction):
    transaction_type: TransactionType = attrs.field(
        default=TransactionType.DEPOSIT, on_setattr=attrs.setters.frozen
    )
    in_buy_amount: float
    in_buy_asset: str

    def unstructure(self) -> Dict:
        c = self.converter(Deposit)
        res = c.unstructure(self)
        return c.unstructure(self)


@attrs.define(kw_only=True)
class Withdraw(Transaction):
    transaction_type: TransactionType = attrs.field(
        default=TransactionType.WITHDRAW, on_setattr=attrs.setters.frozen
    )
    out_sell_amount: float
    out_sell_asset: str

    def unstructure(self) -> Dict:
        c = self.converter(Withdraw)
        res = c.unstructure(self)
        return c.unstructure(self)


@attrs.define(kw_only=True)
class Order(Transaction):
    transaction_type: TransactionType = attrs.field(
        default=TransactionType.ORDER, on_setattr=attrs.setters.frozen
    )
    in_buy_amount: float
    in_buy_asset: str
    out_sell_amount: float
    out_sell_asset: str

    def unstructure(self) -> Dict:
        c = self.converter(Order)
        res = c.unstructure(self)
        return c.unstructure(self)
