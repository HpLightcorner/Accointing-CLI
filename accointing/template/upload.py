from typing import List, Union
import attrs
from pathlib import Path
import csv
import json
from .transaction import Order, Withdraw, Deposit
from .header import HEADER


@attrs.define()
class Upload:
    transactions: List[Union[Order, Withdraw, Deposit]]

    def write(self, path: Path):
        with open(path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)

            writer.writeheader()

            for transaction in self.transactions:
                row = transaction.unstructure()
                writer.writerow(row)
