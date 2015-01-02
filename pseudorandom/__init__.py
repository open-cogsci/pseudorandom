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

	v%-- python: "import pseudorandom; print pseudorandom.__version__" --%

	<http://www.cogsci.nl/smathot>

	`pseudorandom` is a library for generating constrained, pseudorandom matrices.
	This is particularly useful for generating condition/ stimulus lists for
	psychological and neuroscientific experiments.

	## Example

	~~~ .python
	%-- include: "example/example.py" --%
	~~~

	## Dependencies

	`pseudorandom` requires only the Python standard library. Python 2.X and
	Python >= 3.3 are supported.

	## License

	`pseudorandom` is released under the GNU General Public License 3. See the
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

from pseudorandom._dataframe import DataFrame
from pseudorandom._enforce import Enforce
from pseudorandom._constraint import MaxRep, MinDist
from pseudorandom import tools
