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


import urllib
import os


def url(handle):
    """
    """
    return 'https://arpi.unipi.it/handle/%s?mode=full' % handle

def open_handle(handle):
    """
    """
    socket = urllib.urlopen(url(handle))
    return socket

def retrieve_num_authors(handle):
    """
    """
    socket = open_handle(handle)
    for line in socket:
        if 'dc.description.numberofauthors' in line:
            try:
                return int(line.split('</td><td')[-2].split('>')[-1])
            except:
                print('Error for handle %s: "%s"' % (handle, line))

def dump_num_authors(output_file_path='author_dump.txt'):
    """
    """
    if os.path.exists(output_file_path):
        print('Output file %s exists, exiting.' % output_file_path)
        return 
    import rating
    pub_list = rating.load_publication_list()
    handle_list = pub_list.unique_values('handle').keys()
    output_file = open(output_file_path, 'w')
    for handle in handle_list:
        num_authors = retrieve_num_authors(handle)
        print('%s -> %s' % (handle, num_authors))
        output_file.write('%s %s\n' % (handle, num_authors))


if __name__ == '__main__':
    dump_num_authors()
