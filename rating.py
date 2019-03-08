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


import xlrd
import xlwt

import logging
logging.basicConfig(format='>>> %(message)s', level=logging.DEBUG)


def encode_ascii(unicode_string):
    """Encode a unicode string to ascii.
    """
    return unicode_string.encode('ascii', 'replace').replace('\n', '')


DB_FILE_PATH = '../a02_pubblicazioni.xlsx'


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

    def write(self, worksheet, row):
        """Write the basic article info to a worksheet.
        """
        cells = [self.handle, self.row_index, self.author(), self.title,
                 self.author_string, self.num_authors,
                 self.journal or self.volume, self.year, self.doi, self.wos_jif]
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
        impact_factor = self.wos_j5yif
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

        logger.error('Cannot calculate weight...')
        return 0

    def __str__(self):
        """String formatting.
        """
        return '[%s @ row %d for %s], "%s" (%d)' %\
            (self.pub_type, self.row_index, self.author(), self.title,
             self.year)



class ProductDatabase(list):

    """Utility class representing the full list of Product objects from the
    publication excel file.
    """

    def __init__(self, file_path=None, sheet_index=0):
        """Constructor.
        """
        list.__init__(self)
        if file_path is not None:
            logging.info('Opening excel file %s...' % file_path)
            self.workbook = xlrd.open_workbook(file_path)
            logging.info('Loading sheet at index %d...' % sheet_index)
            self.sheet = self.workbook.sheet_by_index(sheet_index)
            logging.info('Done, %d column(s) by %d row(s) found.' %\
                         (self.sheet.ncols, self.sheet.nrows))
            self.__parse()

    def __parse(self, num_rows=None):
        """Parse the content of the file and fill a comprehesive list
        of Product objects.
        """
        logging.info('Parsing file information...')
        num_rows = num_rows or self.sheet.nrows
        for i in range(1, num_rows):
            pub = Product(self.sheet.row(i), i + 1)
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

    def dump_journal_list(self, file_path):
        """Dump an excel file containing all the relevant information for
        the journals.
        """
        logging.info('Dumping journal list...')
        journal_dict = {}
        num_errors = 0
        error_dict = {}
        for pub in self:
            journal = pub.journal
            if journal is not None:
                # Retrieve impact factor and year.
                jif = pub.wos_jif
                year = pub.year
                # Journal already in the dict?
                if journal_dict.has_key(journal):                    
                    entry = journal_dict[journal]
                    entry['num'] += 1
                    if entry.has_key(year):
                        try:
                            assert jif == entry[year]
                        except AssertionError:
                            num_errors += 1
                            key = (journal, year)
                            if error_dict.has_key(key):
                                error_dict[key] += 1
                            else:
                                error_dict[key] = 1
                            logging.error('IF mismatch @ row %d for %s' %\
                                          (pub.row_index, journal))
                            logging.error('Year %d, exp. %s, obs. %s' %\
                                          (year, entry[year], jif))
                            # If the IF was None and now we see something,
                            # most likely it was the previous value being
                            # guilty.
                            if entry[year] is None:
                                logging.info('Overwriting IF for year %s...' %\
                                             (year))
                                entry[year] = jif
                    else:
                        entry[year] = jif
                # Otherwise add the journal.
                else:
                    journal_dict[journal] = {year: jif, 'num': 1}
        logging.info('%d error(s) found.' % num_errors)
        logging.info('Error details: %s' % error_dict)
        keys = journal_dict.keys()
        keys.sort()
        if file_path is not None:

            def __jif(journal, year):
                """
                """
                try:
                    return journal_dict[journal][year]
                except KeyError:
                    return None
            
            logging.info('Writing output file %s...' % file_path)
            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet('Riviste')
            cells = ['Rivista',
                     'Occorrenze',
                     'IF 2013',
                     'IF 2014',
                     'IF 2015',
                     'IF 2016'
            ]
            for col, value in enumerate(cells):
                worksheet.write(0, col, value)
            for i, journal in enumerate(keys):
                cells = [journal,
                         journal_dict[journal]['num'],
                         __jif(journal, 2013),
                         __jif(journal, 2014),
                         __jif(journal, 2015),
                         __jif(journal, 2016)
                ]
                for col, value in enumerate(cells):
                    worksheet.write(i + 1, col, value)
            workbook.save(file_path)
            logging.info('Done.')

    def dump_nojif_journals(self, file_path):
        """Dump the list of publications with no impact factor.
        """
        logging.info('Dumping the list of journals with no impact factor...')
        all_dict = {}
        nojif_dict = {}
        for pub in self:
            journal = pub.journal
            year = pub.year
            if journal is not None:
                if all_dict.has_key(journal):
                    entry = all_dict[journal]
                    if entry.has_key(year):
                        entry[year] += 1
                    else:
                        entry[year] = 1
                else:
                    all_dict[journal] = {year: 1}
                jif = pub.wos_jif
                if jif is None:                    
                    if nojif_dict.has_key(journal):
                        entry = nojif_dict[journal]
                        if entry.has_key(year):
                            entry[year] += 1
                        else:
                            entry[year] = 1
                    else:
                        nojif_dict[journal] = {year: 1}
        if file_path is not None:
            logging.info('Writing output file %s...' % file_path)
            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet('Duplicati DOI')
            keys = nojif_dict.keys()
            keys.sort()
            cells = ['Rivista',
                     'Articoli senza IF 2013',
                     'Articoli senza IF 2014',
                     'Articoli senza IF 2015',
                     'Articoli senza IF 2016'
            ]
            for col, value in enumerate(cells):
                worksheet.write(0, col, value)
            for row, journal in enumerate(keys):
                worksheet.write(row + 1, 0, journal)
                for col, year in enumerate([2013, 2014, 2015, 2016]):
                    try:
                        num = nojif_dict[journal][year]
                    except KeyError:
                        num = 0
                    try:
                        denom = all_dict[journal][year]
                    except KeyError:
                        denom = 0
                    value = '%d/%d' % (num, denom)
                    worksheet.write(row + 1, col + 1, value)
            workbook.save(file_path)
            logging.info('Done.')

    def dump_pubs_no_doi(self, file_path):
        """Dump a list of publications with no DOI.
        """
        logging.info('Dumping the list of publications with no DOI...')
        selection = self.select_journal_pubs(doi=None)
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Articoli no DOI')
        for row, pub in enumerate(selection):
            pub.write(worksheet, row)
        workbook.save(file_path)
        logging.info('Done.')

    def dump_pubs_with_suspect_author_list(self, file_path):
        """
        """
        logging.info('Dumping publications with suspect author list...')
        author_dict = {}
        for line in open('author_dump.txt'):
            handle, num_authors = line.strip('\n').split()
            try:
                num_authors = int(num_authors)
            except:
                num_authors = 0
            author_dict[handle] = num_authors
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Articoli sospetti')
        row = 1
        for pub in self:
            authors = pub.author_string.lower()
            if 'et al' in authors or 'author' in authors or \
               'collaboration' in authors and pub.num_authors < 50:
                pub.write(worksheet, row)
                worksheet.write(row, 10, author_dict[pub.handle])
                row += 1
        workbook.save(file_path)
        logging.info('Done.')

        

def load_db():
    """Load the publication list from the excel file.
    """
    return ProductDatabase('../a02_pubblicazioni.xlsx')



if __name__ == '__main__':
    db = load_db()
    vals = db.unique_values('pub_type')
    books = db.select(pub_type='3.1 Monografia o trattato scientifico')
    for book in books:
        print(book)
    others = db.select(pub_type='5.12 Altro')
    for item in others:
        print(item)
    
    #pub_list.dump_journal_list('py_lista_riviste.xls')
    #pub_list.dump_nojif_journals('py_riviste_no_doi.xls')
    #pub_list.dump_pubs_no_doi('py_articoli_no_doi.xls')
    #pub_list.dump_pubs_with_suspect_author_list('py_articoli_lista_autori_sospetta.xls')
