from pathlib import Path
from typing import List, Dict, Any
from pandas import DataFrame, ExcelWriter

from helper import to_cbm, to_sqmtr

class Report:
    def __init__(self, pur_inv_list:List[ Dict[ str, Any] ], sale_inv_list:List[ Dict[ str, Any] ] ):
        # Check if key in each pur and sale dict are unique 
        self.pur_inv_keys = set( pur_inv_list[0].keys() )
        self.sale_inv_keys = set( sale_inv_list[0].keys() )

        # Remove "_item" and "_id" they are common on both pur and sale
        for common_keys in [ "_id", "_item" ]:
            self.pur_inv_keys.remove( common_keys )
            self.sale_inv_keys.remove( common_keys )
        
        # If any common keys in found other than "_id" and "_item" which was removed in the above for loop
        if len( self.pur_inv_keys.intersection( self.sale_inv_keys ) ) != 0: 
            print( "Purchase Columns:", self.pur_inv_keys )
            print( "Sale Columns:", self.sale_inv_keys)
            print( "Common Columns:", self.pur_inv_keys.intersection( self.sale_inv_keys ))
            print( "Purchase Invoice File and Sale Invoice File may have same Column Name")
            print( "Please Make sure than Column Names in Purchase and Sale Invoice file are not Repeated in each other")
            print( "Press Enter to Continue"); input(); exit()
        
        # Continue if all good

        self.pur_inv_list = pur_inv_list
        self.sale_inv_list = sale_inv_list
        
        # Table design
        table_cols = list( self.pur_inv_keys.union( self.sale_inv_keys ) )
        table_cols.extend( [ "GRADE", "SIZE", "PCS", "BUNDLE", "CBM", "SQMTR"] ) # Additional column
        self.table:Dict[ str, List] = { cols:[] for cols in table_cols }
        

    def pur_sale( self, _id:int, pur_id:int, sale_id:int, item_id:int, pcs:int ):
        cur_pur_inv  = self.pur_inv_list [ pur_id ]
        cur_sale_inv = self.sale_inv_list[ sale_id ]
        cur_item = cur_sale_inv[ "_item" ][ item_id ]

        # Add Info of "pur_inv" to table
        [ self.table[key].append( cur_pur_inv[ key ] ) for key in self.pur_inv_keys ]

        # Add Info of "sale_inv" to table
        [ self.table[key].append( cur_sale_inv[ key ] ) for key in self.sale_inv_keys ]

        # Add These info to table : GRADE, SIZE, PCS, BUNDLE, CBM, SQMTR
        [ self.table[ key ].append( cur_item[ key ] ) for key in ("GRADE","SIZE") ]

        self.table[ "PCS" ].append( pcs )
        
        # Other Computed Columns
        self.table[ "BUNDLE" ].append( pcs // 50 )
        self.table[ "SQMTR" ].append( to_sqmtr( cur_item["SIZE"], pcs, 2 ) )
        self.table[ "CBM" ].append( to_cbm( cur_item["SIZE"], pcs, 4 ) )

    def to_excel(self) :
        p = Path("./Update")
        p.mkdir(exist_ok=True )
        DataFrame( self.table ).to_excel("./Update/Report.xlsx", index=False, sheet_name="Report" )
