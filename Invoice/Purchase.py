from typing import List
from pandas import DataFrame

from helper import load_excel, is_size
from Document import Document
from Item import Item

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
        
    def purchase( self, pur_item:Item ) -> List:

        pur_item = pur_item.clone()
        deducted_list:List[str] = []

        for doc in self.doc_list:
            
            # doc.item_by_size[ item.size ] -> guaranteed to return one element always
            avail_item = doc.item_by_size[ pur_item.size ][0]

            if avail_item.pcs == 0: pass

            if avail_item.pcs >= pur_item.pcs: deduct_pcs = pur_item.pcs
            else: deduct_pcs = avail_item.pcs

            pur_item.pcs -= deduct_pcs
            avail_item.pcs -= deduct_pcs

            if deduct_pcs: deducted_list.append( doc.info["INVOICE"] + "(" + str(deduct_pcs) + ")")

            if pur_item.pcs == 0: return deducted_list

        else: # If Enough pcs not available
            print( "\n!!!!!!!!!!!!!!!!!!!\nStock not available for Size:", pur_item.size )
            print( "Pieces needed:", pur_item.pcs )
            print( "Available Stock: 0")
            input( "\nPlease update the stock to get the result\nPress Enter to close" )
            exit()

    
