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

from qdataframe.pyqt import QTableWidget, QShortcut, QKeySequence, \
	QApplication, Qt
from dataframe import DataFrame
from qdataframe._qcell import QCell
from qdataframe._qcelldelegate import QCellDelegate
from qdataframe._qtableheader import QColumnHeader, QRowHeader
from qdataframe._menu import QCellMenu

def disconnected(fnc):

	def inner(self, *args, **kwdict):

		try:
			self.cellChanged.disconnect()
			cellChanged = True
		except:
			cellChanged = False
		retval = fnc(self, *args, **kwdict)
		if cellChanged:
			self.cellChanged.connect(self.onCellChanged)
		return retval

	return inner

class QDataFrameTable(QTableWidget):

	def __init__(self, df):

		"""
		desc:
			Constructor.

		arguments:
			df:
				desc:	A dataframe.
				type:	QDataFrame
		"""

		QTableWidget.__init__(self, df)
		self.df = df
		self.cellDelegate = QCellDelegate(self)
		self.cellDelegate.move.connect(self.move)
		self.setItemDelegate(self.cellDelegate)
		self.setItemPrototype(QCell())
		self.columnHeader = QColumnHeader(self)
		self.setHorizontalHeader(self.columnHeader)
		self.rowHeader = QRowHeader(self)
		self.setVerticalHeader(self.rowHeader)
		self.refresh()
		self.shortcutCopy = QShortcut(QKeySequence(u'Ctrl+C'), self, self.copy,
			context=Qt.WidgetWithChildrenShortcut)
		self.shortcutPaste = QShortcut(QKeySequence(u'Ctrl+V'), self,
			self.paste, context=Qt.WidgetWithChildrenShortcut)
		self.shortcutCut = QShortcut(QKeySequence(u'Ctrl+X'), self,
			self.cut, context=Qt.WidgetWithChildrenShortcut)
		self.shortcutPrint = QShortcut(QKeySequence(u'Ctrl+P'), self,
			self.df._print, context=Qt.WidgetWithChildrenShortcut)
		self.shortcutClear = QShortcut(QKeySequence(u'Del'), self,
			self.delete, context=Qt.WidgetWithChildrenShortcut)
		self.cellChanged.connect(self.onCellChanged)
		self.currentCellChanged.connect(self.onCurrentCellChanged)

	@property
	def clipboard(self):
		return QApplication.clipboard()

	@property
	def notify(self):
		return self.df.notify

	def move(self, dRow, dCol):

		"""
		desc:
			Move the cursor, i.e. the selected cell.

		arguments:
			dRow:
				desc:	The number of rows to move.
				type:	int
			dCol:
				desc:	The number of columns to move.
				type:	int
		"""

		row = min(self.rowCount()-1, max(1, self.currentRow()+dRow))
		col = min(self.columnCount()-1, max(1, self.currentColumn()+dCol))
		self.setCurrentCell(row, col)

	@disconnected
	def onCellChanged(self, row, colNr):

		"""
		desc:
			Updates the dataframe when a cell in the GUI is changed.

		arguments:
			row:
				desc:	The row number in GUI coordinates.
				type:	int
			colNr:
				desc:	The column number in GUI coordinates.
				type:	int
		"""

		col = self.df.cols[colNr]
		item = self.item(row, colNr)
		self.df.startUndoAction()
		DataFrame.setCell(self.df, (col, row), item.text())
		item.updateStyle()
		self.df.endUndoAction()

	@disconnected
	def onCurrentCellChanged(self, toRow, toCol, fromRow, fromCol):

		"""
		desc:
			Highlights the currently active row and column headers.
		"""

		if fromCol != toCol:
			item = self.horizontalHeaderItem(fromCol)
			if item is not None: item.unhighlight()
			item = self.horizontalHeaderItem(toCol)
			if item is not None: item.highlight()
		if fromRow != toRow:
			item = self.verticalHeaderItem(fromRow)
			if item is not None: item.unhighlight()
			item = self.verticalHeaderItem(toRow)
			if item is not None: item.highlight()

	@disconnected
	def contextMenuEvent(self, e):

		"""
		desc:
			Shows a context menu.

		arguments:
			e:
				type:	QContextMenuEvent
		"""

		selection = self.selectedItems()
		if len(selection) > 1:
			menu = QCellMenu(selection)
		else:
			item = self.itemAt(e.pos())
			menu = QCellMenu([item])
		action = menu.exec_(e.globalPos())
		if action is not None:
			action.do()

	@disconnected
	def refresh(self):

		"""
		desc:
			Restores the GUI from the dataframe.
		"""

		# Give the table the right dimensions
		self.setRowCount(len(self.df))
		self.setColumnCount(len(self.df.cols))
		# Fill the table with QCells
		for colNr, col in enumerate(self.df.cols):
			# Set the column headers
			item = QCell(col, style=u'header')
			self.setHorizontalHeaderItem(colNr, item)
			# Set the cells
			for row in self.df.range:
				item = QCell(self.df[col, row])
				self.setItem(row, colNr, item)
		# Set the row heades
		for row in self.df.range:
			item = QCell(row+1, style=u'row')
			self.setVerticalHeaderItem(row, item)

	def cut(self):

		"""
		desc:
			Copies the current selection to the clipboard, and then clears the
			current selection.
		"""

		self.copy(clear=True)

	def delete(self):

		"""
		desc:
			Clears the current selection.
		"""

		self.copy(clear=True, copy=False)

	@disconnected
	def copy(self, clear=False, copy=True):

		"""
		desc:
			Copies the current selection to the clipboard.

		keywords:
			clear:
				desc:	Indicates whether copied cells should be cleared.
				type:	bool
			copy:
				desc:	Indicates whether cells should be copied to the
						clipboard.
				type:	bool
		"""

		if clear:
			self.df.startUndoAction()
		# Get the start and end of the selection
		l = self.selectedRanges()
		if len(l) == 0:
			return
		firstRow = min([r.topRow() for r in l])
		firstColNr = min([r.leftColumn() for r in l])
		lastRow = max([r.bottomRow() for r in l])
		lastColNr = max([r.rightColumn() for r in l])
		colSpan = lastColNr - firstColNr + 1
		rowSpan = lastRow - firstRow + 1
		# Create an empty list of lists, where the value __empty__ indicates
		# that there's nothing in it (not even an empty string). This allows us
		# to deal with non-contiguous selections.
		matrix = []
		for col in range(rowSpan):
			matrix.append([u'__empty__']*colSpan)
		# Add all selected cells.
		for item in self.selectedItems():
			row = self.row(item)-firstRow
			colNr = self.column(item)-firstColNr
			matrix[row][colNr] = item.text()
			if clear:
				col = self.df.cols[self.column(item)]
				row = self.row(item)
				self.df[col, row] = u''
		# Convert the selection to text and put it on the clipboard
		txt = u'\n'.join([u'\t'.join(_col) for _col in matrix])
		if copy:
			self.clipboard.setText(txt)
		if clear:
			self.df.endUndoAction()

	@disconnected
	def paste(self):

		"""
		desc:
			Pastes the current clipboard contents onto the DataFrame.
		"""

		self.df.startUndoAction()
		txt = self.clipboard.mimeData().text()
		rows = txt.split(u'\n')
		cRow = self.currentRow()
		for row in rows:
			cells = row.split(u'\t')
			cCol = self.currentColumn()
			for cell in cells:
				if cCol >= self.columnCount():
					break
				col = self.df.cols[cCol]
				self.df[col, cRow] = cell
				cCol += 1
			cRow += 1
			if cRow >= self.rowCount():
				break
		self.df.endUndoAction()
