``ally2ledger.py``
==================

This is a simple script for converting exported Ally Bank CSV files into a
Ledger CLI compatible data file. It works by reading the source CSV file,
writing a temporary CSV file, and then converting the temporary CSV file into
a Ledger CLI compatible data file. You can then take the data file, adjust the
formatting, and add it to your primary ledger data file.

Usage
-----

Usage is simple:

::

    # Retrieve Ally Bank CSV export
    $ ./ally2ledger.py "Assets:Liquid:Ally:Checking" ~/Downloads/transactions.csv output.data

For more information, please reference ``ally2ledger.py --help``
