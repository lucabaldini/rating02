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


from rating import load_publication_list, logging


PUBS = load_publication_list()
PUBS.unique_values('pub_type')



def check_journal():
    """All the journal articles must have the journal field set
    """
    selection = PUBS.select(pub_type='1.1 Articolo in rivista',
                                journal=None)
    assert len(selection) == 0


def check_articles():
    """
    """
    selection = PUBS.select(pub_type='1.1 Articolo in rivista', doi=None)
    for pub in selection:
        print(pub)


def check_monographies():
    """All monographies have an ISBN?
    """
    selection = PUBS.select(pub_type='3.1 Monografia o trattato scientifico',
                            isbn=None)
    for pub in selection:
        print(pub)


def check_volume():
    """
    """
    selection = PUBS.select(journal=None, volume=None)
    selection.unique_values('pub_type')
    for pub in selection:
        print pub


def check_author_string():
    """
    """
    logging.info('Checking author string...')
    selection = PUBS.select(author_string=None)
    assert len(selection) == 0
    logging.info('No publications with empty author string---good.')

    def print_info(pub):
        """
        """
        print(pub)
        print('Author string: %s' % pub.author_string)
        print('# authors: %s' % pub.num_authors)
        print('DOI: %s' % pub.doi)
    
    logging.info('"author" in author string?')
    n = 0
    for pub in PUBS:
        if 'author' in pub.author_string:
            print_info(pub)
            n += 1
    logging.info('%d suspicious entries found.\n' % n)
    logging.info('"collaboration" in author string and a few authors?')
    n = 0
    for pub in PUBS:
        if 'collaboration' in pub.author_string.lower() and\
           pub.num_authors < 20:
            print_info(pub)
            n += 1
    logging.info('%d suspicisous entries found.\n' % n)
    logging.info('"at al" in author string?')
    n = 0
    for pub in PUBS:
        if 'et al' in pub.author_string.lower():
            print_info(pub)
            n += 1
    logging.info('%d suspicisous entries found.\n' % n)
    


if __name__ == '__main__':
    #check_journal()
    #check_articles()
    #check_monographies()
    #check_volume()
    check_author_string()
