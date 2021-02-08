from typing import List, Dict, Any

from helper import load_excel
"""
Structure of "self.data":
self.data = [
    {
        "_id":0,
        "_item": [
            { "_id":0, "SIZE": "6X3", "PCS": 500, "GRADE": "C2" },
            { "_id":1, "SIZE": "8X4", "PCS": 650, "GRADE": "C3" },
            .....................................................,
        ],
        "info-1": "something-1",
        "info-2": "something-2",
        .......................,
    }
]
"""

class Sale:
    def __init__( self, path ):
        df = load_excel( path )
        df[ "SIZE" ] = df[ "SIZE" ].str.upper() # Capitalize values of "SIZE" column: "8x4" to "8X4"
        df[ "GRADE" ] = df[ "GRADE" ].str.upper() # Capitalize values of "Grade" column: "c1" to "C1"
        df["PUR_INV_ID"] = df["PUR_INV_ID"].str.upper()
        
        self.inv = []
        
        for _id, bill_num in enumerate( sorted( set( df["BILL NO"] ) ) ):
            each_bill_df = df[ df[ "BILL NO" ] == bill_num ]
            each_data = { "_id": _id  }

            # Get data from all col of first index because they are the same throughout
            # except ( "SIZE", "PCS", "GRADE" ) -> they may change every row
            for col in each_bill_df.columns:
                if col not in ( "SIZE", "PCS", "GRADE" ):
                    each_data[ col ] = each_bill_df[col][ each_bill_df.index[0] ]
            
            # Adding items to data[ _item ]
            each_data[ "_item" ]:List[ Dict[ str, Any ] ] = []
            for ind in each_bill_df.index:
                try:
                    each_data[ "_item" ].append({
                        "_id": len( each_data["_item"] ),
                        "SIZE" : each_bill_df[ "SIZE"  ][ ind ],
                        "PCS"  : int(each_bill_df[ "PCS"   ][ ind ]),
                        "GRADE": each_bill_df[ "GRADE" ][ ind ],
                    })
                except:
                    print( "SIZE or PCS or GRADE Column is missing" )
                    print( "ADD above columns to: sales.xlsx" )
                    print( "Press ENTER Key to exit" )
                    exit()
        
            self.inv.append( each_data )
