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
import itertools
from collections import OrderedDict
from dataframe.py3compat import _basestring, _unicode, py3

class DataFrame(object):

	"""
	desc:
		A lightweight object for storing data. `pseudorandom.DataFrame` is
		similar to the `Pandas.DataFrame` class, but does not require any
		additional libraries, which makes it suitable for environments in which
		only the Python core libraries are available.
	"""

	def __init__(self, cols, rows, default=u'', colValidator=None,
		cellValidator=None):

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
		self._len = rows
		self.default = default
		self.colValidator = colValidator
		self.cellValidator = cellValidator
		for col in self.data:
			self.data[col] = self.emptyCol()

	@classmethod
	def fromLists(cls, cols, rows, *arglist, **kwdict):

		df = cls(cols, len(rows), *arglist, **kwdict)
		for colNr, col in enumerate(cols):
			for row in range(len(rows)):
				df[col, row] = rows[row][colNr]
		return df

	@classmethod
	def fromExcel(cls, path, *arglist, **kwdict):

		"""
		desc:
			Reads an Excel file in any of the formats supported by openpyxl, and
			returns it as a DataFrame. If there are multiple sheets, the first
			sheet is used.

		arguments:
			path:
				desc:	The full path to an Excel file.
				type:	str

		argument-list:
			arglist:	A list of arguments to be passed to the DataFrame
						constructor.

		keyword-dict:
			kwdict:		A dict of keywords to be passed to the DataFrame
						constructor.

		returns:
			type:	DataFrame
		"""

		from openpyxl import load_workbook
		wb = load_workbook(path)
		ws = wb.get_active_sheet()
		cols = None
		rows = []
		_len = 0
		for row in ws.rows:
			if cols is None:
				cols = []
				for cell in row:
					if cell.value is None:
						break
					cols.append(cell.value)
					_len += 1
			else:
				rows.append([cell.value for cell in row[:_len]])
		return cls.fromLists(cols, rows, *arglist, **kwdict)

	@classmethod
	def fromText(cls, path, delimiter=u',', quote=u'"', *arglist, **kwdict):

		"""
		desc:
			Reads a text file, such as a CSV file, and returns it as a
			DataFrame.

		arguments:
			path:
				desc:	The full path to a text file.
				type:	str

		keywords:
			delimiter:
				desc:	A character that delimits columns.
				type:	str
			quote:
				desc:	A character that quotes columns.
				type:	str

		argument-list:
			arglist:	A list of arguments to be passed to the DataFrame
						constructor.

		keyword-dict:
			kwdict:		A dict of keywords to be passed to the DataFrame
						constructor.

		returns:
			type:	DataFrame
		"""

		import csv
		fd = open(path)
		cols = None
		rows = []
		for row in csv.reader(fd, delimiter=delimiter.encode(),
			quotechar=quote.encode()):
			if cols is None:
				cols = row
				continue
			rows.append(row)
		fd.close()
		return cls.fromLists(cols, rows, *arglist, **kwdict)

	def __eq__(self, other):

		if not isinstance(other, DataFrame) or self.cells != other.cells:
			return False
		for row, col in self.cells:
			if self[row, col] != other[row, col]:
				return False
		return True

	def __iter__(self):

		return DataFrameIterator(self)

	def __contains__(self, key):

		if isinstance(key, int):
			return key in self.range
		return key in self.data

	def insert(self, key, index=-1):

		if isinstance(key, int):
			for col in self.cols:
				if key == -1:
					self.data[col].append(self.default)
				elif key < 0:
					self.data[col].insert(key+1, self.default)
				else:
					self.data[col].insert(key, self.default)
			self._len += 1
			return
		if index < 0:
			nPop = -index-1
		else:
			nPop = len(self.cols)-index
		nPop = min(len(self.cols), nPop)
		l = []
		for i in range(nPop):
			l.append(self.data.popitem())
		self.data[key] = self.emptyCol()
		for key, val in l[::-1]:
			self.data[key] = val

	def __delitem__(self, key):

		# Delete row
		if isinstance(key, int):
			if key < 0 or key >= len(self):
				raise Exception(u'Row %s does not exist' % key)
			for col in self.cols:
				self.data[col].pop(key)
			self._len -= 1
			return
		if isinstance(key, _basestring):
			# Delete column
			if not key in self:
				raise Exception(u'Column %s does not exist' % key)
			del self.data[key]

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
			# Getting a DataFrame that is a subset of the current DataFrame:
			#
			# Print the first row
			print(df[0])
			# Print the first two rows
			print(df[0:2])
			# Print the row column
			print(df['word'])
			# Print the first two rows of the word column
			print(df['word', 0:2])

			# Getting a single cell:
			#
			# Print the cell that corresponds to the first row in the word
			# column.
			print(df['word', 0])

			# You can even slice the cells in the DataFrame, by passing a third
			# slice. Note that this will fail if some cells cannot be sliced,
			# for example because they are integers.
			#
			# Getting the first two characters from all rows in the word column.
			print(df['word', :, :2])

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
		if isinstance(key, tuple):
			if len(key) == 2:
				key1, key2 = key
				if isinstance(key1, _basestring) and isinstance(key2, int):
					return self.data[key1][key2]
				if isinstance(key2, _basestring) and isinstance(key1, int):
					return self.data[key2][key1]
				return self[key1][key2]
			if len(key) == 3:
				key1, key2, key3 = key
				df = self[(key1, key2)]
				return df.sliceValues(key3)
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
			_range = list(range(start, stop, step))
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

		return self._len

	def __ne__(self, other):

		return not self == other

	def __setitem__(self, key, val):

		"""
		desc:
			Implements the assignment operator.

		arguments:
			key:
				desc:	The element to get. This can be `int` for rows, `str`
						for columns, or a `tuple` to set a specific cell.
				type:	[str, int, tuple]
			val:
				desc:	The value to set. This should be a list when setting an
						entire column or row.

		example: |
			# Set the word column
			df['word'] = ['cat', 'dog', 'mouse']
			# Set the first row
			df[0] = ['cat', 10]
			# Set the cell that corresponds to the first row in the word column.
			df['word', 0] = 'cat'
		"""

		if isinstance(key, tuple) and len(key) == 2:
			key1, key2 = key
			if isinstance(key1, _basestring) and isinstance(key2, int):
				self.setCell((key1, key2), val)
				return
			if isinstance(key2, _basestring) and isinstance(key1, int):
				self.setCell((key2, key1), val)
				return
		if isinstance(key, int):
			if isinstance(val, DataFrame):
				if val.cols != self.cols:
					raise Exception(u'Non-matching columns for %s' % val)
				if len(val) != 1:
					raise Exception(u'Can only assign DataFrames of length 1')
				for col in self.cols:
					self.setCell((col, key), val[col, 0])
				return
			if len(val) != len(self.cols):
				raise Exception(u'Non-matching length for %s' % val)
			for col in self.cols:
				self.setCell((col, key), val[key])
			return
		if isinstance(key, _basestring):
			if len(val) != len(self):
				raise Exception(u'Non-matching length for %s' % val)
			self.setCell(key, list(val))
			return
		raise Exception(u'Invalid key: %s' % key)

	def setCell(self, key, val):

		if self.cellValidator is not None and not self.cellValidator(val):
			raise Exception(u'"%d" is not a valid value' % val)
		if isinstance(key, tuple) and len(key) == 2:
			self.data[key[0]][key[1]] = val
		elif isinstance(key, _basestring):
			self.data[key] = val
		else:
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
	def cells(self):

		"""
		name:		cells
		returns:
			desc:	A list of all col, row combinations.
			type:	list
		"""

		return list(itertools.product(self.cols, self.range))

	@property
	def cols(self):

		"""
		name:		cols
		returns:
			desc:	A list of collum names
			type:	list
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

	def copyFrom(self, df):

		"""
		desc:
			Turns the current DataFrame into a copy of anothe DataFrame.

		arguments:
				df:		The dataframe to copy.
				type:	DataFrame
		"""

		df = df.copy()
		self.data = df.data
		self._len = df._len

	def copy(self):

		"""
		returns:
				desc:	A deep copy of the current `DataFrame`.
				type:	DataFrame
		"""

		df = DataFrame(self.cols, len(self), default=self.default,
			colValidator=self.colValidator, cellValidator=self.cellValidator)
		df.data = copy.deepcopy(self.data)
		return df

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
			rows = list(range(len(self)))
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
		self._len = len(keep_rows)
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

	def sliceValues(self, _slice):

		for col, row in self.cells:
			self[col, row] = self[col, row][_slice]
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

	def swapCols(self, col1, col2):

		self.rename(col1, '__tmp__')
		self.rename(col2, col1)
		self.rename('__tmp__', col2)

		tmp = self[col1]
		self[col1] = self[col2]
		self[col2] = tmp

	def rename(self, oldKey, newKey):

		if oldKey not in self:
			raise Exception(u'Column "%s" does not exist' % oldKey)
		if newKey in self:
			raise Exception(u'Column "%s" already exists' % newKey)
		if self.colValidator is not None and not self.colValidator(newKey):
			raise Exception(u'"%s" is not a valid column name' % newKey)
		self.data = OrderedDict(
			(newKey if k == oldKey else k, v) for k, v in self.data.items())

	def emptyCol(self):

		return [self.default]*len(self)

class DataFrameIterator:

	def __init__(self, df):
		self.df = df
		self.i = 0

	def __iter__(self):
		return self

	def __next__(self):
		# For Python 3
		return self.next()

	def next(self):
		if self.i >= len(self.df):
			raise StopIteration
		self.i += 1
		if len(self.df.cols) == 1:
			return self.df[self.df.cols[0], self.i - 1]
		return self.df[self.i - 1]

random.seed()
