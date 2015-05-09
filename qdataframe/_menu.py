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

from qdataframe.pyqt import QMenu
from qdataframe._action import QRemoveColumnAction, \
	QInsertColumnAction, QRenameColumnAction, QRemoveRowAction, \
	QInsertRowAction, QCutAction, QCopyAction, QPasteAction, QClearAction

class QColumnMenu(QMenu):

	def __init__(self, item):

		QMenu.__init__(self)
		self.addAction(QInsertColumnAction(self, item, u'left'))
		self.addAction(QInsertColumnAction(self, item, u'right'))
		self.addSeparator()
		self.addAction(QRenameColumnAction(self, item))
		self.addAction(QRemoveColumnAction(self, item))

class QRowMenu(QMenu):

	def __init__(self, item):

		QMenu.__init__(self)
		self.addAction(QInsertRowAction(self, item, u'before'))
		self.addAction(QInsertRowAction(self, item, u'after'))
		self.addSeparator()
		self.addAction(QRemoveRowAction(self, item))

class QCellMenu(QMenu):

	def __init__(self, selection):

		QMenu.__init__(self)
		self.addAction(QCutAction(self, selection))
		self.addAction(QCopyAction(self, selection))
		self.addAction(QPasteAction(self, selection))
		self.addSeparator()
		self.addAction(QClearAction(self, selection))
