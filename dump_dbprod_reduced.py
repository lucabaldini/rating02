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


def dump_dbprod_reduced(file_path):
    """
    """
    db = load_db_prod()
    col_names = [
        'handle',
        'pub_type',
        'author_name',
        'author_surname',
        'title',
        'journal',
        'year',
        'doi',
        'isbn',
        'wos_jif',
        'wos_j5yif'
    ]
    rows = []
    for prod in db:
        row = [prod.__getattribute__(key) for key in col_names]
        rows.append(row)
    table = ExcelTableDump()
    table.add_worksheet('DB prodotti ridotto', col_names, rows)
    table.write(file_path)



if __name__ == '__main__':
    dump_dbprod_reduced('db_prodotti_ridotto.xls')
