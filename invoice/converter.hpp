#pragma once
#include<bits/stdc++.h>
using namespace std;

namespace meta {

    namespace pur {
        const string inFile = "Purchase Invoice.csv" ;
        const string outFile = "Updated Purchase Invoice.csv";
        const string invCol = "Invoice";
    }

    namespace sale {
        const string inFile = "Sale Invoice.csv" ;
        const string outFile = "Updated Sale Invoice.csv";
        const string sz = "Size";
        const string qty = "Pieces";
    }

    namespace name
    {
        
    } // namespace name
    
} // namespace meta

namespace con {

    double feet( const string& num ) {

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

    double sqmtr( string& sz, const string& qty ) {

        // replacing lower_case 'x' to upper_case 'X'
        auto small_x_pos = sz.find( 'x' );
        if( small_x_pos != string::npos ) sz[ small_x_pos ] = 'X';

        // Splitting size eg -> "8x2.5" to "8", "2.5"
        auto pos_X = sz.find( 'X' );
        if( pos_X == string::npos ) { // Just in case if 'x' or 'X' not found
            cout << " x / X not found in Size: " << sz << endl ;
            throw false;
        }

        double len = feet( sz.substr( 0, pos_X ) );
        double brd = feet( sz.substr( pos_X+1  ) );


        return len * brd * stoi( qty );
    }

    double cbm( string& sz, const string& qty ) {
        return sqmtr( sz, qty ) * 0.25 ;
    }

};