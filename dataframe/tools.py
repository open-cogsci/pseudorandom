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

---
desc:
	A module with various helper functions.
---
"""

from dataframe._dataframe import DataFrame

def fromPandas(pdf):

	"""
	desc:
		Converts a Pandas DataFrame to a pseudorandom DataFrame.

	arguments:
		pdf:
			desc:	A Pandas DataFrame.
			type:	DataFrame

	returns:
		desc:	A pseudorandom DataFrame.
		type:	DataFrame
	"""

	cols = list(pdf.columns.values)
	rows = len(pdf)
	df = DataFrame(cols=cols, rows=rows)
	for col in cols:
		for i in range(rows):
			df[col, i] = pdf[col][i]
	return df

def fromText(path, delimiter=u',', quote=u'"'):

	import csv
	fd = open('path')
	cols = None
	rows = []
	for row in csv.reader(fd, delimiter=delimiter, quotechar=quote):
		if cols is None:
			cols = row
			continue
		rows.append(row)
	fd.close()
	df = DataFrame(cols, rows=len(rows))
	for colNr, col in enumerate(cols):
		for rwo in range(len(rows)):
			df[col, row] = rows[row, colNr]
	return df
