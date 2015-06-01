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

import sys
if '--qt5' in sys.argv:
	from PyQt5.QtGui import QKeySequence, QFont, QColor, QIcon, QBrush, QDrag, \
		QStyledItemDelegate
	from PyQt5.QtWidgets import QTableWidget, QApplication, QPushButton, \
		QLabel, QInputDialog, QWidget, QShortcut, QTableWidgetItem, \
		QMenu, QAction, QVBoxLayout, QHBoxLayout, QPixmap, QFileDialog, \
		QHeaderView, QLineEdit, QDialog, QFormLayout, QDialogButtonBox
	from PyQt5.QtCore import Qt, QCoreApplication, QMimeData, QTimer, QEvent, \
		pyqtSignal
	qt5 = True
else:
	from PyQt4.QtGui import QTableWidget, QShortcut, QKeySequence, \
		QApplication, QTableWidgetItem, QFont, QColor, QMenu, QAction, QIcon, \
		QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog, \
		QBrush, QDrag, QPixmap, QStyledItemDelegate, QFileDialog, QHeaderView, \
		QLineEdit, QDialog, QFormLayout, QDialogButtonBox
	from PyQt4.QtCore import Qt, QCoreApplication, QMimeData, QTimer, QEvent, \
		pyqtSignal
	qt5 = False
_ = lambda msg: QCoreApplication.translate(u'QDataFrame', msg)
