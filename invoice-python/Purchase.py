from helper import load_excel, is_size, to_cbm, to_sqmtr
from meta import build_pur_inv
class Purchase:
    def __init__(self, path:str ):
        self.df = load_excel( path, "Invoice" )
        
        # Converting size values to integer
        dtypes = {}
        [ dtypes.__setitem__( col, "int32") for col in self.df.columns if is_size( col ) ]
        self.df = self.df.astype( dtypes )
        
        self.meta = build_pur_inv( self.df )

    def purchase( self, size:str, pcs:int ) -> list :
        size_list = self.df[ size ]
        deducted_list = []
        for ind in self.df.index: # ind is index of invoice
            if size_list[ ind ] == 0: pass

            if size_list[ ind ] >= pcs: deduct_pcs = pcs
            else: deduct_pcs = size_list[ ind ]
            
            self.df.at[ ind, size ] -= deduct_pcs
            pcs -= deduct_pcs

            if deduct_pcs: deducted_list.append( ind + "(" + str(deduct_pcs) + ")")

            if pcs == 0: return deducted_list

        else: # If Enough pcs not available
            print( "\n!!!!!!!!!!!!!!!!!!!\nStock not available for Size:", size )
            print( "Pieces needed:", pcs )
            print( "Available Stock: 0")
            input( "\nPlease update the stock to get the result\nPress Enter to close" )
            exit()

    def add( self, ind:int, col:str, val:any ): self.df.at[ ind, col ] = val

    def comp( self ):
        df = self.df
        df.reset_index(level=0, inplace=True)
        df_row, df_col = len( df ), len( df.columns )

        # Right most 3
        df.insert( df_col  , "TOTAL", [0]*df_row )
        df.insert( df_col+1, "CBM"  , [0]*df_row )
        df.insert( df_col+2, "SQMTR", [0]*df_row )

        # Bottom 3
        self.df.at[ df_row,   "INVOICE" ] = "TOTAL"
        self.df.at[ df_row+1, "INVOICE" ] = "TOTAL CBM"
        self.df.at[ df_row+2, "INVOICE" ] = "TOTAL SQMTR"

        for col in df.columns:
            
            if is_size( col ):
                
                # Bottom 3 rows
                df.at[ df_row+0, col ] = sum( df[ col ].tolist()[:df_row] ) # -1 to ignore last line because it'll contain nan usually
                df.at[ df_row+1, col ] = to_cbm( col, df.at[ df_row, col ] )
                df.at[ df_row+2, col ] = to_sqmtr( col, df.at[ df_row, col ] )

                # Right most 3 col
                for i in range( 0, df_row ):
                    df.at[ i, "TOTAL"] += df.at[ i, col ]  
                    df.at[ i, "CBM"]   += to_cbm( col, df.at[ i, col ] ) 
                    df.at[ i, "SQMTR"] += to_sqmtr( col, df.at[ i, col ] )
                