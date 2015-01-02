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
import copy
from collections import OrderedDict
from pseudorandom.py3compat import _basestring, _unicode, py3

class DataFrame(object):

	"""
	desc:
		A lightweight object for storing data. `pseudorandom.DataFrame` is
		similar to the `Pandas.DataFrame` class, but does not require any
		additional libraries, which makes it suitable for environments in which
		only the Python core libraries are available.
	"""

	def __init__(self, cols, rows, default=u''):

		"""
		desc:
			Constructor. This creates a `DataFrame` with known columns and rows,
			but without any content.

		arguments:
			cols:
				desc:	A list of column names.
				type:	list
			rows:
				desc:	The numer of rows.
				type:	int

		keywords:
			default:	The default value for the cells.
		"""

		if not isinstance(cols, list):
			raise Exception(u'cols must be a list of strings')
		if len(cols) != len(set(cols)):
			raise Exception(u'cols must not contain duplicates')
		if not isinstance(rows, int):
			raise Exception(u'rows must be integer')
		self.data = OrderedDict.fromkeys(cols)
		for col in self.data:
			self.data[col] = [default]*rows

	def __getitem__(self, key):

		"""
		desc:
			Implements the get operator.

		arguments:
			key:
				desc:	The element to get. This can be `slice` or `int` for
						rows, `str` for columns, or a `tuple` to get a set of
						rows for specific columns.
				type:	[str, slice, int, tuple]

		example: |
			print(df[0])
			print(df[0:2])
			print(df['word'])
			print(df['word', 0:2])

		returns:
			desc:	A new `DataFrame` that is a subset of the current
					`DataFrame`.
			type:	DataFrame
		"""

		if isinstance(key, int):
			df = self.copy()
			return df.selectRows(key)
		if isinstance(key, _basestring):
			df = self.copy()
			return df.selectCols(key)
		if isinstance(key, tuple) and len(key) == 2:
			key1, key2 = key
			return self[key1][key2]
		if isinstance(key, slice):
			if key.start is None:
				start = 0
			else:
				start = key.start
			if key.stop is None:
				stop = len(self)
			else:
				stop = key.stop
			if key.step is None:
				step = 1
			else:
				step = key.step
			_range = range(start, stop, step)
			df = self.copy()
			return df.selectRows(_range)
		raise Exception(u'Invalid key: %s' % key)

	def __len__(self):

		"""
		desc:
			Implements the `len()` function.

		example: |
			print('df has %d rows' % len(df))

		returns:
			desc:	The number of rows.
			type:	int
		"""

		return len(list(self.data.values())[0])

	def __setitem__(self, key, val):

		"""
		desc:
			Implements the assignment operator.

		arguments:
			key:
				desc:	The element to get. This can be `int` for rows, `str`
						for columns, or a `tuple` to get a specific cell.
				type:	[str, int, tuple]
			val:
				desc:	The value to set. This should be a list when setting an
						entire column or row.

		example: |
			df['word'] = ['cat', 'dog', 'mouse']
			df[0] = ['cat', 10]
			df['word', 0] = 'cat'
		"""

		if isinstance(key, tuple) and len(key) == 2:
			key1, key2 = key
			if isinstance(key1, _basestring) and isinstance(key2, int):
				self.data[key1][key2] = val
				return
			if isinstance(key2, _basestring) and isinstance(key1, int):
				self.data[key2][key1] = val
				return
		if isinstance(key, int):
			if len(val) != len(self.cols):
				raise Exception(u'Non-matching length for %s' % val)
			for col in self.cols:
				self.data[col][key] = val[key]
			return
		if isinstance(key, _basestring):
			if len(val) != len(self):
				raise Exception(u'Non-matching length for %s' % val)
			self.data[key] = val
			return
		raise Exception(u'Invalid key: %s' % key)

	def __repr__(self):
		return self.__unicode__()

	def __str__(self):
		if py3:
			return self.__unicode__()
		return self.__unicode__().encode('utf-8')

	def __unicode__(self):

		u = u''
		row = []
		matrix = []
		for col in self.data.keys():
			row.append(u'%08s' % col)
		matrix.append(u'   # | ' + u' | '.join(row) + u' |')
		for i in range(len(self)):
			row = []
			for col in self.data.keys():
				row.append(u'%08s' % self.data[col][i])
			matrix.append(u'%04s | ' % i + u' | '.join(row) + u' |')
		max_len = 0
		for row in matrix:
			max_len = max(max_len, len(row))
		matrix = [u'='*max_len] + matrix[:1] + [u'-'*max_len] + matrix[1:] \
			+ [u'='*max_len]
		return _unicode(u'\n'.join(matrix))

	@property
	def cols(self):

		"""
		name:		cols
		returns:
			desc:	The number of columns.
			type:	int
		"""

		return list(self.data.keys())

	@property
	def range(self):

		"""
		name:		range
		returns:
			desc:	A list of all row indices.
			type:	list
		"""

		return list(range(len(self)))

	def copy(self):

		"""
		returns:
				desc:	A deep copy of the current `DataFrame`.
				type:	DataFrame
		"""

		return copy.deepcopy(self)

	def getCols(self, cols):

		if cols is None:
			cols = list(self.data.keys())
		elif isinstance(cols, _basestring):
			cols = [cols]
		elif not isinstance(cols, list):
			raise Exception(u'Invalid column specification: %s' % cols)
		for col in cols:
			if col not in self.cols:
				raise Exception(u'Column "%s" does not exist' % col)
		return cols

	def getRows(self, rows):

		if rows is None:
			rows = range(len(self))
		elif isinstance(rows, int):
			rows = [rows]
		elif not isinstance(rows, list):
			raise Exception(u'Invalid row specification: %s' % rows)
		return rows

	def selectCols(self, cols=None):

		keep_cols = self.getCols(cols)
		for col in self.cols:
			if col not in keep_cols:
				del self.data[col]
		return self

	def selectRows(self, rows=None):

		keep_rows = self.getRows(rows)
		for col in self.cols:
			self.data[col] = [self.data[col][i] for i in keep_rows]
		return self

	def shuffle(self, cols=None):

		"""
		desc:
			Shuffles the current `DataFrame` in place.

		keywords:
			cols:
				desc:	The columns to shuffle or `None` to shuffle all columns.
						Columns are shuffled together, i.e. rows are preserved.
				type:	[list, NoneType]

		returns:
			desc:	The current `DataFrame`.
			type:	DataFrame
		"""

		indices = list(range(0, len(self)))
		random.shuffle(indices)
		for col in self.getCols(cols):
			rcol = []
			for i in indices:
				rcol.append(self.data[col][i])
			self.data[col] = rcol
		return self

	def sort(self, cols=None, key=None):

		"""
		desc:
			Sorts the current `DataFrame` in place.

		keywords:
			cols:
				desc:	The columns to sort or `None` to sort all columns.
				type:	[list, NoneType]
			key:
				desc:	A column to sort by or `None` to sort each column by
						itself.
				type:	[str, NoneType]

		returns:
			desc:	The current `DataFrame`.
			type:	DataFrame
		"""

		cols = self.getCols(cols)
		if key is not None:
			if key not in self.cols:
				raise Exception(u'Column "%s" does not exist' % key)
			sort_values = self.data[key]
		for col in cols:
			if key is not None:
				self.data[col] = [x for (y, x) in sorted(
					zip(sort_values, self.data[col]))]
			else:
				self.data[col].sort()
		return self

	def reverse(self, cols=None):

		"""
		desc:
			Reverses the current `DataFrame` in place.

		keywords:
			cols:
				desc:	The columns to reverse or `None` to reverse all columns.
				type:	[list, NoneType]

		returns:
			desc:	The current `DataFrame`.
			type:	DataFrame
		"""

		for col in self.getCols(cols):
			self.data[col] = self.data[col][::-1]
		return self

	def shift(self, d=1, cols=None):

		"""
		desc:
			Shifts the current `DataFrame` in place. This moves all rows down or
			up, with wrapping. I.e. moving all rows one step down will cause the
			last row to become the first.

		keywords:
			d:
				desc:	The displacement. Positive displacements move rows down.
				type:	int
			cols:
				desc:	The columns to shift or `None` to shift all columns.
				type:	[list, NoneType]

		returns:
			desc:	The current `DataFrame`.
			type:	DataFrame
		"""

		for col in self.getCols(cols):
			self.data[col] = self.data[col][-d:] + self.data[col][:-d]
		return self

	def swapRows(self, i1, i2, i3=None):

		for col in self.cols:
			if i3 == None:
				self.data[col][i1], self.data[col][i2] = \
					self.data[col][i2], self.data[col][i1]
			else:
				self.data[col][i1], self.data[col][i2], self.data[col][i3] = \
					self.data[col][i2], self.data[col][i3], self.data[col][i1]

random.seed()
