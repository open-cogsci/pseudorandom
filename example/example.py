from pseudorandom import Enforce, MaxRep, MinDist
from pseudorandom import tools
import pandas as pd

# Read a datafile with Pandas and convert it to a pseudorandom DataFrame.
pdf = pd.read_csv('example/data.csv')
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
