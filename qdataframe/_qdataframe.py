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

	"""
	desc:
		A decorator that adds the operations done by a function to the undo
		stack.
	"""

	def inner(self, *args, **kwdict):

		if self.autoUpdate:
			undo = self.startUndoAction()
		else:
			undo = False
		retval = fnc(self, *args, **kwdict)
		if undo:
			self.endUndoAction()
		return retval

	return inner

class QDataFrame(DataFrame, QWidget):

	"""
	desc:
		A Qt widget that provides a view of a datawidget.
	"""

	notify = pyqtSignal(_unicode)

	def __init__(self, *arglist, **kwdict):

		"""
		desc:
			Constructor

		argument-list:
			arglist:	See DataFrame.__init__().

		keyword-dict:
			kwdict:		See DataFrame.__init__(). In addition, you can pass
						a `parent`, which should be a QWidget, and a
						`toolButtons`, which is a bool indicating whether
						toolbuttons are shown above the table.
		"""

		if u'parent' in kwdict:
			parent = kwdict[u'parent']
			del kwdict[u'parent']
		else:
			parent = None
		if u'toolButtons' in kwdict and kwdict[u'toolButtons']:
			self.addToolButtons = True
			del kwdict[u'toolButtons']
		else:
			self.addToolButtons = False
		DataFrame.__init__(self, *arglist, **kwdict)
		QWidget.__init__(self, parent)
		self.undoStack = []
		self.inUndoAction = False
		self.autoUpdate = True
		self.table = QDataFrameTable(self)
		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		if self.addToolButtons:
			self.toolButtons = QToolButtons(self)
			self.layout.addWidget(self.toolButtons)
		self.layout.addWidget(self.table)
		self.setLayout(self.layout)
		self.shortcutUndo = QShortcut(QKeySequence(u'Ctrl+Z'), self, self.undo,
			context=Qt.WidgetWithChildrenShortcut)

	def addUndoHistory(self):

		"""
		desc:
			Adds the current state to the undo stack.
		"""

		if not self.inUndoAction:
			self.undoStack.append(self.copy())

	def undo(self):

		"""
		desc:
			Reverts to the last state of the undo stack (if any).
		"""

		self.inUndoAction = True
		if len(self.undoStack) == 0:
			self.inUndoAction = False
			return
		df = self.undoStack.pop()
		self.copyFrom(df)
		self.inUndoAction = False

	def startUndoAction(self):

		"""
		desc:
			Starts an undo action.
		"""

		if self.inUndoAction:
			return False
		self.addUndoHistory()
		self.inUndoAction = True
		return True

	def endUndoAction(self):

		"""
		desc:
			Ends an undo action.
		"""

		self.inUndoAction = False

	def clearUndo(self):

		"""
		desc:
			Clears the undo stack.
		"""

		self.undoStack = []

	def _print(self):

		print(self)

	def setCell(self, key, val):

		DataFrame.setCell(self, key, val)
		if not self.autoUpdate:
			return
		if isinstance(key, tuple) and len(key) == 2:
			col = self.cols.index(key[0])
			row = key[1]
			item = QCell(val)
			self.table.setItem(row, col, item)
		elif isinstance(key, _basestring):
			col = self.cols.index(key)
			for row, _val in zip(self.range, val):
				item = QCell(_val)
				self.table.setItem(row, col, item)

	def uniqueName(self):

		"""
		returns:
			desc:	A unique column name.
			type:	str
		"""

		name = stem = _(u'untitled')
		i = 1
		while name in self.cols:
			name = stem + u'-%d' % i
			i += 1
		return name

	@undoable
	def copyFrom(self, df):

		"""
		desc:
			Turns the current dataframe into a copy of the passed dataframe.

		arguments:
			df:
				desc:	The dataframe to copy.
				type:	DataFrame
		"""

		DataFrame.copyFrom(self, df)
		if not self.autoUpdate:
			return
		self.table.refresh()

	@undoable
	def insert(self, key, index=-1):
		
		DataFrame.insert(self, key, index)
		if not self.autoUpdate:
			return
		self.table.refresh()

	@undoable
	def __delitem__(self, key):

		DataFrame.__delitem__(self, key)
		if not self.autoUpdate:
			return
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
		if not self.autoUpdate:
			return
		self.table.horizontalHeaderItem(
			self.cols.index(newKey)).setText(newKey)
