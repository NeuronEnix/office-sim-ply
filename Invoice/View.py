from pathlib import Path
from typing import List, Dict, Any
from pandas import DataFrame, ExcelWriter

from helper import to_cbm, to_sqmtr

class View:
    def __init__(self ) :
        self.table:Dict[ str, List] = {}
    
    def __setitem__(self, col_name:str, value:Any ):
        try: self.table[col_name].append( value )
        except:self.table[ col_name ] = [ value ]
    
    def __getitem__( self, col_name ):
        try: return self.table[col_name]
        except: return []
    
    def comp_bundle( self, pcs_col_name:str = "PCS" ):
        bundle_list:List[int] = []
        
        try:
            for pcs in self.table[ pcs_col_name ]: bundle_list.append( pcs // 50 )
            self.table["BUNDLE"] = bundle_list
            return self
            
        except: print( "Not found\nPieces Column:", pcs_col_name )
        
    def comp_sqmtr( self, size_col_name:str = "SIZE", pcs_col_name:str = "PCS" ):
        sqmtr_list:List[int] = []
        
        try:
            for size, pcs in zip( self.table[ size_col_name ], self.table[ pcs_col_name ]):
                sqmtr_list.append( to_sqmtr( size, pcs, 4 ) )
            self.table["SQMTR"] = sqmtr_list
            return self
            
        except: print( "One of the col is missing" )
        print( "Size Column:", size_col_name )
        print( "Pieces Column:", pcs_col_name )
        
    def comp_cbm( self, size_col_name:str = "SIZE", pcs_col_name:str = "PCS" ):
        cbm_list:List[int] = []
        
        try:
            for size, pcs in zip( self.table[ size_col_name ], self.table[ pcs_col_name ]):
                cbm_list.append( to_cbm( size, pcs, 4 ) )
            self.table["CBM"] = cbm_list
            return self
            
        except: print( "One of the col is missing" )
        print( "Size Column:", size_col_name )
        print( "Pieces Column:", pcs_col_name )
    
    def comp_all( self, size_col:str = "SIZE", pcs_col:str = "PCS" ) -> "View":
        self.comp_bundle( pcs_col ).comp_cbm(size_col, pcs_col).comp_sqmtr( size_col, pcs_col )
        return self
    
    def to_excel( self, path:str = "./", file_name:str = "file", sheet_name:str = "Sheet 1", writer:ExcelWriter = None  ):
        Path(path).mkdir(exist_ok=True,parents=True )
        
        for c in '\/:*?"<>|': file_name = file_name.replace( c, " " )
        for c in '\/:*?"<>|\'`': sheet_name = sheet_name.replace( c, " " )

        df = DataFrame( self.table )
        if writer: df.to_excel( writer, sheet_name=sheet_name, index=False )
        else: df.to_excel( path + file_name + ".xlsx", sheet_name=sheet_name, index = False )
            
