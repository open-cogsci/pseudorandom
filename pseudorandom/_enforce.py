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
import time
import random
from pseudorandom._exceptions import EnforceFailed
from datamatrix import operations

class Enforce(object):

	"""
	desc:
		A class that enforces a set of constraints by modifying (if necessary)
		the DataMatrix.
	"""

	def __init__(self, dm):

		"""
		desc:
			Constructor.

		arguments:
			dm:
				desc:	The data.
				type:	DataMatrix
		"""

		self.dm = dm[:]
		self.constraints = []
		self.report = None

	def add_constraint(self, constraint, **kwargs):

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

		self.constraints.append(constraint(self, **kwargs))

	def _enforce(self, reverse=False):

		redo = False
		_range = range(len(self.dm))
		if reverse:
			_range = reversed(_range)
		for row in _range:
			if not self.ok(row):
				redo = True
				if reverse:
					heaprange = list(range(row+1, len(self.dm)))
				else:
					heaprange = list(range(row))
				random.shuffle(heaprange)
				for heaprow in heaprange:
					import copy
					# _dm = copy.deepcopy(self.dm)
					_dm = self.dm[:]
					for name, col in self.dm.columns:
						col[row, heaprow] = col[heaprow, row]
					if self.ok(row):
						break
					self.dm = _dm
		return redo

	def enforce(self, maxreshuffle=100, maxpass=100):

		"""
		desc:
			Enforces constraints.

		keywords:
			maxpass:
				desc:	The maximum number of times that the enforce algorithm
						may be restarted.
				type:	int

		returns:
			desc:	A `DataMatrix` that respects the constraints.
			type:	DataMatrix
		"""

		t0 = time.time()
		reverse = False
		for i in range(maxreshuffle):
			self.dm = operations.shuffle(self.dm)
			for j in range(maxpass):
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
				u'Failed to enforce constraints (maxreshuffle = %d)' \
				% maxreshuffle)
		t1 = time.time()
		self.report = {
			u'time'			: t1-t0,
			u'reshuffle'	: i+1,
			}
		return self.dm

	def ok(self, row):

		return all([constraint.ok(row) for constraint in self.constraints])
