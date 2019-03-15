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


def filter_db_pers(db_pers):
    """This is filtering a DocentDatabse object removing all the persons with
    less than 2 products (which automatically get 0 rating points).

    Note that, for the thing to work, this has to be called after a loop
    over the db where the product statistics has been calculated and 
    updated.
    """
    db = DocentDatabase()
    for pers in db_pers:
        if pers.num_products >= 2:
            db.append(pers)
        else:
            print('Filtering out %s (%d products)...' %\
                  (pers.full_name, pers.num_products))
    return db


def dump_rating(file_path, collab_threshold=50):
    """Dump the full rating information.
    """
    # Load the underlying database objects.
    db_prod = load_db_prod()
    db_pers = load_db_pers()
    sub_areas = sorted(Product.SUB_AREA_DICT.keys())

    # First loop over the products, where we mark the invalid as such.
    print('Post-processing product list...')
    for prod in db_prod:
        if prod.row_index in _rating.INVALID:
            print('Marking product @ row %d for %s as invalid...' %\
                  (prod.row_index, prod.author_surname))
            prod.valid = False

    # Break out the docent database into the three sub-areas.
    # Mind at this points the sub-lists still contain the persons with less
    # than 2 products.
    print('Populating sub-areas...')
    pers_dict = {}
    for sub_area in sub_areas:
        pers_dict[sub_area] = db_pers.select(sub_area=sub_area)

    # Actual loop to calculate the rating points and the basic product
    # statistics for all the docents.
    print('Calculating rating points...')
    for sub_area in sub_areas:
        for pers in pers_dict[sub_area]:
            prods = db_prod.select(author_full_name=pers.full_name, valid=True)
            rating = sum(prod.rating_points(sub_area, _rating.RATING_DICT) for\
                         prod in prods)
            num_authors = numpy.array([prod.num_authors for prod in prods])
            # Update the Docent object.
            pers.rating = rating
            pers.num_products = len(prods)
            # Note that we're casting all the numpy scalars to native Python
            # types for the excel interface module to be able to write them in
            # the output file.
            pers.num_collab_products = \
                int((num_authors > collab_threshold).sum())
            pers.min_num_authors = int(num_authors.min())
            pers.mean_num_authors = float(num_authors.mean())
            pers.max_num_authors = int(num_authors.max())

    # Now that we have the basic product statistics we can filter out
    # the docents with less than 2 products.
    for sub_area in sub_areas:
        print('Filtering docent databse for sub-area %s...' % sub_area)
        pers_dict[sub_area] = filter_db_pers(pers_dict[sub_area])

    # Sort the docents and dump the excel file.
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
            pers.ranking = i
            print('%2i -- %s: %f rating points.' %\
                  (i, pers.full_name, pers.rating))
            rows.append([i, pers.full_name, pers.rating, pers.num_products,
                         pers.num_collab_products, pers.min_num_authors,
                         pers.mean_num_authors, pers.max_num_authors])
        table.add_worksheet('Sottoarea %s' % sub_area, col_names, rows)
    table.write(file_path)

    # Do some plotting.
    for sub_area in sub_areas:
        plt.figure('Sottoarea %s' % sub_area, figsize=(12, 8))
        num_persons = len(pers_dict[sub_area])
        num_points = _rating.RATING_POINTS_PER_DOCENT * num_persons
        plt.title('Sottoarea %s (%d docenti, %.3f punti)' %\
                  (sub_area, num_persons, num_points), size=18)
        ranking = numpy.array([pers.ranking for pers in pers_dict[sub_area]])
        rating = numpy.array([pers.rating for pers in pers_dict[sub_area]])
        plt.plot(ranking, rating, 'o')
        plt.xlabel('Ranking')
        plt.ylabel('Rating points')
        for pers in pers_dict[sub_area]:
            x = pers.ranking
            y = pers.rating
            name = pers.full_name.split()[0].title()
            if name in ['Di', 'Del', 'Prada']:
                name += ' %s' % pers.full_name.split()[1].title()
            txt = '%s, %d (%d) <%.1f>' %\
                (name, pers.num_products, pers.num_collab_products,
                 pers.mean_num_authors)
            plt.text(x, y, txt, rotation=20., ha='left', va='bottom')
        leg = 'Cognome, # prod (# prod > %d auth) <mean # auth>' %\
            (collab_threshold)
        plt.text(0.5, 0.9, leg, transform=plt.gca().transAxes, size=12)

        # Calculate the quantiles.
        print('Calculating quantiles for sub-area %s...' % sub_area)
        quantiles = numpy.floor(numpy.linspace(0.22, 0.75, 3) * num_persons)
        quantiles += 0.5
        for q in quantiles:
            plt.axvline(q, ls='dashed')
        quantiles = numpy.concatenate(([-0.5], quantiles, [num_persons + 0.5]))
        psum = 0
        for i, (q1, q2) in enumerate(zip(quantiles[:-1], quantiles[1:])):
            mask = (ranking > q1) * (ranking < q2)
            r = ranking[mask]
            n = len(r)
            frac = float(n) / num_persons
            p = 4 - i
            psum += p * n
            print('%d docents with %d points...' % (n, p))
            plt.text(r.mean(), 2, '%d x %d = %d (%.1f %%)' %\
                     (p, n, n * p, 100. * frac), ha='center')
        print('Total rating points for area %s: %d' % (sub_area, psum))
        plt.savefig('rating02_2018_%s.png' % sub_area)        
    plt.show()


if __name__ == '__main__':
    dump_rating('rating02_2018.xls')
