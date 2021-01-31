from helper import load_excel
from pandas import DataFrame

from Invoice import Invoice

class Purchase:
    def __init__( self, df:DataFrame ):
        
        for ind in df.index:
            print( ind )

            

    
