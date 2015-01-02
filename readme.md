<span class="ModuleDoc YAMLDoc" id="pseudorandom" markdown="1">

# *module* pseudorandom

Copyright 2015 Sebastiaan Mathôt

v0.1.0


<http://www.cogsci.nl/smathot>

`pseudorandom` is a library for generating constrained, pseudorandom matrices.
This is particularly useful for generating condition/ stimulus lists for
psychological and neuroscientific experiments.

## Example

~~~ .python
from pseudorandom import Enforce, MaxRep, MinDist
from pseudorandom import tools
import pandas as pd

# Read a datafile with Pandas and convert it to a pseudorandom DataFrame.
pdf = pd.read_csv('example/data.csv')
df = tools.fromPandas(pdf)
print(df)
# Create an Enforce object, and add two constraints
ef = Enforce(df)
#ef.addConstraint(MaxRep, cols='category', maxRep=1)
ef.addConstraint(MinDist, cols='word', minDist=3)
# Enforce the constraints
df = ef.enforce()
# See the resulting DataFrame and a report of how long the enforcement took.
print(df)
print(ef.report)

~~~

## Dependencies

`pseudorandom` requires only the Python standard library. Python 2.X and
Python >= 3.3 are supported.

## License

`pseudorandom` is released under the GNU General Public License 3. See the
included file `COPYING` for details or visit
<http://www.gnu.org/copyleft/gpl.html>.

## Overview


- [Example](#example)
- [Dependencies](#dependencies)
- [License](#license)
- [Overview](#overview)
- [class __pseudorandom.DataFrame__](#class-__pseudorandomdataframe__)
	- [function __pseudorandom\.DataFrame\.\_\_getitem\_\___\(key\)](#function-__pseudorandomdataframe__getitem____key)
	- [function __pseudorandom\.DataFrame\.\_\_init\_\___\(cols, rows, default=u''\)](#function-__pseudorandomdataframe__init____cols-rows-defaultu)
	- [function __pseudorandom\.DataFrame\.\_\_len\_\___\(\)](#function-__pseudorandomdataframe__len____)
	- [function __pseudorandom\.DataFrame\.\_\_setitem\_\___\(key, val\)](#function-__pseudorandomdataframe__setitem____key-val)
	- [property __pseudorandom.DataFrame.cells__](#property-__pseudorandomdataframecells__)
	- [property __pseudorandom.DataFrame.cols__](#property-__pseudorandomdataframecols__)
	- [function __pseudorandom\.DataFrame\.copy__\(\)](#function-__pseudorandomdataframecopy__)
	- [property __pseudorandom.DataFrame.range__](#property-__pseudorandomdataframerange__)
	- [function __pseudorandom\.DataFrame\.reverse__\(cols=None\)](#function-__pseudorandomdataframereverse__colsnone)
	- [function __pseudorandom\.DataFrame\.shift__\(d=1, cols=None\)](#function-__pseudorandomdataframeshift__d1-colsnone)
	- [function __pseudorandom\.DataFrame\.shuffle__\(cols=None\)](#function-__pseudorandomdataframeshuffle__colsnone)
	- [function __pseudorandom\.DataFrame\.sort__\(cols=None, key=None\)](#function-__pseudorandomdataframesort__colsnone-keynone)
- [class __pseudorandom.Enforce__](#class-__pseudorandomenforce__)
	- [function __pseudorandom\.Enforce\.\_\_init\_\___\(df\)](#function-__pseudorandomenforce__init____df)
	- [function __pseudorandom\.Enforce\.addConstraint__\(constraint, \*\*kwargs\)](#function-__pseudorandomenforceaddconstraint__constraint-kwargs)
	- [function __pseudorandom\.Enforce\.enforce__\(maxReshuffle=100, maxPass=100\)](#function-__pseudorandomenforceenforce__maxreshuffle100-maxpass100)
- [class __pseudorandom.MaxRep__](#class-__pseudorandommaxrep__)
- [class __pseudorandom.MinDist__](#class-__pseudorandommindist__)
- [*module* pseudorandom.tools](#module-pseudorandomtools)
	- [function __pseudorandom\.tools\.fromPandas__\(pdf\)](#function-__pseudorandomtoolsfrompandas__pdf)



<span class="ClassDoc YAMLDoc" id="pseudorandom-DataFrame" markdown="1">

## class __pseudorandom.DataFrame__

A lightweight object for storing data. `pseudorandom.DataFrame` is similar to the `Pandas.DataFrame` class, but does not require any additional libraries, which makes it suitable for environments in which only the Python core libraries are available.

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-__getitem__" markdown="1">

### function __pseudorandom\.DataFrame\.\_\_getitem\_\___\(key\)

Implements the get operator.

__Example:__

~~~ .python
# Getting a DataFrame that is a subset of the current DataFrame:
#
# Print the first row
print(df[0])
# Print the first two rows
print(df[0:2])
# Print the row column
print(df['word'])
# Print the first two rows of the word column
print(df['word', 0:2])

# Getting a single cell:
#
# Print the cell that corresponds to the first row in the word
# column.
print(df['word', 0])

# You can even slice the cells in the DataFrame, by passing a third
# slice. Note that this will fail if some cells cannot be sliced,
# for example because they are integers.
#
# Getting the first two characters from all rows in the word column.
print(df['word', :, :2])
~~~

__Arguments:__

- `key` -- The element to get. This can be `slice` or `int` for rows, `str` for columns, or a `tuple` to get a set of rows for specific columns.
	- Type: str, slice, int, tuple

__Returns:__

A new `DataFrame` that is a subset of the current `DataFrame`.

- Type: DataFrame

</span>

[pseudorandom.DataFrame.__getitem__]: #pseudorandom-DataFrame-__getitem__
[DataFrame.__getitem__]: #pseudorandom-DataFrame-__getitem__
[__getitem__]: #pseudorandom-DataFrame-__getitem__

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-__init__" markdown="1">

### function __pseudorandom\.DataFrame\.\_\_init\_\___\(cols, rows, default=u''\)

Constructor. This creates a `DataFrame` with known columns and rows, but without any content.

__Arguments:__

- `cols` -- A list of column names.
	- Type: list
- `rows` -- The numer of rows.
	- Type: int

__Keywords:__

- `default` -- The default value for the cells.
	- Default: u''

</span>

[pseudorandom.DataFrame.__init__]: #pseudorandom-DataFrame-__init__
[DataFrame.__init__]: #pseudorandom-DataFrame-__init__
[__init__]: #pseudorandom-DataFrame-__init__

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-__len__" markdown="1">

### function __pseudorandom\.DataFrame\.\_\_len\_\___\(\)

Implements the `len()` function.

__Example:__

~~~ .python
print('df has %d rows' % len(df))
~~~

__Returns:__

The number of rows.

- Type: int

</span>

[pseudorandom.DataFrame.__len__]: #pseudorandom-DataFrame-__len__
[DataFrame.__len__]: #pseudorandom-DataFrame-__len__
[__len__]: #pseudorandom-DataFrame-__len__

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-__setitem__" markdown="1">

### function __pseudorandom\.DataFrame\.\_\_setitem\_\___\(key, val\)

Implements the assignment operator.

__Example:__

~~~ .python
# Set the word column
df['word'] = ['cat', 'dog', 'mouse']
# Set the first row
df[0] = ['cat', 10]
# Set the cell that corresponds to the first row in the word column.
df['word', 0] = 'cat'
~~~

__Arguments:__

- `key` -- The element to get. This can be `int` for rows, `str` for columns, or a `tuple` to set a specific cell.
	- Type: str, int, tuple
- `val` -- The value to set. This should be a list when setting an entire column or row.

</span>

[pseudorandom.DataFrame.__setitem__]: #pseudorandom-DataFrame-__setitem__
[DataFrame.__setitem__]: #pseudorandom-DataFrame-__setitem__
[__setitem__]: #pseudorandom-DataFrame-__setitem__

<span class="PropertyDoc YAMLDoc" id="pseudorandom-DataFrame-cells" markdown="1">

### property __pseudorandom.DataFrame.cells__

No description specified.

</span>

[pseudorandom.DataFrame.cells]: #pseudorandom-DataFrame-cells
[DataFrame.cells]: #pseudorandom-DataFrame-cells
[cells]: #pseudorandom-DataFrame-cells

<span class="PropertyDoc YAMLDoc" id="pseudorandom-DataFrame-cols" markdown="1">

### property __pseudorandom.DataFrame.cols__

No description specified.

</span>

[pseudorandom.DataFrame.cols]: #pseudorandom-DataFrame-cols
[DataFrame.cols]: #pseudorandom-DataFrame-cols
[cols]: #pseudorandom-DataFrame-cols

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-copy" markdown="1">

### function __pseudorandom\.DataFrame\.copy__\(\)

No description specified.

__Returns:__

A deep copy of the current `DataFrame`.

- Type: DataFrame

</span>

[pseudorandom.DataFrame.copy]: #pseudorandom-DataFrame-copy
[DataFrame.copy]: #pseudorandom-DataFrame-copy
[copy]: #pseudorandom-DataFrame-copy

<span class="PropertyDoc YAMLDoc" id="pseudorandom-DataFrame-range" markdown="1">

### property __pseudorandom.DataFrame.range__

No description specified.

</span>

[pseudorandom.DataFrame.range]: #pseudorandom-DataFrame-range
[DataFrame.range]: #pseudorandom-DataFrame-range
[range]: #pseudorandom-DataFrame-range

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-reverse" markdown="1">

### function __pseudorandom\.DataFrame\.reverse__\(cols=None\)

Reverses the current `DataFrame` in place.

__Keywords:__

- `cols` -- The columns to reverse or `None` to reverse all columns.
	- Type: list, NoneType
	- Default: None

__Returns:__

The current `DataFrame`.

- Type: DataFrame

</span>

[pseudorandom.DataFrame.reverse]: #pseudorandom-DataFrame-reverse
[DataFrame.reverse]: #pseudorandom-DataFrame-reverse
[reverse]: #pseudorandom-DataFrame-reverse

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-shift" markdown="1">

### function __pseudorandom\.DataFrame\.shift__\(d=1, cols=None\)

Shifts the current `DataFrame` in place. This moves all rows down or up, with wrapping. I.e. moving all rows one step down will cause the last row to become the first.

__Keywords:__

- `d` -- The displacement. Positive displacements move rows down.
	- Type: int
	- Default: 1
- `cols` -- The columns to shift or `None` to shift all columns.
	- Type: list, NoneType
	- Default: None

__Returns:__

The current `DataFrame`.

- Type: DataFrame

</span>

[pseudorandom.DataFrame.shift]: #pseudorandom-DataFrame-shift
[DataFrame.shift]: #pseudorandom-DataFrame-shift
[shift]: #pseudorandom-DataFrame-shift

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-shuffle" markdown="1">

### function __pseudorandom\.DataFrame\.shuffle__\(cols=None\)

Shuffles the current `DataFrame` in place.

__Keywords:__

- `cols` -- The columns to shuffle or `None` to shuffle all columns. Columns are shuffled together, i.e. rows are preserved.
	- Type: list, NoneType
	- Default: None

__Returns:__

The current `DataFrame`.

- Type: DataFrame

</span>

[pseudorandom.DataFrame.shuffle]: #pseudorandom-DataFrame-shuffle
[DataFrame.shuffle]: #pseudorandom-DataFrame-shuffle
[shuffle]: #pseudorandom-DataFrame-shuffle

<span class="FunctionDoc YAMLDoc" id="pseudorandom-DataFrame-sort" markdown="1">

### function __pseudorandom\.DataFrame\.sort__\(cols=None, key=None\)

Sorts the current `DataFrame` in place.

__Keywords:__

- `cols` -- The columns to sort or `None` to sort all columns.
	- Type: list, NoneType
	- Default: None
- `key` -- A column to sort by or `None` to sort each column by itself.
	- Type: str, NoneType
	- Default: None

__Returns:__

The current `DataFrame`.

- Type: DataFrame

</span>

[pseudorandom.DataFrame.sort]: #pseudorandom-DataFrame-sort
[DataFrame.sort]: #pseudorandom-DataFrame-sort
[sort]: #pseudorandom-DataFrame-sort

</span>

[pseudorandom.DataFrame]: #pseudorandom-DataFrame
[DataFrame]: #pseudorandom-DataFrame

<span class="ClassDoc YAMLDoc" id="pseudorandom-Enforce" markdown="1">

## class __pseudorandom.Enforce__

A class that enforces a set of constraints by modifying (if necessary) the `DataFrame`.

<span class="FunctionDoc YAMLDoc" id="pseudorandom-Enforce-__init__" markdown="1">

### function __pseudorandom\.Enforce\.\_\_init\_\___\(df\)

Constructor.

__Arguments:__

- `df` -- The data.
	- Type: DataFrame

</span>

[pseudorandom.Enforce.__init__]: #pseudorandom-Enforce-__init__
[Enforce.__init__]: #pseudorandom-Enforce-__init__
[__init__]: #pseudorandom-Enforce-__init__

<span class="FunctionDoc YAMLDoc" id="pseudorandom-Enforce-addConstraint" markdown="1">

### function __pseudorandom\.Enforce\.addConstraint__\(constraint, \*\*kwargs\)

Adds a constraint to enforce.

__Arguments:__

- `constraint` -- A constraint class. Note, the class itself should be passed, not an instance of the class.
	- Type: type

__Keyword dict:__

- `**kwargs`: The keyword arguments that are passed to the constraint constructor.

</span>

[pseudorandom.Enforce.addConstraint]: #pseudorandom-Enforce-addConstraint
[Enforce.addConstraint]: #pseudorandom-Enforce-addConstraint
[addConstraint]: #pseudorandom-Enforce-addConstraint

<span class="FunctionDoc YAMLDoc" id="pseudorandom-Enforce-enforce" markdown="1">

### function __pseudorandom\.Enforce\.enforce__\(maxReshuffle=100, maxPass=100\)

Enforces constraints.

__Keywords:__

- `maxPass` -- The maximum number of times that the enforce algorithm may be restarted.
	- Type: int
	- Default: 100
- `maxReshuffle` -- No description
	- Default: 100

__Returns:__

A `DataFrame` that respects the constraints.

- Type: DataFrame

</span>

[pseudorandom.Enforce.enforce]: #pseudorandom-Enforce-enforce
[Enforce.enforce]: #pseudorandom-Enforce-enforce
[enforce]: #pseudorandom-Enforce-enforce

</span>

[pseudorandom.Enforce]: #pseudorandom-Enforce
[Enforce]: #pseudorandom-Enforce

<span class="ClassDoc YAMLDoc" id="pseudorandom-MaxRep" markdown="1">

## class __pseudorandom.MaxRep__

Limits the number of times that a value can occur in direct succession. A maxRep of 1 means that values cannot be repeated.

__Example:__

~~~ .python
ef = Enforce(df)
ef.addConstraint(MaxRep, cols=['word'], maxRep=2)
~~~

</span>

[pseudorandom.MaxRep]: #pseudorandom-MaxRep
[MaxRep]: #pseudorandom-MaxRep

<span class="ClassDoc YAMLDoc" id="pseudorandom-MinDist" markdown="1">

## class __pseudorandom.MinDist__

Sets a minimum distance between value repetitions. A minimum distance of 2 avoids direct repetitions.

__Example:__

~~~ .python
ef = Enforce(df)
ef.addConstraint(MinDist, cols=['word'], minDist=2)
~~~

</span>

[pseudorandom.MinDist]: #pseudorandom-MinDist
[MinDist]: #pseudorandom-MinDist

<span class="ModuleDoc YAMLDoc" id="pseudorandom-tools" markdown="1">

## *module* pseudorandom.tools

A module with various helper functions.

<span class="FunctionDoc YAMLDoc" id="pseudorandom-tools-fromPandas" markdown="1">

### function __pseudorandom\.tools\.fromPandas__\(pdf\)

Converts a Pandas DataFrame to a pseudorandom DataFrame.

__Arguments:__

- `pdf` -- A Pandas DataFrame.
	- Type: DataFrame

__Returns:__

A pseudorandom DataFrame.

- Type: DataFrame

</span>

[pseudorandom.tools.fromPandas]: #pseudorandom-tools-fromPandas
[tools.fromPandas]: #pseudorandom-tools-fromPandas
[fromPandas]: #pseudorandom-tools-fromPandas

</span>

[pseudorandom.tools]: #pseudorandom-tools
[tools]: #pseudorandom-tools

</span>

[pseudorandom]: #pseudorandom


[Example]: #example
[Dependencies]: #dependencies
[License]: #license
[Overview]: #overview
[class __pseudorandom.DataFrame__]: #class-__pseudorandomdataframe__
[function __pseudorandom\.DataFrame\.\_\_getitem\_\___\(key\)]: #function-__pseudorandomdataframe__getitem____key
[function __pseudorandom\.DataFrame\.\_\_init\_\___\(cols, rows, default=u''\)]: #function-__pseudorandomdataframe__init____cols-rows-defaultu
[function __pseudorandom\.DataFrame\.\_\_len\_\___\(\)]: #function-__pseudorandomdataframe__len____
[function __pseudorandom\.DataFrame\.\_\_setitem\_\___\(key, val\)]: #function-__pseudorandomdataframe__setitem____key-val
[property __pseudorandom.DataFrame.cells__]: #property-__pseudorandomdataframecells__
[property __pseudorandom.DataFrame.cols__]: #property-__pseudorandomdataframecols__
[function __pseudorandom\.DataFrame\.copy__\(\)]: #function-__pseudorandomdataframecopy__
[property __pseudorandom.DataFrame.range__]: #property-__pseudorandomdataframerange__
[function __pseudorandom\.DataFrame\.reverse__\(cols=None\)]: #function-__pseudorandomdataframereverse__colsnone
[function __pseudorandom\.DataFrame\.shift__\(d=1, cols=None\)]: #function-__pseudorandomdataframeshift__d1-colsnone
[function __pseudorandom\.DataFrame\.shuffle__\(cols=None\)]: #function-__pseudorandomdataframeshuffle__colsnone
[function __pseudorandom\.DataFrame\.sort__\(cols=None, key=None\)]: #function-__pseudorandomdataframesort__colsnone-keynone
[class __pseudorandom.Enforce__]: #class-__pseudorandomenforce__
[function __pseudorandom\.Enforce\.\_\_init\_\___\(df\)]: #function-__pseudorandomenforce__init____df
[function __pseudorandom\.Enforce\.addConstraint__\(constraint, \*\*kwargs\)]: #function-__pseudorandomenforceaddconstraint__constraint-kwargs
[function __pseudorandom\.Enforce\.enforce__\(maxReshuffle=100, maxPass=100\)]: #function-__pseudorandomenforceenforce__maxreshuffle100-maxpass100
[class __pseudorandom.MaxRep__]: #class-__pseudorandommaxrep__
[class __pseudorandom.MinDist__]: #class-__pseudorandommindist__
[*module* pseudorandom.tools]: #module-pseudorandomtools
[function __pseudorandom\.tools\.fromPandas__\(pdf\)]: #function-__pseudorandomtoolsfrompandas__pdf