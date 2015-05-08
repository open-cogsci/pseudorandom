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
desc: |
	Copyright 2015 Sebastiaan Mathôt

	v%-- python: "import dataframe; print dataframe.__version__" --%

	<http://www.cogsci.nl/smathot>

	- `dataframe.DataFrame` is a simple class for tabular data, i.e. data that
	is organized as numbered rows and named columns.
	- `qdataframe.QDataFrame` is a PyQt widget for viewing and manipulating a
	`dataframe.DataFrame`.
	- `qdataframe.Enforce` provides functionality for pseudorandomization. This
	is particularly useful for generating condition/ stimulus lists for
	psychological and neuroscientific experiments.

	Current unittest status: [![Build Status](https://travis-ci.org/smathot/python-pseudorandom.svg?branch=master)](https://travis-ci.org/smathot/python-pseudorandom)

	## Example 1: Creating and viewing a DataFrame

	~~~ .python
	%-- include: "examples/example-basic.py" --%
	~~~

	## Example 2: Pseudorandomization

	~~~ .python
	%-- include: "examples/example-pseudorandomization.py" --%
	~~~

	## Dependencies

	`dataframe` requires only the Python standard library. Python 2.X and
	Python >= 3.3 are supported. `qdataframe` is compatible with PyQt4 and
	PyQt5.

	## License

	`datafrane` is released under the GNU General Public License 3. See the
	included file `COPYING` for details or visit
	<http://www.gnu.org/copyleft/gpl.html>.

	## Overview

	%--
	toc:
		mindepth: 2
	--%
---
"""

__version__ = u'0.1.0'

from dataframe._dataframe import DataFrame
from dataframe._enforce import Enforce
from dataframe._constraint import MaxRep, MinDist
from dataframe._exceptions import EnforceFailed, InvalidConstraint
from dataframe import tools
