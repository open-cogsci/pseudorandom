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
from pseudorandom import tools, DataFrame, Enforce, MaxRep, MinDist
from pseudorandom.py3compat import _basestring
import pandas as pd

class PseudoRandomTest(unittest.TestCase):

	"""
	desc:
		Basic unit testing for pseudorandom.
	"""

	def setUp(self):

		pdf = pd.read_csv('example/data.csv')
		self.df = tools.fromPandas(pdf)

	def test_slicing(self):

		# Test basic slicing
		self.assertTrue(self.df['word', :4] == self.df['word'][:4])
		self.assertTrue(self.df['word', :4] == self.df[:4, 'word'])
		self.assertTrue(self.df['word', :4] != self.df['word'][:5])
		self.assertTrue(self.df['word', :4] != self.df['category'][:4])
		# Check whether the correct DataTypes are returned
		self.assertTrue(isinstance(self.df['word', 0:1], DataFrame))
		self.assertTrue(isinstance(self.df['word', 0], _basestring))
		# Test iterator
		self.assertTrue(list(self.df['word', :4]) == 4*['cat'])
		# Test cell slicing
		self.df['firstLetter'] = self.df['word', :, :1]
		self.assertTrue(self.df['firstLetter', 0] == 'c')

	def test_constraintMaxRep(self):

		ef = Enforce(self.df)
		ef.addConstraint(MaxRep, maxRep=1)
		df = ef.enforce()
		for row in df.range[1:]:
			self.assertTrue(df[row] != df[row-1])

	def test_constraintMinDist(self):

		ef = Enforce(self.df)
		ef.addConstraint(MinDist, cols=['word'], minDist=3)
		df = ef.enforce()
		for row in df.range[3:]:
			s = set(df['word', row-3:row])
			self.assertTrue(len(s) == 3)

if __name__ == '__main__':
	unittest.main()
