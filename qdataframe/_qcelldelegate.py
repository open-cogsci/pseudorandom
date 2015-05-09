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

from qdataframe.pyqt import QStyledItemDelegate, pyqtSignal, QEvent, Qt

class QCellDelegate(QStyledItemDelegate):

	"""
	desc:
		A delegate that intercepts left and right keypresses to move to previous
		and next cells in the table.
	"""

	move = pyqtSignal(int, int)

	def eventFilter(self, lineEdit, e):

		if e.type() == QEvent.KeyPress:
			if e.key() in [Qt.Key_Left, Qt.Key_Right]:
				self.commitData.emit(lineEdit)
				self.closeEditor.emit(lineEdit, self.NoHint)
				if e.key() == Qt.Key_Left:
					self.move.emit(0, -1)
				else:
					self.move.emit(0, 1)
				return True
		return QStyledItemDelegate.eventFilter(self, lineEdit, e)
