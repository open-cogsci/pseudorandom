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

from qdataframe.pyqt import QWidget, QIcon, QHBoxLayout, QLabel

class QDropIndicator(QWidget):

	def __init__(self, table):

		QWidget.__init__(self, table)
		self.table = table
		self.colPixmap = QLabel()
		self.colPixmap.setPixmap(QIcon.fromTheme(u'go-top').pixmap(24,24))
		self.rowPixmap = QLabel()
		self.rowPixmap.setPixmap(QIcon.fromTheme(u'go-first').pixmap(24,24))
		self.layout = QHBoxLayout(self)
		self.layout.addWidget(self.rowPixmap)
		self.layout.addWidget(self.colPixmap)
		self.setLayout(self.layout)
		self.hide()

	def indicate(self, item):

		row = self.table.row(item)
		col = self.table.column(item)
		if row == 0:
			self.rowPixmap.show()
			self.colPixmap.hide()
		else:
			self.rowPixmap.hide()
			self.colPixmap.show()
		y = self.table.rowViewportPosition(row)
		x = self.table.columnViewportPosition(col)
		self.move(x, y)
		self.show()
