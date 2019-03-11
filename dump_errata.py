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


from rating import *


def dump_errata(file_path):
    """Dump a list of papers with the same DOI and different unique handles.
    """
    db_prod = load_db_prod()

    print('Searching for errata...')
    rows = []
    for prod in db_prod:
        title = prod.title.lower()
        if title.startswith('errat') or title.startswith('corrig'):
            print('Erratum @ row %d for %s' %\
                  (prod.row_index, prod.author_surname))
            row = [prod.author_surname, prod.row_index, prod.handle, prod.title]
            rows.append(row)

    print('Dumping errata...')
    table = ExcelTableDump()
    col_names = ['Autore', 'Riga', 'Handle', 'Titolo']
    table.add_worksheet('Errata', col_names, rows)        
    table.write(file_path)
        


if __name__ == '__main__':
    dump_errata('errata.xls')
