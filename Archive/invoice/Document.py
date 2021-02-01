from typing import List, Dict
from Item import Item

class Document:
    def __init__( self, item_list:List[ List ], other_info:Dict ):
        self.info:Dict = other_info
        # self.item_list:List[Item] = [ Item( *each_item ) for each_item in item_list ]

        self.item_list:List[Item] = []
        self.item_by_size:Dict[std,List[Item]] = {}
        
        for i, each_item in enumerate( item_list ):
            item = Item( *each_item )
            self.item_list.append( item )

            # for fast access ( find item by size )
            try: self.item_by_size[ item.size ].append( item )
            except: self.item_by_size[ item.size ] = [ item ]        

    def __str__(self):
        return str( [ str(item) for item in self.item_list ] )