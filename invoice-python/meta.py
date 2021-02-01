from pandas import DataFrame
from helper import is_size
from typing import Dict, List, Any
from json import dumps


# Meta Data Holders
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
pur_inv:Dict[ int, Dict[ str, Any] ] = {}


sale_inv = {}


pur_sale: List[ Dict[ str, Any ] ]

def build_pur_inv( df:DataFrame ):
    df = df.reset_index(drop=True)
    for ind in df.index:
        pur_inv[ ind ] = {}
        pur_inv[ ind ][ "_item" ]:Dict[ str, int ] = {}
        for col in df.columns:
            if is_size( col ): pur_inv[ ind ]["_item"][ col ] = int( df[col][ind] )
            else: pur_inv[ ind ][ col ] = df[ col ][ ind ]
    return pur_inv