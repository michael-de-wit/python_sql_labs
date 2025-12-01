import psycopg2

connection = psycopg2.connect(
    database="ga_postgres_crm_lab",
    password="osfuh1115"
)

print('connected')

cursor = connection.cursor()

user_wants_to_quit = False

while user_wants_to_quit == False:
    user_response_table_to_modify = input("\n Which table do you want to work with? " \
        "\n 1. companies" \
        "\n 2. employees" \
        "\n 3. quit" \
        "\n\n response: ")
    
    user_wants_to_modify_companies = True if user_response_table_to_modify == '1' else False
    user_wants_to_modify_employees = True if user_response_table_to_modify == '2' else False
    user_wants_to_quit = True if user_response_table_to_modify == '3' else False

    if user_wants_to_modify_companies == True:
        user_response_action_to_take_on_companies_table = input("\n What do you want to do with the companies table? " \
        "\n 1. View companies" \
        "\n 2. Add company" \
        "\n 3. Modify company data" \
        "\n 4. Remove company" \
        "\n 5. quit" \
        "\n\n response: ")   

        user_wants_to_view_companies = True if user_response_action_to_take_on_companies_table == '1' else False
        user_wants_to_add_company = True if user_response_action_to_take_on_companies_table == '2' else False
        user_wants_to_modify_company = True if user_response_action_to_take_on_companies_table == '3' else False
        user_wants_to_remove_company = True if user_response_action_to_take_on_companies_table == '4' else False
        user_wants_to_quit = True if user_response_action_to_take_on_companies_table == '5' else False

        if user_wants_to_view_companies == True:
            print("")
            cursor.execute("SELECT * FROM companies")
            print(cursor.fetchall())
        elif user_wants_to_add_company == True:
            name_of_company_to_add = input("\n Name of company to add: ")
            try:
                cursor.execute("INSERT INTO companies (company_name) VALUES(%s)", [name_of_company_to_add])
                connection.commit()
                cursor.execute("SELECT id from companies WHERE company_name LIKE %s", [name_of_company_to_add])
                id_of_added_company = cursor.fetchone()[0]
                print(f"\n Added id: {id_of_added_company}; company name: {name_of_company_to_add}")
            except psycopg2.errors.UniqueViolation:
                connection.rollback()
                cursor.execute("SELECT id from companies WHERE company_name LIKE %s", [name_of_company_to_add])
                id_of_added_company = cursor.fetchone()[0]
                print(f"Not added. The company {id_of_added_company} {name_of_company_to_add} already exists")
        elif user_wants_to_modify_company == True:
            cursor.execute("SELECT * FROM companies")
            print(cursor.fetchall())
            id_of_company_to_modify = input("\n Which company do you want to modify? company id: ")
            print("")
            cursor.execute("SELECT company_name from companies WHERE id = %s", [id_of_company_to_modify])
            name_of_company_to_modify = cursor.fetchone()[0]
            new_name_of_company_to_modify = input(f"New name for {name_of_company_to_modify}: ")
            try:
                cursor.execute("UPDATE companies SET company_name=%s WHERE id = %s", [new_name_of_company_to_modify, id_of_company_to_modify])
                connection.commit()
            except:
                print("Not updated. Something went wrong.")
        elif user_wants_to_remove_company == True:
            cursor.execute("SELECT * FROM companies")
            print(cursor.fetchall())
            id_of_company_to_remove = input("\n Which company do you want to remove? company id: ")
            try:
                cursor.execute("SELECT company_name from companies WHERE id = %s", [id_of_company_to_remove])
                name_of_company_to_remove = cursor.fetchone()[0]
                cursor.execute("DELETE FROM companies WHERE id = %s", [id_of_company_to_remove])
                connection.commit()
                print(f"Removed {id_of_company_to_remove} {name_of_company_to_remove}")
            except:
                print("Not removed. Something went wrong.")
    elif user_wants_to_modify_employees == True:
        user_response_action_to_take_on_employees_table = input("\n What do you want to do with the employees table? " \
        "\n 1. View employees" \
        "\n 2. Add employee" \
        "\n 3. Modify employee data" \
        "\n 4. Remove employee" \
        "\n 5. quit" \
        "\n\n response: ")  

        user_wants_to_view_employees = True if user_response_action_to_take_on_employees_table == '1' else False
        user_wants_to_add_employee = True if user_response_action_to_take_on_employees_table == '2' else False
        user_wants_to_modify_employee = True if user_response_action_to_take_on_employees_table == '3' else False
        user_wants_to_remove_employee = True if user_response_action_to_take_on_employees_table == '4' else False
        user_wants_to_quit = True if user_response_action_to_take_on_employees_table == '5' else False

        if user_wants_to_view_employees == True:
            try:
                print("")
                cursor.execute("SELECT e.id, e.employee_name, c.company_name FROM employees e LEFT JOIN companies c on e.company_id=c.id")
                print(cursor.fetchall())
            except:
                print("Something went wrong.")
        elif user_wants_to_add_employee:
            name_of_employee_to_add = input("\n Name of employee to add: ")
            try:
                cursor.execute("INSERT INTO employees (employee_name) VALUES(%s)", [name_of_employee_to_add])
                connection.commit()
                cursor.execute("SELECT id from employees WHERE employee_name LIKE %s", [name_of_employee_to_add])
                id_of_added_employee = cursor.fetchone()[0]
                print(f"\n Added id: {id_of_added_employee}; employee name: {name_of_employee_to_add}")
            except psycopg2.errors.UniqueViolation:
                connection.rollback()
                cursor.execute("SELECT id from employees WHERE employee_name LIKE %s", [name_of_employee_to_add])
                id_of_added_employee = cursor.fetchone()[0]
                print(f"Not added. The employee {id_of_added_employee} {name_of_employee_to_add} already exists")
            
            cursor.execute("SELECT * FROM companies")
            print(cursor.fetchall())
            company_id_of_employee_to_add = input("\n Company id of employee: ")
            print("")
            try:
                cursor.execute("UPDATE employees SET company_id=%s WHERE id = %s", [company_id_of_employee_to_add, id_of_added_employee])
                connection.commit()

                cursor.execute("SELECT company_name from companies WHERE id = %s", [company_id_of_employee_to_add])
                name_of_company_of_employee_to_add = cursor.fetchone()[0]    
                print(f"Add eid {id_of_added_employee} {name_of_employee_to_add} to cid {company_id_of_employee_to_add} {name_of_company_of_employee_to_add}")
            except:
                print("Company id not added. Something went wrong.")

        elif user_wants_to_modify_employee:
            print("")
            cursor.execute("SELECT e.id, e.employee_name, c.company_name FROM employees e LEFT JOIN companies c on e.company_id=c.id")
            print(cursor.fetchall())
            id_of_employee_to_modify = input("\n Which employee do you want to modify? employee id: ")
            print("")
            cursor.execute("SELECT employee_name from employees WHERE id = %s", [id_of_employee_to_modify])
            name_of_employee_to_modify = cursor.fetchone()[0]

            cursor.execute("SELECT company_id from employees WHERE id = %s", [id_of_employee_to_modify])
            company_id_of_employee_to_modify = cursor.fetchone()[0]    

            cursor.execute("SELECT company_name from companies WHERE id = %s", [company_id_of_employee_to_modify])
            name_of_company_of_employee_to_modify = cursor.fetchone()[0]    

            user_response_action_to_take_on_employee_modification = input(f"\n What do you want to modify for eid {id_of_employee_to_modify} {name_of_employee_to_modify} from cid {company_id_of_employee_to_modify} {name_of_company_of_employee_to_modify}? \n 1. Employee name \n 2. Company ID \n 3. quit \n Response: ")

            user_wants_to_modify_employee_name = True if user_response_action_to_take_on_employee_modification == '1' else False
            user_wants_to_modify_employee_company_id = True if user_response_action_to_take_on_employee_modification == '2' else False
            user_wants_to_quit = True if user_response_action_to_take_on_employee_modification == '3' else False    

            if user_wants_to_modify_employee_name == True:
                new_name_of_employee_to_modify = input(f"New name for {name_of_employee_to_modify}: ")
                try:
                    cursor.execute("UPDATE employees SET employee_name=%s WHERE id = %s", [new_name_of_employee_to_modify, id_of_employee_to_modify])
                    connection.commit()
                except:
                    print("Not updated. Something went wrong.")
            if user_wants_to_modify_employee_company_id == True:
                print("")
                cursor.execute("SELECT * FROM companies")
                print(cursor.fetchall())
                new_company_id_of_employee_to_modify = input(f"New company ID for {name_of_employee_to_modify}: ")
                try:
                    cursor.execute("UPDATE employees SET company_id=%s WHERE id = %s", [new_company_id_of_employee_to_modify, id_of_employee_to_modify])
                    connection.commit()
        
                    cursor.execute("SELECT e.id, e.employee_name, c.company_name FROM employees e LEFT JOIN companies c on e.company_id=c.id WHERE e.id=%s", [id_of_employee_to_modify])
                    print(cursor.fetchall())

                except:
                    print("Not updated. Something went wrong.")
        elif user_wants_to_remove_employee:
            cursor.execute("SELECT e.id, e.employee_name, c.company_name FROM employees e LEFT JOIN companies c on e.company_id=c.id")
            print(cursor.fetchall())
            id_of_employee_to_remove = input("\n Which employee do you want to remove? employee id: ")  

            try:
                cursor.execute("SELECT employee_name from employees WHERE id = %s", [id_of_employee_to_remove])
                name_of_employee_to_remove = cursor.fetchone()[0]
                cursor.execute("DELETE FROM employees WHERE id = %s", [id_of_employee_to_remove])
                connection.commit()
                print(f"\n Removed eid {id_of_employee_to_remove} {name_of_employee_to_remove}")
            except:
                print("Not removed. Something went wrong.")
             
print('\n closing connection')
connection.close