from typing import List, Dict
from Item import Item

class Document:
    def __init__( self, item_list:List[ List ], other_info:Dict ):
        self.info:Dict = other_info
        self.item_list:List[Item] = [ Item( *each_item ) for each_item in item_list ]

    def __str__(self):
        return str( [ str(item) for item in self.item_list ] )