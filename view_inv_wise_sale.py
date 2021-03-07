from typing import List, Dict, Any
from helper import to_cbm, to_sqmtr
from View import View
# from helper import to_cbm, to_sqmtr

class Inv_Wise:

    # Pass each inv of pur_inv_list, it'll create the key with combination of below mentioned values
    @staticmethod
    def getKey( pur_inv ): return " - ".join( [ pur_inv[ "PUR_INV_ID" ], pur_inv["SHIP_ID"], pur_inv["INVOICE NO"] ] )

    def __init__(self, pur_inv_list:List[ Dict[ str, Any] ], sale_inv_list:List[ Dict[ str, Any] ] ):
        self.pur_inv_list = pur_inv_list
        self.sale_inv_list = sale_inv_list
        
        # key as: PUR_INC_ID + SHIP_ID + INVOICE NO
        # { key: View() }
        self.inv:Dict[ str, View ] = {}
        for each_invoice in self.pur_inv_list:
            self.inv[ self.getKey( each_invoice )  ] = View()
            
    def pur_sale( self, _id:int, pur_id:int, sale_id:int, item_id:int, pcs:int, opening_bal:int, closing_bal:int ):
        cur_pur_inv  = self.pur_inv_list [ pur_id ]
        cur_sale_inv = self.sale_inv_list[ sale_id ]
        cur_item = cur_sale_inv[ "_item" ][ item_id ]

        self.inv[ self.getKey( cur_pur_inv ) ][ "BILL DATE"  ] = cur_sale_inv[ "BILL DATE"  ]
        self.inv[ self.getKey( cur_pur_inv ) ][ "BILL NO"    ] = cur_sale_inv[ "BILL NO"    ]
        self.inv[ self.getKey( cur_pur_inv ) ][ "PARTY NAME" ] = cur_sale_inv[ "PARTY NAME" ]
        self.inv[ self.getKey( cur_pur_inv ) ][ "GRADE"      ] = cur_item[ "GRADE"      ]
        self.inv[ self.getKey( cur_pur_inv ) ][ "SIZE"       ] = cur_item[ "SIZE"       ]
        self.inv[ self.getKey( cur_pur_inv ) ][ "PCS"        ] = cur_item[ "PCS"        ]

    def to_excel(self) :
        for each_key in self.inv:
            # len() is used to see if view contains any value, if it does then only "to_excel()"
            if len( self.inv[ each_key]["PCS"] ) > 0:
                self.inv[ each_key ].comp_all().to_excel( "./Update/Invoice Wise/", each_key, each_key )
