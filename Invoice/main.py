import pandas as pd
from json import dumps
from Purchase import Purchase
from Sale import Sale
from pathlib import Path



pur = Purchase( "./pur_inv.xlsx" )
sale = Sale( "./sale_inv.xlsx" )

# Populating pur_sale table by going through each sale against purchase
for each_sale_inv in sale.inv:

    # if PUR_INV_ID was specified explicitly on sale_inv_xlsx
    pur_inv_id = str(each_sale_inv["PUR_INV_ID"]).strip()
    if pur_inv_id == "nan" or pur_inv_id == "" : pur_inv_id = None

    for item in each_sale_inv[ "_item" ]:
        pur.purchase( item["SIZE"], item["PCS"], each_sale_inv[ "_id"], item["_id"], pur_inv_id=pur_inv_id )

from Report import Report
from view_ship_wise_sale import Ship_Wise

view_list = [
    Report( pur.inv, sale.inv ),
    Ship_Wise( pur.inv, sale.inv )
]

for view in view_list:
    for each_pur_sale in pur.pur_sale:

        # Common function for every view in view_list to handle each sale transaction
        view.pur_sale( 
            each_pur_sale["_id"],
            each_pur_sale["pur_id"],
            each_pur_sale["sale_id"],
            each_pur_sale["item_id"],
            each_pur_sale["pcs"],
        )

# After making all the views, write them to excel using to_excel ( all view must implement it )
[ view.to_excel() for view in view_list ]

# To JSON
p = Path("./meta")
p.mkdir(exist_ok=True )

with open( "./meta/purchase.json", 'w') as f: f.write( str(pur.inv).replace("'",'"').replace('""', '"') )
with open( "./meta/sale.json", 'w') as f: f.write( str(sale.inv).replace("'",'"') )
with open( "./meta/pur_sale.json", 'w') as f: f.write( str(pur.pur_sale).replace("'",'"') )

pur.to_excel()