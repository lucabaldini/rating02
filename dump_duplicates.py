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


def dump_duplicates(file_path):
    """Dump a list of papers with the same DOI and different unique handles.
    """
    db_prod = load_db_prod()
    db_pers = load_db_pers()

    print('Searching for duplicates...')
    rows = []
    for pers in db_pers:
        prods = db_prod.select(author_full_name=pers.full_name)
        unique = ProductDatabase()
        for prod in prods:
            try:
                duplicate = unique[unique.index(prod)]
                print('%s is a duplicate of %s.' % (prod, duplicate))
                row = [pers.full_name, prod.row_index, prod.handle, prod.doi,
                       prod.title, prod.journal, prod.year,
                       prod.impact_factor(), duplicate.row_index,
                       duplicate.handle, duplicate.doi, duplicate.title,
                       duplicate.journal, duplicate.year,
                       duplicate.impact_factor()]
                rows.append(row)
            except ValueError:
                unique.append(prod)

    print('Dumping duplicates...')
    table = ExcelTableDump()
    col_names = ['Autore', 'Riga 1', 'Handle 1', 'DOI 1', 'Titolo 1',
                 'Rivista 1', 'Anno 1', 'Impact factor 1', 'Riga 2', 'Handle 2',
                 'DOI 2', 'Titolo 2', 'Rivista 2', 'Anno 2', 'Impact factor 2']
    table.add_worksheet('Duplicati', col_names, rows)        
    table.write(file_path)
        


if __name__ == '__main__':
    dump_duplicates('duplicates.xls')
