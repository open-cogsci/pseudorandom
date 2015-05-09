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

from qdataframe.pyqt import QTableWidgetItem, QFont, QColor, Qt, qt5, \
	QBrush
from dataframe.py3compat import _unicode

class QCell(QTableWidgetItem):

	def __init__(self, val=u'', style=None):

		QTableWidgetItem.__init__(self, _unicode(val))
		self._style = style
		self.updateStyle()

	def setHeaderStyle(self):

		fnt = QFont()
		fnt.setWeight(QFont.Black)
		self.setFont(fnt)
		self.unhighlight()

	def draggable(self):

		return self.style in (u'header', u'row')

	def event(self, e):

		print(e)

	@property
	def style(self):

		if self._style is None:
			try:
				float(self.text())
				return u'numeric'
			except:
				return u'text'
		return self._style

	def updateStyle(self):

		if self.style == u'numeric':
			self.setTextAlignment(Qt.AlignRight)
		elif self.style == u'text':
			self.setTextAlignment(Qt.AlignLeft)
		elif self.style == u'header':
			self.setTextAlignment(Qt.AlignCenter)
			self.setHeaderStyle()
			self.setFlags(self.flags() & ~Qt.ItemIsSelectable)
		elif self.style == u'row':
			self.setTextAlignment(Qt.AlignRight)
			self.setFlags(self.flags() & ~Qt.ItemIsEditable \
				& ~Qt.ItemIsSelectable)
			self.setHeaderStyle()
		elif self.style == u'disabled':
			self.setFlags(self.flags() & ~Qt.ItemIsEnabled \
				& ~Qt.ItemIsSelectable)
		else:
			raise Exception(u'Unknown style: %s' % style)

	def highlight(self):

		self.setBackground(QBrush(QColor(u'#d3d7cf')))

	def unhighlight(self):

		self.setBackground(QBrush(QColor(u'#eeeeec')))
