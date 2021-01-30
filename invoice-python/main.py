import pandas as pd
import numpy as np
import math
df = pd.read_excel( "./pur_inv.xlsx")
[df.drop( ind, inplace = True ) for ind in df.index if str(df["Invoice"][ind]).strip() == "" or str(df["Invoice"][ind]).strip() == "nan" ]
print( df )