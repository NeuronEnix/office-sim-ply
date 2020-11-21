#pragma once
#include<bits/stdc++.h>
using namespace std;

namespace Config {

    namespace Purchase_Invoice {
        const string inputFileName = "Purchase Invoice.csv" ;
        const string outputFileName = "Updated Purchase Invoice.csv";
        const string invNumAlias = "Invoice";
    }

    namespace Sale_Invoice {
        const string inputFileName = "Sale Invoice.csv" ;
        const string outputFileName = "Updated Sale Invoice.csv";
        const string sizeAlias = "Size";
        const string qtyAlias = "Pieces";
    }

    namespace name
    {
        
    } // namespace name
    
} // namespace Config

namespace Helper {

    double sizeConvertor( const string& num ) {
        if( "8"    == num ) return  2.44;
        if( "7"    == num ) return  2.14;
        if( "6"    == num ) return  1.84;
        if( "5"    == num ) return  1.54;
        if( "4"    == num ) return  1.22;
        if( "3"    == num ) return  0.92;
        if( "2.75" == num ) return  0.84;
        if( "2.5"  == num ) return  0.76;
        if( "2.25" == num ) return  0.69;
    }

    double getMultipliedValue( const string& str ){    
        const int pos = str.find( 'x' );    
        double first  = sizeConvertor( str.substr( 0, pos ) );
        double second = sizeConvertor( str.substr( pos+1  ) );
        return first * second ;
    }

    double to_cbm(  const string& itemSize, const uint64_t itemQty ) { 
        return itemQty*(double)0.25*getMultipliedValue( itemSize );
    }
    double to_sqmtr( const string& itemSize, const uint64_t itemQty ) { 
        return itemQty*getMultipliedValue( itemSize );
    }

    void attach_1D_vector_as_last_column_of_2D_vector( const vector<string>& vec_1d, vector< vector < string > >& vec_2d ) {
        for (size_t i = 0; i < vec_1d.size(); i++)
            vec_2d[i].push_back( vec_1d[i] ) ;
    }
    
} // namespace Helper

