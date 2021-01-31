#include<bits/stdc++.h>

#include "CSV-Parser-CPP/CSV_Parser/CSV_Parser.hpp"
#include "common.hpp"

using namespace std;

template<class T>
int findEleColWise( const vector< vector<T> >& vec, int colPos, T ele ) {
    for (size_t i = 0; i < vec.size(); i++) 
        if( vec[i][colPos] == ele ) return i;
    return -1;
    
}

class Sale_Invoice {

private:
    CSV_Parser *parser;
    void sumDuplicates() {
        auto& data = this->parser->getData();
        auto sizePos = this->parser->getHeaderPos( "Size" );
        auto piecesPos = this->parser->getHeaderPos( "Pieces" );
        // cout << sizePos;
        // cout << piecesPos;
        // return;
        // cout << endl << piecesPos;
        for( int i=data.size()-1; i>=0; --i ) {
            const int foundPos = findEleColWise( data, sizePos, data[i][sizePos] );
            if( foundPos == i ) continue;
            data[i][sizePos] = to_string( stoull(data[foundPos][piecesPos]) + stoull(data[i][piecesPos]) );
            data.erase( data.begin() + foundPos );
        }
    }

public:
    Sale_Invoice();

    void writeToFile() { this->parser->writeToFile( Config::Sale_Invoice::outputFileName ); }
    vector< pair< string, uint64_t > > getSoldItems();
    vector< vector< string > >& getParsedData() { return this->parser->getData(); }

};

// Constructor

Sale_Invoice::Sale_Invoice() {
    this->parser = new CSV_Parser();
    this->parser->readFromFile( Config::Sale_Invoice::inputFileName );
    // this->sumDuplicates();
}


// Public Methods

vector< pair< string, uint64_t > > Sale_Invoice::getSoldItems(){
    vector< pair< string, uint64_t > > sizeQtyPair;

    size_t qtyHeaderPos  = this->parser->getHeaderPos( Config::Sale_Invoice::qtyAlias  );
    size_t sizeHeaderPos = this->parser->getHeaderPos( Config::Sale_Invoice::sizeAlias );
    
    for( auto& eachRow: parser->getData() ) {
        sizeQtyPair.emplace_back(
            make_pair( eachRow[ sizeHeaderPos ], std::stoull( eachRow[ qtyHeaderPos ] ) )
        );
    }
    
    return sizeQtyPair;
}
