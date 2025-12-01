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
            # try:
            cursor.execute("SELECT company_name from companies WHERE id = %s", [id_of_company_to_remove])
            name_of_company_to_remove = cursor.fetchone()[0]
            cursor.execute("DELETE FROM companies WHERE id = %s", [id_of_company_to_remove])
            connection.commit()
            print(f"Removed {id_of_company_to_remove} {name_of_company_to_remove}")
            # except:
            #     print("Not removed. Something went wrong.")
             
print('closing connection')
connection.close