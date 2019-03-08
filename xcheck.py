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


from rating import load_db_prod, logging, ProductDatabase


DB = load_db_prod()


def basic_info():
    """
    """
    vals = DB.unique_values('pub_type')
    books = DB.select(pub_type='3.1 Monografia o trattato scientifico')
    for book in books:
        print(book)
    others = DB.select(pub_type='5.12 Altro')
    for item in others:
        print(item)


def check_journal():
    """All the journal articles must have the journal field set
    """
    sel = DB.select(pub_type='1.1 Articolo in rivista', journal=None)
    assert len(sel) == 0


def check_article_doi():
    """Dump a list of all the articles with no DOI.
    """
    sel = DB.select(pub_type='1.1 Articolo in rivista', doi=None)
    for item in sel:
        print(item)


def check_monography_isbn():
    """All monographies have an ISBN?

    FIXME: restore the isbn field.
    """
    sel = DB.select(pub_type='3.1 Monografia o trattato scientifico', isbn=None)
    for item in sel:
        print(item)
  


if __name__ == '__main__':
    basic_info()
    check_journal()
    #check_article_doi()
    check_monography_isbn()
    #check_author_string()

