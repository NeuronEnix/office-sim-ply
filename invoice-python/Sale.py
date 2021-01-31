from helper import load_excel

class Sale:
    def __init__( self, path ):
        self.df = load_excel( path )

        # Capitalize sizes i.e  "8x4" to "8X4"
        self.df[ "SIZE" ] = self.df[ "SIZE" ].str.upper()
    
    def add( self, ind:int, col:str, val:any ): self.df.at[ ind, col ] = val

    def sold( self, sale_ind:int, inv_list:list ): self.add( sale_ind, "INVOICE", ", ".join( inv_list ) )

    def size_at( self, ind:int ) -> str: return self.df.at[ ind, "SIZE"]
    def pcs_at( self, ind:int )  -> str: return self.df.at[ ind, "PIECES"]
    