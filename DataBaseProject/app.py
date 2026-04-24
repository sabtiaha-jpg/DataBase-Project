from datetime import date, timedelta 
from flask import Flask, render_template, request, redirect, url_for
from db_connection import DatabaseConnection

app = Flask(__name__)

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '2002',
    'database': 'BioLineCompany'
}

db_instance = DatabaseConnection(**DB_CONFIG)
connection = db_instance.get_connection()

@app.route("/")
def index():
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Company")
        companies = cursor.fetchall()
        cursor.close()
        return render_template("index.html", companies=companies)
    return "Database connection failed."

@app.route("/add_company", methods=["GET", "POST"])
def add_company():
    if request.method == "POST":
        name = request.form['name']
        ceo = request.form['ceo']
        founded_year = request.form['founded_year']
        city = request.form['city']
        address = request.form['address']
        website = request.form['website']

        if connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO Company (CompanyName, CEO, FoundedYear, City, Address, Website)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (name, ceo, founded_year, city, address, website)
            )
            connection.commit()
            cursor.close()

        return redirect(url_for("index"))

    return render_template("add_company.html")


@app.route("/edit_company", methods=["POST"])
def edit_company():
    company_id = request.form.get('company_id')
    company_name = request.form.get('company_name')
    ceo = request.form.get('ceo')
    city = request.form.get('city')
    address = request.form.get('address')
    founded_year = request.form.get('founded_year')
    website = request.form.get('website')

    if not all([company_id, company_name, ceo, city, address, founded_year, website]):
        return "All fields are required.", 400

    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE Company
                SET CompanyName = %s,
                    CEO = %s,
                    City = %s,
                    Address = %s,
                    FoundedYear = %s,
                    Website = %s
                WHERE CompanyId = %s
            """
            cursor.execute(query, (company_name, ceo, city, address, founded_year, website, company_id))
            connection.commit()
            cursor.close()
            return redirect(url_for("index"))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500


@app.route("/delete_company/<int:company_id>")
def delete_company(company_id):
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Company WHERE CompanyId = %s", (company_id,))
        connection.commit()
        cursor.close()
    return redirect(url_for("index"))

@app.route("/departments/<int:company_id>")
def departments(company_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Company WHERE CompanyId = %s", (company_id,))
    company = cursor.fetchone()

    if not company:
        return "Company not found", 404

    cursor.execute("SELECT * FROM Department WHERE CompanyId = %s", (company_id,))
    departments = cursor.fetchall()
    cursor.close()

    return render_template("departments.html", company=company, departments=departments)

@app.route("/delete_department/<int:department_id>")
def delete_department(department_id):
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Department WHERE DepartmentId = %s", (department_id,))
        connection.commit()
        cursor.close()
    return redirect(url_for("departments"))

@app.route("/employees/<int:department_id>")
def employees(department_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Department WHERE DepartmentId = %s", (department_id,))
    department = cursor.fetchone()

    if not department:
        return "Department not found", 404

    cursor.execute("SELECT * FROM Employee WHERE DepartmentId = %s", (department_id,))
    employees = cursor.fetchall()
    cursor.close()

    return render_template("employees.html", department=department, employees=employees)

@app.route("/customers")
def customers():
    if connection:
        cursor = connection.cursor(dictionary=True)

        # Fetch customers
        cursor.execute("SELECT * FROM Customer")
        customers = cursor.fetchall()

        # Fetch dropdown options
        cursor.execute("SELECT CustomerTypeId, TypeName FROM CustomerType")
        customer_types = cursor.fetchall()

        cursor.execute("SELECT MethodId, MethodName FROM PaymentMethod")
        payment_methods = cursor.fetchall()

        cursor.close()

        return render_template("customers.html", customers=customers,
                               customer_types=customer_types,
                               payment_methods=payment_methods)

    return "Database connection failed.", 500


@app.route("/add_customer", methods=["POST"])
def add_customer():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        customer_type = request.form['customer_type']
        payment_method = request.form['payment_method']

        if connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO Customer 
                (FirstName, LastName, ContactNumber, Email, ShippingAddress, CustomerTypeId, PaymentMethodId) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (first_name, last_name, contact, email, address, customer_type, payment_method)
            )
            connection.commit()
            cursor.close()
        return redirect(url_for("customers"))

@app.route("/edit_customer", methods=["POST"])
def edit_customer():
    customer_id = request.form['customer_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    contact = request.form['contact']
    email = request.form['email']
    address = request.form['address']
    customer_type = request.form['customer_type']
    payment_method = request.form['payment_method']

    if connection:
        try:
            cursor = connection.cursor()
            update_query = """
                UPDATE Customer
                SET 
                FirstName = %s, 
                LastName = %s, 
                ContactNumber = %s, 
                Email = %s, 
                ShippingAddress = %s,
                CustomerTypeId = %s,
                PaymentMethodId = %s
                WHERE CustomerId = %s
            """
            cursor.execute(update_query, (first_name, last_name, contact, email, address, customer_type, payment_method, customer_id))
            connection.commit()
            cursor.close()
            return redirect(url_for("customers"))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/delete_customer/<int:customer_id>")
def delete_customer(customer_id):
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Customer WHERE CustomerId = %s", (customer_id,))
        connection.commit()
        cursor.close()
    return redirect(url_for("customers"))

@app.route("/suppliers")
def suppliers():
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # Get supplier list
        cursor.execute("""
            SELECT s.*, st.TypeName AS SupplierTypeName
            FROM Supplier s
            JOIN SupplierType st ON s.SupplierTypeId = st.SupplierTypeId
        """)

        suppliers = cursor.fetchall()

        # Get supplier types
        cursor.execute("SELECT SupplierTypeId, TypeName FROM SupplierType")
        supplier_types = cursor.fetchall()

        cursor.close()
        return render_template("suppliers.html", suppliers=suppliers, supplier_types=supplier_types)

    return "Database connection failed."


@app.route("/add_supplier", methods=["GET", "POST"])
def add_supplier():
    if request.method == "POST":
        # handle form submission
        company = request.form["supplier_company"]
        contact = request.form["contact_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]
        website = request.form["website"]
        supplier_type = request.form["supplier_type"]

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Supplier (SupplierCompany, ContactName, PhoneNumber, Email, Address, Website, SupplierTypeId)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (company, contact, phone, email, address, website, supplier_type))
        connection.commit()
        cursor.close()
        return redirect(url_for("suppliers"))

    # GET method - load form with supplier types
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT SupplierTypeId, TypeName FROM SupplierType")
    supplier_types = cursor.fetchall()
    cursor.close()
    return render_template("add_supplier.html", supplier_types=supplier_types)


@app.route("/edit_supplier", methods=["POST"])
def edit_supplier():
    supplier_id = request.form.get('supplier_id')
    company = request.form.get('company')
    contact_name = request.form.get('contact_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    website = request.form.get('website')
    supplier_type = request.form.get('supplier_type')

    if not (supplier_id and company and contact_name and phone and email and address and website and supplier_type):
        return "All fields are required.", 400

    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Supplier WHERE SupplierId = %s", (supplier_id,))
            supplier = cursor.fetchone()

            if not supplier:
                cursor.close()
                return "Supplier not found.", 404

            update_query = """
                UPDATE Supplier
                SET SupplierCompany = %s, ContactName = %s, PhoneNumber = %s, Email = %s, 
                    Address = %s, Website = %s, SupplierTypeId = %s
                WHERE SupplierId = %s
            """
            cursor.execute(update_query, (company, contact_name, phone, email, address, website, supplier_type, supplier_id))
            connection.commit()
            cursor.close()
        except Exception as e:
            return f"An error occurred while updating the supplier: {e}", 500
    else:
        return "Database connection failed.", 500

    return redirect(url_for("suppliers"))

@app.route("/delete_supplier/<int:supplier_id>")
def delete_supplier(supplier_id):
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Supplier WHERE SupplierId = %s", (supplier_id,))
        connection.commit()
        cursor.close()
    return redirect(url_for("suppliers"))

@app.route("/branch/<int:company_id>")
def branch(company_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Company WHERE CompanyId = %s", (company_id,))
    branch = cursor.fetchone()
    cursor.close()

    if not branch:
        return "Branch not found.", 404

    return render_template("branch.html", branch=branch)

@app.route("/add_department/<int:company_id>", methods=["POST"])
def add_department(company_id):
    department_name = request.form.get("department_name")

    if not department_name:
        return "Invalid data provided.", 400

    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO Department (DepartmentName, EmployeeCount, CompanyId)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (department_name, 0, company_id))
            connection.commit()
            cursor.close()
            return redirect(url_for("departments", company_id=company_id))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/delete_department/<int:department_id>/<int:company_id>")
def delete_department_with_redirect(department_id, company_id):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Department WHERE DepartmentId = %s", (department_id,))
            connection.commit()
            cursor.close()
            return redirect(url_for("departments", company_id=company_id))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500


@app.route("/add_employee/<int:department_id>", methods=["POST"])
def add_employee(department_id):
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    address = request.form.get("address")
    gender = request.form.get("gender")
    date_of_hire = request.form.get("date_of_hire")
    date_of_birth = request.form.get("date_of_birth")
    salary = request.form.get("salary")
    position = request.form.get("position")
    work_hours = request.form.get("work_hours")
    branch_id = request.form.get("branch_id")
    manager_id = request.form.get("manager_id")
    manager_id = int(manager_id) if manager_id else None


    if not all([first_name, last_name, email, phone_number, address, gender,
                date_of_hire, date_of_birth, salary, position, work_hours]):
        return "Invalid data provided.", 400

    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO Employee (
                    FirstName, LastName, Email, PhoneNumber, Address,
                    Gender, DateOfHire, DateOfBirth, Salary,
                    DepartmentId, Position, WorkHours)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                first_name, last_name, email, phone_number, address,
                gender, date_of_hire, date_of_birth, salary,
                department_id, position, work_hours))
            connection.commit()
            cursor.close()
            return redirect(url_for("employees", department_id=department_id))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500


@app.route("/delete_employee/<int:employee_id>/<int:department_id>")
def delete_employee(employee_id, department_id):
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM Employee WHERE EmployeeId = %s"
            cursor.execute(query, (employee_id,))
            connection.commit()
            cursor.close()
            return redirect(url_for("employees", department_id=department_id))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/edit_employee", methods=["POST"])
def edit_employee():
    employee_id = request.form.get("employee_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    address = request.form.get("address")
    gender = request.form.get("gender")
    date_of_hire = request.form.get("date_of_hire")
    date_of_birth = request.form.get("date_of_birth")
    salary = request.form.get("salary")
    position = request.form.get("position")
    work_hours = request.form.get("work_hours")
    department_id = request.form.get("department_id")

    if not all([employee_id, first_name, last_name, email, phone_number, address, gender,
                date_of_hire, date_of_birth, salary, position, work_hours, department_id]):
        return "Invalid data provided.", 400

    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE Employee
                SET FirstName = %s, LastName = %s, Email = %s, PhoneNumber = %s, Address = %s, 
                    Gender = %s, DateOfHire = %s, DateOfBirth = %s, Salary = %s,
                    Position = %s, WorkHours = %s, DepartmentId = %s 
                WHERE EmployeeId = %s
            """
            cursor.execute(query, (
                first_name, last_name, email, phone_number, address,
                gender, date_of_hire, date_of_birth, salary,
                position, work_hours, department_id,employee_id))
            connection.commit()
            cursor.close()
            return redirect(request.referrer)
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500


@app.route("/products/<int:company_id>")
def products(company_id):
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Company WHERE CompanyId = %s", (company_id,))
            branch = cursor.fetchone()

            if not branch:
                return "Branch not found", 404

            cursor.execute("SELECT * FROM Product WHERE CompanyId = %s", (company_id,))
            products = cursor.fetchall()
            cursor.close()

            return render_template("products.html", branch=branch, products=products)
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/add_product/<int:company_id>", methods=["POST"])
def add_product(company_id):
    product_name = request.form.get("product_name")
    category = request.form.get("category")
    cost_price = request.form.get("cost_price")
    selling_price = request.form.get("selling_price")
    discount_rate = request.form.get("discount_rate") or 0
    quantity_in_stock = request.form.get("quantity_in_stock") or 0
    expiration_date = request.form.get("expiration_date")
    return_policy = request.form.get("return_policy") or "No Return"

    # Use default StatusId = 1 for 'Available'
    status_id = 1

    if not (product_name and category and cost_price and selling_price):
        return "Invalid data provided.", 400

    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO Product (
                    ProductName, Category, CostPrice, SellingPrice, DiscountRate,
                    QuantityInStock, ExpirationDate, StatusId, DateAdded, ReturnPolicy, CompanyId
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s)
            """
            cursor.execute(query, (
                product_name, category, cost_price, selling_price, discount_rate,
                quantity_in_stock, expiration_date, status_id, return_policy, company_id
            ))
            connection.commit()
            cursor.close()
            return redirect(url_for("products", company_id=company_id))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500


@app.route("/edit_product", methods=["POST"])
def edit_product():
    product_id = request.form.get("product_id")
    product_name = request.form.get("product_name")
    category = request.form.get("category")
    cost_price = request.form.get("cost_price")
    selling_price = request.form.get("selling_price")
    discount_rate = request.form.get("discount_rate")
    quantity_in_stock = request.form.get("quantity_in_stock")
    expiration_date = request.form.get("expiration_date")
    return_policy = request.form.get("return_policy")
    company_id = request.form.get("company_id")

    if not (product_id and product_name and category and cost_price and selling_price and company_id):
        return "Invalid data provided.", 400

    # Safely convert numeric values
    try:
        discount_rate = float(discount_rate or 0)
        quantity_in_stock = int(quantity_in_stock or 0)
        cost_price = float(cost_price)
        selling_price = float(selling_price)
    except ValueError:
        return "Invalid numeric values.", 400

    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE Product
                SET ProductName = %s, Category = %s, CostPrice = %s, SellingPrice = %s, DiscountRate = %s,
                    QuantityInStock = %s, ExpirationDate = %s, ReturnPolicy = %s
                WHERE ProductId = %s
            """
            cursor.execute(query, (
                product_name, category, cost_price, selling_price, discount_rate,
                quantity_in_stock, expiration_date, return_policy or "No Return", product_id
            ))
            connection.commit()
            cursor.close()
            return redirect(url_for("products", company_id=company_id))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/delete_product/<int:product_id>/<int:company_id>")
def delete_product(product_id, company_id):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Product WHERE ProductId = %s", (product_id,))
            connection.commit()
            cursor.close()
            return redirect(url_for("products", company_id=company_id))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500



@app.route("/purchase/<int:company_id>")
def purchase(company_id):
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Company WHERE CompanyId = %s", (company_id,))
            branch = cursor.fetchone()

            if not branch:
                return "Branch not found", 404

            cursor.execute("""
                SELECT Purchase.PurchaseId, Purchase.PurchaseDate, Purchase.TotalCost, Supplier.SupplierCompany
                FROM Purchase
                JOIN Supplier ON Purchase.SupplierId = Supplier.SupplierId
                WHERE Purchase.CompanyId = %s
            """, (company_id,))
            purchases = cursor.fetchall()
            cursor.close()

            return render_template("purchases.html", branch=branch, purchases=purchases)
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/add_purchase/<int:company_id>", methods=["GET", "POST"])
def add_purchase(company_id):
    if request.method == "GET":
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Company WHERE CompanyId = %s", (company_id,))
                branch = cursor.fetchone()

                if not branch:
                    return "Branch not found", 404

                cursor.execute("SELECT SupplierId, SupplierCompany FROM Supplier")
                suppliers = cursor.fetchall()

                cursor.execute("SELECT ProductId, ProductName, CostPrice FROM Product WHERE CompanyId = %s", (company_id,))
                products = cursor.fetchall()
                cursor.close()

                return render_template("add_purchase.html", branch=branch, suppliers=suppliers, products=products)
            except Exception as e:
                return f"An error occurred: {e}", 500
        else:
            return "Database connection failed.", 500

    elif request.method == "POST":
        supplier_id = request.form.get("supplier_id")
        total_cost = 0
        product_details = request.form.getlist("product_id")
        quantities = request.form.getlist("quantity")
        costs = request.form.getlist("cost")

        if not supplier_id or not product_details or not quantities or not costs:
            return "Invalid data provided.", 400

        if connection:
            try:
                cursor = connection.cursor()

                purchase_query = """
                    INSERT INTO Purchase (PurchaseDate, SupplierId, CompanyId, TotalCost)
                    VALUES (NOW(), %s, %s, %s)
                """
                cursor.execute(purchase_query, (supplier_id, company_id, total_cost))
                purchase_id = cursor.lastrowid

                for product_id, quantity, cost in zip(product_details, quantities, costs):
                    total_cost += int(quantity) * float(cost)
                    detail_query = """
                        INSERT INTO PurchaseDetail (PurchaseId, ProductId, Quantity, CostPerUnit)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(detail_query, (purchase_id, product_id, quantity, cost))

                    update_product_query = """
                        UPDATE Product SET QuantityInStock = QuantityInStock + %s WHERE ProductId = %s
                    """
                    cursor.execute(update_product_query, (quantity, product_id))

                cursor.execute("UPDATE Purchase SET TotalCost = %s WHERE PurchaseId = %s", (total_cost, purchase_id))

                connection.commit()
                cursor.close()
                return redirect(url_for("purchase", company_id=company_id))
            except Exception as e:
                return f"An error occurred: {e}", 500
        else:
            return "Database connection failed.", 500

@app.route("/purchase_details/<int:purchase_id>")
def purchase_details(purchase_id):
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            purchase_query = """
                SELECT p.PurchaseId, p.PurchaseDate, p.TotalCost, p.CompanyId, s.SupplierCompany
                FROM Purchase p
                JOIN Supplier s ON p.SupplierId = s.SupplierId
                WHERE p.PurchaseId = %s
            """
            cursor.execute(purchase_query, (purchase_id,))
            purchase = cursor.fetchone()

            product_query = """
                SELECT pd.Quantity, pd.CostPerUnit, pr.ProductName, (pd.Quantity * pd.CostPerUnit) AS TotalCost
                FROM PurchaseDetail pd
                JOIN Product pr ON pd.ProductId = pr.ProductId
                WHERE pd.PurchaseId = %s
            """
            cursor.execute(product_query, (purchase_id,))
            products = cursor.fetchall()
            cursor.close()

            return render_template(
                "purchase_details.html", purchase=purchase, products=products
            )
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/delete_purchase/<int:purchase_id>", methods=["GET", "POST"])
def delete_purchase(purchase_id):
    if connection:
        try:
            cursor = connection.cursor()
            delete_details_query = "DELETE FROM PurchaseDetail WHERE PurchaseId = %s"
            cursor.execute(delete_details_query, (purchase_id,))

            delete_purchase_query = "DELETE FROM Purchase WHERE PurchaseId = %s"
            cursor.execute(delete_purchase_query, (purchase_id,))
            connection.commit()
            cursor.close()
            return redirect(request.referrer)
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/sales/<int:branch_id>")
def sales(branch_id):
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT s.SaleId, s.TotalRevenue, s.SaleDate, c.FirstName AS CustomerFirstName, c.LastName AS CustomerLastName
                FROM Sale s
                INNER JOIN Customer c ON s.CustomerId = c.CustomerId
                WHERE s.CompanyId = %s
            """
            cursor.execute(query, (branch_id,))
            sales = cursor.fetchall()
            cursor.close()

            cursor = connection.cursor(dictionary=True)
            branch_query = "SELECT * FROM Company WHERE CompanyId = %s"
            cursor.execute(branch_query, (branch_id,))
            branch = cursor.fetchone()
            cursor.close()

            return render_template("sales.html", sales=sales, branch=branch)
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/delete_sale/<int:sale_id>", methods=["GET"])
def delete_sale(sale_id):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM SaleDetail WHERE SaleId = %s", (sale_id,))
            cursor.execute("DELETE FROM Sale WHERE SaleId = %s", (sale_id,))
            connection.commit()
            cursor.close()
            return redirect(request.referrer)
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/add_sale/<int:branch_id>")
def get_add_sale(branch_id):
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            branch_query = "SELECT * FROM Company WHERE CompanyId = %s"
            cursor.execute(branch_query, (branch_id,))
            branch = cursor.fetchone()

            customers_query = """
                SELECT CustomerId, FirstName, LastName
                FROM Customer
            """
            cursor.execute(customers_query)
            customers = cursor.fetchall()

            products_query = """
                SELECT ProductId, ProductName, SellingPrice, QuantityInStock
                FROM Product
                WHERE CompanyId = %s
            """
            cursor.execute(products_query, (branch_id,))
            products = cursor.fetchall()
            cursor.close()

            return render_template(
                "add_sale.html", 
                branch=branch, 
                customers=customers, 
                products=products
            )
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500

@app.route("/add_sale/<int:branch_id>", methods=["POST"])
def add_sale(branch_id):
    customer_id = request.form.get("customer_id")
    products = request.form.getlist("product_id")
    quantities = request.form.getlist("quantity")
    prices = request.form.getlist("price")
    total_costs = request.form.getlist("total_cost")
    error_message = None

    if not customer_id or not products or not quantities or not prices:
        return "Invalid data provided.", 400

    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            # 1. Check that each quantity is available in stock
            for product_id, quantity in zip(products, quantities):
                cursor.execute("SELECT QuantityInStock, ProductName FROM Product WHERE ProductId = %s", (product_id,))
                result = cursor.fetchone()
                if not result:
                    error_message = "Product not found."
                    break
                if int(quantity) > int(result["QuantityInStock"]):
                    error_message = f"Not enough stock for '{result['ProductName']}'. Only {result['QuantityInStock']} left."
                    break

            if error_message:
                # Get form data again for the page
                branch_query = "SELECT * FROM Company WHERE CompanyId = %s"
                cursor.execute(branch_query, (branch_id,))
                branch = cursor.fetchone()

                customers_query = "SELECT CustomerId, FirstName, LastName FROM Customer"
                cursor.execute(customers_query)
                customers = cursor.fetchall()

                products_query = """
                    SELECT ProductId, ProductName, SellingPrice, QuantityInStock
                    FROM Product
                    WHERE CompanyId = %s
                """
                cursor.execute(products_query, (branch_id,))
                products_list = cursor.fetchall()
                cursor.close()
                return render_template(
                    "add_sale.html",
                    branch=branch,
                    customers=customers,
                    products=products_list,
                    error_message=error_message
                )

            # 2. Proceed with sale insert as before
            cursor = connection.cursor()
            total_revenue = sum(float(tc) for tc in total_costs)
            sale_query = """
                INSERT INTO Sale (CustomerId, CompanyId, TotalRevenue)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sale_query, (customer_id, branch_id, total_revenue))
            sale_id = cursor.lastrowid

            for product_id, quantity, price in zip(products, quantities, prices):
                sale_detail_query = """
                    INSERT INTO SaleDetail (SaleId, ProductId, Quantity, SellingPrice)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sale_detail_query, (sale_id, product_id, quantity, price))

                update_stock_query = """
                    UPDATE Product
                    SET QuantityInStock = QuantityInStock - %s
                    WHERE ProductId = %s
                """
                cursor.execute(update_stock_query, (quantity, product_id))

            connection.commit()
            cursor.close()
            return redirect(url_for("sales", branch_id=branch_id))
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500


@app.route("/sale_details/<int:sale_id>")
def sale_details(sale_id):
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            sale_query = """
                SELECT s.SaleId, s.SaleDate, s.TotalRevenue, s.CompanyId, c.FirstName AS CustomerFirstName, c.LastName AS CustomerLastName
                FROM Sale s
                JOIN Customer c ON s.CustomerId = c.CustomerId
                WHERE s.SaleId = %s
            """
            cursor.execute(sale_query, (sale_id,))
            sale = cursor.fetchone()

            products_query = """
                SELECT p.ProductName, sd.Quantity, sd.SellingPrice, (sd.Quantity * sd.SellingPrice) AS TotalCost
                FROM SaleDetail sd
                JOIN Product p ON sd.ProductId = p.ProductId
                WHERE sd.SaleId = %s
            """
            cursor.execute(products_query, (sale_id,))
            products = cursor.fetchall()

            cursor.close()

            return render_template("sale_details.html", sale=sale, products=products)
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Database connection failed.", 500



@app.route('/reporting', methods=['GET'])
def reporting():
    cursor = connection.cursor(dictionary=True)

    # Date filter (optional)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    date_filter = ""
    date_values = ()
    if start_date and end_date:
        date_filter = "WHERE s.SaleDate BETWEEN %s AND %s"
        date_values = (start_date, end_date)

    # Employees per company and salary
    cursor.execute("""
        SELECT c.CompanyName AS company_name,
            COUNT(e.EmployeeId) AS total_employees,
            ROUND(SUM(e.Salary),2) AS total_salaries
        FROM Employee e
        JOIN Department d ON e.DepartmentId = d.DepartmentId
        JOIN Company c ON d.CompanyId = c.CompanyId
        WHERE e.IsActive = 1
        GROUP BY c.CompanyId, c.CompanyName
    """)
    employees_report = cursor.fetchall()


    # Top-selling products
    cursor.execute("""
        SELECT p.ProductName AS product_name,
               SUM(sd.Quantity) AS total_quantity,
               ROUND(SUM(sd.Quantity * sd.SellingPrice), 2) AS total_revenue
        FROM SaleDetail sd
        JOIN Product p ON sd.ProductId = p.ProductId
        GROUP BY p.ProductId, p.ProductName
        ORDER BY total_quantity DESC
        LIMIT 5
    """)
    top_products = cursor.fetchall()

    # Employees per department (with company) and salary
    cursor.execute("""
        SELECT c.CompanyName AS company_name,
            d.DepartmentName AS department_name,
            COUNT(e.EmployeeId) AS total_employees,
            ROUND(SUM(e.Salary),2) AS total_salaries
        FROM Employee e
        JOIN Department d ON e.DepartmentId = d.DepartmentId
        JOIN Company c ON d.CompanyId = c.CompanyId
        WHERE e.IsActive = 1
        GROUP BY c.CompanyId, c.CompanyName, d.DepartmentId, d.DepartmentName
        ORDER BY c.CompanyName, d.DepartmentName
    """)
    employees_report = cursor.fetchall()

    cursor.execute("""
        SELECT e.EmployeeId,
            CONCAT(e.FirstName, ' ', e.LastName) AS EmployeeName,
            e.Position,
            c.CompanyName,
            e.Email,
            e.PhoneNumber
        FROM Employee e
        JOIN Department d ON e.DepartmentId = d.DepartmentId
        JOIN Company c ON d.CompanyId = c.CompanyId
        WHERE e.IsActive = 1
    """)
    employees_detailed = cursor.fetchall()


    # Recent hires
    cursor.execute("""
        SELECT EmployeeId,
               CONCAT(FirstName,' ',LastName) AS Name,
               DateOfHire
        FROM Employee
        WHERE DateOfHire >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        ORDER BY DateOfHire DESC
    """)
    recent_hires = cursor.fetchall()


    # Company Inventory Table
    cursor.execute("""
        SELECT c.CompanyName, p.ProductName, p.QuantityInStock AS Quantity
        FROM Product p
        JOIN Company c ON p.CompanyId = c.CompanyId
        ORDER BY c.CompanyName, p.ProductName
    """)
    company_inventory = cursor.fetchall()

    cursor.execute("""
        SELECT c.CompanyName, ROUND(SUM(p.QuantityInStock * p.CostPrice), 2) AS InventoryValue
        FROM Product p
        JOIN Company c ON p.CompanyId = c.CompanyId
        GROUP BY c.CompanyId
        ORDER BY c.CompanyName
    """)
    company_inventory_value = cursor.fetchall()


    # Expiring products
    cursor.execute("""
        SELECT ProductId, ProductName, ExpirationDate
        FROM Product
        WHERE ExpirationDate BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
          AND IsActive = 1
    """)
    expiring_products = cursor.fetchall()

    # Out of stock
    cursor.execute("""
        SELECT ProductId, ProductName
        FROM Product
        WHERE QuantityInStock = 0 AND IsActive = 1
    """)
    out_of_stock = cursor.fetchall()

    # Products by category
    cursor.execute("""
        SELECT Category,
               COUNT(ProductId) AS NumProducts,
               ROUND(AVG(SellingPrice),2) AS AvgPrice
        FROM Product
        WHERE IsActive = 1
        GROUP BY Category
    """)
    products_by_category = cursor.fetchall()

    # Sales by month
    cursor.execute("""
        SELECT DATE_FORMAT(SaleDate, '%Y-%m') AS SaleMonth,
               ROUND(SUM(TotalRevenue),2) AS MonthlyRevenue
        FROM Sale
        GROUP BY SaleMonth
        ORDER BY SaleMonth DESC
    """)
    sales_by_month = cursor.fetchall()

    # Revenue by product
    cursor.execute("""
        SELECT p.ProductName,
               ROUND(SUM(sd.Quantity * sd.SellingPrice),2) AS Revenue
        FROM SaleDetail sd
        JOIN Product p ON sd.ProductId = p.ProductId
        GROUP BY p.ProductId
        ORDER BY Revenue DESC
    """)
    revenue_by_product = cursor.fetchall()

    # Recent orders
    cursor.execute("""
        SELECT CONCAT(c.FirstName,' ',c.LastName) AS CustomerName,
               s.SaleId, s.SaleDate, s.TotalRevenue
        FROM Sale s
        JOIN Customer c ON s.CustomerId = c.CustomerId
        ORDER BY s.SaleDate DESC
        LIMIT 10
    """)
    recent_orders = cursor.fetchall()

    # Customer spending
    cursor.execute("""
        SELECT CONCAT(c.FirstName,' ',c.LastName) AS CustomerName,
               COUNT(s.SaleId) AS NumOrders,
               ROUND(SUM(s.TotalRevenue),2) AS TotalSpent
        FROM Customer c
        LEFT JOIN Sale s ON c.CustomerId = s.CustomerId
        WHERE c.IsActive = 1
        GROUP BY c.CustomerId
        ORDER BY TotalSpent DESC
    """)
    customer_spending = cursor.fetchall()

    # Supplier products
    cursor.execute("""
        SELECT s.SupplierCompany, COUNT(sp.ProductId) AS ProductCount
        FROM Supplier s
        LEFT JOIN SupplierProduct sp ON s.SupplierId = sp.SupplierId
        WHERE s.IsActive = 1
        GROUP BY s.SupplierId
        ORDER BY ProductCount DESC
    """)
    supplier_products = cursor.fetchall()

    cursor.execute(f"""
        SELECT c.CompanyName AS company_name,
            ROUND(SUM(s.TotalRevenue),2) AS total_revenue,
            COUNT(s.SaleId) AS sales_count
        FROM Sale s
        JOIN Company c ON s.CompanyId = c.CompanyId
        {"WHERE s.SaleDate BETWEEN %s AND %s" if start_date and end_date else ""}
        GROUP BY c.CompanyId, c.CompanyName
    """, (start_date, end_date) if start_date and end_date else ())
    revenues = cursor.fetchall()
    
    # Supplier purchases
    cursor.execute("""
        SELECT s.SupplierCompany,
               COUNT(p.PurchaseId) AS NumPurchases,
               ROUND(SUM(p.TotalCost),2) AS TotalCost
        FROM Purchase p
        JOIN Supplier s ON p.SupplierId = s.SupplierId
        GROUP BY s.SupplierId
        ORDER BY TotalCost DESC
    """)
    supplier_purchases = cursor.fetchall()

    cursor.execute("SELECT * FROM Company ORDER BY CompanyName")
    all_companies = cursor.fetchall()

    cursor.close()

    return render_template("reporting.html",
                           all_companies=all_companies,
                           revenues=revenues,
                           top_products=top_products,
                           employees_report=employees_report,
                           employees_detailed=employees_detailed,
                           recent_hires=recent_hires,
                           company_inventory=company_inventory,
                           company_inventory_value=company_inventory_value,
                           expiring_products=expiring_products,
                           out_of_stock=out_of_stock,
                           products_by_category=products_by_category,
                           sales_by_month=sales_by_month,
                           revenue_by_product=revenue_by_product,
                           recent_orders=recent_orders,
                           customer_spending=customer_spending,
                           supplier_products=supplier_products,
                           supplier_purchases=supplier_purchases,
                           start_date=start_date,
                           end_date=end_date)

@app.route('/employees_by_dept', methods=['GET'])
def employees_by_dept():
    cursor = connection.cursor(dictionary=True)

    # All companies for the first dropdown
    cursor.execute("SELECT CompanyId, CompanyName FROM Company")
    companies = cursor.fetchall()

    selected_company_id = request.args.get('company_id')
    selected_department_id = request.args.get('department_id')

    departments = []
    employees = []

    if selected_company_id:
        cursor.execute("""
            SELECT DepartmentId, DepartmentName
            FROM Department
            WHERE CompanyId = %s
        """, (selected_company_id,))
        departments = cursor.fetchall()

    if selected_department_id:
        cursor.execute("""
            SELECT e.EmployeeId,
                   CONCAT(e.FirstName, ' ', e.LastName) AS Name,
                   e.Email,
                   e.PhoneNumber,
                   e.Gender,
                   e.DateOfHire,
                   e.DateOfBirth,
                   e.Salary,
                   e.Address,
                   c.CompanyName
            FROM Employee e
            JOIN Department d ON e.DepartmentId = d.DepartmentId
            JOIN Company c ON d.CompanyId = c.CompanyId
            WHERE e.DepartmentId = %s
              AND e.IsActive = 1
        """, (selected_department_id,))
        employees = cursor.fetchall()

    cursor.close()
    return render_template('employees_by_dept.html',
                           companies=companies,
                           departments=departments,
                           employees=employees,
                           selected_company_id=selected_company_id,
                           selected_department_id=selected_department_id)

@app.route('/company_financials', methods=['GET'])
def company_financials():
    cursor = connection.cursor(dictionary=True)

    # Get all companies for the dropdown
    cursor.execute("SELECT CompanyId, CompanyName FROM Company")
    companies = cursor.fetchall()

    # Get parameters
    company_id = request.args.get('company_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    financials = None
    low_stock_products = []
    selected_company = None
    company_employees_salary = []

    if company_id:
        # Financials
        date_filter = ""
        date_values = ()
        if start_date and end_date:
            date_filter = "AND s.SaleDate BETWEEN %s AND %s"
            date_values = (start_date, end_date)

        cursor.execute(f"""
            SELECT IFNULL(SUM(s.TotalRevenue), 0) AS TotalRevenue
            FROM Sale s
            WHERE s.CompanyId = %s
            {date_filter}
        """, (company_id,) + date_values)
        total_revenue = cursor.fetchone()['TotalRevenue']

        cursor.execute(f"""
            SELECT IFNULL(SUM(p.TotalCost), 0) AS TotalExpenditure
            FROM Purchase p
            WHERE p.CompanyId = %s
            {date_filter.replace('s.SaleDate', 'p.PurchaseDate')}
        """, (company_id,) + date_values)
        total_expenditure = cursor.fetchone()['TotalExpenditure']

        profit = total_revenue - total_expenditure

        financials = {
            'TotalRevenue': total_revenue,
            'TotalExpenditure': total_expenditure,
            'Profit': profit
        }

        # Get selected company name
        cursor.execute("SELECT CompanyName FROM Company WHERE CompanyId=%s", (company_id,))
        selected_company = cursor.fetchone()

        # Low Stock Products for the company
        cursor.execute("""
            SELECT ProductName, QuantityInStock
            FROM Product
            WHERE CompanyId = %s AND QuantityInStock <= 5
        """, (company_id,))
        low_stock_products = cursor.fetchall()

        # Company Employee Summary
        cursor.execute("""
            SELECT c.CompanyName,
                   COUNT(e.EmployeeId) AS TotalEmployees,
                   ROUND(SUM(e.Salary), 2) AS TotalMonthlySalaries
            FROM Company c
            JOIN Department d ON c.CompanyId = d.CompanyId
            JOIN Employee e ON d.DepartmentId = e.DepartmentId
            WHERE c.CompanyId = %s AND e.IsActive = 1
            GROUP BY c.CompanyId, c.CompanyName
        """, (company_id,))
        company_employees_salary = cursor.fetchall()

    cursor.close()
    return render_template(
        "company_financials.html",
        companies=companies,
        company_id=company_id,
        selected_company=selected_company,
        financials=financials,
        low_stock_products=low_stock_products,
        company_employees_salary=company_employees_salary,
        start_date=start_date,
        end_date=end_date
    )


def get_company_name(company_id):
    """
    Fetch the company name from the database based on the company_id.
    """
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT CompanyName FROM Company WHERE CompanyId = %s"
            cursor.execute(query, (company_id,))
            result = cursor.fetchone()
            cursor.close()
            return result['CompanyName'] if result else "Unknown Company"
        except Exception as e:
            print(f"An error occurred while fetching the company name: {e}")
            return "Unknown Company"
    else:
        print("Database connection is not available.")
        return "Unknown Company"

if __name__ == "__main__":
    app.run(debug=True)

