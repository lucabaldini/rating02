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



def dump_suspect_author_lists(file_path=None, max_author_length=3799,
                              collab_author_threshold=20):
    """Dump a list of papers with suspect author lists.
    """
    db = load_db_prod()
    print('Dumping suspect author lists...')

    # Bookkeeping.
    rows = []
    suspect_handles = []

    # Product loop.
    for prod in db:
        handle = prod.handle
        authors = prod.author_string.lower()
        num_authors = prod.num_authors
        num_splits = len(authors.split(';'))
        error_summary = []
        if len(authors) < max_author_length and num_authors != num_splits:
            error_summary.append('split mismatch (%d)' % num_splits)
        if 'et al' in authors:
            error_summary.append('contains "et al"')
        if 'author' in authors:
            error_summary.append('contains "author"')
        if 'collab' in authors and num_authors < collab_author_threshold:
            error_summary.append('collab')
        if len(error_summary) > 0:
            if handle not in suspect_handles:
                print('%s, %s' % (prod, error_summary))
                rows.append([handle, error_summary, num_authors, authors])
                suspect_handles.append(handle)
    print('Done, %s suspect entries found.' % len(rows))

    # Write the output file.
    if file_path is not None:
        col_names = ['Handle', 'Errors', 'Num. Authors', 'Author list']
        dump_excel_table(file_path, 'Suspect author lists', col_names, rows)


if __name__ == '__main__':
    dump_suspect_author_lists('suspect_author_lists.xls')
