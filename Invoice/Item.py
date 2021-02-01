import copy
from typing import List, Dict
from helper import to_cbm, to_sqmtr

class Item:
    def __init__(self, size:str, pcs:int, grade:int = None , round_up_sqmtr:int = None, round_up_cbm:int = None ):

        # Initializing
        self._size = size
        self._pcs = pcs
        self._grade = grade
        self._round_up_cbm = round_up_cbm
        self._round_up_sqmtr = round_up_sqmtr       
        
        self.re_calc_all()
    
    def re_calc_sqmtr( self, round_up:int = None) -> "Item": 
        if round_up: self._round_up_sqmtr = round_up
        self.sqmtr = to_sqmtr( self._size, self._pcs, self._round_up_sqmtr )
        return self
    def re_calc_cbm( self, round_up:int = None ) -> "Item":
        if round_up: self._round_up_cbm = round_up
        self.cbm = to_cbm( self._size, self._pcs, self._round_up_cbm )
        return self
    
    def re_calc_all( self ): self.re_calc_sqmtr().re_calc_cbm()
    
    def clone( self ) -> "Item": return copy.copy( self )


    # get, set -> _size
    def get_size( self ) -> str: return self._size
    def set_size( self, new_size ): self._size = new_size; self.re_calc_all()
    size = property( get_size, set_size )

    # get, set -> _pcs
    def get_pcs( self ) -> str: return self._pcs
    def set_pcs( self, new_pcs ): self._pcs = new_pcs; self.re_calc_all()
    pcs = property( get_pcs, set_pcs )

    # get, set -> _grade
    def get_grade( self ) -> str: return self._grade
    def set_grade( self, new_grade ): self._grade = new_grade; self.re_calc_all()
    grade = property( get_grade, set_grade )

    # get, set -> _sqmtr
    def get_sqmtr( self ) -> float: return self._sqmtr
    def set_sqmtr( self, new_sqmtr ): self._sqmtr = new_sqmtr 
    sqmtr = property( get_sqmtr, set_sqmtr )

    # get, set -> _cbm
    def get_cbm( self ) -> float: return self._cbm
    def set_cbm( self, new_cbm ): self._cbm = new_cbm
    cbm = property( get_cbm, set_cbm )

    def __str__( self ) -> str: return "SIZE:{0}; PCS:{1}; GRADE:{2}; SQMTR:{3}; CBM:{4}".format( self._size, self._pcs, self._grade, self.sqmtr, self.cbm )

