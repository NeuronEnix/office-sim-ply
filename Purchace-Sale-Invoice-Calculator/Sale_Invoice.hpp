#include<bits/stdc++.h>

#include "CSV-Parser-CPP/CSV_Parser/CSV_Parser.hpp"
#include "common.hpp"

using namespace std;

class Sale_Invoice {

private:
    CSV_Parser *parser;

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
