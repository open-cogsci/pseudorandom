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
	QApplication, Qt, QDrag, QMimeData, QTimer
from dataframe import DataFrame
from qdataframe._qcell import QCell
from qdataframe._qdropindicator import QDropIndicator
from qdataframe._menu import QColumnMenu, QRowMenu, QCellMenu, \
	QRowSelectionMenu, QColumnSelectionMenu, QCellSelectionMenu

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
		self.setItemPrototype(QCell())
		self.horizontalHeader().setVisible(False)
		self.verticalHeader().setVisible(False)
		self.setAcceptDrops(True)
		self.refresh()
		self.shortcutCopy = QShortcut(QKeySequence(u'Ctrl+C'), self, self.copy,
			context=Qt.WidgetWithChildrenShortcut)
		self.shortcutPaste = QShortcut(QKeySequence(u'Ctrl+V'), self,
			self.paste, context=Qt.WidgetWithChildrenShortcut)
		self.shortcutCut = QShortcut(QKeySequence(u'Ctrl+X'), self,
			self.cut, context=Qt.WidgetWithChildrenShortcut)
		self.shortcutPrint = QShortcut(QKeySequence(u'Ctrl+P'), self,
			self.df._print, context=Qt.WidgetWithChildrenShortcut)
		self.cellChanged.connect(self.onCellChanged)
		self.currentCellChanged.connect(self.onCurrentCellChanged)
		self.pendingDragData = None
		self.dragTimer = None
		self.dropIndicator = QDropIndicator(self)

	@property
	def clipboard(self):
		return QApplication.clipboard()

	@property
	def notify(self):
		return self.df.notify

	def mousePressEvent(self, e):

		QTableWidget.mousePressEvent(self, e)
		if e.buttons() != Qt.LeftButton:
			return
		item = self.itemAt(e.pos())
		if item is None:
			return
		if item.style in (u'row', u'header'):
			# Drags are not started right away, but only after the mouse has been
			# pressed for a minimum interval. To accomplish this, we set a timer,
			# and cancel the timer when the mouse cursor is released.
			if self.dragTimer is not None:
				self.dragTimer.stop()
			self.pendingDragData = u'__%s__:%s' % (item.style, item.text())
			self.dragTimer = QTimer()
			self.dragTimer.setSingleShot(True)
			self.dragTimer.setInterval(150)
			self.dragTimer.timeout.connect(self.startDrag)
			self.dragTimer.start()
			e.accept()

	def mouseReleaseEvent(self, e):

		"""
		desc:
			Cancels pending drag operations when the mouse is released to
			quickly. This avoids accidental dragging.

		arguments:
			e:
				desc:	A mouse event.
				type:	QMouseEvent
		"""

		QTableWidget.mouseReleaseEvent(self, e)
		self.pendingDragData = None

	def startDrag(self):

		if self.pendingDragData is None:
			return
		mimeData = QMimeData()
		mimeData.setText(self.pendingDragData)
		drag = QDrag(self)
		drag.setMimeData(mimeData)
		drag.exec_()
		self.dropIndicator.hide()

	def dragMoveEvent(self, e):

		self.dragEnterEvent(e)

	def dragEnterEvent(self, e):

		item = self.itemAt(e.pos())
		if item is None or (self.column(item) != 0 and self.row(item) != 0) or \
			(self.column(item) == 0 and self.row(item) == 0):
			e.ignore()
			return
		self.dropIndicator.indicate(item)
		e.accept()

	def dropEvent(self, e):

		"""
		desc:
			Processes drop events to reorder rows and columns.
		"""

		item = self.itemAt(e.pos())
		if item is None:
			e.ignore()
			return
		mimeData = e.mimeData()
		if not mimeData.hasText():
			e.ignore()
			return
		msg = mimeData.text()
		if msg.startswith('__row__:'):
			try:
				fromRow = int(msg[8:])-1
			except:
				e.ignore()
				return
			if fromRow not in self.df.range:
				e.ignore()
				return
			if item.style == u'row':
				toRow = int(item.text())-1
				e.accept()
				if fromRow != toRow:
					if fromRow > toRow:
						fromRow += 1
					self.df.insert(toRow)
					self.df[toRow] = self.df[fromRow]
					del self.df[fromRow]
				self.refresh()
				return
		if msg.startswith('__header__:'):
			try:
				fromCol = msg[11:]
			except:
				e.ignore()
				return
			if fromCol not in self.df.cols:
				e.ignore()
				return
			if item.style == u'header':
				toCol = item.text()
				e.accept()
				if fromCol != toCol:
					self.df.insert(u'__tmp__', index=self.df.cols.index(toCol))
					self.df[u'__tmp__'] = self.df[fromCol]
					del self.df[fromCol]
					self.df.rename(u'__tmp__', fromCol)
				self.refresh()
				return
		e.ignore()

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

		col = self.df.cols[colNr-1]
		item = self.item(row, colNr)
		if row == 0:
			try:
				self.df.rename(col, item.text())
			except Exception as e:
				self.notify(e)
				item.setText(col)
		else:
			DataFrame.setCell(self.df, (col, row-1), item.text())
			item.updateStyle()

	def onCurrentCellChanged(self, toRow, toCol, fromRow, fromCol):

		"""
		desc:
			Prevents the cursor from going into headers, and highlights headers.
		"""

		if fromRow != 0 and fromCol != 0:
			item = self.item(fromRow, 0)
			if item is not None: item.unhighlight()
			item = self.item(0, fromCol)
			if item is not None: item.unhighlight()
		if toRow != 0 and toCol != 0:
			item = self.item(toRow, 0)
			if item is not None: item.highlight()
			item = self.item(0, toCol)
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
			styles = []
			for item in selection:
				if item.style not in styles:
					styles.append(item.style)
			if len(styles) == 1:
				if styles[0] == u'row':
					menu = QRowSelectionMenu(selection)
				elif styles[0] == u'header':
					menu = QColumnSelectionMenu(selection)
			else:
				menu = QCellSelectionMenu(selection)
		else:
			item = self.itemAt(e.pos())
			if item.style == u'header':
				menu = QColumnMenu(item)
			elif item.style == u'row':
				menu = QRowMenu(item)
			else:
				menu = QCellMenu(item)
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
		self.setRowCount(len(self.df)+1)
		self.setColumnCount(len(self.df.cols)+1)
		# Create header row
		for colNr, col in enumerate(self.df.cols):
			item = QCell(col, style=u'header')
			self.setItem(0, colNr+1, item)
		# Create number column
		for row in self.df.range:
			item = QCell(row+1, style=u'row')
			self.setItem(row+1, 0, item)
		# Create disabled corner
		self.setItem(0, 0, QCell(style=u'disabled'))
		# Fill the table with QCells
		for colNr, col in enumerate(self.df.cols):
			for row in self.df.range:
				item = QCell(self.df[col, row])
				self.setItem(row+1, colNr+1, item)

	def cut(self):

		"""
		desc:
			Copies the current selection to the clipboard, and then clears the
			current selection.
		"""

		self.copy(clear=True)

	@disconnected
	def copy(self, clear=False):

		"""
		desc:
			Copies the current selection to the clipboard.

		keywords:
			clear:
				desc:	Indicates whether copied cells should be cleared.
				type:	bool
		"""

		# Get the start and end of the selection
		firstRow = min([r.topRow() for r in self.selectedRanges()])
		firstColNr = min([r.leftColumn() for r in self.selectedRanges()])
		lastRow = max([r.bottomRow() for r in self.selectedRanges()])
		lastColNr = max([r.rightColumn() for r in self.selectedRanges()])
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
				col = self.cols[self.column(item)-1]
				row = self.row(item)-1
				self[col, row] = u''
		# Convert the selection to text and put it on the clipboard
		txt = u'\n'.join([u'\t'.join(_col) for _col in matrix])
		self.clipboard.setText(txt)
		if clear:
			self.refresh()

	@disconnected
	def paste(self):

		"""
		desc:
			Pastes the current clipboard contents onto the DataFrame.
		"""

		txt = self.clipboard.mimeData().text()
		rows = txt.split(u'\n')
		cRow = self.currentRow()
		for row in rows:
			cells = row.split(u'\t')
			cCol = self.currentColumn()
			for cell in cells:
				if cCol >= self.columnCount():
					break
				col = self.df.cols[cCol-1]
				if cRow == 0:
					try:
						self.df.rename(self, col, cell)
					except Exception as e:
						self.notify(e)
				else:
					DataFrame.setCell(self.df, (col, cRow-1), cell)
				cCol += 1
			cRow += 1
			if cRow >= self.rowCount():
				break
		self.refresh()
