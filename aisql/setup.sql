-- Create Source table
CREATE TABLE Source (
    source_id BIGINT PRIMARY KEY,
    source_name VARCHAR(255),
    source_type VARCHAR(255) CHECK (source_type IN ('App', 'Website', 'Form')),
    website_url VARCHAR(255)
);

-- Create Brand table
CREATE TABLE Brand (
    brand_id BIGINT PRIMARY KEY,
    brand_name VARCHAR(255),
    brand_country VARCHAR(255),
    contact_email VARCHAR(255),
    website_url VARCHAR(255)
);

-- Create Category table
CREATE TABLE Category (
    category_id BIGINT PRIMARY KEY,
    category_name VARCHAR(255)
);

-- Create BrandCategory junction table
CREATE TABLE BrandCategory (
    brand_id BIGINT,
    category_id BIGINT,
    PRIMARY KEY (brand_id, category_id),
    FOREIGN KEY (brand_id) REFERENCES Brand(brand_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

-- Create Collaboration table
CREATE TABLE Collaboration (
    collaboration_id BIGINT PRIMARY KEY,
    brand_id BIGINT,
    source_id BIGINT,
    application_link VARCHAR(255),
    collaboration_type VARCHAR(255),
    application_date DATE,
    approval_date DATE,
    collaboration_status VARCHAR(255) CHECK (collaboration_status IN ('Approved', 'Declined', 'Pending')),
    FOREIGN KEY (brand_id) REFERENCES Brand(brand_id),
    FOREIGN KEY (source_id) REFERENCES Source(source_id)
);

-- Create Product table
CREATE TABLE Product (
    product_id BIGINT PRIMARY KEY,
    collaboration_id BIGINT,
    product_name VARCHAR(255),
    product_status VARCHAR(255) CHECK (product_status IN ('Received', 'Not Received')),
    received_date DATE,
    FOREIGN KEY (collaboration_id) REFERENCES Collaboration(collaboration_id)
);

-- Create ContentRequirement table
CREATE TABLE ContentRequirement (
    requirement_id BIGINT PRIMARY KEY,
    product_id BIGINT,
    content_type VARCHAR(255)  CHECK (content_type IN ('Video', 'Post', 'Story')),
    platform VARCHAR(255) CHECK (platform IN ('Instagram', 'Tiktok', 'YouTube')),
    deadline DATE,
    content_url VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Create ContentStatus table
CREATE TABLE ContentStatus (
    status_id BIGINT PRIMARY KEY,
    requirement_id BIGINT,
    content_status VARCHAR(255) CHECK (content_status IN ('Not Started', 'In Progress', 'Completed')),
    start_date DATE,
    completed_date DATE,
    FOREIGN KEY (requirement_id) REFERENCES ContentRequirement(requirement_id)
);

-- Create Compensation table
CREATE TABLE Compensation (
    compensation_id BIGINT PRIMARY KEY,
    status_id BIGINT,
    collaboration_id BIGINT,
    compensation_type VARCHAR(255) CHECK (compensation_type IN ('App Payment', 'Paypal', 'Gift Card', 'Bank Transfer', 'No compensation')),
    amount DECIMAL(10,2),
    received_date DATE,
    compensation_status VARCHAR(255) CHECK (compensation_status IN ('Completed', 'Pending')),
    FOREIGN KEY (status_id) REFERENCES ContentStatus(status_id),
    FOREIGN KEY (collaboration_id) REFERENCES Collaboration(collaboration_id)
);