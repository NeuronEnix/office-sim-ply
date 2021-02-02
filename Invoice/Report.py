from typing import List, Dict, Any
from pandas import DataFrame
from helper import to_cbm, to_sqmtr
import pandas as pd
class Report:
    def __init__(self, pur_inv:List[ Dict[ str, Any] ], sale_inv:List[ Dict[ str, Any] ], pur_sale:List[ Dict[ str, int] ] ):
        # Check if key in each pur and sale dict are unique 
        pur_inv_keys = set( pur_inv[0].keys() )
        sale_inv_keys = set( sale_inv[0].keys() )

        # Remove "_item" and "_id" they are common on both pur and sale
        for common_keys in [ "_id", "_item" ]:
            pur_inv_keys.remove( common_keys )
            sale_inv_keys.remove( common_keys )
        
        # If any common keys in found other than "_id" and "_item" which was removed in the above for loop
        if len( pur_inv_keys.intersection( sale_inv_keys ) ) != 0: 
            print( "Purchase Columns:", pur_inv_keys )
            print( "Sale Columns:", sale_inv_keys)
            print( "Common Columns:", pur_inv_keys.intersection( sale_inv_keys ))
            print( "Purchase Invoice File and Sale Invoice File may have same Column Name")
            print( "Please Make sure than Column Names in Purchase and Sale Invoice file are not Repeated in each other")
            print( "Press Enter to Continue"); input(); exit()
        
        # Falls through if all good

        table_cols = list( pur_inv_keys.union( sale_inv_keys ) )
        table_cols.extend( [ "GRADE", "SIZE", "PCS", "BUNDLE", "CBM", "SQMTR"] ) # Additional column
        table:Dict[ str, List] = { cols:[] for cols in table_cols }

        for cur_pur_sale in pur_sale:

            cur_pur_inv  = pur_inv [ cur_pur_sale[ "pur_id" ] ]
            cur_sale_inv = sale_inv[ cur_pur_sale[ "sale_id"] ]
            cur_item = cur_sale_inv[ "_item" ][ cur_pur_sale[ "item_id"] ]

            # Add Info of "pur_inv" to table
            [ table[key].append( cur_pur_inv[ key ] ) for key in pur_inv_keys ]

            # Add Info of "sale_inv" to table
            [ table[key].append( cur_sale_inv[ key ] )  for key in sale_inv_keys ]

            # Add These info to table : GRADE, SIZE, PCS, BUNDLE, CBM, SQMTR
            [ table[ key ].append( cur_item[ key ] ) for key in ("GRADE","SIZE","PCS") ]
            
            # Other Computed Columns
            table[ "BUNDLE" ].append( cur_item["PCS"] // 50 )
            table[ "SQMTR" ].append( to_sqmtr( cur_item["SIZE"], cur_item["PCS"], 2 ) )
            table[ "CBM" ].append( to_cbm( cur_item["SIZE"], cur_item["PCS"], 4 ) )

        self.df = DataFrame( table )
