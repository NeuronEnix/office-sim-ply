#pragma once
#include<bits/stdc++.h>
using namespace std;

string inFileName = "inv.csv";
string outFileName = "out.csv";

#define FAST_IO ios_base::sync_with_stdio(false); cin.tie(NULL);
#define FIN  freopen ( inFileName.c_str()  , "r", stdin  );
#define FOUT freopen ( outFileName.c_str() , "w", stdout );

#define all( var ) var.begin(), var.end()

#define fo(  var, init, till       ) for( int var = (init); var < (till); ++var         )
#define fos( var, init, till, step ) for( int var = (init); var < (till); var += (step) )

#define rfo(  var, init, till       ) for( int var = (init); var >= (till); --var         )
#define rfos( var, init, till, step ) for( int var = (init); var >= (till); var -= (step) )

#define foe( val, vals ) for( auto &val : vals )

typedef long long ll; typedef unsigned long long ull;

typedef vector<int> vi; typedef vector<string> vs;
typedef vector< vi > vvi; typedef vector< vs > vvs;

#define in_i( var ) int var; cin >> var;
#define in_s( var ) string var; cin >> var;

#define in_vi( var, size ) vi var( size ); foe( each, var ) cin >> each;
#define in_vs( var, size ) vs var( size ); foe( each, var ) cin >> each;

#define in_vvi( var_vvi, size_r, size_c ) vvi var_vvi( size_r, vi(size_c) ); foe( var_vi, var_vvi ) foe( each, var_vi ) cin >> each;
#define in_vvs( var_vvs, size_r, size_c ) vvs var_vvs( size_r, vs(size_c) ); foe( var_vs, var_vvs ) foe( each, var_vs ) cin >> each;

#define deb( var ) cout << #var << " : " << var << '\n';
#define deb_v( var_v )   { foe( each , var_v  ) cout << each << " "; cout << '\n' ; }
#define deb_vv( var_vv ) { foe( var_v, var_vv ) { cout << "(" << var_v.size() << ")  "; deb_v( var_v ) }     ; cout << '\n' ; }

#define deb_m( var_m ) { for( auto& each: var_m ) cout << "Key: " << each.first << " Value: " << each.second << '\n'; }

int toInt( const string& str ){
    if( str.size() == 0 ) throw "Null string Passed to toInt()";
    for( const char& ch: str )
        if( !isdigit( ch ) ) throw "Invalid Integer was passed to toInt()";
    return stoi( str );
}

double toDouble( const string& str ){
    stringstream ss( str );
    double val;
    ss >> val;
    return val;
}