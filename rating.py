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

import logging
logging.basicConfig(format='>>> %(message)s', level=logging.DEBUG)



def encode_ascii(unicode_string):
    """Encode a unicode string to ascii.
    """
    return unicode_string.encode('ascii', 'replace').replace('\n', '')



class Publication(object):

    """Class representing a publication.
    """

    FIELD_DICT = {
        'handle'        : 0,
        'author_surname': 1,
        'author_name'   : 2,
        'year'          : 3,
        'title'         : 4,
        'pub_type'      : 5,
        'relevance'     : 6,
        'refereeing'    : 7,
        'ssd'           : 9,
        'author_string' : 18,
        'num_authors'   : 19,
        'doi'           : 22,
        'isbn'          : 23,
        'isi'           : 24,
        'volume'        : 34,
        'journal'       : 35,
        'issn'          : 37,
        'volume_number' : 43,
        'issue_number'  : 44     
    }

    FORMAT_DICT = {
        'year'          : int,
        'num_authors'   : int
    }

    MAX_AUTHOR_STRING_LEN = 3800

    def __init__(self, row, row_index):
        """Constructor from a row of an excel file.
        """
        self.__setattr__('row_index', row_index)
        for (attr, col) in self.FIELD_DICT.items():
            val = row[col].value
            try:
                val = self.FORMAT_DICT[attr](val)
            except KeyError:
                val = encode_ascii(val)
            if not val:
                val = None
            self.__setattr__(attr, val)
        self.truncated = len(self.author_string) >= self.MAX_AUTHOR_STRING_LEN

    def last_author(self):
        """Return the last author in the author string.
        """
        return self.author_string.rsplit(';', 2)[-2].strip()

    def __str__(self):
        """String formatting.
        """
        return '[%s @ row %d for %s %s.], "%s", %s (%d)' %\
            (self.pub_type, self.row_index, self.author_surname,
             self.author_name[:1], self.title, self.journal or self.volume,
             self.year)



class PublicationList(list):

    """Utility class representing the full list of Publication objects from the
    publication excel file.
    """

    def __init__(self, file_path=None, sheet_index=0):
        """Constructor.
        """
        list.__init__(self)
        if file_path is not None:
            logging.info('Opening excel file %s...' % file_path)
            self.workbook = xlrd.open_workbook('Area 02 pubblicazioni.xls')
            logging.info('Loading sheet at index %d...' % sheet_index)
            self.sheet = self.workbook.sheet_by_index(sheet_index)
            logging.info('Done, %d column(s) by %d row(s) found.' %\
                         (self.sheet.ncols, self.sheet.nrows))
            self.__parse()

    def __parse(self, num_rows=None):
        """Parse the content of the file and fill a comprehesive list
        of Publication objects.
        """
        logging.info('Parsing file information...')
        num_rows = num_rows or self.sheet.nrows
        for i in range(1, num_rows):
            pub = Publication(self.sheet.row(i), i + 1)
            self.append(pub)
        logging.info('Done, %d row(s) parsed.' % num_rows)

    def at(self, index):
        """Retrieve the publication at a given index.
        """
        try:
            return self[index]
        except IndexError:
            return None

    def at_row(self, row_index):
        """Retrieve the publication at a given row index in the excel file.
        """
        return self.at(row_index - 2)

    def select(self, quiet=False, **kwargs):
        """Select a subsample of publications based on a given set of
        criteria.
        """
        if kwargs == {}:
            return self
        if not quiet:
            logging.info('Selecting publications with %s...' % kwargs)
        selection = PublicationList()
        for pub in self:
            accept = True
            for (attr, val) in kwargs.items():
                if pub.__getattribute__(attr) != val:
                    accept = False
                    break
            if accept:
                selection.append(pub)
        if not quiet:
            logging.info('Done, %d item(s) selected.' % len(selection))
        return selection

    def match_title(self, pattern, **kwargs):
        """
        """
        logging.info('Selecting titles matching "%s" with %s...' %\
                     (pattern, kwargs))
        selection = PublicationList()
        for pub in self.select(True, **kwargs):
            if pattern.lower() in pub.title.lower():
                selection.append(pub)
        logging.info('Done, %d item(s) selected.' % len(selection))
        return selection

    def match_author_string(self, pattern, **kwargs):
        """
        """
        logging.info('Selecting author strings matching "%s" with %s...' %\
                     (pattern, kwargs))
        selection = PublicationList()
        for pub in self.select(True, **kwargs):
            if pattern.lower() in pub.author_string.lower():
                selection.append(pub)
        logging.info('Done, %d item(s) selected.' % len(selection))
        return selection

    def unique_values(self, field, **kwargs):
        """Basic stat of the unique values for a given field.
        """
        logging.info('Listing unique values for field %s with %s...' %\
                     (field, kwargs))
        selection = self.select(True, **kwargs)
        val_dict = {}
        for pub in selection:
            val = pub.__getattribute__(field)
            if val in val_dict.keys():
                val_dict[val] += 1
            else:
                val_dict[val] = 1
        keys = val_dict.keys()
        keys.sort()
        for key in keys:
            logging.info('%s: %s' % (key, val_dict[key]))
        logging.info('Grand-total: %d entries in %d value(s)' %\
                     (sum(val_dict.values()), len(keys)))
        return val_dict
        


def load_publication_list():
    """Load the publication list from the excel file.
    """
    return PublicationList('Area 02 pubblicazioni.xls')



if __name__ == '__main__':
    pub_list = load_publication_list()
    pub_list.unique_values('pub_type')
