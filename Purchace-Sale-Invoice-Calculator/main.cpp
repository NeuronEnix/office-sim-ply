#include<bits/stdc++.h>

#include "Purchase_Invoice.hpp"
#include "Sale_Invoice.hpp"
#include "common.hpp"
#include "a.hpp"

using namespace std;
int main() {
    Purchase_Invoice *pur_inv = new Purchase_Invoice();
    Sale_Invoice *sale_inv = new Sale_Invoice();
    
    vector< string > invLogDetails ;

    for( auto& eachSoldItem: sale_inv->getSoldItems() )
        invLogDetails.push_back( pur_inv->deduct( eachSoldItem ) );

    auto& saleInvParsedData = sale_inv->getParsedData();    
    Helper::attach_1D_vector_as_last_column_of_2D_vector( invLogDetails, saleInvParsedData );

    saleInvParsedData.push_back( vector<string>{""} );

    saleInvParsedData.push_back( vector< string > { Config::Purchase_Invoice::invNumAlias, "Total Pieaces", "CBM", "SQMTR" } ) ;

    uint64_t grandTotalQty = 0;
    double grandTotalCBM = 0, grandTotalSQMTR = 0;

    for( const auto& eachInv: pur_inv->getDeductedLog() ) {

        uint64_t curTotQty = 0;
        double curTotCBM = 0, curTotSQMTR = 0;

        for( const auto& eachSizeQty: eachInv.second ) { // eachInv sizeQty as u_map< string:"Size", uint64_t:"Qty" >
            curTotQty   += eachSizeQty.second;
            curTotCBM   += Helper::to_cbm  ( eachSizeQty.first, eachSizeQty.second );
            curTotSQMTR += Helper::to_sqmtr( eachSizeQty.first, eachSizeQty.second );    
        }

        grandTotalQty += curTotQty; grandTotalCBM = curTotCBM; grandTotalQty = curTotSQMTR;
        // Invoice Number, TotalQtyDeducted, TotalCBM, TotalSQMTR
        saleInvParsedData.push_back( vector<string>{ eachInv.first, to_string( curTotQty ), to_string( curTotCBM ), to_string( curTotSQMTR ) } );
        
    }

    saleInvParsedData.push_back( vector<string>{""} );

    saleInvParsedData.push_back( vector<string> { "Grand Total"       , to_string( grandTotalQty   ) } ) ;
    saleInvParsedData.push_back( vector<string> { "Grand Total CBM"   , to_string( grandTotalCBM   ) } ) ;
    saleInvParsedData.push_back( vector<string> { "Grand Total SQMTR" , to_string( grandTotalSQMTR ) } ) ;

    pur_inv->writeToFile();
    sale_inv->writeToFile();
        
}
