import pandas as pd
from Purchase import Purchase
from Sale import Sale

pur = Purchase( "./pur_inv.xlsx" )
sale = Sale( "./sale_inv.xlsx" )

for ind in sale.df.index:
    inv_list = pur.purchase( sale.size_at( ind ), sale.pcs_at( ind ) )
    sale.sold( ind, inv_list )

pur.comp()
print( pur.df )
print( sale.df )

# Writing to excel
writer = pd.ExcelWriter( "./Update.xlsx", engine="xlsxwriter" )
pur.df.to_excel( writer, sheet_name="pur_upd" )
sale.df.to_excel( writer, sheet_name="sale_upd")
writer.save()
