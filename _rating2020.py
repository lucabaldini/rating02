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


"""Total number of rating points to be assigned.

Technically we have 76 professors and 190 points (2.5 points per persons).
Triggiani has zero products and therefore gets zero points---and we loose his
2.5 points. It's not clear to me whether this brings us down to 188 or 187, and
for the time being I am conservatively assuming 187.
"""
TOTAL_RATING_POINTS = 187
NUM_DOCENTS = 75

"""Average number of rating points per docent.
"""
RATING_POINTS_PER_DOCENT = TOTAL_RATING_POINTS / float(NUM_DOCENTS)

"""Docents with zero products. (I realize the variable name is somewhat
dismissive, but I didn't mean to be judjamental.)
"""
ZERO_DOCENTS = ['TRIGGIANI GIUSEPPE']

"""
"""
LOA_SCALING_DICT = {
    # 152 + 137 + 45 gg
    'CIAMPINI DONATELLA': 1.229,
    # 91 + 153 gg
    'ROCCATAGLIATA VERONICA': 1.167
}


"""Dictionary of the impact factors for some of the journals that got left
behind in the db file.
"""
IMPACT_FACTOR_DICT = {
    'ASTRONOMY & ASTROPHYSICS': 4.902,
    'GIORNALE DI FISICA DELLA SOCIETÀ ITALIANA DI FISICA': 0.,
    'IEEE TRANSACTIONS ON RADIATION AND PLASMA MEDICAL SCIENCES': 0.,
    'IL NUOVO CIMENTO C': 0.,
    'INTERNATIONAL JOURNAL OF HIGH ENERGY PHYSICS': 0.,
    'JOURNAL OF GEOPHYSICAL RESEARCH. SPACE PHYSICS': 0.,
    'JOURNAL OF MEDICAL IMAGING': 0.,
    'JOURNAL OF PHYSICS. CONFERENCE SERIES': 0.,
    'OPEN PHYSICS': 0.,
    'PHYSICAL REVIEW A': 2.7,
    'PHYSICAL REVIEW. A': 2.7,
    'PHYSICAL REVIEW B': 3.8,
    'PHYSICAL REVIEW. B': 3.8,
    'PHYSICAL REVIEW C': 3.3,
    'PHYSICAL REVIEW. C': 3.3,
    'PHYSICAL REVIEW D': 4.4,
    'PHYSICAL REVIEW. D': 4.4,
    'PHYSICAL REVIEW E': 2.4,
    'PHYSICAL REVIEW. E': 2.4,
    'PHYSICAL REVIEW LETTERS': 8.0,
    'MONTHLY NOTICES OF THE ROYAL ASTRONOMICAL SOCIETY. LETTERS': 4.9,
    'POS PROCEEDINGS OF SCIENCE': 0.,
    'JOURNAL OF HIGH ENERGY ASTROPHYSICS (PRINT)': 2.3,
    'JOURNAL OF HIGH ENERGY PHYSICS': 4.911,
    'NANO LETTERS': 12.1,
    'NANOTECHNOLOGY': 3.4,
    'NATURE PHYSICS': 22.8,
    'UNIVERSE': 0.
}


"""List of duplicates, indexed by row number.
"""
DUPLICATES = [
    208,
    354,
    594,
    611,
    729,
    745,
    1261,
    1877,
    6067,
    6089,
    2791,
    4040,
    4308,
    4440,
    4455,
    4574,
    4590,
    4954,
    5298
]


"""List of errata, indexed by row number.
"""
ERRATA = [
    205,
    320,
    559,
    583,
    613,
    669,
    1569,
    1631,
    1829,
    3095,
    3471,
    4405,
    4429,
    4457,
    4513,
    5021,
    5652,
    5712
]


"""List of invalid products.
"""
INVALID = DUPLICATES + ERRATA


"""Dictionary with the rating points for the products that need to be
exhamined "by hand".
"""
RATING_DICT = {
    # [1.2  @ row 4872 for SHORE, S.], "Astronomy: Cosmic exhumation" (2017),
    # 1 author(s), IF = 44.958
    '11568/893099' : 7.8,

    # [3.1  @ row 2199 for FERRANTE, I.], "Elaborazione dei segnali per la
    # fisica" (2015), 1 author(s), IF = None
    '11568/758521' : 2.,

    # [3.1  @ row 3307 for POGGIANI, R.], "High Energy Astrophysical
    # Techniques" (2017), 1 author(s), IF = None
    '11568/831239' : 10.,

    # [3.1  @ row 3308 for POGGIANI, R.], "Optical, Infrared and Radio
    # Astronomy" (2017), 1 author(s), IF = None
    '11568/831178' : 10.,

    # [3.1  @ row 1662 for D'ELIA, M.], "Introduction to the Basic Concepts
    # of Modern Physics" (2016), 2 author(s), IF = None
    '11568/957130' : 10.,

    # [3.1  @ row 4785 for ROSSI, P.], "La scuola pisana di Fisica (1840-1950)"
    # (2018), 2 author(s), IF = None
    '11568/939183' : 10.,

    # [3.1  @ row 4871 for SHORE, S.], "A Dirty Window: Diffuse and Translucent
    # Molecular Gas in the Interstellar Medium, Astrophysics and Space Science
    # Library, Volume 442" (2017), 2 author(s), IF = None
    '11568/893101' : 10.,

    # Duplicate of the previous one.
    '11568/893089' : 10.,

    # [3.8  @ row 4781 for ROSSI, P.], "Quando Albert divent? Einstein" (2018),
    # 2 author(s), IF = None
    '11568/939539' : 0.,

    # [5.12 @ row 1904 for DONATI, S.], "Mu2e Technical Design Report" (2015),
    # 263 author(s), IF = None
    '11568/687079' : 0.,

    # [5.12 @ row 222 for BELCARI, N.], "Corrigendum to ?TRIMAGE: A dedicated
    # trimodality (PET/MR/EEG) imaging tool for schizophrenia? [Eur Psychiatry
    # 50 (2018) 7?20] (S0924933817330134) (10.1016/j.eurpsy.2017.11.007))"
    # (2018), 42 author(s), IF = None
    '11568/938653' : 0.,

    # [5.12 @ row 459 for CAPACCIOLI, S.], "Revisione teorica dei: modelli di
    # rock physics ?pressure dependent?,  modelli Vp/Vs  alla base
    # dell'indicatore Rp+Rs e del modello di rock physics alla base della
    # rotazione del background trend AVA" (2015), 4 author(s), IF = None
    '11568/825566' : 0.,

    # [5.12 @ row 482 for CAPACCIOLI, S.], "Pore pressure prediction for
    # overpressure zones detection: Modelli di Rock Physics e  Stima Vp/Vs
    # da rotazione Background trend." (2016), 4 author(s), IF = None
    '11568/825711' : 0.,

    # [5.12 @ row 1090 for CIGNONI, M.], "The Gaia-LSST Synergy: resolved
    # stellar populations in selected Local Group stellar systems" (2018),
    # 20 author(s), IF = None
    '11568/951554' : 0.,

    # [5.12 @ row 3400 for PRADA MORONI, P.], "Investigating the population of
    # Galactic star formation regions and star clusters within a Wide-Fast-Deep
    # Coverage of the Galactic Plane" (2018), 35 author(s), IF = None
    '11568/946973' : 0.,

    # [6.1  @ row 501 for CARELLI, G.], "Metodo non invasivo per misurare il
    # contenuto idrico assoluto di una foglia" (2016), 7 author(s), IF = None
    '11568/858130' : 3.16,

    # [7.1  @ row 996 for CAVASINNI, V.], "Fisica e Fisici a Pisa nel Novecento"
    # (2018), 7 author(s), IF = None
    '11568/939892' : 0.,

    # [7.1  @ row 2499 for LAMANNA, G.], "Proceedings of the GPU Computing in
    # High-Energy Physics 2014 Conference (GPUHEP2014)" (2015), 4 author(s),
    # IF = None
    '11568/947581' : 0.,

    # [7.1  @ row 308 for BISOGNI, M.], "Editorial" (2016), 5 author(s),
    # IF = 1.211
    '11568/844185' : 0.,

    # [7.1  @ row 4769 for ROSSI, P.], "Unibook. Per un database
    # sull'Universita`" (2017), 3 author(s), IF = None
    '11568/881356' : 0.,

    # Added in 2020.

    # Software Punzi.
    '11568/1019749': 0.,

    # Software Rizzi.
    '11568/991681': 0.,

    # [3.1  @ row 4422 for RIZZO, G.],
    # "Matera Building Stones: Comparison between Bioclastic and Lithoclastic Calcarenites" (2019)
    '11568/1015046': 0.,

    # Brevetto Bisogni, Morrocchi Sportelli.
    # [6.1  @ row 340 for BISOGNI, M.], "Metodo e apparato per l'acquisizione
    # dati per tomografia ad emissione di positroni in adroterapia a fascio acceso" (2018)
    '11568/1013900': 4.16,

    # Recensione in rivista Roddaro.
    '11568/1017473': 0.,

    # 3.1  @ row 996 for CHIOFALO, M.], "La Fisica della Materia" (2019)
    '11568/1028007': 2.
}
