from typing import List, Dict

from helper import load_excel, is_size

"""
Structure of "self.inv":
self.inv = [
    {
        "_id": 0,
        "_item": {
            "8X4":4,
            .......,
            "3X2":10
        },
        "info-1": "something-1",
        "info-2": "something-2",
    }
]
"""

"""
Structure of "self.pur_sale":

self.pur_sale = [
    { pur_ind:1, sale_ind:1, item_ind:1 },
    { pur_ind:1, sale_ind:1, item_ind:2 },
    { pur_ind:1, sale_ind:2, item_ind:1 },
    .........................,
]
"""
class Purchase:
    def __init__(self, path:str ):
        df = load_excel( path )
        self.inv = []
        self.pur_sale:List[ Dict[str,int] ] = []

        for ind in df.index:
            each_invoice = { "_id":ind }
            each_invoice[ "_item" ]:Dict[ str, int ] = {}
            for col in df.columns:
                if is_size( col ): each_invoice["_item"][ col ] = int( df[col][ind] ) # _item:{ Size:pcs }
                else: each_invoice[ col ] = df[ col ][ ind ] # Other info
            self.inv.append( each_invoice )

    def purchase( self, size:str, pcs:int, sale_id:int, item_id:int ) -> None:
        for each_inv in self.inv:
            each_inv_item = each_inv["_item"]
            
            # if 0 pcs available in cur invoice then pass
            if each_inv_item[ size ] == 0: pass

            # compute pcs to be deducted based on availability
            if each_inv_item[ size ] >= pcs: deduct_pcs = pcs
            else: deduct_pcs = each_inv_item[ size ]

            # deduct stuffs on invoice
            pcs -= deduct_pcs
            each_inv_item[ size ] -= deduct_pcs

            if deduct_pcs: self.pur_sale.append({
                "_id":len( self.pur_sale ),
                "pur_id" : each_inv[ "_id" ],
                "sale_id": sale_id,
                "item_id": item_id,
                "pcs": deduct_pcs
            })

            if pcs == 0: return
        
        # After going through all invoices
        # if pcs are still left to be deducted then
        print( "\n!!!!!!!!!!!!!!!!!!!\nStock not available for Size:", size )
        print( "PCS needed:", pcs )
        print( "Available Stock: 0")
        input( "\nPlease update the stock to get the result\nPress Enter to close" )
        exit()
