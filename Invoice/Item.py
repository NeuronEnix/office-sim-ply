from typing import List, Dict
from helper import to_cbm, to_sqmtr

class Item:
    def __init__(self, size:str, pcs:int, grade:int = None ):

        # Initializing
        self.size, self.pcs, self.grade = size, pcs, grade
        self.re_calc_cbm().re_calc_sqmtr()
    
    def re_calc_sqmtr( self, round_up:int = None) -> "Item": 
        self.sqmtr = to_sqmtr( self.size, self.pcs, round_up )
        return self
    def re_calc_cbm( self, round_up:int = None ) -> "Item":
        self.cbm = to_cbm( self.size, self.pcs, round_up )
        return self

    def get_sqmtr( self ) -> float: return self._sqmtr
    def set_sqmtr( self, new_sqmtr ): self._sqmtr = new_sqmtr 
    sqmtr = property( get_sqmtr, set_sqmtr )

    def get_cbm( self ) -> float: return self._cbm
    def set_cbm( self, new_cbm ): self._cbm = new_cbm
    cbm = property( get_cbm, set_cbm )

    def __str__( self ) -> str: return "SIZE:{0}; PCS:{1}; GRADE:{2}; SQMTR:{3}; CBM:{4}".format( self.size, self.pcs, self.grade, self.sqmtr, self.cbm )
