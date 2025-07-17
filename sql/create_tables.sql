CREATE TABLE Property (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    property_title VARCHAR(255),
    address VARCHAR(255),
    market VARCHAR(50),
    flood VARCHAR(50),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state CHAR(2),
    zip VARCHAR(10),
    property_type VARCHAR(50),
    highway VARCHAR(50),
    train VARCHAR(50),
    tax_rate DECIMAL(5,2),
    sqft_basement INT,
    htw ENUM('Yes', 'No'),
    pool ENUM('Yes', 'No'),
    commercial ENUM('Yes', 'No'),
    water VARCHAR(50),
    sewage VARCHAR(50),
    year_built INT,
    sqft_mu INT,
    sqft_total INT,
    parking VARCHAR(50),
    bed INT,
    bath INT,
    basement_yes_no ENUM('Yes', 'No'),
    layout VARCHAR(50),
    rent_restricted ENUM('Yes', 'No'),
    neighborhood_rating INT,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    subdivision VARCHAR(50),
    school_average DECIMAL(5,2)
);

CREATE TABLE Leads (
    lead_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    reviewed_status VARCHAR(50),
    most_recent_status VARCHAR(50),
    source VARCHAR(50),
    occupancy VARCHAR(50),
    net_yield DECIMAL(5,2),
    irr DECIMAL(5,2),
    selling_reason VARCHAR(50),
    seller_retained_broker VARCHAR(50),
    final_reviewer VARCHAR(50),
    FOREIGN KEY (property_id) REFERENCES Property(property_id)
);

CREATE TABLE Valuation (
    valuation_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    previous_rent DECIMAL(10,2),
    list_price DECIMAL(10,2),
    zestimate DECIMAL(10,2),
    arv DECIMAL(10,2),
    expected_rent DECIMAL(10,2),
    rent_zestimate DECIMAL(10,2),
    low_fmr DECIMAL(10,2),
    high_fmr DECIMAL(10,2),
    redfin_value DECIMAL(10,2),
    FOREIGN KEY (property_id) REFERENCES Property(property_id)
);

CREATE TABLE HOA (
    hoa_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa DECIMAL(10,2),
    hoa_flag ENUM('Yes', 'No'),
    FOREIGN KEY (property_id) REFERENCES Property(property_id)
);

CREATE TABLE Rehab (
    rehab_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    underwriting_rehab DECIMAL(10,2),
    rehab_calculation DECIMAL(10,2),
    paint ENUM('Yes', 'No'),
    flooring_flag ENUM('Yes', 'No'),
    foundation_flag ENUM('Yes', 'No'),
    roof_flag ENUM('Yes', 'No'),
    hvac_flag ENUM('Yes', 'No'),
    kitchen_flag ENUM('Yes', 'No'),
    bathroom_flag ENUM('Yes', 'No'),
    appliances_flag ENUM('Yes', 'No'),
    windows_flag ENUM('Yes', 'No'),
    landscaping_flag ENUM('Yes', 'No'),
    trashout_flag ENUM('Yes', 'No'),
    FOREIGN KEY (property_id) REFERENCES Property(property_id)
);

CREATE TABLE Taxes (
    taxes_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    taxes DECIMAL(10,2),
    FOREIGN KEY (property_id) REFERENCES Property(property_id)
);