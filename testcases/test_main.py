#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
This file is part of pseudorandom.

pseudorandom is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pseudorandom is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pseudorandom.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest
from datamatrix import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pseudorandom import Enforce, MaxRep, MinDist


def test_constraintMaxRep():

    dm = io.readtxt('examples/data.csv')
    ef = Enforce(dm)
    ef.add_constraint(MaxRep, maxrep=1)
    dm = ef.enforce()
    for row in range(len(dm)):
        for cell1, cell2 in zip(dm[row], dm[row-1]):
            assert cell1 != cell2


def test_constraintMinDist():

    dm = io.readtxt('examples/data.csv')
    ef = Enforce(dm)
    ef.add_constraint(MinDist, cols=[dm.word], mindist=3)
    dm = ef.enforce()
    for row in range(3, len(dm)):
        s = dm.word[row-3:row].unique
        assert len(s) == 3


if __name__ == '__main__':
    unittest.main()
