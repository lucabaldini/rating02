#!/usr/bin/env python
#
# Copyright (C) 2017--2019, Luca Baldini.
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

import os
import pickle
import logging
logging.basicConfig(format='>>> %(message)s', level=logging.DEBUG)

import xlrd
import xlwt


def encode_ascii(unicode_string):
    """Encode a unicode string to ascii.
    """
    return unicode_string.encode('ascii', 'replace').replace('\n', '')


def dump_excel_table(file_path, worksheet_name, col_names, rows):
    """
    """
    logging.info('Writing data table to %s...' % file_path)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(worksheet_name)
    for col, name in enumerate(col_names):
        worksheet.write(0, col, name)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            worksheet.write(i + 1, j, val)
    workbook.save(file_path)
    logging.info('Done.')




DB_PROD_FILE_PATH = 'db_prodotti.xlsx'
DB_PERS_FILE_PATH = 'db_docenti.xlsx'



class Product(object):

    """Class representing a generic product (i.e., a row in the input excel
    file).
    """

    FIELD_DICT = {
        'handle'        : 0,
        'year'          : 1,
        'title'         : 2,
        'pub_type'      : 3,
        'author_name'   : 7,
        'author_surname': 8,
        'author_string' : 30,
        'num_authors'   : 31,
        'doi'           : 38,
        'isbn'          : 40,
        'volume'        : 64,
        'journal'       : 54,
        'wos_jif'       : 124,
        'wos_j5yif'     : 129
    }

    FORMAT_DICT = {
        'year'          : int,
        'num_authors'   : int,
        'wos_jif'       : float,
        'wos_j5yif'     : float
    }

    SUB_AREA_DICT = {
        'a'             : 'Sperimentali grandi collaborazioni',
        'b'             : 'Sperimentali piccole collaborazioni',
        'c'             : 'Teorici'
    }

    WEIGHTING_INDEX_DICT = {
        'a'             : 0.3333333333333,
        'b'             : 0.3333333333333,
        'c'             : 0.5
    }
    
    def __init__(self, row, row_index):
        """Constructor from a row of an excel file.
        """
        self.__setattr__('row_index', row_index)
        for (attr, col) in self.FIELD_DICT.items():
            val = row[col].value
            try:
                val = self.FORMAT_DICT[attr](val)
            except:
                val = encode_ascii(val)
            if not val:
                val = None
            self.__setattr__(attr, val)

    def last_author(self):
        """Return the last author in the author string.
        """
        return self.author_string.rsplit(';', 2)[-2].strip()

    def author(self):
        """Concatenate the author name and surname.
        """
        return '%s, %s.' % (self.author_surname, self.author_name[:1])

    def impact_factor(self):
        """Return the impact factor of the jornal.
        """
        return self.wos_j5yif

    def write(self, worksheet, row):
        """Write the basic article info to a worksheet.
        """
        cells = [self.handle, self.row_index, self.author(), self.title,
                 self.author_string, self.num_authors,
                 self.journal or self.volume, self.year, self.doi,
                 self.impact_factor()]
        for col, value in enumerate(cells):
            worksheet.write(row, col, value)

    @classmethod
    def _weighting_index(self, sub_area):
        """Return the weighting index for the rating evaluation for publications
        in journals and proceedings.
        """
        return self.WEIGHTING_INDEX_DICT[sub_area]

    def _weight_to_rating_points(self, weight, sub_area):
        """Convert the weight to actual rating points for publications
        in journals and proceedings.
        """
        q = self._weighting_index(sub_area)
        return 6. * weight / min(self.num_authors**q, 10.)

    def rating_points(self, sub_area):
        """Return the rating points for the product.

        Mind this is the main function encapsulating all the logic for the
        rating evaluation.
        """
        impact_factor = self.impact_factor()
        pub_type = self.pub_type

        if pub_type == '1.1 Articolo in rivista':
            if impact_factor is None:
                w = 0.2
            elif impact_factor < 1:
                w = 0.6
            elif impact_factor < 3:
                w = 1.
            else:
                w = 1.3
            return self._weight_to_rating_points(w, sub_area)

        if pub_type == '1.5 Abstract in rivista':
            return 0.

        if pub_type == '1.6 Traduzione in rivista':
            return 0.

        if pub_type == '2.1 Contributo in volume':
            if impact_factor is None:
                return 0.
            else:
                return 0.6

        if pub_type == '2.2 Prefazione/Postfazione':
            return 0.

        if pub_type == '2.3 Breve introduzione':
            return 0.

        if pub_type == '3.1 Monografia o trattato scientifico':
            # FIXME: to be implemented
            return 0.

        if pub_type == '3.8 Traduzione di libro':
            # FIXME: to be discussed
            return 0.

        if pub_type == '4.1 Contributo in Atti di convegno':
            if impact_factor is None:
                w = 0.
            else:
                w = 0.3
            return self._weight_to_rating_points(w, sub_area)   

        if pub_type == '4.2 Abstract in Atti di convegno':
            return 0.

        if pub_type == '4.3 Poster':
            return 0.

        if pub_type == '5.12 Altro':
            # FIXME: to be discussed
            return 0.

        if pub_type == '6.1 Brevetto':
            # FIXME: to be discussed
            return 0.

        if pub_type == '7.1 Curatela':
            # FIXME: to be discussed.
            return 0.

        logging.error('Cannot calculate weight...')
        return 0

    def __str__(self):
        """String formatting.
        """
        return '[%s @ row %d for %s], "%s" (%d)' %\
            (self.pub_type[:4], self.row_index, self.author(), self.title,
             self.year)


    
class Database(list):

    """Base class for a database.

    A few notes about the logic. We read each of the databases from excel
    files, and this class is acting as a base class for all the real db
    instances (i.e., the product and docent db). The __init__() method does
    all the bookkeeping work, while the actual internal of how the information
    in the excel files is used is delegated to the parse() method, which is
    no-ops in the base class and must be reimplemented in sub-classes.

    Since the product database is generally quite large, and most of its
    information is irrelvant for our purposes, in order to decrease the
    bootstrap time, we do create a pickles version of the database on the
    first read and use that for subsequent accesses. (Simply remove the pickle
    file to recreate it.)

    Note that none of the xlrd object is preserved as class members, since
    that would make pickling problematic.
    """

    def __init__(self, file_path=None, sheet_index=0):
        """Constructor.        
        """
        list.__init__(self)
        # If file_path is None create an empty database (this is used for
        # the underlying selction mechanism.)
        if file_path is None:
            return
        pickle_file_path = '%s.pickle' % file_path
        # Case 1: the pickled file path exists, so use it.
        if os.path.exists(pickle_file_path):
            logging.info('Loading pickled db from %s...' % pickle_file_path)
            for item in pickle.load(open(pickle_file_path, 'rb')):
                self.append(item)
        # Case 2: read the actual data from the original excel file.
        else:
            logging.info('Opening excel file %s...' % file_path)
            workbook = xlrd.open_workbook(file_path)
            logging.info('Loading sheet at index %d...' % sheet_index)
            sheet = workbook.sheet_by_index(sheet_index)
            logging.info('Done, %d column(s) by %d row(s) found.' %\
                         (sheet.ncols, sheet.nrows))
            self.parse(sheet)
            logging.info('Dumping pickled db to %s...' % pickle_file_path)
            pickle.dump(self, open(pickle_file_path, 'wb'))

    def parse(self, sheet):
        """Do-nothing parse mehod to be reimplemented in derived classes.
        """
        raise NotImplementedError



class ProductDatabase(Database):

    """Utility class representing the full list of Product objects from the
    publication excel file.
    """

    def parse(self, sheet, num_rows=None):
        """Parse the content of the file and fill a comprehesive list
        of Product objects.
        """
        logging.info('Parsing file information...')
        num_rows = num_rows or sheet.nrows
        for i in range(1, num_rows):
            pub = Product(sheet.row(i), i + 1)
            self.append(pub)
        logging.info('Done, %d row(s) parsed.' % num_rows)

    def select(self, quiet=False, **kwargs):
        """Select a subsample of publications based on a given set of
        criteria.
        """
        if kwargs == {}:
            return self
        if not quiet:
            logging.info('Selecting publications with %s...' % kwargs)
        selection = ProductDatabase()
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

    def select_journal_pubs(self, quiet=False, **kwargs):
        """Select all the publications on a journal (i.e., where the journal
        field is not None).
        """
        selection = ProductDatabase()
        for pub in self:
            if pub.journal is not None:
                selection.append(pub)
        if kwargs != {}:
            selection = selection.select(quiet, **kwargs)
        return selection

    def match_title(self, pattern, **kwargs):
        """
        """
        logging.info('Selecting titles matching "%s" with %s...' %\
                     (pattern, kwargs))
        selection = ProductDatabase()
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
        selection = ProductDatabase()
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


    
class Docent:

    """Basic class representing a docent.
    """

    def __init__(self, identifier, full_name, sc, ssd):
        """Constructor.
        """
        self.identifier = identifier
        self.full_name = full_name
        self.sc = sc
        self.ssd = ssd

    def __str__(self):
        """String formatting.
        """
        return self.full_name


    
class DocentDatabase(Database):

    """Class representing the person database.
    """

    def parse(self, sheet):
        """Parse method.
        """
        pass
    

        

def load_db_prod():
    """Load the publication list from the excel file.
    """
    return ProductDatabase(DB_PROD_FILE_PATH)


def load_db_pers():
    """Load the personnel DB from the excel file.
    """
    return DocentDatabase(DB_PERS_FILE_PATH)



if __name__ == '__main__':
    db1 = load_db_prod()
    db2 = load_db_pers()
