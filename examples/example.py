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
