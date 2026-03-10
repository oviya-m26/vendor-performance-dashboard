import pandas as pd
import sqlite3
import logging 
from ingestion_db import ingest_db
def create_vendor_summary(conn):
    vendor_sales_summary = pd.read_sql_query("""WITH FreightSummary AS(select VendorNumber, SUM(Freight) as FreightCost from vendor_invoice
GROUP BY VendorNumber),
PurchaseSummary AS( SELECT p.VendorNumber,
p.VendorName,
p.Brand,
p.PurchasePrice,
pp.Volume,
pp.Price as ActualPrice,
SUM(p.Quantity) as TotalPurchaseQuantity,
SUM(p.Dollars) as TotalPurchaseDollars
FROM purchases p
JOIN purchase_prices pp
ON p.Brand = pp.Brand
where p.purchasePrice>0
GROUP BY p.VendorNumber,p.VendorName,p.Brand,p.PurchasePrice,pp.Volume,pp.Price
ORDER BY TotalPurchaseDollars
),
SalesSummary AS (SELECT VendorNo,
Brand,
SUM(SalesPrice) as TotalSalesPrice,
SUM(SalesDollars) as TotalSalesDollars,
SUM(SalesQuantity) as TotalSalesQuantity,
SUM(ExciseTax) as TotalExciseTax
FROM sales
GROUP BY VendorNo, Brand)
SELECT 
ps.VendorNumber,
ps.VendorName,
ps.Brand,
ps.PurchasePrice,
ps.ActualPrice,
ps.Volume,
ps.TotalPurchaseQuantity,
ps.TotalPurchaseDollars,
ss.TotalSalesQuantity,
ss.TotalSalesDollars,
ss.TotalSalesPrice,
ss.TotalExciseTax,
fs.FreightCost
FROM PurchaseSummary ps 
LEFT JOIN SalesSummary ss
ON ps.VendorNumber = ss.VendorNo
AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs 
ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC""",conn)
    
return vendor_sales_Summary

def clean_data(vendor_sales_Summary):
    vendor_sales_Summary['Volume']=vendor_sales_Summary['Volume'].astype('float64')
    vendor_sales_Summary.fillna(0,inplace=True)
    vendor_sales_Summary['VendorName']=vendor_sales_Summary['VendorName'].str.strip()
    vendor_sales_Summary['Description']=vendor_sales_Summary['Description'].str.strip()
    
    vendor_sales_Summary['GrossProfit'] = vendor_sales_Summary['TotalSalesDollars']-vendor_sales_Summary['TotalPurchaseDollars']
    vendor_sales_Summary['ProfitMargin']=(vendor_sales_Summary['GrossProfit']/vendor_sales_Summary['TotalSalesDollars'])*100
    vendor_sales_Summary['StockTurnover'] = vendor_sales_Summary['TotalSalesQuantity'] / vendor_sales_Summary['TotalPurchaseQuantity']
    vendor_sales_Summary['SalesToPurchaseRatio'] = vendor_sales_Summary['TotalSalesDollars']/vendor_sales_Summary['TotalPurchaseDollars']
    return vendor_sales_Summary
    
if __name__ = '__main__':
    conn=sqlite3.connect('inventory.db')
    logging.info('Creating Vendor Summary Table....')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())
    logging.info('Ingesting data.......')
    ingest_db(clean_df,vendor_sales_summary;,conn)
    logging.info('Completed')

logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s-%(levelname)s-%(message)s".
    filemode="a"
)