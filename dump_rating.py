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


from rating import *



def dump_rating(file_path):
    """Dump the full rating information.
    """
    db_prod = load_db_prod()
    db_pers = load_db_pers()
    for sub_area in sorted(Product.SUB_AREA_DICT.keys()):
        print('Calculating rating points for sub-area %s...' % sub_area)
        for pers in db_pers.select(sub_area=sub_area):
            prods = db_prod.select(author_full_name=pers.full_name)
            rating = sum(prod.rating_points(sub_area) for prod in prods)
            print(rating)



if __name__ == '__main__':
    dump_rating('rating02_2018.xls')
