<span class="ModuleDoc YAMLDoc" id="pseudorandom" markdown="1">

# *module* pseudorandom

Copyright 2015-2016 Sebastiaan Mathôt

v0.2.0


<http://www.cogsci.nl/smathot>

A package for pseudorandomization of DataMatrix objects. That is, it allows
you to apply certain constraints to the randomization.

Current unittest status: [![Build Status](https://travis-ci.org/smathot/python-pseudorandom.svg?branch=master)](https://travis-ci.org/smathot/python-pseudorandom)

## Example

~~~ .python
from datamatrix import io
from pseudorandom import Enforce, MaxRep, MinDist

# Read a datafile with Pandas and convert it to a pseudorandom DataFrame.
dm = io.readtxt('examples/data.csv')
print(dm)
# Create an Enforce object, and add two constraints
ef = Enforce(dm)
ef.add_constraint(MaxRep, cols=[dm.category], maxrep=1)
ef.add_constraint(MinDist, cols=[dm.word], mindist=4)
# Enforce the constraints
dm = ef.enforce()
# See the resulting DataFrame and a report of how long the enforcement took.
print(dm)
print(ef.report)

~~~

## Dependencies

- [python-datamatrix](https://github.com/smathot/python-datamatrix)

## License

`pseudorandom` is released under the GNU General Public License 3. See the
included file `COPYING` for details or visit
<http://www.gnu.org/copyleft/gpl.html>.

## Overview


- [Example](#example)
- [Dependencies](#dependencies)
- [License](#license)
- [Overview](#overview)
- [class __pseudorandom.Enforce__](#class-__pseudorandomenforce__)
	- [function __pseudorandom\.Enforce\.\_\_init\_\___\(dm\)](#function-__pseudorandomenforce__init____dm)
	- [function __pseudorandom\.Enforce\.add\_constraint__\(constraint, \*\*kwargs\)](#function-__pseudorandomenforceadd_constraint__constraint-kwargs)
	- [function __pseudorandom\.Enforce\.enforce__\(maxreshuffle=100, maxpass=100\)](#function-__pseudorandomenforceenforce__maxreshuffle100-maxpass100)
- [class __pseudorandom.MaxRep__](#class-__pseudorandommaxrep__)
- [class __pseudorandom.MinDist__](#class-__pseudorandommindist__)



<span class="ClassDoc YAMLDoc" id="pseudorandom-Enforce" markdown="1">

## class __pseudorandom.Enforce__

A class that enforces a set of constraints by modifying (if necessary) the DataMatrix.

<span class="FunctionDoc YAMLDoc" id="pseudorandom-Enforce-__init__" markdown="1">

### function __pseudorandom\.Enforce\.\_\_init\_\___\(dm\)

Constructor.

__Arguments:__

- `dm` -- The data.
	- Type: DataMatrix

</span>

[pseudorandom.Enforce.__init__]: #pseudorandom-Enforce-__init__
[Enforce.__init__]: #pseudorandom-Enforce-__init__
[__init__]: #pseudorandom-Enforce-__init__

<span class="FunctionDoc YAMLDoc" id="pseudorandom-Enforce-add_constraint" markdown="1">

### function __pseudorandom\.Enforce\.add\_constraint__\(constraint, \*\*kwargs\)

Adds a constraint to enforce.

__Arguments:__

- `constraint` -- A constraint class. Note, the class itself should be passed, not an instance of the class.
	- Type: type

__Keyword dict:__

- `**kwargs`: The keyword arguments that are passed to the constraint constructor.

</span>

[pseudorandom.Enforce.add_constraint]: #pseudorandom-Enforce-add_constraint
[Enforce.add_constraint]: #pseudorandom-Enforce-add_constraint
[add_constraint]: #pseudorandom-Enforce-add_constraint

<span class="FunctionDoc YAMLDoc" id="pseudorandom-Enforce-enforce" markdown="1">

### function __pseudorandom\.Enforce\.enforce__\(maxreshuffle=100, maxpass=100\)

Enforces constraints.

__Keywords:__

- `maxreshuffle` -- No description
	- Default: 100
- `maxpass` -- The maximum number of times that the enforce algorithm may be restarted.
	- Type: int
	- Default: 100

__Returns:__

A `DataMatrix` that respects the constraints.

- Type: DataMatrix

</span>

[pseudorandom.Enforce.enforce]: #pseudorandom-Enforce-enforce
[Enforce.enforce]: #pseudorandom-Enforce-enforce
[enforce]: #pseudorandom-Enforce-enforce

</span>

[pseudorandom.Enforce]: #pseudorandom-Enforce
[Enforce]: #pseudorandom-Enforce

<span class="ClassDoc YAMLDoc" id="pseudorandom-MaxRep" markdown="1">

## class __pseudorandom.MaxRep__

Limits the number of times that a value can occur in direct succession. A maxrep of 1 means that values cannot be repeated.

__Example:__

~~~ .python
ef = Enforce(df)
ef.add_constraint(MaxRep, cols=['word'], maxrep=2)
~~~

</span>

[pseudorandom.MaxRep]: #pseudorandom-MaxRep
[MaxRep]: #pseudorandom-MaxRep

<span class="ClassDoc YAMLDoc" id="pseudorandom-MinDist" markdown="1">

## class __pseudorandom.MinDist__

Sets a minimum distance between value repetitions. A minimum distance of 2 avoids direct repetitions.

__Example:__

~~~ .python
ef = Enforce(dm)
ef.add_constraint(MinDist, cols=['word'], mindist=2)
~~~

</span>

[pseudorandom.MinDist]: #pseudorandom-MinDist
[MinDist]: #pseudorandom-MinDist

</span>

[pseudorandom]: #pseudorandom


[Example]: #example
[Dependencies]: #dependencies
[License]: #license
[Overview]: #overview
[class __pseudorandom.Enforce__]: #class-__pseudorandomenforce__
[function __pseudorandom\.Enforce\.\_\_init\_\___\(dm\)]: #function-__pseudorandomenforce__init____dm
[function __pseudorandom\.Enforce\.add\_constraint__\(constraint, \*\*kwargs\)]: #function-__pseudorandomenforceadd_constraint__constraint-kwargs
[function __pseudorandom\.Enforce\.enforce__\(maxreshuffle=100, maxpass=100\)]: #function-__pseudorandomenforceenforce__maxreshuffle100-maxpass100
[class __pseudorandom.MaxRep__]: #class-__pseudorandommaxrep__
[class __pseudorandom.MinDist__]: #class-__pseudorandommindist__