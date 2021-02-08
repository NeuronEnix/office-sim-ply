from typing import List, Dict
from pandas import ExcelWriter
from View import View
from helper import load_excel, is_size

"""
Structure of "self.inv":
self.inv = [
    {
        "_id": 0,  #Auto indexing from -> 0,
        "_item": {  # _item is of the form { size : pcs } 
            "8X4":4, # Length=8, Breadth=4, Pieces=4
            "3X2":10 # Length=3, Breadth=2, Pieces=20
            .......,
        },
        
        # these fields are automatically made based on the columns present in the excel sheet
        "other_fld_1": "something-1",
        "other_fld_2": "something-2",
        "...........": "...........",
        "other_fld_n": "something-n",
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
        df["PUR_INV_ID"] = df["PUR_INV_ID"].str.upper()
        df["SHIP_ID"] = df["SHIP_ID"].str.upper()
        df["INVOICE NO"] = df["INVOICE NO"].str.upper()
        
        self.inv = []
        self.pur_sale:List[ Dict[str,int] ] = []

        for ind in df.index:
            each_invoice = { "_id":ind }
            each_invoice[ "_item" ]:Dict[ str, int ] = {}
            for col in df.columns:
                if is_size( col ): each_invoice["_item"][ col ] = int( df[col][ind] ) # _item:{ Size:pcs }
                else: each_invoice[ col ] = df[ col ][ ind ] # Other info
            self.inv.append( each_invoice )

    def purchase( self, size:str, pcs:int, sale_id:int, item_id:int, pur_inv_id:str = None ) -> None:
        tot_pcs = pcs
        if pur_inv_id:
            
            for each_pur_inv in self.inv:
                if each_pur_inv["PUR_INV_ID"] == pur_inv_id: 
                    inv_list = [ each_pur_inv ]; break
            else: 
                print( "Not Found -> PUR_INV_ID: ", pur_inv_id )
                print("Press Enter to Exit!"); input(); exit()

        else: inv_list = self.inv

        for each_inv in inv_list:
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
        print( "PCS needed:", tot_pcs )
        print( "Available PCS: ", tot_pcs-pcs)
        print( "Difference:",pcs)
        input( "\nPlease update the stock to get the result\nPress Enter to close" )
        exit()

    def to_excel( self ):
        view = View()
        item_size_list = list( self.inv[0]["_item"].keys() )
        other_col_list = list( self.inv[0].keys() )
        [ other_col_list.remove( col_to_be_removed ) for col_to_be_removed in ["_id","_item"] ]
        for each_inv in self.inv:
            comp_view = View()

            for other_col in other_col_list: view[other_col] = each_inv[other_col]
            for size in item_size_list:
                view[ size ] = each_inv["_item"][ size ]

                # Computation part of Total pcs, bundle, cbm, sqmtr
                comp_view[ "SIZE" ], comp_view[ "PCS" ]  = size, each_inv["_item"][ size ]
                comp_view.comp_bundle().comp_cbm().comp_sqmtr()

            for comp_col in ("PCS", "BUNDLE", "CBM", "SQMTR" ): 
                view[ comp_col ] = sum( comp_view[ comp_col ] )
        writer = ExcelWriter( "./Update/Stock Report.xlsx", engine='xlsxwriter' )

        # Invoice Wise Report
        view.to_excel( writer=writer, sheet_name="inv_wise")

        # Size Wise Report
        size_wise_rep = View()
        size_wise_rep.table["SIZE"] = item_size_list
        for each_size in size_wise_rep["SIZE"]:
            size_wise_rep["PCS"] = sum( view[ each_size ] )
        
        size_wise_rep.comp_all().to_excel( sheet_name="size_wise", writer=writer)
            
        writer.save()
