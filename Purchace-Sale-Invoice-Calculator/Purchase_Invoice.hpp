#include<bits/stdc++.h>

#include "CSV-Parser-CPP/CSV_Parser/CSV_Parser.hpp"
#include "common.hpp"

using namespace std;


class Purchase_Invoice {

private:
CSV_Parser *parser;
    // u_map< inv_num, qty >
    unordered_map< string, unordered_map< string, uint64_t > > deductedLog;

    string log( const string& itemSize, const uint64_t qtyToBeDeducted, const string& invNumber );

public:

    // Constructor
    Purchase_Invoice() { 
        this->parser = new CSV_Parser();
        this->parser->readFromFile( Config::Purchase_Invoice::inputFileName );
    }

    void writeToFile() { this->parser->writeToFile( Config::Purchase_Invoice::outputFileName ); }
    string deduct( const pair< string, uint64_t >& soldItemSizeQtyPair );
    unordered_map< string, unordered_map< string, uint64_t > >&  getDeductedLog() { return this->deductedLog; }

};

// Private Methods
string Purchase_Invoice::log( const string& itemSize, const uint64_t qtyToBeDeducted, const string& invNumber ) {
        if( this->deductedLog.find( invNumber ) != this->deductedLog.end() ) 
            this->deductedLog[ invNumber ][ itemSize ] += qtyToBeDeducted;
        else
            this->deductedLog[ invNumber ][ itemSize ] = qtyToBeDeducted;
        return invNumber + "( " + to_string( qtyToBeDeducted ) + " )";
}

// Public Methods
string Purchase_Invoice::deduct( const pair< string, uint64_t >& soldItemSizeQtyPair ) {

    const string& itemSize = soldItemSizeQtyPair.first;
    uint64_t itemQtyRequired  = soldItemSizeQtyPair.second;
        
    const size_t sizeHeaderPos = this->parser->getHeaderPos( itemSize );
    const size_t invNumHeaderPos = this->parser->getHeaderPos( Config::Purchase_Invoice::invNumAlias );


    string deductedLogDetail = "";

    for( auto& eachInvoice: this->parser->getData() ) {

        auto curInvQty = stoull( eachInvoice[ sizeHeaderPos ] );
        auto curInvNum = eachInvoice[ invNumHeaderPos ];

        if( curInvQty == 0 ) continue;
        uint64_t deductedQty = curInvQty < itemQtyRequired ? curInvQty : itemQtyRequired;

        itemQtyRequired -= deductedQty;
        
        deductedLogDetail += this->log( itemSize, deductedQty, curInvNum ) + "; ";

        eachInvoice[ sizeHeaderPos ] = to_string( stoull( eachInvoice[ sizeHeaderPos ] ) - deductedQty );

        if( itemQtyRequired == 0 ) break;
    }

    if( itemQtyRequired != 0 ) throw underflow_error( "Not Enough Pieces Available in Purchase Invoice");
    
    return deductedLogDetail;
}





