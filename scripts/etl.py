import json
import mysql.connector
from mysql.connector import Error

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'db_user',
    'password': '6equj5_db_user',
    'database': 'home_db'
}

# Load JSON data (assumed to be at 'data/property_data.json')
with open('data/fake_property_data.json', 'r') as file:
    properties_data = json.load(file)

# Helper function to handle missing or empty values and type conversion
def get_value(data, key, type_func=None):
    value = data.get(key)
    if value is None or (isinstance(value, str) and (value == '' or value.isspace())):
        return None
    if type_func:
        try:
            return type_func(value)
        except (ValueError, TypeError):
            return None
    return value

# Connect to MySQL and load data
try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        cursor = connection.cursor()

        for property_data in properties_data:
            # Insert into Property table
            property_fields = (
                get_value(property_data, 'Property_Title'),
                get_value(property_data, 'Address'),
                get_value(property_data, 'Market'),
                get_value(property_data, 'Flood'),
                get_value(property_data, 'Street_Address'),
                get_value(property_data, 'City'),
                get_value(property_data, 'State'),
                get_value(property_data, 'Zip'),
                get_value(property_data, 'Property_Type'),
                get_value(property_data, 'Highway'),
                get_value(property_data, 'Train'),
                get_value(property_data, 'Tax_Rate', float),
                get_value(property_data, 'SQFT_Basement', int),
                get_value(property_data, 'HTW'),
                get_value(property_data, 'Pool'),
                get_value(property_data, 'Commercial'),
                get_value(property_data, 'Water'),
                get_value(property_data, 'Sewage'),
                get_value(property_data, 'Year_Built', int),
                get_value(property_data, 'SQFT_MU', int),
                get_value(property_data, 'SQFT_Total', int),
                get_value(property_data, 'Parking'),
                get_value(property_data, 'Bed', int),
                get_value(property_data, 'Bath', int),
                get_value(property_data, 'BasementYesNo'),
                get_value(property_data, 'Layout'),
                get_value(property_data, 'Rent_Restricted'),
                get_value(property_data, 'Neighborhood_Rating', int),
                get_value(property_data, 'Latitude', float),
                get_value(property_data, 'Longitude', float),
                get_value(property_data, 'Subdivision'),
                get_value(property_data, 'School_Average', float)
            )
            cursor.execute("""
                INSERT INTO Property (
                    property_title, address, market, flood, street_address, city, state, zip, property_type,
                    highway, train, tax_rate, sqft_basement, htw, pool, commercial, water, sewage, year_built,
                    sqft_mu, sqft_total, parking, bed, bath, basement_yes_no, layout, rent_restricted,
                    neighborhood_rating, latitude, longitude, subdivision, school_average
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, property_fields)
            property_id = cursor.lastrowid

            # Insert into Leads table
            leads_fields = (
                property_id,
                get_value(property_data, 'Reviewed_Status'),
                get_value(property_data, 'Most_Recent_Status'),
                get_value(property_data, 'Source'),
                get_value(property_data, 'Occupancy'),
                get_value(property_data, 'Net_Yield', float),
                get_value(property_data, 'IRR', float),
                get_value(property_data, 'Selling_Reason'),
                get_value(property_data, 'Seller_Retained_Broker'),
                get_value(property_data, 'Final_Reviewer')
            )
            cursor.execute("""
                INSERT INTO Leads (
                    property_id, reviewed_status, most_recent_status, source, occupancy, net_yield, irr,
                    selling_reason, seller_retained_broker, final_reviewer
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, leads_fields)

            # Insert into Taxes table
            taxes_fields = (
                property_id,
                get_value(property_data, 'Taxes', float)
            )
            cursor.execute("""
                INSERT INTO Taxes (property_id, taxes) VALUES (%s, %s)
            """, taxes_fields)

            # Insert into Valuation table (assuming Valuation is an array in JSON)
            for valuation in property_data.get('Valuation', []):
                valuation_fields = (
                    property_id,
                    get_value(valuation, 'Previous_Rent', float),
                    get_value(valuation, 'List_Price', float),
                    get_value(valuation, 'Zestimate', float),
                    get_value(valuation, 'ARV', float),
                    get_value(valuation, 'Expected_Rent', float),
                    get_value(valuation, 'Rent_Zestimate', float),
                    get_value(valuation, 'Low_FMR', float),
                    get_value(valuation, 'High_FMR', float),
                    get_value(valuation, 'Redfin_Value', float)
                )
                cursor.execute("""
                    INSERT INTO Valuation (
                        property_id, previous_rent, list_price, zestimate, arv, expected_rent, rent_zestimate,
                        low_fmr, high_fmr, redfin_value
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, valuation_fields)

            # Insert into HOA table (assuming HOA is an array in JSON)
            for hoa in property_data.get('HOA', []):
                hoa_fields = (
                    property_id,
                    get_value(hoa, 'HOA', float),
                    get_value(hoa, 'HOA_Flag')
                )
                cursor.execute("""
                    INSERT INTO HOA (property_id, hoa, hoa_flag) VALUES (%s, %s, %s)
                """, hoa_fields)

            # Insert into Rehab table (assuming Rehab is an array in JSON)
            for rehab in property_data.get('Rehab', []):
                rehab_fields = (
                    property_id,
                    get_value(rehab, 'Underwriting_Rehab', float),
                    get_value(rehab, 'Rehab_Calculation', float),
                    get_value(rehab, 'Paint'),
                    get_value(rehab, 'Flooring_Flag'),
                    get_value(rehab, 'Foundation_Flag'),
                    get_value(rehab, 'Roof_Flag'),
                    get_value(rehab, 'HVAC_Flag'),
                    get_value(rehab, 'Kitchen_Flag'),
                    get_value(rehab, 'Bathroom_Flag'),
                    get_value(rehab, 'Appliances_Flag'),
                    get_value(rehab, 'Windows_Flag'),
                    get_value(rehab, 'Landscaping_Flag'),
                    get_value(rehab, 'Trashout_Flag')
                )
                cursor.execute("""
                    INSERT INTO Rehab (
                        property_id, underwriting_rehab, rehab_calculation, paint, flooring_flag, foundation_flag,
                        roof_flag, hvac_flag, kitchen_flag, bathroom_flag, appliances_flag, windows_flag,
                        landscaping_flag, trashout_flag
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, rehab_fields)

        # Commit all changes
        connection.commit()
        print("Data successfully loaded into the database.")

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Database connection closed.")