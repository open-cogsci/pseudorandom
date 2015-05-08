<span class="ModuleDoc YAMLDoc" id="dataframe" markdown="1">

# *module* dataframe

Copyright 2015 Sebastiaan Mathôt

v0.1.0


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

~~~

## Example 2: Pseudorandomization

~~~ .python
from dataframe import Enforce, MaxRep, MinDist
from dataframe import tools
import pandas as pd

# Read a datafile with Pandas and convert it to a pseudorandom DataFrame.
pdf = pd.read_csv('examples/data.csv')
df = tools.fromPandas(pdf)
print(df)
# Create an Enforce object, and add two constraints
ef = Enforce(df)
ef.addConstraint(MaxRep, cols='category', maxRep=1)
ef.addConstraint(MinDist, cols='word', minDist=4)
# Enforce the constraints
df = ef.enforce()
# See the resulting DataFrame and a report of how long the enforcement took.
print(df)
print(ef.report)

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


- [Example 1: Creating and viewing a DataFrame](#example-1-creating-and-viewing-a-dataframe)
- [Example 2: Pseudorandomization](#example-2-pseudorandomization)
- [Dependencies](#dependencies)
- [License](#license)
- [Overview](#overview)
- [class __dataframe.DataFrame__](#class-__dataframedataframe__)
	- [function __dataframe\.DataFrame\.\_\_getitem\_\___\(key\)](#function-__dataframedataframe__getitem____key)
	- [function __dataframe\.DataFrame\.\_\_init\_\___\(cols, rows, default=u'', cellValidator=None, colValidator=None\)](#function-__dataframedataframe__init____cols-rows-defaultu-cellvalidatornone-colvalidatornone)
	- [function __dataframe\.DataFrame\.\_\_len\_\___\(\)](#function-__dataframedataframe__len____)
	- [function __dataframe\.DataFrame\.\_\_setitem\_\___\(key, val\)](#function-__dataframedataframe__setitem____key-val)
	- [property __dataframe.DataFrame.cells__](#property-__dataframedataframecells__)
	- [property __dataframe.DataFrame.cols__](#property-__dataframedataframecols__)
	- [function __dataframe\.DataFrame\.copy__\(\)](#function-__dataframedataframecopy__)
	- [property __dataframe.DataFrame.range__](#property-__dataframedataframerange__)
	- [function __dataframe\.DataFrame\.reverse__\(cols=None\)](#function-__dataframedataframereverse__colsnone)
	- [function __dataframe\.DataFrame\.shift__\(d=1, cols=None\)](#function-__dataframedataframeshift__d1-colsnone)
	- [function __dataframe\.DataFrame\.shuffle__\(cols=None\)](#function-__dataframedataframeshuffle__colsnone)
	- [function __dataframe\.DataFrame\.sort__\(cols=None, key=None\)](#function-__dataframedataframesort__colsnone-keynone)
- [class __dataframe.Enforce__](#class-__dataframeenforce__)
	- [function __dataframe\.Enforce\.\_\_init\_\___\(df\)](#function-__dataframeenforce__init____df)
	- [function __dataframe\.Enforce\.addConstraint__\(constraint, \*\*kwargs\)](#function-__dataframeenforceaddconstraint__constraint-kwargs)
	- [function __dataframe\.Enforce\.enforce__\(maxReshuffle=100, maxPass=100\)](#function-__dataframeenforceenforce__maxreshuffle100-maxpass100)
- [class __dataframe.MaxRep__](#class-__dataframemaxrep__)
- [class __dataframe.MinDist__](#class-__dataframemindist__)
- [*module* dataframe.tools](#module-dataframetools)
	- [function __dataframe\.tools\.fromPandas__\(pdf\)](#function-__dataframetoolsfrompandas__pdf)



<span class="ClassDoc YAMLDoc" id="dataframe-DataFrame" markdown="1">

## class __dataframe.DataFrame__

A lightweight object for storing data. `pseudorandom.DataFrame` is similar to the `Pandas.DataFrame` class, but does not require any additional libraries, which makes it suitable for environments in which only the Python core libraries are available.

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-__getitem__" markdown="1">

### function __dataframe\.DataFrame\.\_\_getitem\_\___\(key\)

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

[dataframe.DataFrame.__getitem__]: #dataframe-DataFrame-__getitem__
[DataFrame.__getitem__]: #dataframe-DataFrame-__getitem__
[__getitem__]: #dataframe-DataFrame-__getitem__

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-__init__" markdown="1">

### function __dataframe\.DataFrame\.\_\_init\_\___\(cols, rows, default=u'', cellValidator=None, colValidator=None\)

Constructor. This creates a `DataFrame` with known columns and rows, but without any content.

__Arguments:__

- `cols` -- A list of column names.
	- Type: list
- `rows` -- The numer of rows.
	- Type: int

__Keywords:__

- `default` -- The default value for the cells.
	- Default: u''
- `cellValidator` -- No description
	- Default: None
- `colValidator` -- No description
	- Default: None

</span>

[dataframe.DataFrame.__init__]: #dataframe-DataFrame-__init__
[DataFrame.__init__]: #dataframe-DataFrame-__init__
[__init__]: #dataframe-DataFrame-__init__

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-__len__" markdown="1">

### function __dataframe\.DataFrame\.\_\_len\_\___\(\)

Implements the `len()` function.

__Example:__

~~~ .python
print('df has %d rows' % len(df))
~~~

__Returns:__

The number of rows.

- Type: int

</span>

[dataframe.DataFrame.__len__]: #dataframe-DataFrame-__len__
[DataFrame.__len__]: #dataframe-DataFrame-__len__
[__len__]: #dataframe-DataFrame-__len__

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-__setitem__" markdown="1">

### function __dataframe\.DataFrame\.\_\_setitem\_\___\(key, val\)

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

[dataframe.DataFrame.__setitem__]: #dataframe-DataFrame-__setitem__
[DataFrame.__setitem__]: #dataframe-DataFrame-__setitem__
[__setitem__]: #dataframe-DataFrame-__setitem__

<span class="PropertyDoc YAMLDoc" id="dataframe-DataFrame-cells" markdown="1">

### property __dataframe.DataFrame.cells__

No description specified.

</span>

[dataframe.DataFrame.cells]: #dataframe-DataFrame-cells
[DataFrame.cells]: #dataframe-DataFrame-cells
[cells]: #dataframe-DataFrame-cells

<span class="PropertyDoc YAMLDoc" id="dataframe-DataFrame-cols" markdown="1">

### property __dataframe.DataFrame.cols__

No description specified.

</span>

[dataframe.DataFrame.cols]: #dataframe-DataFrame-cols
[DataFrame.cols]: #dataframe-DataFrame-cols
[cols]: #dataframe-DataFrame-cols

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-copy" markdown="1">

### function __dataframe\.DataFrame\.copy__\(\)

No description specified.

__Returns:__

A deep copy of the current `DataFrame`.

- Type: DataFrame

</span>

[dataframe.DataFrame.copy]: #dataframe-DataFrame-copy
[DataFrame.copy]: #dataframe-DataFrame-copy
[copy]: #dataframe-DataFrame-copy

<span class="PropertyDoc YAMLDoc" id="dataframe-DataFrame-range" markdown="1">

### property __dataframe.DataFrame.range__

No description specified.

</span>

[dataframe.DataFrame.range]: #dataframe-DataFrame-range
[DataFrame.range]: #dataframe-DataFrame-range
[range]: #dataframe-DataFrame-range

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-reverse" markdown="1">

### function __dataframe\.DataFrame\.reverse__\(cols=None\)

Reverses the current `DataFrame` in place.

__Keywords:__

- `cols` -- The columns to reverse or `None` to reverse all columns.
	- Type: list, NoneType
	- Default: None

__Returns:__

The current `DataFrame`.

- Type: DataFrame

</span>

[dataframe.DataFrame.reverse]: #dataframe-DataFrame-reverse
[DataFrame.reverse]: #dataframe-DataFrame-reverse
[reverse]: #dataframe-DataFrame-reverse

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-shift" markdown="1">

### function __dataframe\.DataFrame\.shift__\(d=1, cols=None\)

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

[dataframe.DataFrame.shift]: #dataframe-DataFrame-shift
[DataFrame.shift]: #dataframe-DataFrame-shift
[shift]: #dataframe-DataFrame-shift

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-shuffle" markdown="1">

### function __dataframe\.DataFrame\.shuffle__\(cols=None\)

Shuffles the current `DataFrame` in place.

__Keywords:__

- `cols` -- The columns to shuffle or `None` to shuffle all columns. Columns are shuffled together, i.e. rows are preserved.
	- Type: list, NoneType
	- Default: None

__Returns:__

The current `DataFrame`.

- Type: DataFrame

</span>

[dataframe.DataFrame.shuffle]: #dataframe-DataFrame-shuffle
[DataFrame.shuffle]: #dataframe-DataFrame-shuffle
[shuffle]: #dataframe-DataFrame-shuffle

<span class="FunctionDoc YAMLDoc" id="dataframe-DataFrame-sort" markdown="1">

### function __dataframe\.DataFrame\.sort__\(cols=None, key=None\)

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

[dataframe.DataFrame.sort]: #dataframe-DataFrame-sort
[DataFrame.sort]: #dataframe-DataFrame-sort
[sort]: #dataframe-DataFrame-sort

</span>

[dataframe.DataFrame]: #dataframe-DataFrame
[DataFrame]: #dataframe-DataFrame

<span class="ClassDoc YAMLDoc" id="dataframe-Enforce" markdown="1">

## class __dataframe.Enforce__

A class that enforces a set of constraints by modifying (if necessary) the `DataFrame`.

<span class="FunctionDoc YAMLDoc" id="dataframe-Enforce-__init__" markdown="1">

### function __dataframe\.Enforce\.\_\_init\_\___\(df\)

Constructor.

__Arguments:__

- `df` -- The data.
	- Type: DataFrame

</span>

[dataframe.Enforce.__init__]: #dataframe-Enforce-__init__
[Enforce.__init__]: #dataframe-Enforce-__init__
[__init__]: #dataframe-Enforce-__init__

<span class="FunctionDoc YAMLDoc" id="dataframe-Enforce-addConstraint" markdown="1">

### function __dataframe\.Enforce\.addConstraint__\(constraint, \*\*kwargs\)

Adds a constraint to enforce.

__Arguments:__

- `constraint` -- A constraint class. Note, the class itself should be passed, not an instance of the class.
	- Type: type

__Keyword dict:__

- `**kwargs`: The keyword arguments that are passed to the constraint constructor.

</span>

[dataframe.Enforce.addConstraint]: #dataframe-Enforce-addConstraint
[Enforce.addConstraint]: #dataframe-Enforce-addConstraint
[addConstraint]: #dataframe-Enforce-addConstraint

<span class="FunctionDoc YAMLDoc" id="dataframe-Enforce-enforce" markdown="1">

### function __dataframe\.Enforce\.enforce__\(maxReshuffle=100, maxPass=100\)

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

[dataframe.Enforce.enforce]: #dataframe-Enforce-enforce
[Enforce.enforce]: #dataframe-Enforce-enforce
[enforce]: #dataframe-Enforce-enforce

</span>

[dataframe.Enforce]: #dataframe-Enforce
[Enforce]: #dataframe-Enforce

<span class="ClassDoc YAMLDoc" id="dataframe-MaxRep" markdown="1">

## class __dataframe.MaxRep__

Limits the number of times that a value can occur in direct succession. A maxRep of 1 means that values cannot be repeated.

__Example:__

~~~ .python
ef = Enforce(df)
ef.addConstraint(MaxRep, cols=['word'], maxRep=2)
~~~

</span>

[dataframe.MaxRep]: #dataframe-MaxRep
[MaxRep]: #dataframe-MaxRep

<span class="ClassDoc YAMLDoc" id="dataframe-MinDist" markdown="1">

## class __dataframe.MinDist__

Sets a minimum distance between value repetitions. A minimum distance of 2 avoids direct repetitions.

__Example:__

~~~ .python
ef = Enforce(df)
ef.addConstraint(MinDist, cols=['word'], minDist=2)
~~~

</span>

[dataframe.MinDist]: #dataframe-MinDist
[MinDist]: #dataframe-MinDist

<span class="ModuleDoc YAMLDoc" id="dataframe-tools" markdown="1">

## *module* dataframe.tools

A module with various helper functions.

<span class="FunctionDoc YAMLDoc" id="dataframe-tools-fromPandas" markdown="1">

### function __dataframe\.tools\.fromPandas__\(pdf\)

Converts a Pandas DataFrame to a pseudorandom DataFrame.

__Arguments:__

- `pdf` -- A Pandas DataFrame.
	- Type: DataFrame

__Returns:__

A pseudorandom DataFrame.

- Type: DataFrame

</span>

[dataframe.tools.fromPandas]: #dataframe-tools-fromPandas
[tools.fromPandas]: #dataframe-tools-fromPandas
[fromPandas]: #dataframe-tools-fromPandas

</span>

[dataframe.tools]: #dataframe-tools
[tools]: #dataframe-tools

</span>

[dataframe]: #dataframe


[Example 1: Creating and viewing a DataFrame]: #example-1-creating-and-viewing-a-dataframe
[Example 2: Pseudorandomization]: #example-2-pseudorandomization
[Dependencies]: #dependencies
[License]: #license
[Overview]: #overview
[class __dataframe.DataFrame__]: #class-__dataframedataframe__
[function __dataframe\.DataFrame\.\_\_getitem\_\___\(key\)]: #function-__dataframedataframe__getitem____key
[function __dataframe\.DataFrame\.\_\_init\_\___\(cols, rows, default=u'', cellValidator=None, colValidator=None\)]: #function-__dataframedataframe__init____cols-rows-defaultu-cellvalidatornone-colvalidatornone
[function __dataframe\.DataFrame\.\_\_len\_\___\(\)]: #function-__dataframedataframe__len____
[function __dataframe\.DataFrame\.\_\_setitem\_\___\(key, val\)]: #function-__dataframedataframe__setitem____key-val
[property __dataframe.DataFrame.cells__]: #property-__dataframedataframecells__
[property __dataframe.DataFrame.cols__]: #property-__dataframedataframecols__
[function __dataframe\.DataFrame\.copy__\(\)]: #function-__dataframedataframecopy__
[property __dataframe.DataFrame.range__]: #property-__dataframedataframerange__
[function __dataframe\.DataFrame\.reverse__\(cols=None\)]: #function-__dataframedataframereverse__colsnone
[function __dataframe\.DataFrame\.shift__\(d=1, cols=None\)]: #function-__dataframedataframeshift__d1-colsnone
[function __dataframe\.DataFrame\.shuffle__\(cols=None\)]: #function-__dataframedataframeshuffle__colsnone
[function __dataframe\.DataFrame\.sort__\(cols=None, key=None\)]: #function-__dataframedataframesort__colsnone-keynone
[class __dataframe.Enforce__]: #class-__dataframeenforce__
[function __dataframe\.Enforce\.\_\_init\_\___\(df\)]: #function-__dataframeenforce__init____df
[function __dataframe\.Enforce\.addConstraint__\(constraint, \*\*kwargs\)]: #function-__dataframeenforceaddconstraint__constraint-kwargs
[function __dataframe\.Enforce\.enforce__\(maxReshuffle=100, maxPass=100\)]: #function-__dataframeenforceenforce__maxreshuffle100-maxpass100
[class __dataframe.MaxRep__]: #class-__dataframemaxrep__
[class __dataframe.MinDist__]: #class-__dataframemindist__
[*module* dataframe.tools]: #module-dataframetools
[function __dataframe\.tools\.fromPandas__\(pdf\)]: #function-__dataframetoolsfrompandas__pdf