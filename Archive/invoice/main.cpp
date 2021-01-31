#include<bits/stdc++.h>
#include "CSV_Parser/CSV_Parser.hpp"


using namespace std;

int main() {
    CSV_Parser pur = CSV_Parser();
    CSV_Parser sale = CSV_Parser();
    
    // Reading stuffs from file
    pur.readFromFile( "pur.csv" );
    sale.readFromFile( "sale.csv" );

    
    return 0;
}