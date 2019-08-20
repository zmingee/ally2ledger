#!/bin/python
"""
``ally2ledger.py`` is a Python 3.7+ script for converting an exported Ally Bank
CSV to a Ledger CLI compatible data file.
"""

from typing import Dict, List
import argparse
import csv
import logging
import subprocess
import sys
import tempfile

LOGGER = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Convert Ally Bank CSV export to Ledger-compatible output'
    )
    parser.add_argument('account', help='Ledger account name')
    parser.add_argument(
        'input',
        metavar='INPUT-FILE',
        help='Ally Bank CSV file to convert'
    )
    parser.add_argument(
        'output',
        metavar='OUTPUT-FILE',
        help='Path to Ledger-compatible output file'
    )

    return parser.parse_args()


def read_input_csv(path: str) -> List[Dict[str, str]]:
    """
    Read the input CSV file and deserialize data.

    :param str path: Path to input CSV file
    :return: List of CSV rows
    :rtype: List[Dict[str, str]]
    """

    transactions = []
    with open(path, 'r') as input_fp:
        input_reader = csv.DictReader(
            input_fp,
            fieldnames=[
                "date",
                "time",
                "amount",
                "type",
                "description"
            ],
            dialect=csv.unix_dialect
        )
        for (idx, row) in enumerate(input_reader):
            if not idx:
                continue
            transactions.append(row)

    transactions.reverse()

    return transactions


def write_output_csv(transactions: List[Dict[str, str]]) -> str:
    """
    Write the temporary output CSV file for Ledger to convert.

    :param transactions: List of transactions to add to CSV
    :return: Path to output CSV file
    :rtype: str
    """

    # pylint: disable=line-too-long
    with tempfile.NamedTemporaryFile('w', prefix='ledger-', suffix='.csv', newline='', delete=False) as fp:
        output_writer = csv.DictWriter(
            fp,
            dialect=csv.unix_dialect,
            fieldnames=[
                'amount',
                'date',
                'description',
                'note'
            ]
        )

        output_writer.writeheader()

        for row in transactions:
            output_writer.writerow({
                'amount': row['amount'],
                'date': row['date'],
                'description': row['description'],
                'note': row['type']
            })

    return fp.name


def convert_csv(input_csv: str, account: str) -> None:
    """
    Convert an input CSV file into a Ledger CLI compatible data file.

    :param str input_csv: Path to input CSV file
    :param str account: Name of account to associate with transactions
    :return: Does not return
    :rtype: None
    """

    cmd = (
        f'ledger convert {input_csv} '
        '--input-date-format "%Y-%m-%d" '
        f'--account {account} '
    )
    proc = subprocess.run(cmd.split(' '), capture_output=True, check=True)

    return proc.stdout


def main(args: argparse.Namespace) -> None:
    """
    Read an input CSV file, write a temporary CSV output file, and then convert
    the output file to a Ledger CLI compatible data file.
    """

    transactions = read_input_csv(args.input)
    output = write_output_csv(transactions)
    stdout = convert_csv(output, args.account)

    with open(args.output, 'wb') as fp:
        fp.write(stdout)

    sys.exit(0)


if __name__ == "__main__":
    main(_parse_args())

#  vim: set ts=8 sw=4 tw=0 et :
