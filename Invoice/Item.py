from typing import List, Dict
from helper import to_cbm, to_sqmtr

class Item:
    def __init__(self, size:str, pcs:int, grade:int = None , round_up_sqmtr:int = None, round_up_cbm:int = None ):

        # Initializing
        self.size = size
        self.pcs = pcs
        self.grade = grade
        self.round_up_cbm = round_up_cbm
        self.round_up_sqmtr = round_up_sqmtr       
        
        self.re_calc_sqmtr().re_calc_cbm()
    
    def re_calc_sqmtr( self, round_up:int = None) -> "Item": 
        if round_up: self.round_up_sqmtr = round_up
        self.sqmtr = to_sqmtr( self.size, self.pcs, self.round_up_sqmtr )
        return self
    def re_calc_cbm( self, round_up:int = None ) -> "Item":
        if round_up: self.round_up_cbm = round_up
        self.cbm = to_cbm( self.size, self.pcs, self.round_up_cbm )
        return self

    def get_sqmtr( self ) -> float: return self._sqmtr
    def set_sqmtr( self, new_sqmtr ): self._sqmtr = new_sqmtr 
    sqmtr = property( get_sqmtr, set_sqmtr )

    def get_cbm( self ) -> float: return self._cbm
    def set_cbm( self, new_cbm ): self._cbm = new_cbm
    cbm = property( get_cbm, set_cbm )

    def __str__( self ) -> str: return "SIZE:{0}; PCS:{1}; GRADE:{2}; SQMTR:{3}; CBM:{4}".format( self.size, self.pcs, self.grade, self.sqmtr, self.cbm )
