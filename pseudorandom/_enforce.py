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

import random
import itertools
from pseudorandom.py3compat import *

class Enforce(object):

	"""
	desc:
		A class that enforces a set of constraints by modifying (if necessary)
		the `DataFrame`.
	"""

	def __init__(self, df):

		"""
		desc:
			Constructor.

		arguments:
			df:
				desc:	The data.
				type:	DataFrame
		"""

		self.df = df.copy()
		self.constraints = []

	def addConstraint(self, constraint, **kwargs):

		"""
		desc:
			Adds a constraint to enforce.

		arguments:
			constraint:
				desc:	A constraint class. Note, the class itself should be
						passed, not an instance of the class.
				type:	type

		keyword-dict:
			kwargs:		The keyword arguments that are passed to the constraint
						constructor.
		"""

		self.constraints.append(constraint([self.df], **kwargs))

	def _enforce(self, reverse=False):

		redo = False
		_range = self.df.range
		if reverse:
			_range = reversed(_range)
		for row in _range:
			if not self.ok(row):
				redo = True
				if reverse:
					heapRange = list(range(row+1, len(self.df)))
				else:
					heapRange = list(range(row))
				random.shuffle(heapRange)
				for heapRow in heapRange:
					_df = self.df.copy()
					self.df.swapRows(row, heapRow)
					if self.ok(row) and self.ok(heapRow):
						break
					self.df.data = _df.data
		return redo

	def enforce(self, maxReshuffle=100, maxPass=100):

		"""
		desc:
			Enforces constraints.

		keywords:
			maxPass:
				desc:	The maximum number of times that the enforce algorithm
						may be restarted.
				type:	int

		returns:
			desc:	A `DataFrame` that respects the constraints.
			type:	DataFrame
		"""

		reverse = False
		for i in range(maxPass):
			redo = self._enforce(reverse=reverse)
			if not redo:
				break
			reverse = not reverse
		else:
			if maxReshuffle == 0:
				raise Exception(u'Failed to enforce constraints')
			self.df.shuffle()
			self.enforce(maxReshuffle=maxReshuffle-1, maxPass=maxPass)
		return self.df

	def ok(self, row):

		return all([constraint.ok(row) for constraint in self.constraints])
