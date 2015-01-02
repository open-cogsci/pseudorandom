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

class Constraint(object):

	def __init__(self, ldf, **kwargs):

		self.df = ldf[0]
		self.init(**kwargs)

	def ok(self, df, row):

		raise NotImplementedError

	@staticmethod
	def count(l):

		return len(set(l))

class MaxRep(Constraint):

	"""
	desc:
		Limits the number of times that a value can occur in direct succession.
		A maxRep of 1 means that values cannot be repeated.

	example: |
		ef = Enforce(df)
		ef.addConstraint(MaxRep, cols=['word'], maxRep=2)
	"""

	def init(self, cols=None, maxRep=1):

		self.maxRep = maxRep
		self.cols = self.df.getCols(cols)

	def ok(self, row):

		if row < self.maxRep:
			return True
		for col in self.cols:
			# We only check for preceding repetitions. I.e. in the string:
			# AABABBB
			# The number of repetitions would be:
			# 1211123
			if row < self.maxRep:
				continue
			l = self.df.data[col][row-self.maxRep:row+1]
			if self.count(l) == 1:
				return False
		return True

class MinDist(Constraint):

	"""
	desc:
		Sets a minimum distance between value repetitions. A minimum distance of
		2 avoids direct repetitions.

	example: |
		ef = Enforce(df)
		ef.addConstraint(MinDist, cols=['word'], minDist=2)
	"""

	def init(self, cols=None, minDist=2):

		self.minDist = minDist
		self.cols = self.df.getCols(cols)

	def ok(self, row):

		for col in self.cols:
			l = self.df.data[col][row-self.minDist+1:row] \
				+ self.df.data[col][row+1:row+self.minDist]
			if self.df.data[col][row] in l:
				return False
		return True
