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

from qdataframe.pyqt import QAction, QIcon, _, QKeySequence

class QRemoveColumnAction(QAction):

	def __init__(self, parent, df, col):

		QAction.__init__(self, QIcon.fromTheme(u'list-remove'),
			_(u'Remove %s' % col), parent)
		self.df = df
		self.col = col

	def do(self):

		del self.df[self.col]

class QInsertColumnAction(QAction):

	def __init__(self, parent, df, col, side):

		QAction.__init__(self, QIcon.fromTheme(u'list-add'),
			_(u'Insert new column %s' % side), parent)
		self.side = side
		self.df = df
		self.col = col

	def do(self):

		name = u'untitled'
		while name in self.df:
			name = u'_'+name
		index = self.df.cols.index(self.col)
		if self.side == u'right':
			index += 1
		self.df.insert(name, index=index)

class QRenameColumnAction(QAction):

	def __init__(self, parent, df, col):

		QAction.__init__(self, QIcon.fromTheme(u'accessories-text-editor'),
			_(u'Rename %s' % col), parent)
		self.df = df
		self.col = col

	def do(self):

		self.df.table.columnHeader.editHeader(self.df.cols.index(self.col))

class QRemoveRowAction(QAction):

	def __init__(self, parent, df, row):

		QAction.__init__(self, QIcon.fromTheme(u'list-remove'),
			_(u'Remove row %d') % (row+1), parent)
		self.df = df
		self.row = row

	def do(self):

		del self.df[self.row]

class QInsertRowAction(QAction):

	def __init__(self, parent, df, row, side):

		QAction.__init__(self, QIcon.fromTheme(u'list-add'),
			_(u'Insert new row %s' % side), parent)
		self.df = df
		self.row = row
		self.side = side

	def do(self):

		index = self.row
		if self.side == u'after':
			index += 1
		self.df.insert(index)

class QSelectionAction(QAction):

	def __init__(self, parent, selection, text, icon, shortcut=None):

		self.selection = selection
		self.table = self.selection[0].tableWidget()
		QAction.__init__(self, QIcon.fromTheme(icon), text, parent)
		if shortcut is not None:
			self.setShortcut(QKeySequence(shortcut))

	def do(self):

		pass

class QCutAction(QSelectionAction):

	def __init__(self, parent, selection):

		QSelectionAction.__init__(self, parent, selection, _(u'Cut'),
			u'edit-cut', shortcut=u'Ctrl+X')

	def do(self):

		self.table.cut()

class QCopyAction(QSelectionAction):

	def __init__(self, parent, selection):

		QSelectionAction.__init__(self, parent, selection, _(u'Copy'),
			u'edit-copy', shortcut=u'Ctrl+C')

	def do(self):

		self.table.copy()

class QPasteAction(QSelectionAction):

	def __init__(self, parent, selection):

		QSelectionAction.__init__(self, parent, selection, _(u'Paste'),
			u'edit-paste', shortcut=u'Ctrl+V')

	def do(self):

		self.table.paste()

class QClearAction(QSelectionAction):

	def __init__(self, parent, selection):

		QSelectionAction.__init__(self, parent, selection, _(u'Clear'),
			u'edit-delete', shortcut=u'Del')
		if self.table.clipboard.text() == u'':
			self.setEnabled(False)

	def do(self):

		self.table.delete()
