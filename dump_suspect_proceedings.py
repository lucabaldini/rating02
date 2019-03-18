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



def dump_suspect_proceedings(file_path):
    """Dump a list of papers wich seem proceedings in disguise.
    """
    db = load_db_prod()
    db.select(pub_type='1.1 Articolo in rivista')

    print('Dumping suspect proceedings...')
    # Bookkeeping.
    rows = []

    # Product loop.
    for prod in db:
        handle = prod.handle
        author = prod.author()
        title = prod.title
        journal = prod.journal
        if journal is not None and 'proc' in journal.lower():
            print(handle, author, journal)

    print('Done, %s suspect entries found.' % len(rows))

    # Write the output file.
    #table = ExcelTableDump()
    #col_names = ['Handle', 'Errors', 'Num. Authors', 'Author list']
    #table.add_worksheet('Lista autori sospetta', col_names, rows)
    #table.write(file_path)



if __name__ == '__main__':
    dump_suspect_proceedings('suspect_proceedings.xls')
