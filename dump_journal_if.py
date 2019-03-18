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


def dump_journal_if(file_path):
    """Loop over all the journal articles and dump a dictionary of all the
    impact factor for the four years.

    This can potentuially be used to fill in the gaps for the database entries
    where the impact factor is missing for unknown reasons.
    """
    db = load_db_prod(False).select(pub_type='1.1 Articolo in rivista')

    # Book-keeping dictionary.
    if_dict = {}

    # Loop over the journals.
    print('Looping over the products...')
    for prod in db:
        impact_factor = prod.impact_factor()
        if impact_factor is None:
            continue
        journal = prod.journal
        year = prod.year
        if journal in if_dict:
            if year in if_dict[journal]:
                assert impact_factor == if_dict[journal][year]
            else:
                if_dict[journal][year] = impact_factor
        else:
            if_dict[journal] = {year: impact_factor}
    print('Done, IF for %d journal(s) written.' % len(if_dict))

    # Dump the dictionary to a pickle file.
    print('Dumping the IF dict to %s...' % file_path)
    pickle.dump(if_dict, open(file_path, 'wb'))
    print('Done.')


if __name__ == '__main__':
    dump_journal_if('journal_if.pickle')
