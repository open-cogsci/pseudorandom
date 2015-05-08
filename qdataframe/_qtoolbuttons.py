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

from qdataframe.pyqt import QWidget, QHBoxLayout, QPushButton, QIcon, \
	QInputDialog, _

class QToolButtons(QWidget):

	def __init__(self, df):

		QWidget.__init__(self, df)
		self.df = df
		self.layout = QHBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.addRowButton = QPushButton(QIcon.fromTheme(u'list-add'),
			_(u'Add rows'))
		self.addRowButton.clicked.connect(self.addRow)
		self.addColButton = QPushButton(QIcon.fromTheme(u'list-add'),
			_(u'Add columns'))
		self.addColButton.clicked.connect(self.addColumn)
		self.importFileButton = QPushButton(QIcon.fromTheme(u'document-open'),
			_(u'Import from file'))
		self.importFileButton.clicked.connect(self.importFile)
		self.importClipboardButton = QPushButton(QIcon.fromTheme(u'edit-paste'),
			_(u'Import from clipboard'))
		self.importClipboardButton.clicked.connect(self.importClipboard)
		self.layout.addWidget(self.addRowButton)
		self.layout.addWidget(self.addColButton)
		self.layout.addWidget(self.importFileButton)
		self.layout.addWidget(self.importClipboardButton)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def addRow(self):

		n, ok = QInputDialog.getInt(self, _(u'New rows'),
			_(u'How many rows do you want to add?'), value=1, min=1)
		if not ok:
			return
		for i in range(n):
			self.df.insert(-1)

	def addColumn(self):

		n, ok = QInputDialog.getInt(self, _(u'New columns'),
			_(u'How many columns do you want to add? (You can change the names '
			u'later.)'), value=1, min=1)
		if not ok:
			return
		for i in range(n):
			self.df.insert(self.df.uniqueName())

	def importFile(self):

		pass

	def importClipboard(self):

		pass
