from typing import List
from pandas import DataFrame

from helper import load_excel, is_size
from Document import Document

class Purchase:
    def __init__( self, df:DataFrame ):
        
        self.doc_list:List[Document] = []

        # Go through each row 
        for ind in df.index:
            item_list = []
            other_info = {}

            #from each cell extract the col header, if it is size then add to item_list( [SIZE, PCS] ) else add to other_info
            for col in df.columns:
                # item_list.append( [ size, pcs, grade, round_up_sqmtr, round_up_cbm ] )
                if is_size( col ):
                    item_list.append( [ col, df[col][ind], None, 2, 3 ] )
                else: other_info[ col ] = df[col][ind]

            self.doc_list.append( Document( item_list, other_info ) )

    
