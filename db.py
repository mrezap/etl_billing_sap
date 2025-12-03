from sqlalchemy import create_engine
from config import DB_URL

engine = create_engine(
    DB_URL,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 60,
        "keepalives_interval": 10,
        "keepalives_count": 5
    },
    pool_pre_ping=True
)

column_set = [
                            '"Sales Organization"', '"Sales Org. Desc"',
                            '"Distribution Channel"', '"Dist.Chan.Desc"',
                            '"Site Code"', '"Site Desc"', '"Cust.Code"',
                            '"Cust.Location"', '"Trans.Zone"', '"Kecamatan"',
                            '"Salesman Code"', '"Salesman Name"',
                            '"Uniqcode Salesman"', '"Sold to Party Code"',
                            '"Sold to Party Name"', '"ID Outlet"',
                            '"City of Customer"', '"SO Number"',
                            '"SO Item No"', '"PO Customer"', '"Delivery No"',
                            '"DO Item no"', '"TOP code"', '"TOP Description"',
                            '"Billing Date"', '"Billing Type"',
                            '"Billing Document"', '"Bill item no"',
                            '"Article Code"', '"Article Description"',
                            '"Item Group Code"', '"Item Group Desc"',
                            '"Item Category"', '"Item Category Desc"',
                            '"Brand"', '"Brand Name"', '"Old Material Number"',
                            '"Vendor"', '"Vendor Name"', '"Document Currency"',
                            '"No Faktur Pajak"', '"SO Type"',
                            '"SO Type Description"', '"Payer Code"',
                            '"Payer Name"', '"Billto Code"', '"Billto Name"',
                            '"BBID-PM"', '"BBID-PM Description"',
                            '"Validity PM"', '"PM Discount"', '"BBID-PnP"',
                            '"BBID-PnP Description"', '"Validity PnP"',
                            '"PnP Discount"', '"BBID-CRM"',
                            '"BBID-CRM Description"', '"Validity CRM"',
                            '"CRM Discount"', '"BBID-Vendor"',
                            '"BBID-Vendor Description"', '"Validity Vendor"',
                            '"Vendor Discount"', '"Promo ID"',
                            '"Promo Vendor Description"',
                            '"Condition Contract"',
                            '"Unit price in frgn curr"',
                            '"Disc price in frgn curr"', '"Kurs"',
                            '"Quantity"', '"SRP Value"', '"Delta Price-SRP"',
                            '"Unit Price Exc Tax"', '"Unit Price With Tax"',
                            '"Discount Amount Per Unit Exc Tax"',
                            '"Discount Amount Per Unit Inc Tax"',
                            '"Nett Amount Per Price Inc Tax"',
                            '"Nett Amount Per Price Exc Tax"',
                            '"Total Gross Price Inc Tax"',
                            '"Total Gross Price Exc Tax"',
                            '"Total Discount Amount Exc Tax"',
                            '"Total Discount Amount with Tax"',
                            '"Total Nett Amount No Tax"', '"Total Amount Tax"',
                            '"Total Nett Amount with Tax"', '"Lot (batch)"',
                            '"Remark"', '"Ext. Code"', '"Ext. System Name"',
                            '"Exp. Code"', '"Exp. Name"', '"AWB Number"',
                            '"Quantity EA"', '"Quantity PC"', '"Quantity LS"'
                        ]

sp_name = "dwh.insert_billing_latest_data"