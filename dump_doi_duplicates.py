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

from rating import load_db, logging



def dump_doi_duplicates(file_path=None):
    """Dump a list of papers with the same DOI and different unique handles.
    """
    db = load_db()
        
    logging.info('Dumping DOI duplicates...')

    # Some bookkeeping variables.
    handle_dict = {}
    doi_dict = {}
    num_errors = 0
    error_doi_list = []

    #Start the loop.
    for pub in db:
        doi = pub.doi
        if doi is not None:
            handle = pub.handle
            label = '%s @ row %d.' % (pub.author(), pub.row_index)
            if handle_dict.has_key(handle):
                handle_dict[handle].append(label)
            else:
                handle_dict[handle] = [label]
            if doi_dict.has_key(doi):
                try:
                    assert handle in doi_dict[doi]
                except AssertionError:
                    num_errors += 1
                    doi_dict[doi].append(handle)
                    error_doi_list.append(doi)
                    logging.error('Duplicated DOI (%s) for %s' % (doi, pub))
            else:
                doi_dict[doi] = [handle]
    logging.info('%d error(s) found.' % num_errors)

    # Write the output file.
    if file_path is not None:
        logging.info('Writing output file %s...' % file_path)
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Duplicati DOI')
        cells = ['DOI',
                 'Handle 1',
                 'Handle 2',
                 'Handle 3',
                 'Handle 4',
                 'Handle 5'
        ]
        for col, value in enumerate(cells):
            worksheet.write(0, col, value)
        for i, doi in enumerate(error_doi_list):
            worksheet.write(i + 1, 0, doi)
            for col, value in enumerate(doi_dict[doi]):
                value = '%s %s' % (value, handle_dict[value])
                worksheet.write(i + 1, col + 1, value)
        workbook.save(file_path)
        logging.info('Done.')


if __name__ == '__main__':
    dump_doi_duplicates('doi_duplicates.xls')
