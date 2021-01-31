import pandas as pd
import re

feet_equiv = {
    "8"    : 2.44,
    "7"    : 2.14,
    "6"    : 1.84,
    "5"    : 1.54,
    "4"    : 1.22,
    "3"    : 0.92,
    "2.75" : 0.84,
    "2.5"  : 0.76,
    "2.25" : 0.69
}

def is_size( size:str ): 
    return re.search( "[0-9].*[xX][0-9]", size )

def get_size( size:str ): return size.split("X")

def to_sqmtr( size:str, pcs:int, round_up:int = None ) -> float:
    l,w = get_size( size )
    res = feet_equiv[ l ] * feet_equiv[ w ] * pcs
    return  res if round_up == None else round( res, round_up )
    
def to_cbm( size:str, pcs:int, round_up:int = None ):
    res = to_sqmtr( size, pcs ) / 1000 * 0.25
    return res if round_up == None else round( res, round_up ) 

def load_excel( path:str, index:str = None, trimNaN:bool = True ) :
    df = pd.read_excel( path )

    # Remove trailing empty rows
    col_1 = df.columns[0]
    if trimNaN: [df.drop( ind, inplace = True ) for ind in df.index if str(df[col_1][ind]).strip() == "" or str(df[col_1][ind]).strip() == "nan" ]
    
    # Capitalization of all column names
    df.columns = map( str.upper, df.columns )

    # Setting Index
    if index: df.set_index( index.upper(), inplace=True )

    return df
