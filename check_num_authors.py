#!/usr/bin/env python
#
# Copyright (C) 2017, Luca Baldini.
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


import xlrd
import xlwt

import logging
logging.basicConfig(format='>>> %(message)s', level=logging.DEBUG)


def check_num_authors():
    """
    """
    arpi_dict = {}
    for line in open('author_dump.txt'):
        handle, num_authors = line.strip('\n').split()
        if num_authors != 'None':
            num_authors = int(num_authors)
        arpi_dict[handle] = num_authors    
    workbook = xlrd.open_workbook('Area-02-Numero-Autori.xls')
    sheet = workbook.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        row = sheet.row(i)
        handle = row[4].value
        num_authors = int(row[8].value)
        try:
            assert num_authors == arpi_dict[handle]
        except KeyError:
            logging.warn('Handle %s @ row %d not retrieved from ARPI' %\
                         (handle, i + 1))
        except AssertionError:
            logging.error('Error for handle %s @ row %d (%s vs. %s)' %\
                          (handle, i + 1, num_authors, arpi_dict[handle]))


if __name__ == '__main__':
    check_num_authors()
