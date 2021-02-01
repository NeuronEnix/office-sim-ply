from helper import load_excel
from meta import build_sale_inv
class Sale:
    def __init__( self, path ):
        self.df = load_excel( path )

        # Capitalize sizes i.e  "8x4" to "8X4"
        self.df[ "SIZE" ] = self.df[ "SIZE" ].str.upper()
        self.df[ "GRADE" ] = self.df[ "GRADE" ].str.upper()

        # Converting PCS values from int64 to int32
        dtypes = {}
        dtypes.__setitem__( "PCS", "int") 
        self.df = self.df.astype( dtypes )

        build_sale_inv( self.df )
    
    def add( self, ind:int, col:str, val:any ): self.df.at[ ind, col ] = val

    def sold( self, sale_ind:int, inv_list:list ): self.add( sale_ind, "INVOICE", ", ".join( inv_list ) )

    def size_at( self, ind:int ) -> str: return self.df.at[ ind, "SIZE"]
    def pcs_at( self, ind:int )  -> str: return self.df.at[ ind, "PCS"]
    