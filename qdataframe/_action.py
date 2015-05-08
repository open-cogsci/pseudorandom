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

from qdataframe.pyqt import QAction, QIcon

class QCellAction(QAction):

	def __init__(self, parent, item, text, icon):

		self.item = item
		self.col = self.item.text()
		self.dataFrame = self.item.tableWidget().df
		QAction.__init__(self, QIcon.fromTheme(icon), text, parent)

	def do(self):

		pass

class QRemoveColumnAction(QCellAction):

	def __init__(self, parent, item):

		QCellAction.__init__(self, parent, item, u'Remove %s' % item.text(),
			u'list-remove')

	def do(self):

		del self.dataFrame[self.col]

class QInsertColumnAction(QCellAction):

	def __init__(self, parent, item):

		QCellAction.__init__(self, parent, item, u'Insert column left',
			u'list-add')

	def do(self):

		name = u'untitled'
		while name in self.dataFrame:
			name = u'_'+name
		self.dataFrame.insert(name, index=self.dataFrame.cols.index(self.col))

class QRenameColumnAction(QCellAction):

	def __init__(self, parent, item):

		QCellAction.__init__(self, parent, item, u'Rename %s' % item.text(),
			u'accessories-text-editor')

	def do(self):

		self.dataFrame.table.editItem(self.item)

class QRemoveRowAction(QCellAction):

	def __init__(self, parent, item):

		QCellAction.__init__(self, parent, item, u'Remove row %s' % item.text(),
			u'list-remove')

	def do(self):

		del self.dataFrame[int(self.item.text())-1]

class QInsertRowAction(QCellAction):

	def __init__(self, parent, item):

		QCellAction.__init__(self, parent, item, u'Insert row before',
			u'list-add')

	def do(self):

		self.dataFrame.insert(int(self.item.text())-1)

class QSelectionAction(QAction):

	def __init__(self, parent, selection, text, icon):

		self.selection = selection
		self.dataFrame = self.selection[0].tableWidget()
		QAction.__init__(self, QIcon.fromTheme(icon), text, parent)

	def do(self):

		pass

class QRemoveRowSelectionAction(QSelectionAction):

	def __init__(self, parent, selection):

		QSelectionAction.__init__(self, parent, selection,
			u'Remove %d rows' % len(selection), u'list-remove')

	def do(self):

		l = [int(item.text())-1 for item in self.selection]
		for row in sorted(l, reverse=True):
			del self.dataFrame[row]

class QRemoveColumnSelectionAction(QSelectionAction):

	def __init__(self, parent, selection):

		QSelectionAction.__init__(self, parent, selection,
			u'Remove %d columns' % len(selection), u'list-remove')

	def do(self):

		l = [item.text() for item in self.selection]
		for col in l:
			del self.dataFrame[col]
