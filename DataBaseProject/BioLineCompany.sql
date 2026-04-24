--  Mohammed Salem - Sabtia Assad

CREATE DATABASE IF NOT EXISTS BioLineCompany;
USE BioLineCompany;

CREATE TABLE PaymentMethod (
  MethodId        TINYINT UNSIGNED PRIMARY KEY,
  MethodName      VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE CustomerType (
  CustomerTypeId  TINYINT UNSIGNED PRIMARY KEY,
  TypeName        VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE ProductStatus (
  StatusId        TINYINT UNSIGNED PRIMARY KEY,
  StatusName      VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE SupplierType (
  SupplierTypeId  TINYINT UNSIGNED PRIMARY KEY,
  TypeName        VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE Company (
  CompanyId           INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  CompanyName         VARCHAR(64) NOT NULL,
  CEO                 VARCHAR(64) NOT NULL,
  FoundedYear         YEAR NOT NULL,
  City                VARCHAR(64) NOT NULL,
  Address             VARCHAR(100) NOT NULL,
  Website             VARCHAR(255),
  NumberOfEmployees   INT UNSIGNED NOT NULL DEFAULT 0,
  CreatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  IsActive            TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE Department (
  DepartmentId        INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  DepartmentName      VARCHAR(64) NOT NULL,
  EmployeeCount       INT UNSIGNED NOT NULL DEFAULT 0,
  CompanyId           INT UNSIGNED NOT NULL,
  CreatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  IsActive            TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY (CompanyId, DepartmentName),
  FOREIGN KEY (CompanyId) REFERENCES Company(CompanyId)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE Employee (
  EmployeeId          INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  FirstName           VARCHAR(32) NOT NULL,
  LastName            VARCHAR(32) NOT NULL,
  Position            VARCHAR(64),
  PhoneNumber         VARCHAR(20),
  Email               VARCHAR(255) NOT NULL UNIQUE,
  Address             VARCHAR(100),
  Gender              ENUM('Male','Female') NOT NULL,
  DateOfHire          DATE NOT NULL,
  DateOfBirth         DATE NOT NULL,
  Salary              DECIMAL(12,2) NOT NULL,
  WorkHours           INT UNSIGNED NOT NULL DEFAULT 8,
  DepartmentId        INT UNSIGNED NOT NULL,
  CreatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  IsActive            TINYINT(1) NOT NULL DEFAULT 1,
  FOREIGN KEY (DepartmentId) REFERENCES Department(DepartmentId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE TABLE Product (
  ProductId           INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  ProductName         VARCHAR(100) NOT NULL,
  Category            VARCHAR(64)  NOT NULL,
  CostPrice           DECIMAL NOT NULL,
  SellingPrice        DECIMAL NOT NULL,
  DiscountRate        DECIMAL NOT NULL DEFAULT 0.00,
  QuantityInStock     INT UNSIGNED NOT NULL DEFAULT 0,
  ExpirationDate      DATE,
  StatusId            TINYINT UNSIGNED NOT NULL,
  DateAdded           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ReturnPolicy        VARCHAR(64),
  CompanyId           INT UNSIGNED NOT NULL,
  CreatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  IsActive            TINYINT(1) NOT NULL DEFAULT 1,
  CONSTRAINT CHK_Product_DiscountRate CHECK (DiscountRate BETWEEN 0 AND 100),
  INDEX (ProductName),
  FOREIGN KEY (StatusId) REFERENCES ProductStatus(StatusId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (CompanyId) REFERENCES Company(CompanyId)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE Customer (
  CustomerId          INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  FirstName           VARCHAR(32) NOT NULL,
  LastName            VARCHAR(32) NOT NULL,
  ContactNumber       VARCHAR(20),
  Email               VARCHAR(255),
  ShippingAddress     VARCHAR(200),
  CustomerTypeId      TINYINT UNSIGNED NOT NULL,
  PaymentMethodId     TINYINT UNSIGNED NOT NULL,
  CreatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  IsActive            TINYINT(1) NOT NULL DEFAULT 1,
  FOREIGN KEY (CustomerTypeId) REFERENCES CustomerType(CustomerTypeId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (PaymentMethodId) REFERENCES PaymentMethod(MethodId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE TABLE Supplier (
  SupplierId          INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  SupplierCompany     VARCHAR(100) NOT NULL,
  ContactName         VARCHAR(100),
  PhoneNumber         VARCHAR(20),
  Email               VARCHAR(255),
  Address             VARCHAR(100),
  Website             VARCHAR(255),
  SupplierTypeId      TINYINT UNSIGNED NOT NULL,
  CreatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  IsActive            TINYINT(1) NOT NULL DEFAULT 1,
  FOREIGN KEY (SupplierTypeId) REFERENCES SupplierType(SupplierTypeId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE TABLE Purchase (
  PurchaseId          INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  PurchaseDate        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  SupplierId          INT UNSIGNED NOT NULL,
  CompanyId           INT UNSIGNED NOT NULL,
  TotalCost           DECIMAL(14,2) NOT NULL,
  FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (CompanyId) REFERENCES Company(CompanyId)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE PurchaseDetail (
  PurchaseDetailId    INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  PurchaseId          INT UNSIGNED NOT NULL,
  ProductId           INT UNSIGNED NOT NULL,
  Quantity            INT UNSIGNED NOT NULL,
  CostPerUnit         DECIMAL NOT NULL,
  FOREIGN KEY (PurchaseId) REFERENCES Purchase(PurchaseId)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE TABLE Sale (
  SaleId              INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  SaleDate            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CustomerId          INT UNSIGNED NOT NULL,
  CompanyId           INT UNSIGNED NOT NULL,
  TotalRevenue        DECIMAL NOT NULL,
  INDEX (SaleDate),
  FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (CompanyId) REFERENCES Company(CompanyId)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE SaleDetail (
  SaleDetailId        INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  SaleId              INT UNSIGNED NOT NULL,
  ProductId           INT UNSIGNED NOT NULL,
  Quantity            INT UNSIGNED NOT NULL,
  SellingPrice        DECIMAL NOT NULL,
  FOREIGN KEY (SaleId) REFERENCES Sale(SaleId)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE TABLE SupplierProduct (
  SupplierProductId   INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  SupplierId          INT UNSIGNED NOT NULL,
  ProductId           INT UNSIGNED NOT NULL,
  FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

-- =============================================================================
-- AUTOMATIC COUNTS

DELIMITER $$

-- 2.2 Increment Department.EmployeeCount when an employee is added
DROP TRIGGER IF EXISTS trg_IncDeptCount$$
CREATE TRIGGER trg_IncDeptCount
AFTER INSERT ON Employee
FOR EACH ROW
BEGIN
  UPDATE Department
  SET EmployeeCount = EmployeeCount + 1
  WHERE DepartmentId = NEW.DepartmentId;
END$$

-- 2.3 Decrement Department.EmployeeCount when an employee is removed
DROP TRIGGER IF EXISTS trg_DecDeptCount$$
CREATE TRIGGER trg_DecDeptCount
AFTER DELETE ON Employee
FOR EACH ROW
BEGIN
  UPDATE Department
  SET EmployeeCount = EmployeeCount - 1
  WHERE DepartmentId = OLD.DepartmentId;
END$$

-- 2.4 Update Company.NumberOfEmployees after an employee is added
DROP TRIGGER IF EXISTS trg_UpdateCompanyEmployeeCount_AfterInsert$$
CREATE TRIGGER trg_UpdateCompanyEmployeeCount_AfterInsert
AFTER INSERT ON Employee
FOR EACH ROW
BEGIN
  UPDATE Company
  SET NumberOfEmployees = (
    SELECT SUM(EmployeeCount)
    FROM Department
    WHERE CompanyId = (
      SELECT CompanyId FROM Department WHERE DepartmentId = NEW.DepartmentId
    )
  )
  WHERE CompanyId = (
    SELECT CompanyId FROM Department WHERE DepartmentId = NEW.DepartmentId
  );
END$$

-- 2.5 Update Company.NumberOfEmployees after an employee is removed
DROP TRIGGER IF EXISTS trg_UpdateCompanyEmployeeCount_AfterDelete$$
CREATE TRIGGER trg_UpdateCompanyEmployeeCount_AfterDelete
AFTER DELETE ON Employee
FOR EACH ROW
BEGIN
  UPDATE Company
  SET NumberOfEmployees = (
    SELECT SUM(EmployeeCount)
    FROM Department
    WHERE CompanyId = (
      SELECT CompanyId FROM Department WHERE DepartmentId = OLD.DepartmentId
    )
  )
  WHERE CompanyId = (
    SELECT CompanyId FROM Department WHERE DepartmentId = OLD.DepartmentId
  );
END$$

DELIMITER ;



-- =============================================================================
-- DATA

INSERT INTO PaymentMethod VALUES (1,'Cash'),(2,'Credit Card'),(3,'Bank Transfer');
INSERT INTO CustomerType VALUES (1,'Retail'),(2,'Wholesale');
INSERT INTO ProductStatus VALUES (1,'Available');
INSERT INTO SupplierType VALUES (1,'Local'),(2,'International');

INSERT INTO Company (CompanyName,CEO,FoundedYear,City,Address,Website)
VALUES ('BioLine Ramallah','Abd AlSalam Sarary',2005,'Ramallah','Al kolliya Al Ahliyya Street Al Assad Building','https://www.bioline.ps'),
        ('BioLine Bethlehem','Mohammad Salem',2020,'Bethlehem','Jerusalem Hebron St.','https://www.bioline.ps'),
        ('BioLine Hebron','Sabtia Asad',2024,'Hebron','Ein Sara st.','https://www.bioline.ps');

INSERT INTO Department (DepartmentName, CompanyId) VALUES
  ('Sales',1),('Logistics',1),('Technical',1),('Cleaning',1),
  ('Sales',2),('Logistics',2),('Technical',2),('Cleaning',2),
  ('Sales',3),('Logistics',3),('Technical',3);

-- Company 1 Employees
INSERT INTO Employee (FirstName, LastName, Position, PhoneNumber, Email, Address, Gender, DateOfHire, DateOfBirth, Salary, DepartmentId) VALUES
  ('Alaa', 'Nasser', 'Sales Manager', '0599000001', 'alaa.nasser1@bioline.ps', 'Ramallah Main St.', 'Male',   '2020-03-01', '1985-07-12', 2550.00, 1),
  ('Lina', 'Jaber',  'Sales Rep',     '0599000002', 'lina.jaber1@bioline.ps',  'Ramallah Main St.', 'Female', '2021-01-13', '1990-11-22', 2100.00, 1),
  ('Tareq', 'Awad',  'Account Exec',  '0599000003', 'tareq.awad1@bioline.ps',  'Ramallah Main St.', 'Male',   '2022-05-15', '1989-03-15', 2300.00, 1),
  ('Khaled', 'Sultan', 'Logistics Lead', '0599000004', 'khaled.sultan1@bioline.ps', 'Ramallah Log St.', 'Male',   '2021-02-01', '1984-08-10', 2000.00, 2),
  ('Sahar', 'Mousa',   'Driver',         '0599000005', 'sahar.mousa1@bioline.ps',   'Ramallah Log St.', 'Female', '2022-09-01', '1993-02-23', 1900.00, 2),
  ('Majed', 'Zein',    'Logistics Coord','0599000006', 'majed.zein1@bioline.ps',    'Ramallah Log St.', 'Male',   '2023-04-12', '1992-10-30', 2100.00, 2),
  ('Salma', 'Abu Salah', 'Technician',     '0599000007', 'salma.abu1@bioline.ps',   'Ramallah Tech St.','Female','2020-10-12','1988-01-05',2000.00, 3),
  ('Hatem', 'Jad',      'Lab Specialist',  '0599000008', 'hatem.jad1@bioline.ps',   'Ramallah Tech St.','Male',  '2022-06-19','1991-06-14',2450.00, 3),
  ('Rami', 'Qasim',     'IT Support',      '0599000009', 'rami.qasim1@bioline.ps',  'Ramallah Tech St.','Male',  '2021-03-22','1995-12-22',2050.00, 3);

INSERT INTO Employee (FirstName, LastName, Position, PhoneNumber, Email, Address, Gender, DateOfHire, DateOfBirth, Salary, DepartmentId) VALUES
  ('Dana', 'Odeh',   'Sales Manager', '0599000010', 'dana.odeh2@bioline.ps',  'Bethlehem Main St.', 'Female', '2020-03-01', '1991-07-19', 2000.00, 4),
  ('Ruba', 'Mansour','Sales Rep',     '0599000011', 'ruba.mansour2@bioline.ps','Bethlehem Main St.','Female', '2021-01-13', '1994-04-02', 2150.00, 4),
  ('Samir','Tawfiq', 'Account Exec',  '0599000012', 'samir.tawfiq2@bioline.ps','Bethlehem Main St.','Male',   '2022-05-15', '1987-02-10', 2400.00, 4),
  ('Yousef', 'Salim', 'Logistics Lead', '0599000013', 'yousef.salim2@bioline.ps', 'Bethlehem Log St.', 'Male',   '2021-02-01', '1988-12-25', 2050.00, 5),
  ('Waleed', 'Haddad','Driver',         '0599000014', 'waleed.haddad2@bioline.ps','Bethlehem Log St.','Male',   '2022-09-01', '1992-02-28', 1925.00, 5),
  ('Sabreen','Ali',   'Logistics Coord', '0599000015', 'sabreen.ali2@bioline.ps',  'Bethlehem Log St.','Female', '2023-04-12', '1994-09-11', 2150.00, 5),
  ('Ihab', 'Abu Odeh',   'Technician',     '0599000016', 'ihab.aboudeh2@bioline.ps', 'Bethlehem Tech St.','Male',  '2020-10-12','1989-09-08', 2650.00, 6),
  ('Firas','Qadri',      'Lab Specialist', '0599000017', 'firas.qadri2@bioline.ps',  'Bethlehem Tech St.','Male',  '2022-06-19','1992-03-16', 2500.00, 6),
  ('Samar','Sultan',     'IT Support',     '0599000018', 'samar.sultan2@bioline.ps', 'Bethlehem Tech St.','Female','2021-03-22','1996-10-29', 2100.00, 6);
INSERT INTO Employee (FirstName, LastName, Position, PhoneNumber, Email, Address, Gender, DateOfHire, DateOfBirth, Salary, DepartmentId) VALUES
  ('Mona', 'Hamdan', 'Sales Manager', '0599000019', 'mona.hamdan3@bioline.ps', 'Hebron Main St.', 'Female', '2020-03-01', '1998-06-15', 3150.00, 7),
  ('Yara', 'Darwish','Sales Rep',     '0599000020', 'yara.darwish3@bioline.ps','Hebron Main St.','Female', '2021-01-13', '1997-08-03', 2180.00, 7),
  ('Ahmad','Khattab','Account Exec',  '0599000021', 'ahmad.khattab3@bioline.ps','Hebron Main St.','Male',   '2022-05-15', '1986-11-24', 2320.00, 7),
  ('Leen', 'Qawasmeh', 'Logistics Lead', '0599000022', 'leen.qawasmeh3@bioline.ps', 'Hebron Log St.', 'Female', '2021-02-01', '1995-04-05', 2000.00, 8),
  ('Omar', 'Salam',     'Driver',         '0599000023', 'omar.salam3@bioline.ps',    'Hebron Log St.','Male',   '2022-09-01', '1993-09-17', 1980.00, 8),
  ('Rami', 'Najjar',    'Logistics Coord','0599000024', 'rami.najjar3@bioline.ps',   'Hebron Log St.','Male',   '2023-04-12', '1990-05-19', 2150.00, 8),
  ('Hatem', 'Awad',     'Technician',     '0599000025', 'hatem.awad3@bioline.ps',   'Hebron Tech St.','Male',  '2020-10-12','1992-08-03', 2300.00, 9),
  ('Dalia','Shaheen',   'Lab Specialist', '0599000026', 'dalia.shaheen3@bioline.ps','Hebron Tech St.','Female','2022-06-19','1995-03-22', 2480.00, 9),
  ('Ali',  'Khatib',    'IT Support',     '0599000027', 'ali.khatib3@bioline.ps',   'Hebron Tech St.','Male',  '2021-03-22','1997-10-01', 2080.00, 9);

INSERT INTO Employee (FirstName, LastName, Position, PhoneNumber, Email, Address, Gender, DateOfHire, DateOfBirth, Salary, DepartmentId) VALUES
('Sam', 'Mhmd', 'Logestic','0591231234','sam@bioline.ps','hebron','Male','2025-06-02','2000-09-09',1500,11);
INSERT INTO Product (ProductName, Category, CostPrice, SellingPrice, DiscountRate, QuantityInStock, ExpirationDate, StatusId, ReturnPolicy, CompanyId) VALUES
('Microscope A','Lab', 400,  600,  5,  4, '2028-12-31', 1, '30 Days', 1),
('Microscope B','Lab', 410,  630,  4,  28, '2028-11-30', 1, '30 Days', 1),
('Test Tube Set','Lab', 50,   80,  10, 200, '2025-06-25', 1, 'No Return', 1),
('Pipette','Lab', 70,   120, 5,  100, '2025-09-09', 1, '7 Days', 1),
('Beaker', 'Lab', 20,   40,  0,  150, '2026-12-22', 1, '7 Days', 1),
('Burette','Lab', 25,   45,  0,  100, '2026-01-01', 1, 'No Return', 1),
('Spectrophotometer','Equipment',0,1200,6,5, '2025-12-12', 1, '30 Days', 1),
('pH Meter','Equipment',120,180,2,10, '2027-01-01',  1, '14 Days', 1),
('Centrifuge Mini', 'Equipment',900,1300,3,4, '2029-07-22', 1, '60 Days', 1),
('Hotplate', 'Lab', 80,   120, 5,  40, '2028-12-11', 1, '7 Days', 1),
('Stirrer', 'Lab', 35,   60,  0,  60, '2026-01-01', 1, 'No Return', 1),
('Thermometer', 'Lab', 15,   25,  5,  80, '2027-08-11', 1, '7 Days', 1),
('Slides Pack','Lab', 30,   45,  15, 500, '2025-12-29', 1, 'No Return', 1),
('Gloves Box', 'Lab', 10,   18,  0,  400, '2027-05-09', 1, 'No Return', 1),
('Lab Coat','Lab', 25,   38,  0,  250, '2029-01-01', 1, 'No Return', 1);

INSERT INTO Product (ProductName, Category, CostPrice, SellingPrice, DiscountRate, QuantityInStock, ExpirationDate, StatusId, ReturnPolicy, CompanyId) VALUES
('Centrifuge','Equipment', 2000, 2700, 3,  5, '2029-05-01',1, '60 Days', 2),
('Chemical Kit A', 'Chemicals', 180,  260, 0,  5, '2027-03-20', 1, '7 Days', 2),
('Incubator','Equipment', 900,  1300,2,  8, '2029-01-01',1, '30 Days', 2),
('Slides Pack', 'Lab', 30,   45,  15, 500, '2025-12-12',1, 'No Return', 2),
('Gloves Box','Lab', 10,   18,  0,  400, '2026-05-22', 1, 'No Return', 2),
('Lab Coat','Lab',25,   38,  0,  250, '2026-02-11',1, 'No Return', 2),
('Beaker','Lab',20,   40,  0,  150, '2029-01-01', 1, '7 Days', 2),
('Spectrophotometer','Equipment',800,1200,6,5,'2026-05-15', 1, '30 Days', 2),
('pH Meter','Equipment',120,180,2,10,'2025-12-31', 1, '14 Days', 2),
('Hotplate','Lab',80,   120, 5,  0, '2026-02-02', 1, '7 Days', 2),
('Stirrer','Lab',35,   60,  0,  60, '2029-01-01',1, 'No Return', 2);


INSERT INTO Product (ProductName, Category, CostPrice, SellingPrice, DiscountRate, QuantityInStock, ExpirationDate, StatusId, ReturnPolicy, CompanyId) VALUES
('Incubator','Equipment', 900, 1300,2, 8, '2026-05-16',1, '30 Days', 3),
('Chemical Kit B', 'Chemicals', 185,  270, 1,40, '2027-04-15', 1, '7 Days', 3),
('Centrifuge Mini','Equipment', 950,  1350,2, 2, '2027-01-09', 1, '60 Days', 3),
('Spectrophotometer','Equipment',800,1200,6,5,'2026-12-12',1, '30 Days', 3),
('Test Tube Set',  'Lab', 50,80, 10, 200, '2025-09-09', 1, 'No Return', 3),
('Pipette','Lab', 70,120, 5,  100, '2028-01-01',1, '7 Days', 3),
('Beaker', 'Lab',20,40, 0,  150, '2029-05-12',1, '7 Days', 3),
('Stirrer', 'Lab',35,60, 0,  1,'2025-12-31',1, 'No Return', 3),
('Thermometer','Lab',15, 25,  8,  80, '2027-01-09', 1, '7 Days', 3),
('Microscope A','Lab',400, 600, 5, 0, '2028-12-31',1, '30 Days', 3);


INSERT INTO Customer (FirstName, LastName, ContactNumber, Email, ShippingAddress, CustomerTypeId, PaymentMethodId) VALUES
('Sami', 'Taha', '0569112233', 'sami.taha@sample.com', 'Ramallah, Main Road 12', 1, 1),
('Hanan', 'Samer', '0569003344', 'hanan.samer@sample.com', 'Hebron, Market Street 19', 2, 2),
('Khaled', 'Nasr', '0569887766', 'khaled.nasr@sample.com', 'Bethlehem, School Street 4', 1, 3),
('Rami', 'Matar', '0569112244', 'rami.matar@sample.com', 'Nablus, Old Town 13', 2, 1),
('Tala', 'Shami', '0569003355', 'tala.shami@sample.com', 'Jenin, Market 6', 1, 2),
('Dima', 'Awad', '0569776543', 'dima.awad@sample.com', 'Tulkarem, Al-Madina 33', 2, 3),
('Omar', 'Amin', '0569332211', 'omar.amin@sample.com', 'Qalqilia, Main Sq 5', 1, 1),
('Nader', 'Hasan', '0569771234', 'nader.hasan@sample.com', 'Ramallah, Garden 88', 2, 2),
('Lina', 'Arafat', '0569222333', 'lina.arafat@sample.com', 'Jericho, Bridge 22', 1, 3),
('Maha', 'Farid', '0569334455', 'maha.farid@sample.com', 'Bethlehem, Church St 1', 2, 1),
('Karam', 'Jouda', '0569004443', 'karam.jouda@sample.com', 'Hebron, Main St 9', 1, 2),
('Alaa', 'Sabri', '0569888888', 'alaa.sabri@sample.com', 'Salfit, Road 3', 2, 3),
('Eman', 'Bader', '0569666677', 'eman.bader@sample.com', 'Ramallah, Park 77', 1, 1),
('Hussein', 'Hamdi', '0569444466', 'hussein.hamdi@sample.com', 'Hebron, Elm St 5', 2, 2),
('Zein', 'Majed', '0569771111', 'zein.majed@sample.com', 'Tulkarem, Hill 11', 1, 3),
('Jamal', 'Dabbas', '0569112231', 'jamal.dabbas@sample.com', 'Jenin, North 12', 2, 1),
('Sally', 'Rashid', '0569223344', 'sally.rashid@sample.com', 'Nablus, West 8', 1, 2),
('Nisreen', 'Qasem', '0569778888', 'nisreen.qasem@sample.com', 'Qalqilia, East 4', 2, 3),
('Hossam', 'Tariq', '0569444422', 'hossam.tariq@sample.com', 'Jericho, Market 5', 1, 1),
('Nour', 'Qadri', '0569002221', 'nour.qadri@sample.com', 'Bethlehem, South 17', 2, 2);

INSERT INTO Supplier (SupplierCompany, ContactName, PhoneNumber, Email, Address, Website, SupplierTypeId) VALUES
('LabSupplies Ltd.','Majed Hasan', '022224000', 'majed@labsupplies.com', 'Ramallah',   'http://labsupplies.com', 1),
('RamBio Co.','Ali Nimer',   '022226000', 'ali@rambio.com',        'Ramallah',   'http://rambio.com', 1),
('Nablus Equipments', 'Nader Arafat','092228000', 'nader@nabluseq.com',    'Nablus',     'http://nabluseq.com', 1),
('AlQuds Scientific', 'Samah Deeb',  '022223000', 'samah@alqudsci.com',    'Jerusalem',  'http://alqudsci.com', 1),
('Bethlehem Chem', 'Rami Ziad',   '022225000', 'rami@bethchem.com',     'Bethlehem',  'http://bethchem.com', 1),
('Hebron BioSuppliers', 'Firas Saleh', '022229000', 'firas@hebronbio.com',   'Hebron',     'http://hebronbio.com', 1),
('GlobalBio',           'Layla Dabbas','022225555', 'layla@globalbio.com',   'Bethlehem',  'http://globalbio.com', 2),
('EuroMedLab',          'George K.',   '0033123456','george@euromedlab.eu',  'Paris',      'http://euromedlab.eu', 2),
('Sigma Internat.',     'Linda Shaw',  '0044222111','linda@sigma.com',       'London',     'http://sigma.com', 2),
('AsiaLab Import',      'Wei Zhang',   '0086133555','wei@asialab.com',       'Beijing',    'http://asialab.com', 2),
('BioAfrica',           'Thandiwe N.', '0027222444','thandiwe@bioafrica.com','Cape Town',  'http://bioafrica.com', 2),
('AmeriLab',            'John Smith',  '0012023333','john@amerilab.com',     'New York',   'http://amerilab.com', 2);


INSERT INTO SupplierProduct (SupplierId, ProductId) VALUES
(1,  1), (1,  2), (1,  3);
INSERT INTO SupplierProduct (SupplierId, ProductId) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (1, 13), (2, 14), (3, 15), (4, 27), (5, 28), (6, 29), (7, 30), (8, 31), (9, 32), (10, 33), (11, 34), (12, 35),
(1, 36), (2, 37), (3, 38), (4, 39), (5, 40), (6, 41), (7, 42), (8, 43), (9, 44), (10, 45), (11, 46), (12, 47);



INSERT INTO Purchase (PurchaseDate, SupplierId, CompanyId, TotalCost) VALUES
('2024-05-15 09:30:00', 1, 1, 1400.00),
('2024-06-02 15:00:00', 7, 2, 2600.00),
('2024-06-03 10:00:00', 8, 3, 1800.00),
('2024-06-03 13:00:00', 2, 1, 900.00),
('2024-06-04 10:00:00', 11,2, 1500.00),
('2024-06-04 14:00:00', 3, 3, 1050.00),
('2024-06-04 17:00:00', 9, 1, 1350.00),
('2024-06-05 09:00:00', 4, 2, 1620.00),
('2024-06-05 10:30:00', 12,3, 1420.00);

INSERT INTO Purchase (PurchaseDate, SupplierId, CompanyId, TotalCost) VALUES
('2024-06-01 09:00:00', 1, 1, 800.00),
('2024-06-01 10:00:00', 2, 2, 900.00),
('2024-06-01 11:00:00', 3, 3, 950.00),
('2024-06-01 12:00:00', 4, 1, 1100.00),
('2024-06-01 13:00:00', 5, 2, 720.00),
('2024-06-01 14:00:00', 6, 3, 670.00),
('2024-06-02 09:00:00', 7, 1, 1200.00),
('2024-06-02 10:00:00', 8, 2, 1050.00),
('2024-06-02 11:00:00', 9, 3, 860.00),
('2024-06-02 12:00:00', 10, 1, 760.00),
('2024-06-02 13:00:00', 11, 2, 980.00),
('2024-06-02 14:00:00', 12, 3, 920.00);


INSERT INTO PurchaseDetail (PurchaseId, ProductId, Quantity, CostPerUnit) VALUES
(1, 1, 3, 400.00), (1, 2, 2, 410.00),
(2, 3, 6, 50.00), (2, 4, 1, 70.00),
(3, 5, 8, 20.00), (3, 6, 5, 25.00),
(4, 7, 1, 0.00), (4, 8, 4, 120.00),
(5, 9, 2, 900.00), (5, 10, 1, 80.00),
(6, 11, 5, 35.00), (6, 12, 3, 15.00),
(7, 13, 1, 30.00), (7, 14, 3, 10.00),
(8, 15, 2, 25.00), (8, 27, 4, 110.00),
(9, 28, 5, 180.00), (9, 29, 1, 900.00),
(10, 30, 2, 950.00), (10, 31, 2, 800.00),
(11, 32, 1, 50.00), (11, 33, 2, 70.00),
(12, 34, 4, 20.00), (12, 35, 3, 25.00);


INSERT INTO Sale (SaleDate, CustomerId, CompanyId, TotalRevenue) VALUES
('2024-06-05 09:05:00', 1,  1, 1860.00), 
('2024-06-05 10:00:00', 2,  2, 280.00),  
('2024-06-05 10:30:00', 3,  3, 205.00),  
('2024-06-05 11:00:00', 4,  1, 1560.00), 
('2024-06-05 11:15:00', 5,  2, 1420.00), 
('2024-06-05 12:00:00', 6,  3, 230.00), 
('2024-06-05 12:15:00', 7,  1, 81.00),   
('2024-06-05 13:00:00', 8,  2, 1426.00), 
('2024-06-05 13:45:00', 9,  3, 3220.00), 
('2024-06-05 14:10:00', 10, 1, 3750.00), 
('2024-06-05 15:20:00', 11, 2, 173.00),  
('2024-06-05 16:30:00', 12, 3, 114.00);  


INSERT INTO SaleDetail (SaleId, ProductId, Quantity, SellingPrice) VALUES
(1, 1, 1, 600.00), (1, 2, 2, 630.00),
(2, 3, 2, 80.00), (2, 4, 1, 120.00),
(3, 5, 4, 40.00), (3, 6, 1, 45.00),
(4, 7, 1, 1200.00), (4, 8, 2, 180.00),
(5, 9, 1, 1300.00), (5, 10, 1, 120.00),
(6, 11, 3, 60.00), (6, 12, 2, 25.00),
(7, 13, 1, 45.00), (7, 14, 2, 18.00),
(8, 15, 2, 38.00), (8, 27, 1, 1350.00),
(9, 28, 2, 260.00), (9, 29, 2, 1350.00),
(10, 30, 1, 1350.00), (10, 31, 2, 1200.00),
(11, 32, 3, 45.00), (11, 33, 1, 38.00),
(12, 34, 1, 38.00), (12, 35, 2, 38.00);

