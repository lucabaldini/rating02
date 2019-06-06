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


import numpy
import matplotlib.pyplot as plt

from rating import *

import _rating2018 as _rating


CANDIDATES = ['BONATI CLAUDIO',
              'CAMARLINGHI NICCOLO\'',
              'CASAROSA GIULIA',
              'CIGNONI MICHELE']
YEAR = 2018


def go():
    """
    """
    db_prod = load_db_prod()
    db_pers = load_db_pers()
    sub_areas = sorted(Product.SUB_AREA_DICT.keys())

    # First loop over the products, where we mark the invalid as such, and
    # we manually set the journal impact factor where necessary.
    print('Post-processing product list...')
    for prod in db_prod:
        # Mark invalids.
        if prod.row_index in _rating.INVALID:
            print('Marking product @ row %d for %s as invalid...' %\
                  (prod.row_index, prod.author_surname))
            prod.valid = False
        # Set impact factor if necessary.
        if prod.pub_type == '1.1 Articolo in rivista' and \
           prod.impact_factor() is None and \
           prod.journal in _rating.IMPACT_FACTOR_DICT.keys():
            journal = prod.journal
            impact_factor = _rating.IMPACT_FACTOR_DICT[journal]
            print('Setting IF for %s @ row %d to %.3f...' %\
                  (journal, prod.row_index, impact_factor))
            prod.set_impact_factor(impact_factor)
    
    for full_name in CANDIDATES:
        docent = db_pers.select(full_name=full_name, quiet=True)[0]
        print(docent)
        prods = db_prod.select(quiet=True, author_full_name=full_name,
                               year=YEAR, valid=True)
        rating_points = numpy.array([p.rating_points(docent.sub_area,
                                                     _rating.RATING_DICT) \
                                     for p in prods])
        num_authors = numpy.array([p.num_authors for p in prods])
        print('Number of products in 2018: %d' % len(rating_points))
        print('Total rating points in 2018: %.3f' % rating_points.sum())
        print('Co-authors (min, median, max): %d, %.3f, %d' %\
              (num_authors.min(), numpy.median(num_authors), num_authors.max()))
        print('\n')


if __name__ == '__main__':
    go()
