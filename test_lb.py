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


from rating import load_db

db = load_db()

pubs = db.select(author_name='LUCA', author_surname='BALDINI')
print('Done, %d publication(s) selected.' % len(pubs))

sub_area = 'a'

print('Calulating rating points...')
rating = sum(pub.rating_points(sub_area) for pub in pubs)
print('Rating: %.3f' % rating)

    


