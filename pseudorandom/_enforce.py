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

import time
import random
import itertools
from pseudorandom.py3compat import *
from pseudorandom._exceptions import EnforceFailed

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
		self.report = None

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
					if self.ok(row):
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

		t0 = time.time()
		reverse = False
		for i in range(maxReshuffle):
			self.df.shuffle()
			for j in range(maxPass):
				if not self._enforce(reverse=reverse):
					break
				reverse = not reverse
			else:
				# If the maximum passes were exhausted, restart the loop
				continue
			# If the maximum passes were not exhausted, we are done
			break
		else:
			raise EnforceFailed(
				u'Failed to enforce constraints (maxReshuffle = %d)' \
				% maxReshuffle)
		t1 = time.time()
		self.report = {
			u'time'			: t1-t0,
			u'reshuffle'	: i+1,
			}
		return self.df

	def ok(self, row):

		return all([constraint.ok(row) for constraint in self.constraints])
