from typing import List
from pandas import DataFrame

from helper import load_excel, is_size
from Document import Document
from Item import Item

class Sale:
    def __init__( self, df:DataFrame ):
        
        self.doc_list:List[Document] = build_data( df )
        
    # Unfinished
    def sold( self, doc_ind:int, inv_list:List ) -> List:

        self.doc_list[ doc_ind ].info[ "INVOICE" ] = inv_list
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

    
def build_data( df ):
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
                doc_list.append( Document( item_list, other_info ) )

            

            # clear them after creating the data 
            item_list = []
            other_info = {}

            prev_bill_num = cur_bill_num

            # first grab all the data from  the columns which will be same 
            # until new bill num is encountered except for SIZE and PCS 

            for col in df.columns:
                if col not in ("SIZE","GRADE","PCS"): other_info[ col ] = df[col][ ind ]

        if cur_bill_num == prev_bill_num:
            # item_list.append( [ size, pcs, grade, round_up_sqmtr, round_up_cbm ] )
            item_list.append( [ df["SIZE"][ind], df["PCS"][ind], df["GRADE"][ind], 2, 3 ] )

    else: #if there is any remaining data to be appended 
        if prev_bill_num: #initially prev_bill_num will be "None" so append data at first iteration
            # append previously collected data ( which is done below this condition block )
            doc_list.append( Document( item_list, other_info ) )
    return doc_list