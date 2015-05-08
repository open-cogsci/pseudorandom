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
	QInsertRowAction, QRemoveRowSelectionAction, QRemoveColumnSelectionAction

class QColumnMenu(QMenu):

	def __init__(self, item):

		QMenu.__init__(self)
		self.addAction(QInsertColumnAction(self, item))
		self.addAction(QRenameColumnAction(self, item))
		self.addAction(QRemoveColumnAction(self, item))

class QRowMenu(QMenu):

	def __init__(self, item):

		QMenu.__init__(self)
		self.addAction(QInsertRowAction(self, item))
		self.addAction(QRemoveRowAction(self, item))

class QCellMenu(QMenu):

	pass

class QRowSelectionMenu(QMenu):

	def __init__(self, selection):

		QMenu.__init__(self)
		self.addAction(QRemoveRowSelectionAction(self, selection))

class QColumnSelectionMenu(QMenu):

	def __init__(self, selection):

		QMenu.__init__(self)
		self.addAction(QRemoveColumnSelectionAction(self, selection))

class QCellSelectionMenu(QMenu):

	pass
