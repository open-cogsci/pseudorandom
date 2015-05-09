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

from qdataframe.pyqt import QWidget, QVBoxLayout, _, pyqtSignal, \
	QShortcut, QKeySequence, Qt
from qdataframe._qdataframetable import QDataFrameTable
from qdataframe._qtoolbuttons import QToolButtons
from qdataframe._qcell import QCell
from dataframe import DataFrame
from dataframe.py3compat import _basestring, _unicode

def undoable(fnc):

	def inner(self, *args, **kwdict):

		undo = self.startUndoAction()
		retval = fnc(self, *args, **kwdict)
		if undo:
			self.endUndoAction()
		return retval

	return inner

class QDataFrame(DataFrame, QWidget):

	notify = pyqtSignal(_unicode)

	def __init__(self, parent, *arglist, **kwdict):

		DataFrame.__init__(self, *arglist, **kwdict)
		QWidget.__init__(self, parent)
		self.undoStack = []
		self.inUndoAction = False
		self.table = QDataFrameTable(self)
		self.toolButtons = QToolButtons(self)
		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.addWidget(self.toolButtons)
		self.layout.addWidget(self.table)
		self.setLayout(self.layout)
		self.shortcutCopy = QShortcut(QKeySequence(u'Ctrl+Z'), self, self.undo,
			context=Qt.WidgetWithChildrenShortcut)

	def addUndoHistory(self):

		if not self.inUndoAction:
			self.undoStack.append(self.copy())

	def undo(self):

		if len(self.undoStack) == 0:
			return
		df = self.undoStack.pop()
		self.data = df.data
		self._len = df._len
		self.table.refresh()

	def startUndoAction(self):

		if self.inUndoAction:
			return False
		self.addUndoHistory()
		self.inUndoAction = True
		return True

	def endUndoAction(self):

		self.inUndoAction = False

	def clearUndo(self):

		self.undoStack = []

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

	def uniqueName(self):

		name = stem = _(u'untitled')
		i = 1
		while name in self.cols:
			name = stem + u'-%d' % i
			i += 1
		return name

	@undoable
	def insert(self, key, index=-1):

		DataFrame.insert(self, key, index)
		self.table.refresh()

	@undoable
	def __delitem__(self, key):

		DataFrame.__delitem__(self, key)
		if len(self.cols) == 0:
			self.insert(self.uniqueName())
			self.notify.emit(_(u'Created empty column'))
		if len(self) == 0:
			self.insert(0)
			self.notify(_(u'Created empty row'))
		self.table.refresh()

	@undoable
	def __setitem__(self, key, val):
		DataFrame.__setitem__(self, key, val)

	@undoable
	def rename(self, oldKey, newKey):
		DataFrame.rename(self, oldKey, newKey)
