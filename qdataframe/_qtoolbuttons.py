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

from qdataframe.pyqt import QWidget, QHBoxLayout, QPushButton, QIcon, QMenu, \
	QInputDialog, _, QAction, QFileDialog

class QToolButtons(QWidget):

	def __init__(self, df):

		QWidget.__init__(self, df)
		self.df = df
		self.table = self.df.table
		self.layout = QHBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		# Add menu
		self.addButton = QPushButton(QIcon.fromTheme(u'list-add'),
			_(u'Add'))
		self.addMenu = QMenu(self)
		self.addRowAction = QAction(QIcon.fromTheme(
			u'list-add'), _(u'Rows'), self.addMenu)
		self.addRowAction.triggered.connect(self.addRow)
		self.addMenu.addAction(self.addRowAction)
		self.addColumnAction = QAction(QIcon.fromTheme(
			u'list-add'), _(u'Columns'), self.addMenu)
		self.addColumnAction.triggered.connect(self.addColumn)
		self.addMenu.addAction(self.addColumnAction)
		self.addButton.setMenu(self.addMenu)
		# Import menu
		self.importButton = QPushButton(QIcon.fromTheme(u'document-open'),
			_(u'Import data'))
		self.importMenu = QMenu(self)
		# Import Excel
		self.importExcelAction = QAction(QIcon.fromTheme(
			u'x-office-spreadsheet'), _(u'Excel'), self.importMenu)
		self.importExcelAction.triggered.connect(self.importExcel)
		self.importMenu.addAction(self.importExcelAction)
		self.importMenu.addAction(self.importExcelAction)
		# Import text
		self.importTextAction = QAction(QIcon.fromTheme(
			u'text-x-generic'), _(u'Text data'), self.importMenu)
		self.importTextAction.triggered.connect(self.importText)
		self.importMenu.addAction(self.importTextAction)
		self.importButton.setMenu(self.importMenu)
		self.layout.addWidget(self.addButton)
		self.layout.addWidget(self.importButton)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def addRow(self):

		n, ok = QInputDialog.getInt(self, _(u'New rows'),
			_(u'How many rows do you want to add?'), value=1, min=1)
		if not ok:
			return
		self.df.startUndoAction()
		for i in range(n):
			self.df.insert(-1)
		self.df.endUndoAction()

	def addColumn(self):

		n, ok = QInputDialog.getInt(self, _(u'New columns'),
			_(u'How many columns do you want to add? (You can change the names '
			u'later.)'), value=1, min=1)
		if not ok:
			return
		self.df.startUndoAction()
		for i in range(n):
			self.df.insert(self.df.uniqueName())
		self.df.endUndoAction()

	def importExcel(self):

		path = QFileDialog.getOpenFileName(self, _(u'Import Excel file'),
			filter=_(u'Excel files (*.xlsx *.xls)'))
		if path == u'':
			return
		try:
			df = self.df.fromExcel(path)
		except:
			self.df.notify.emit(_(u'Failed to open "%s"') % path)
			return
		self.df.copyFrom(df)

	def importText(self):

		from qdataframe._qtextimportdialog import QTextImportDialog

		path = QFileDialog.getOpenFileName(self, _(u'Import text file'),
			filter=_(u'Text files (*.csv *.txt *.*)'))
		if path == u'':
			return
		delimiter, quote = QTextImportDialog(self.table,
			path).getTextImportSettings()
		if delimiter is None:
			return
		try:
			df = self.df.fromText(path, delimiter=delimiter, quote=quote)
		except:
			self.df.notify.emit(_(u'Failed to open "%s"') % path)
			return
		self.df.copyFrom(df)

	def importClipboard(self):

		pass
