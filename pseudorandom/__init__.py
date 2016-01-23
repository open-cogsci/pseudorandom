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
	Copyright 2015-2016 Sebastiaan Mathôt

	v%-- python: "import pseudorandom; print pseudorandom.__version__" --%

	<http://www.cogsci.nl/smathot>

	A package for pseudorandomization of DataMatrix objects. That is, it allows
	you to apply certain constraints to the randomization.

	Current unittest status: [![Build Status](https://travis-ci.org/smathot/python-pseudorandom.svg?branch=master)](https://travis-ci.org/smathot/python-pseudorandom)

	## Example

	~~~ .python
	%-- include: "examples/example.py" --%
	~~~

	## Dependencies

	- [python-datamatrix](https://github.com/smathot/python-datamatrix)

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

__version__ = u'0.2.0'

from pseudorandom._enforce import Enforce
from pseudorandom._constraint import MaxRep, MinDist
from pseudorandom._exceptions import EnforceFailed, InvalidConstraint
