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

from qdataframe.pyqt import QDialog, QFormLayout, QLabel, QLineEdit, Qt, \
	QDialogButtonBox, QIcon, _
from qdataframe._qdataframe import QDataFrame

class QTextImportDialog(QDialog):

	"""
	desc:
		A dialog for choosing a delimiter and quotation character during text
		input.
	"""

	def __init__(self, table, path):

		"""
		desc:
			Constructor.

		arguments:
			table:
				desc:	A table
				type:	QDataFrameTable
			path:
				desc:	The path to a text file to import.
				type:	str
		"""

		QDialog.__init__(self, table)
		self.table = table
		self.df = table.df
		self.path = path
		self.labelDelimiter = QLabel(_(u'Delimiter (column separator)'), self)
		self.labelQuoteChar = QLabel(_(u'Quote character'), self)
		self.labelPreview = QLabel(_(u'Preview'), self)
		self.editDelimiter = QLineEdit(u',', self)
		self.editDelimiter.textChanged.connect(self.updatePreview)
		self.editQuoteChar = QLineEdit(u'"', self)
		self.editQuoteChar.textChanged.connect(self.updatePreview)
		self.buttonBox = QDialogButtonBox(self)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.preview = QDataFrame([], 0, parent=self)
		self.layout = QFormLayout(self)
		self.layout.addRow(self.labelDelimiter, self.editDelimiter)
		self.layout.addRow(self.labelQuoteChar, self.editQuoteChar)
		self.layout.addRow(self.labelPreview)
		self.layout.addRow(self.preview)
		self.layout.addRow(self.buttonBox)
		self.setLayout(self.layout)
		self.setWindowTitle(_(u'Import text data'))
		self.setWindowIcon(QIcon.fromTheme(u'text-x-generic'))
		self.hasOk = False
		self.updatePreview()

	def updatePreview(self):

		"""
		desc:
			Updates the preview of the data.
		"""

		try:
			df = QDataFrame.fromText(self.path,
				delimiter=self.editDelimiter.text(),
				quote=self.editQuoteChar.text(), parent=self.table)
			self.buttonBox.setStandardButtons(
				QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		except Exception as e:
			df = QDataFrame([u'Failed to read'], 0, parent=self.table)
			self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
		self.preview.copyFrom(df)

	def getTextImportSettings(self):

		"""
		desc:
			Executes the dialog and returns the chosen settings.

		returns:
			desc:	A (delimiter, quote) tuple. If the dialog was cancelled,
					both values are None.
			type:	tuple
		"""

		if self.exec_() == QDialog.Rejected:
			return None, None
		return self.editDelimiter.text(), self.editQuoteChar.text()
