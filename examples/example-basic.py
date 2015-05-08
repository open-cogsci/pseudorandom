from qdataframe import QDataFrame
from qdataframe.pyqt import QApplication
import sys
app = QApplication(sys.argv)
df = QDataFrame(None, cols=['a', 'b'], rows=2)
df['a'] = [1,2]
df['b'] = [3,4]
df['b', 1] = 'Test'
df.resize(600, 600)
df.setWindowTitle(u'QDataFrame')
df.show()
sys.exit(app.exec_())
