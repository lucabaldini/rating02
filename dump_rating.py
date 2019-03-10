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

from rating import *

import _rating2018 as _rating



def dump_rating(file_path, collab_threshold=20):
    """Dump the full rating information.
    """
    db_prod = load_db_prod()
    db_pers = load_db_pers()
    sub_areas = sorted(Product.SUB_AREA_DICT.keys())

    print('Populating sub-areas...')
    pers_dict = {}
    for sub_area in sub_areas:
        pers_dict[sub_area] = db_pers.select(sub_area=sub_area)

    print('Calculating rating points...')
    for sub_area in sub_areas:
        for pers in pers_dict[sub_area]:
            prods = db_prod.select(author_full_name=pers.full_name)
            rating = sum(prod.rating_points(sub_area, _rating.RATING_DICT) for\
                         prod in prods)
            num_authors = numpy.array([prod.num_authors for prod in prods])
            # Update the Docent object.
            pers.rating = rating
            pers.num_products = len(prods)
            pers.num_collab_products = (num_authors > collab_threshold).sum()
            pers.min_num_authors = num_authors.min()
            pers.mean_num_authors = num_authors.mean()
            pers.max_num_authors = num_authors.max()


    print('Sorting docents within sub-areas...')
    table = ExcelTableDump()
    col_names = ['Ranking', 'Nome', 'Punti rating', 'Numero prodotti',
                 'Numero prodotti con > %d autori' % collab_threshold,
                 '# autori min', '# autori medio', '# autori max']
    for sub_area in sub_areas:
        rows = []
        pers_dict[sub_area].sort(reverse=True)
        print('Ratings points for sub-area %s:' % sub_area)
        for i, pers in enumerate(pers_dict[sub_area]):
            print('%2i -- %s: %f rating points.' %\
                  (i, pers.full_name, pers.rating))
            rows.append([i, pers.full_name, pers.rating, pers.num_products,
                         pers.num_collab_products, pers.min_num_authors,
                         pers.mean_num_authors, pers.max_num_authors])
        table.add_worksheet('Sottoarea %s' % sub_area, col_names, rows)
    table.write(file_path)


if __name__ == '__main__':
    dump_rating('rating02_2018.xls')
