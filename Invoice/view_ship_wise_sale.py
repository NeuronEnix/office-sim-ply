from typing import List, Dict, Any
from helper import to_cbm, to_sqmtr
from View import View
# from helper import to_cbm, to_sqmtr

class Ship_Wise:
    def __init__(self, pur_inv_list:List[ Dict[ str, Any] ], sale_inv_list:List[ Dict[ str, Any] ] ):
        self.pur_inv_list = pur_inv_list
        self.sale_inv_list = sale_inv_list
        
        # { "SHIP_ID": { "BILL NO": { fd1: "Data", fd2: "Data" } } }
        self.ship:Dict[ str, Dict[str, Dict[str,Any] ] ] = {}
        self.container_num: Dict[ str, str ] = {} 
        for each_invoice in self.pur_inv_list:
            self.ship[ each_invoice[ "SHIP_ID" ] ] = {}
            self.container_num[ each_invoice[ "SHIP_ID" ] ] = each_invoice[ "CNTNR NO" ]

    def pur_sale( self, _id:int, pur_id:int, sale_id:int, item_id:int, pcs:int ):
        cur_pur_inv  = self.pur_inv_list [ pur_id ]
        cur_sale_inv = self.sale_inv_list[ sale_id ]
        cur_item = cur_sale_inv[ "_item" ][ item_id ]

        ship_id = cur_pur_inv[ "SHIP_ID"]
        bill_num = cur_sale_inv["BILL NO"]
        pur_invoice_num = cur_pur_inv["INVOICE NO"]
        
        try:
            self.ship[ ship_id ][ bill_num ][ "PCS" ] += pcs
            self.ship[ ship_id ][ bill_num ][ "CBM" ] += to_cbm( cur_item["SIZE"], pcs )
            self.ship[ ship_id ][ bill_num ][ "SQMTR" ] += to_sqmtr( cur_item["SIZE"], pcs )
            self.ship[ ship_id ][ bill_num ][ "REFERENCE" ].add( pur_invoice_num )
        except:
            self.ship[ ship_id ][ bill_num ] = { 
                "BILL NO" : cur_sale_inv["BILL NO"],
                "BILL DATE": cur_sale_inv["BILL DATE"],
                "PARTY NAME": cur_sale_inv["PARTY NAME"],
                "PCS" : pcs,
                "CBM" : to_cbm( cur_item["SIZE"], pcs ),
                "SQMTR" : to_sqmtr( cur_item["SIZE"], pcs ),
                "REFERENCE": set( [pur_invoice_num] )

            }

    def to_excel(self) :
        for ship_key, each_ship in zip(self.ship.keys(), self.ship.values()):
            ship_view = View()
            
            for bill in each_ship.values():
                bill[ "CBM" ] = round( bill["CBM"], 4 )
                bill[ "SQMTR" ] = round( bill["SQMTR"], 2 )
                bill[ "REFERENCE" ] = ", ".join( sorted(bill["REFERENCE"]) )
                for col in bill.keys(): 
                    ship_view[ col ] = bill[ col ]

            container_num = self.container_num[ ship_key ]
            ship_view.to_excel( "./Update/Ship Wise/", ship_key + " - " + container_num, sheet_name=container_num )
            