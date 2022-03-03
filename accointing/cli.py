import typer
from pathlib import Path
from enum import Enum
from .formats import CryptoCom
from .template import Upload


class InputFileFormat(str, Enum):
    CRYPTO_COM = "crypto.com"


LOADER = {InputFileFormat.CRYPTO_COM: CryptoCom.loader}

app = typer.Typer()


@app.callback()
def callback():
    """
    A simple CLI for Accointing.com
    """


@app.command()
def convert(format: InputFileFormat, path: Path, out: Path):
    """
    Convert from a file given by an exchange to the Accointing.com template format.
    """
    file = LOADER[format](path)

    # Convert to template
    transactions = [
        transaction.to_template()
        for transaction in file.transactions
        if transaction.is_convertible()
    ]

    # Write to out-file
    upload = Upload(transactions=transactions)
    upload.write(out)
