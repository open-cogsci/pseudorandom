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

from qdataframe.pyqt import QHeaderView, QLineEdit, Qt
from qdataframe._menu import QColumnMenu, QRowMenu
from dataframe.py3compat import _unicode

class QRowHeader(QHeaderView):

	def __init__(self, table):

		QHeaderView.__init__(self, Qt.Vertical, table)
		self.table = table
		self.df = table.df
		self.setMovable(True)
		self.sectionMoved.connect(self.moveRows)
		self.setClickable(True)

	def moveRows(self, logicalIndex, fromRow, toRow):

		_fromRow = fromRow
		_toRow = toRow
		self.df.startUndoAction()
		self.df.autoUpdate = False
		if toRow > fromRow:
			toRow += 1
		else:
			fromRow += 1
		self.df.insert(toRow)
		self.df[toRow] = self.df[fromRow]
		del self.df[fromRow]
		self.df.autoUpdate = True
		self.df.endUndoAction()
		self.df.table.refresh()
		# Restore the logical to visual index mapping
		self.sectionMoved.disconnect()
		self.moveSection(_toRow, _fromRow)
		self.sectionMoved.connect(self.moveRows)

	def contextMenuEvent(self, e):

		row = self.logicalIndexAt(e.pos())
		QRowMenu(self.df, row).go(e.globalPos())

class QColumnHeader(QHeaderView):

	"""
	desc:
		An editable column header. Adapted from:

		http://www.qtcentre.org/threads/12835-How-to-edit-Horizontal-Header-\
			Item-in-QTableWidget
	"""

	def __init__(self, table):

		QHeaderView.__init__(self, Qt.Horizontal, table)
		self.table = table
		self.df = table.df
		self.setMovable(True)
		self.setClickable(True)
		self.line = QLineEdit(parent=self.viewport())
		self.line.setAlignment(Qt.AlignCenter)
		self.line.setHidden(True)
		self.line.blockSignals(True)
		self.sectionDoubleClicked.connect(self.editHeader)
		self.sectionMoved.connect(self.moveColumns)
		self.line.editingFinished.connect(self.doneEditing)

	def moveColumns(self, logicalIndex, fromColNr, toColNr):

		_fromColNr = fromColNr
		_toColNr = toColNr
		self.df.startUndoAction()
		self.df.autoUpdate = False
		if toColNr > fromColNr:
			toColNr += 1
		tmp = self.df.uniqueName()
		col = self.df.cols[fromColNr]
		# Call the DataFrame functions directly to bypass the GUI operations
		# that are added by QDataFrame
		self.df.insert(tmp, index=toColNr)
		self.df[tmp] = self.df[col]
		del self.df[col]
		self.df.rename(tmp, col)
		self.df.autoUpdate = True
		self.df.endUndoAction()
		self.df.table.refresh()
		# Restore the logical to visual index mapping
		self.sectionMoved.disconnect()
		self.moveSection(_toColNr, _fromColNr)
		self.sectionMoved.connect(self.moveColumns)

	def contextMenuEvent(self, e):

		i = self.logicalIndexAt(e.pos())
		col = self.df.cols[i]
		QColumnMenu(self.df, col).go(e.globalPos())

	def doneEditing(self):

		self.line.setHidden(True)
		self.line.blockSignals(True)
		self.df.table.setFocus()
		self.df.table.setCurrentCell(0, self.df.cols.index(self.oldName))
		try:
			self.df.rename(self.oldName, self.line.text())
		except Exception as e:
			self.df.notify.emit(_unicode(e))

	def editHeader(self, section):

		self.oldName = self.df.cols[section]
		edit_geometry = self.line.geometry()
		edit_geometry.setWidth(self.sectionSize(section))
		edit_geometry.moveLeft(self.sectionViewportPosition(section))
		self.line.setGeometry(edit_geometry)
		self.line.setText(self.oldName)
		self.line.setHidden(False)
		self.line.setFocus()
		self.line.blockSignals(False)
		self.line.selectAll()
