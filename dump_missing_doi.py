#!/usr/bin/env python
#
# Copyright (C) 2019, Luca Baldini.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import xlwt

from rating import load_db_prod, dump_excel_table



def dump_missing_doi(file_path=None):
    """Dump a list of papers in (supposedly) refereed journals missing the
    DOI field.
    """
    db = load_db_prod().select(pub_type='1.1 Articolo in rivista', doi=None)
    print('Dumping suspect author lists...')

    # Bookkeeping.
    rows = []

    # Product loop.
    for prod in db:
        handle = prod.handle
        print(prod)
        rows.append([handle, prod.pub_type, prod.author(), prod.title,
                     prod.journal, prod.year, prod.impact_factor()])
    print('Done, %s suspect entries found.' % len(rows))

    # Write the output file.
    if file_path is not None:
        col_names = ['Handle', 'Author', 'Title', 'Journal', 'Year',
                     'Impact factor']
        dump_excel_table(file_path, 'Missing DOI', col_names, rows)


if __name__ == '__main__':
    dump_missing_doi('missing_doi.xls')
