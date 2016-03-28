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

from datamatrix.py3compat import *
from pseudorandom._exceptions import InvalidConstraint
from datamatrix._datamatrix._basecolumn import BaseColumn

class Constraint(object):

	def __init__(self, enforce, **kwargs):

		self.enforce = enforce
		self.init(**kwargs)

	def setcols(self, cols):

		if cols is None:
			self.cols = self.dm.column_names
		elif isinstance(cols, BaseColumn):
			self.cols = [cols.name]
		else:
			self.cols = [col.name for col in cols]
		if not self.cols:
			raise InvalidConstraint(u'No (valid) columns specified')

	def ok(self, row):

		raise NotImplementedError

	@staticmethod
	def count(l):

		return len(set(l))

	@property
	def dm(self):

		return self.enforce.dm

class MaxRep(Constraint):

	"""
	desc:
		Limits the number of times that a value can occur in direct succession.
		A maxrep of 1 means that values cannot be repeated.

	example: |
		ef = Enforce(df)
		ef.add_constraint(MaxRep, cols=['word'], maxrep=2)
	"""

	def init(self, cols=None, maxrep=1):

		if maxrep < 1:
			raise InvalidConstraint(u'maxrep should be >= 1')
		self.maxrep = maxrep
		self.setcols(cols)

	def ok(self, row):

		if row < self.maxrep:
			return True
		for colname in self.cols:
			col = self.dm[colname]
			# We only check for preceding repetitions. I.e. in the string:
			# AABABBB
			# The number of repetitions would be:
			# 1211123
			if row < self.maxrep:
				continue
			l = col[row-self.maxrep:row+1]
			if self.count(l) == 1:
				return False
		return True

class MinDist(Constraint):

	"""
	desc:
		Sets a minimum distance between value repetitions. A minimum distance of
		2 avoids direct repetitions.

	example: |
		ef = Enforce(dm)
		ef.add_constraint(MinDist, cols=['word'], mindist=2)
	"""

	def init(self, cols=None, mindist=2):

		if mindist < 2:
			raise InvalidConstraint(u'mindist should be >= 2')
		self.mindist = mindist
		self.setcols(cols)

	def ok(self, row):

		for colname in self.cols:
			col = self.dm[colname]
			context = list(col[row-self.mindist+1:row]) \
				+ list(col[row+1:row+self.mindist])
			target = col[row]
			if target in context:
				return False
		return True
