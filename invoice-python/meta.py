from pandas import DataFrame
from helper import is_size
from typing import Dict, List, Any
from json import dumps


# Meta Data Holders

pur_inv:Dict[ int, Dict[ str, Any] ] = {}
"""
index:int
pur_inv[ index ] = {
    "info-1": "something-1",
    "info-2": "something-2",
    .......................,
    "info-n": "something-n",
    "_item": {
        "8X4":4,
        .......,
        "3X2":10
    }
}
"""

sale_inv = {}
"""
index:int
sale_inv[ index ] = {
    "info-1": "something-1",
    "info-2": "something-2",
    .......................,
    "info-n": "something-n",
    "_item": [
        { "SIZE": "6X3", "PCS": 500, "GRADE": "C2" },
        { "SIZE": "8X4", "PCS": 650, "GRADE": "C3" },
        { "SIZE": "...", "PCS": ..., "GRADE": ".." },
        ............................................
    ]
}
"""

pur_sale: List[ Dict[ str, int ] ]
"""
pur_sale = [
    { pur_ind:1, sale_ind:1, item_ind:1 },
    { pur_ind:1, sale_ind:1, item_ind:2 },
    { pur_ind:1, sale_ind:2, item_ind:1 },
    .........................,
]
"""


def build_pur_inv( df:DataFrame ) -> "pur_inv":
    global pur_inv
    df = df.reset_index(drop=True)
    for ind in df.index:
        pur_inv[ ind ] = {}
        pur_inv[ ind ][ "_item" ]:Dict[ str, int ] = {}
        for col in df.columns:
            if is_size( col ): pur_inv[ ind ]["_item"][ col ] = int( df[col][ind] )
            else: pur_inv[ ind ][ col ] = df[ col ][ ind ] # Other info
    return pur_inv

def sale_inv_data_appender( item_list, other_info ):
    global sale_inv
    ind = len( sale_inv )
    sale_inv[ ind ] = other_info
    
    sale_inv[ ind ][ "_item" ]:List[ Dict[str,Any]] = []
    for item in item_list:
        sale_inv[ ind ][ "_item" ].append( {
            "SIZE": item[0],
            "PCS" : int(item[1]),
            "GRADE" : item[2]
        })

def build_sale_inv( df:DataFrame ) -> "sale_inv":
    df = df.reset_index(drop=True)
    prev_bill_num = cur_bill_num = None

    doc_list:List[Document] = []
    item_list = []
    other_info = {}

    # Data Builder
    # Go through each row 
    for ind in df.index:
        cur_bill_num = df[ "BILL" ][ind]

        if cur_bill_num != prev_bill_num:
            if prev_bill_num: #initially prev_bill_num will be "None" so append data at first iteration
                # append previously collected data ( which is done below this condition block )
                sale_inv_data_appender( item_list, other_info )
            # clear them after creating the data 
            item_list = []
            other_info = {}

            # so that at the following line can build data of current index
            prev_bill_num = cur_bill_num

            # first grab all the data from  the columns which will be same 
            # until new bill num is encountered except for SIZE, PCS, GRADE
            for col in df.columns:
                if col not in ("SIZE","GRADE","PCS"): other_info[ col ] = df[col][ ind ]

        if cur_bill_num == prev_bill_num:
            # item_list.append( [ size, pcs, grade, round_up_sqmtr, round_up_cbm ] )
            # try: grade = df["GRADE"][ind]
            # except grade = None
            item_list.append( [ df["SIZE"][ind], df["PCS"][ind], df["GRADE"][ind] if "GRADE" in df else None, 2, 3 ] )

    else: #if there is any remaining data to be appended 
        if prev_bill_num: #initially prev_bill_num will be "None" so append data at first iteration
            # append previously collected data ( which is done below this condition block )
            sale_inv_data_appender( item_list, other_info )
    # print( dumps( sale_inv, indent=2))
    return sale_inv


def add_to_pur_sale( pur_ind:int, sale_ind:int, item_ind:int ) -> 'pur_sale':
    global pur_sale
    
    return pur_sale