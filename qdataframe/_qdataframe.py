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

from qdataframe.pyqt import QWidget, QVBoxLayout, QLabel, _, pyqtSignal
from qdataframe._qdataframetable import QDataFrameTable
from qdataframe._qtoolbuttons import QToolButtons
from qdataframe._qcell import QCell
from dataframe import DataFrame
from dataframe.py3compat import _basestring, _unicode

class QDataFrame(DataFrame, QWidget):

	notify = pyqtSignal(_unicode)

	def __init__(self, parent, *arglist, **kwdict):

		DataFrame.__init__(self, *arglist, **kwdict)
		QWidget.__init__(self, parent)
		self.table = QDataFrameTable(self)
		self.toolButtons = QToolButtons(self)
		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.addWidget(self.toolButtons)
		self.layout.addWidget(self.table)
		self.setLayout(self.layout)

	def _print(self):

		print(self)

	def setCell(self, key, val):

		if isinstance(key, tuple) and len(key) == 2:
			col = self.cols.index(key[0])
			row = key[1]
			item = QCell(val)
			self.table.setItem(row+1, col+1, item)
		elif isinstance(key, _basestring):
			col = self.cols.index(key)
			for row, _val in zip(self.range, val):
				item = QCell(_val)
				self.table.setItem(row+1, col+1, item)
		DataFrame.setCell(self, key, val)

	def insert(self, key, index=-1):

		DataFrame.insert(self, key, index)
		self.table.refresh()

	def uniqueName(self):

		name = stem = _(u'untitled')
		i = 1
		while name in self.cols:
			name = stem + u'-%d' % i
			i += 1
		return name

	def __delitem__(self, key):

		DataFrame.__delitem__(self, key)
		if len(self.cols) == 0:
			self.insert(self.uniqueName())
			self.notify.emit(_(u'Created empty column'))
		if len(self) == 0:
			self.insert(0)
			self.notify(_(u'Created empty row'))
		self.table.refresh()
