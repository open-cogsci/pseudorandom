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

class QCellAction(QAction):

	def __init__(self, parent, item, text, icon):

		self.item = item
		self.col = self.item.text()
		self.df = self.item.tableWidget().df
		self.table = self.df.table
		QAction.__init__(self, QIcon.fromTheme(icon), text, parent)

	def do(self):

		pass

class QRemoveColumnAction(QCellAction):

	def __init__(self, parent, item):

		QCellAction.__init__(self, parent, item, _(u'Remove %s') % item.text(),
			u'list-remove')

	def do(self):

		del self.df[self.col]

class QInsertColumnAction(QCellAction):

	def __init__(self, parent, item, side):

		QCellAction.__init__(self, parent, item,
			_(u'Insert new column %s' % side), u'list-add')
		self.side = side

	def do(self):

		name = u'untitled'
		while name in self.df:
			name = u'_'+name
		index = self.df.cols.index(self.col)
		if self.side == u'right':
			index += 1
		self.df.insert(name, index=index)

class QRenameColumnAction(QCellAction):

	def __init__(self, parent, item):
		QCellAction.__init__(self, parent, item, _(u'Rename %s') % item.text(),
			u'accessories-text-editor')

	def do(self):

		self.table.editItem(self.item)

class QRemoveRowAction(QCellAction):

	def __init__(self, parent, item):

		QCellAction.__init__(self, parent, item,
			_(u'Remove row %s') % item.text(), u'list-remove')

	def do(self):

		del self.df[int(self.item.text())-1]

class QInsertRowAction(QCellAction):

	def __init__(self, parent, item, side):

		QCellAction.__init__(self, parent, item, _(u'Insert new row %s' % side),
			u'list-add')
		self.side = side

	def do(self):

		index = int(self.item.text())
		if self.side == u'before':
			index -= 1
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
