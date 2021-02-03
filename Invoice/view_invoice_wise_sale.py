from typing import List, Dict, Any

from View import View
# from helper import to_cbm, to_sqmtr

class Invoice_Wise:
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
        self.view = View()

    def pur_sale( self, _id:int, pur_id:int, sale_id:int, item_id:int, pcs:int ):
        cur_pur_inv  = self.pur_inv_list [ pur_id ]
        cur_sale_inv = self.sale_inv_list[ sale_id ]
        cur_item = cur_sale_inv[ "_item" ][ item_id ]

        # Add Info of "pur_inv" to table
        for key in self.pur_inv_keys: self.view[key] = cur_pur_inv[ key ]

        # Add Info of "sale_inv" to table
        for key in self.sale_inv_keys: self.view[key] = cur_sale_inv[ key ] 

        # Add These info to table : GRADE, SIZE, PCS, BUNDLE, CBM, SQMTR
        for key in ("GRADE","SIZE"): self.view[ key ] = cur_item[ key ]

        self.view[ "PCS" ] = pcs

    def to_excel(self) :
        self.view.comp_bundle().comp_cbm().comp_sqmtr()
        self.view.to_excel("./Update", "Sales Report - Complete Details", "Report")
