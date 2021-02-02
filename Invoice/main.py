import pandas as pd
from json import dumps
from Purchase import Purchase
from Sale import Sale
from pathlib import Path

pur = Purchase( "./pur_inv.xlsx" )
sale = Sale( "./sale_inv.xlsx" )

for each_sale_inv in sale.inv:
    for item in each_sale_inv[ "_item" ]:
        pur.purchase( item["SIZE"], item["PCS"], each_sale_inv[ "_id"], item["_id"] )

from Report import Report
report = Report( pur.inv, sale.inv, pur.pur_sale )

# Writing to excel
writer = pd.ExcelWriter( "./Update.xlsx", engine="xlsxwriter" )
report.df.to_excel( writer, sheet_name="Report", index=False, merge_cells=True)
writer.save()

# To JSON
p = Path("./meta")
p.mkdir(exist_ok=True )

with open( "./meta/purchase.json", 'w') as f: f.write( str(pur.inv).replace("'",'"').replace('""', '"') )
with open( "./meta/sale.json", 'w') as f: f.write( str(sale.inv).replace("'",'"') )
with open( "./meta/pur_sale.json", 'w') as f: f.write( str(pur.pur_sale).replace("'",'"') )
