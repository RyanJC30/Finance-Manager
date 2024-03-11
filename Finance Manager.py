import os
import getpass


# ------------------ Start-up functions ------------------ #

# Function to create the 'data' folder if it doesn't exist
def create_data_folder():
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)

create_data_folder()

# Function to create the 'users.txt' file inside the 'data' folder
def create_users_file():

    # Call create_data_folder to ensure 'data' folder exists
    users_txt_path = os.path.join("data", "users.txt")
    open(users_txt_path, "a").close()

create_users_file()

# Function to create individual users folder to add their files to
def create_user_folder(user_name):
    users_folder = os.path.join("data", "Users")
    user_folder = os.path.join(users_folder, user_name)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    return user_folder


# Function to create files if they do not exist already
def create_file_if_not_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w"):
            pass


# Function to create all user files when the user registers
def create_required_files(user_name):
    user_folder = create_user_folder(user_name)

    # List of required files to be created in users folder
    files_to_create = [
        "expenses_debits.txt",
        "expenses_other.txt",
        "income.txt",
        "credits.txt",
        "investments.txt",
        "investment_calculator.txt",
        "reports.txt"
    ]

    for file_name in files_to_create:
        file_path = os.path.join(user_folder, file_name)
        create_file_if_not_exists(file_path)
        
        write_to_file(user_folder, file_name, {})



# ------------------ General functions ------------------ #

# Function to read data from a text file for a specific user and file
def read_from_file(user_name, file_name, create=False):

    if file_name == "users.txt":
        file_path = os.path.join("data", file_name)
    else:
        user_folder = create_user_folder(user_name)
        file_path = os.path.join(user_folder, file_name)

    # If the file doesn't exist and create is True, create an empty file
    if not os.path.exists(file_path) and create:
        
        with open(file_path, "w"):
            pass

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            if not lines:
                return {}  # Return an empty dictionary if the file is empty
            data = {}
            for line in lines:
                key, value = line.strip().split(',')
                data[key] = value
            return data
    else:
        return {}  # Return an empty dictionary if the file doesn't exist


# Function to write data to a text file
def write_to_file(folder, file_name, data):

    file_path = os.path.join(folder, file_name)

    # Create the folder if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        # For other user-specific files, iterate over key-value pairs
        for key, value in data.items():
            file.write(f"{key},{value}\n")


# Function to write user credentials to a text file
def write_user_credentials_to_file(folder, username, password):

    file_path = os.path.join(folder, "users.txt")

    # Create the folder if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "a") as file:
        # Write the new username and password
        file.write(f"{username},{password}\n")



# ------------------ Additional functions ------------------ #

# Function to get numerical input from the user with error handling
def get_numerical_input(prompt):

    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError as e:
            print(f"Invalid input: Please enter a valid numerical value.")


# Function to initialize financial data for a specific user
def initialize_financial_data(user_name):
    
    debits = read_from_file(user_name, "expenses_debits.txt") or {}
    other_expenses = read_from_file(user_name, "expenses_other.txt") or {}
    credits = read_from_file(user_name, "credits.txt") or {}
    investments = read_from_file(user_name, "investments.txt") or {}

    # Initializing income data values (Good practice to add values)
    income_data = read_from_file(user_name, "income.txt") or {
        "income": 0,
        "Income_TAX": 0,
        "Income_Less_Tax": 0,
        "UIF": 0.01,
        "TOTAl_NET_INCOME": 0
    }

    return debits, other_expenses, credits, investments, income_data



# ------------------ Register & login functions ------------------ #

# Function to register new users
def register_user():
    print("\nRegister:")
    while True:
        username = input("Enter your username: ")
        
        # Checking if username already exists in login data file and asking user to re-enter
        users_data = read_from_file("data", "users.txt")
        if username in users_data:
            print("Username already exists. Please choose a different username.")
        else:
            break

    # Use getpass to securely input the password (Does not show when inputting into console: better security)
    password = getpass.getpass("Enter your password: ")

    # Add the new user to the users.txt data
    users_data[username] = password

    # Write the new username and password to the users.txt file
    write_user_credentials_to_file("data", username, password)

    # Create necessary files for the new user
    create_required_files(username)

    print("Registration successful. You can now log in.")


# Function to handle user login
def login_user():

    print("\nLogin:")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Check if the username and password match
    users_data = read_from_file("data", "users.txt")
    if username in users_data and users_data[username] == password:
        print(f"Welcome, {username}!")
        return username  # Return the username if login is successful
    else:
        print("Invalid username or password. Please try again.")
        return None

# Function to authenticate the user
def authenticate_user():

    while True:
        print("\nAuthentication Menu:")
        print("1. Register")
        print("2. Login")
        print("0. Exit")

        choice = input("Enter your choice (0-2): ")

        if choice == "0":
            print("Exiting the authentication system.")
            return None

        elif choice == "1":
            register_user()

        elif choice == "2":
            username = login_user() # returning username when completing function
            if username:
                return username

        else:
            print("Invalid choice. Please enter a number between 0 and 2.")



# ------------------ Functions for Managing Income, Expenses, Credits & Investments ------------------ #


# ------------------ Income functions ------------------ #

# Function to display an income report
def view_income_report(income, Income_TAX, Income_Less_Tax, UIF, TOTAl_NET_INCOME):
    
    print("\nIncome report:")
     
    print("\nGross income      = R{:.2f}".format(round(float(income), 2)))
    print("income TAX        = R{:.2f}".format(float(Income_TAX)))
    print("income less Tax   = R{:.2f}".format(round(float(Income_Less_Tax), 2)))
    print("UIF deduction     = R{:.2f}".format(round(float(income) * UIF, 2)))
    print("Total net income  = R{:.2f}".format(round(float(TOTAl_NET_INCOME), 2)))


# Function menu to manage income data for a specific user
def manage_income(user_name):
    
    # Initialize financial data for the specific user
    debits, other_expenses, credits, investments, income_data = initialize_financial_data(user_name)

    while True:
        print("\nManage Income:")
        print("1. Income Calculator")
        print("2. View Income Report")
        print("3. Go back to the main menu")

        choice = input("Enter your choice (1-3): ")

        # Update income_data with the results of the income_calculator
        if choice == "1":
            
            income, Income_TAX, Income_Less_Tax, UIF, TOTAl_NET_INCOME = income_calculator()
            income_data["income"] = income
            income_data["Income_TAX"] = Income_TAX
            income_data["Income_Less_Tax"] = Income_Less_Tax
            income_data["UIF"] = UIF
            income_data["TOTAl_NET_INCOME"] = TOTAl_NET_INCOME
            
            # Write updated income data to the file
            write_to_file(create_user_folder(user_name), "income.txt", income_data)

        # Call the view_income_report function with appropriate parameters
        elif choice == "2":
            
            view_income_report(
                income_data["income"],
                income_data["Income_TAX"],
                float(income_data["Income_Less_Tax"]),
                float(income_data["UIF"]),
                float(income_data["TOTAl_NET_INCOME"])
            )

        # Break out of the loop to go back to the main menu
        elif choice == "3":
            break  

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

    return income_data


# Function to calculate income
def income_calculator():
    
    print("Income calculator.\n")

    calculation_type = ""
    while calculation_type != "days" and calculation_type != "hours":
        calculation_type = input("How would you like to calculate your future income, via 'days' or 'hours' worked? ").lower()
        if calculation_type != "days" and calculation_type != "hours":
            print("Please enter 'days' or 'hours'.")

    hourly_rate = get_numerical_input("What is your hourly income rate?: R")

    double_day_income = ""
    while double_day_income != "yes" and double_day_income != "no":
        
        # calculates whether public holidays/ Sundays should be double pay or 1.5 pay depending on company requirements
        double_day_income = input("Are you generally scheduled to work on Sundays or public holidays? Enter 'yes' or 'no': ").lower() 
        if double_day_income != "yes" and double_day_income != "no":
            print("Please enter 'yes' or 'no'.")

    if double_day_income == "yes":
        double_day_percentage = 0.5 # 1 and a half pay (Value is the extra amount)
    else:
        double_day_percentage = 1.0 # double pay (Value is the extra amount)


    # - Income questions & calculations -
    
    income = 0
    average_hours = 176
    months_per_year = 12
    
    # Questions for calculating income via days worked
    if calculation_type == "days":
        total_hours_per_day = get_numerical_input("How many paid hours per day do you work? ")
        
        total_days = get_numerical_input("How many days have you worked for the month? ")
        total_double_days = get_numerical_input("How many days out of your total days are Sundays or public holidays? ")
        total_hours = total_hours_per_day * total_days
        income = hourly_rate * total_hours + (total_double_days * hourly_rate * total_hours_per_day * double_day_percentage) # Adding only additional as it is included all hours already

    # Questions for calculating income via hours per month worked
    elif calculation_type == "hours":
        hours = get_numerical_input("Enter the total amount of hours you have worked for the month: ")
        total_double_hours = get_numerical_input("How many hours out of your total hours are on Sundays or public holidays? ")
        income = hourly_rate * hours + (total_double_hours * hourly_rate * double_day_percentage) # Adding only additional as it is included all hours already

    average_annual_income = hourly_rate * average_hours * months_per_year


    # - Tax bracket values -
    
    UIF = 0.01
    Income_TAX = 0
    Income_Less_Tax = 0

    # Tax bracket - annual income (Maximum)
    Tax_Bracket_1 = 237100
    Tax_Bracket_2 = 370500
    Tax_Bracket_3 = 512800
    Tax_Bracket_4 = 673000
    Tax_Bracket_5 = 857900
    Tax_Bracket_6 = 1817000
    Tax_Bracket_7 = 1817001 # and more

    # Tax bracket - percentage
    TB1_Percent = 0.18
    TB2_Percent = 0.26
    TB3_Percent = 0.31
    TB4_Percent = 0.36
    TB5_Percent = 0.39
    TB6_Percent = 0.41
    TB7_Percent = 0.45

    # Tax bracket - Extra tax on tax percentage per bracket
    TB1_extra_tax = 0
    TB2_extra_tax = 3556.50 #(42678/12)
    TB3_extra_tax = 6446.83 #(77362/12)
    TB4_extra_tax = 10122.92 #(121475/12)
    TB5_extra_tax = 14928.92 #(179147/12)
    TB6_extra_tax = 20938.17 #(251258/12)
    TB7_extra_tax = 53707.42 #(644489/12)


    # - Tax bracket calculations -

    # List of tax brackets
    tax_brackets = [
        (Tax_Bracket_1, TB1_Percent, 0),
        (Tax_Bracket_2, TB2_Percent, TB2_extra_tax),
        (Tax_Bracket_3, TB3_Percent, TB3_extra_tax),
        (Tax_Bracket_4, TB4_Percent, TB4_extra_tax),
        (Tax_Bracket_5, TB5_Percent, TB5_extra_tax),
        (Tax_Bracket_6, TB6_Percent, TB6_extra_tax),
        (Tax_Bracket_7, TB7_Percent, TB7_extra_tax)
    ]

    # Iterate over tax brackets
    for i, (bracket, percent, extra_tax) in enumerate(tax_brackets):
        if average_annual_income <= bracket:
            taxable_percentage_amount = income - (0 if i == 0 else tax_brackets[i - 1][0])
            Income_Less_Tax = income - (taxable_percentage_amount * percent) - (extra_tax if i != 0 else 0)
            Income_TAX = round(income * percent, 2)
            break


    # Results

    TOTAl_NET_INCOME = Income_Less_Tax - (income * UIF)  # UIF calculated on gross income not net.
    
    print("\nGross income      = R{:.2f}".format(round(income, 2)))
    print("Income TAX        = R{:.2f}".format(Income_TAX))
    print("Income less Tax   = R{:.2f}".format(Income_Less_Tax))
    print("UIF deduction     = R{:.2f}".format(income * UIF))
    print("\nTotal net income  = R{:.2f}".format(TOTAl_NET_INCOME))

    return income, Income_TAX, Income_Less_Tax, UIF, float(TOTAl_NET_INCOME)



# ------------------ Expense functions ------------------ #

# Function to display an expense report
def show_expense_report(debits, other_expenses):
    
    print("\nExpense report:\n")
    print(f"{'- Debit orders -':<20} {'Value (R)':>8}")
    print("-" * 35)

    total_expense = 0
    for expense, value in debits.items():
        total_expense += float(value)
        print(f"{expense:<20} R{float(value):>7.2f}")

    print(f"\n{'- Additional -':<20} {'Value (R)':>8}")
    print("-" * 35)
    for expense, value in other_expenses.items():
        total_expense += float(value)
        print(f"{expense:<20} R{float(value):>7.2f}")
    
    print("\n")
    print("-" * 35)    
    print(f"{'Total Expenses':<20} R{total_expense:>7.2f}")
    

# Function to amend or remove an expense   
def amend_or_remove_expense(expenses):
    
    print("\nChoose an expense to amend or remove:")

    for index, (expense, value) in enumerate(expenses.items(), 1):
        print(f"{index}. {expense}: R{float(value):.2f}")

    choice = input("Enter the number of the expense to amend or remove (or '0' to go back): ")

    if choice == "0":
        return None  # Go back to the previous menu

    try:
        choice_index = int(choice)
        selected_expense = list(expenses.keys())[choice_index - 1]

        # Capture the value before removing
        removed_value = expenses[selected_expense]

        new_value = input(f"Enter the new value for {selected_expense} or 'r' to remove it: ")

        
        if new_value.lower() == 'r':
            # Remove expense
            del expenses[selected_expense]
            print(f"{selected_expense} expense of R{float(removed_value):.2f} has been successfully removed.")
        
        else:
            # Amend expense
            expenses[selected_expense] = float(new_value)
            print(f"{selected_expense} has been successfully amended to R{float(new_value):.2f}.")

    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")

    return amend_or_remove_expense(expenses)


# Function to add an additional expense
def add_additional_expense(expenses):  
    
    expense_name = input("Enter the name of the expense: ")
    expense_value = get_numerical_input("Enter the value of the expense: ")
    expenses[expense_name] = expense_value
    print(f"{expense_name} expense of R{expense_value:.2f} has been successfully added.")


# Function to manage expenses data & menu for a specific user
def manage_expenses(current_user):
    
    debits_data = read_from_file(current_user, "expenses_debits.txt") or {}
    other_expenses_data = read_from_file(current_user, "expenses_other.txt") or {}

    while True:
        
        # Expense menu
        print("\nManage Expenses:")
        print("1. Show expense report")
        print("2. Amend or remove expenses")
        print("3. Add expense")
        print("4. Go back to the main menu")

        choice = input("Enter your choice (1-4): ")

        # Show expense report menu option
        if choice == "1":
            show_expense_report(debits_data, other_expenses_data)

        # Amend or remove expenses menu option
        elif choice == "2":
            while True:
                expense_type = input("Enter '1' for debit order expenses or '2' for additional expenses: ")

                # Debit expenses
                if expense_type == "1":
                    print("\nDebit expenses:")
                    selected_expense = amend_or_remove_expense(debits_data)
                    if selected_expense is not None:
                        new_value = input(f"Enter the new value for {selected_expense} or 'r' to remove it: ")
                        if new_value.lower() == "r":
                            del debits_data[selected_expense]
                            print(f"{selected_expense} expense has been removed successfully.")
                        else:
                            try:
                                debits_data[selected_expense] = float(new_value)
                                print(f"{selected_expense} expense has been amended successfully.")
                            except ValueError:
                                print("Invalid input. Please enter a valid numerical value.")
                                continue  # Ask the user to re-enter
                    break  # Exit the loop once a valid choice is made
                
                # additional expenses
                elif expense_type == "2":
                    print("\nDebit expenses:")
                    selected_expense = amend_or_remove_expense(other_expenses_data)
                    if selected_expense is not None:
                        new_value = input(f"Enter the new value for {selected_expense} or 'r' to remove it: ")
                        if new_value.lower() == "r":
                            del other_expenses_data[selected_expense]
                            print(f"{selected_expense} has been removed successfully.")
                        else:
                            try:
                                other_expenses_data[selected_expense] = float(new_value)
                                print(f"{selected_expense} has been amended successfully.")
                            except ValueError:
                                print("Invalid input. Please enter a valid numerical value.")
                                continue
                    break

                else:
                    print("Invalid option. Please enter '1' or '2'.")

            # Write updated expenses data to the files
            write_to_file(create_user_folder(current_user), "expenses_debits.txt", debits_data)
            write_to_file(create_user_folder(current_user), "expenses_other.txt", other_expenses_data)

        # Add expense menu option
        elif choice == "3":
            while True:
                expense_type = input("Enter '1' for debit order expenses or '2' for additional expenses: ")

                if expense_type == "1":
                    print("\nAdd debit expense:\n")
                    add_additional_expense(debits_data)
                    break
                elif expense_type == "2":
                    print("\nAdd additional expense:\n")
                    add_additional_expense(other_expenses_data)
                    break
                else:
                    print("Invalid expense type. Please enter '1' or '2'.")

            # Write updated expenses data to the files
            write_to_file(create_user_folder(current_user), "expenses_debits.txt", debits_data)
            write_to_file(create_user_folder(current_user), "expenses_other.txt", other_expenses_data)

        # Back to main menu option
        elif choice == "4":
            return

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")



# ------------------ Credit functions ------------------ #

# Function to display a credit report
def show_credit_report(credits):
    
    print("\nCredit report:")
    
    total_credits = 0
    print(f"\n{'Credits':<20} {'Value (R)':>8}")
    print("-" * 35)
    for credit, value in credits.items():
        total_credits += float(value)
        print(f"{credit:<20} R{float(value):>7.2f}")
    print(f"\n{'Total credits':<20} R{total_credits:>7.2f}")
  
  
# Function to amend or remove a credit
def amend_or_remove_credit(credits_data):
    
    print("\nAmend or remove credit:")

    if not credits_data:
        print("There are no credits available.")
        return None

    print("\nChoose a credit to amend or remove:")

    for index, (credit, value) in enumerate(credits_data.items(), 1):
        print(f"{index}. {credit}: R{float(value):.2f}")

    choice = input("Enter the number of the credit to amend or remove (or '0' to go back): ")

    if choice == "0":
        return None

    try:
        choice_index = int(choice)
        selected_credit = list(credits_data.keys())[choice_index - 1]

        while True:
            new_value = input(f"Enter the new value for {selected_credit} or 'r' to remove it: ")

            if new_value.lower() == 'r':
                del credits_data[selected_credit]
                print(f"{selected_credit} has been successfully removed.")
                break
            else:
                try:
                    credits_data[selected_credit] = float(new_value)
                    print(f"{selected_credit} has been successfully amended to R{float(new_value):.2f}.")
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid numerical value.")

        # Write updated credits data to the file
        write_to_file(create_user_folder(current_user), "credits.txt", credits_data)

    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")

    return amend_or_remove_credit(credits_data)


# Function to add a new credit
def add_credit(credits_data):
    
    print("\nAdd credit:")
    credit_name = input("Enter the name of the credit: ")

    credit_value = get_numerical_input("Enter the value of the credit: ")

    credits_data[credit_name] = credit_value
    print(f"{credit_name} with a value of R{float(credit_value):.2f} has been successfully added.")

    # Write updated credits data to the file
    write_to_file(create_user_folder(current_user), "credits.txt", credits_data)


# Function to manage credits and menu for a specific user
def manage_credits(user_name):

    # Construct the file path for credits.txt in the user's folder
    credits_file_path = os.path.join("data", "Users", user_name, "credits.txt")

    # Read existing credits data from the file
    credits_data = read_from_file(user_name, "credits.txt") or {}

    while True:
        print("\nManage Credits:")
        print("1. Show credit report")
        print("2. Amend or remove credits")
        print("3. Add credit")
        print("4. Go back to main menu")

        choice = input("Enter your choice (1-4): ")
        
        # Show credit report menu option
        if choice == "1":
            show_credit_report(credits_data)

        # Amend or remove credit menu option
        elif choice == "2":
            selected_credit = amend_or_remove_credit(credits_data)
            if selected_credit is not None:
                new_value = input(f"Enter the new value for {selected_credit} or 'r' to remove it: ")
                if new_value.lower() == "r":
                    del credits_data[selected_credit]
                else:
                    credits_data[selected_credit] = float(new_value)

        # Add new credit menu option
        elif choice == "3":
            add_credit(credits_data)

        # Go back to the main menu option
        elif choice == "4":
            break  

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")



# ------------------ Investment functions ------------------ #


# Function to manage investments data and menu
def manage_investments(user_name):
    
    
    # Construct the file path for investments.txt in the user's folder
    investments_file_path = os.path.join("data", "Users", user_name, "investments.txt")

    # Read existing investments data from the file
    investments_data = read_from_file(user_name, "investments.txt") or {}

    while True:
        print("\nManage Investments:")
        print("1. View investments")
        print("2. Amend or remove investments")
        print("3. Add investment")
        print("4. Percentage Calculator and Report")
        print("5. Go back to main menu")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            show_investment_report(investments_data)

        elif choice == "2":
            selected_investment = amend_or_remove_investment(investments_data)
            if selected_investment is None:
                continue
            write_to_file(create_user_folder(user_name), "investments.txt", investments_data)

        elif choice == "3":
            add_investment(investments_data)
            write_to_file(create_user_folder(user_name), "investments.txt", investments_data)

        elif choice == "4":
            percentage_calculator_menu(user_name)

        elif choice == "5":
            write_to_file(create_user_folder(user_name), "investments.txt", investments_data)
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


# Function to display an investment report
def show_investment_report(investments):
    
    print("\nInvestment report:")

    total_investments_value = sum(float(value) for value in investments.values())
    print(f"\n{'Total Investments':<20} R{total_investments_value:.2f}")
    
    # Sort investments by value in descending order
    sorted_investments = sorted(investments.items(), key=lambda x: float(x[1]), reverse=True)

    print(f"\n{'Investment':<20} {'Value (R)':<15}")
    print("-" * 50)

    for investment, value in sorted_investments:
        value_float = float(value)
        percentage = (value_float / total_investments_value) * 100
        print(f"{investment:<20} R{value_float:.2f} ({percentage:.2f}%)")


# Function to amend or remove an investment
def amend_or_remove_investment(investments):
    
    if not investments:
        print("\nThere are no investments available to amend or remove.")
        return None  # Go back to the previous menu

    print("\nAmend or remove investment:")
    print("\nChoose an investment to amend or remove:")

    for index, (investment, value) in enumerate(investments.items(), 1):
        print(f"{index}. {investment}: R{float(value):.2f}")

    choice = input("Enter the number of the investment to amend or remove (or '0' to go back): ")

    if choice == "0":
        return None  # Go back to the previous menu

    try:
        choice_index = int(choice)
        selected_investment = list(investments.keys())[choice_index - 1]

        while True:
            new_value = input(f"Enter the new value for {selected_investment} or 'r' to remove it: ")

            if new_value.lower() == 'r':
                print(f"{selected_investment} investment has been removed successfully.")
                del investments[selected_investment]
                break
            else:
                try:
                    new_value = float(new_value)
                    investments[selected_investment] = new_value
                    print(f"\n{selected_investment} value has been updated to R{new_value:.2f}.")
                    break
                except ValueError:
                    print("\nInvalid input. Please enter a valid numerical value for the investment or 'r' to remove it.")

        # Update the investments.txt file
        write_to_file(create_user_folder(current_user), "investments.txt", investments)

    except (ValueError, IndexError):
        print("\nInvalid choice. Please enter a valid number.")
        return amend_or_remove_investment(investments)


# Function to add a new investment
def add_investment(investments):
    
    print("\nAdd investment:")
    investment_name = input("Enter the name of the investment: ")
    
    investment_value = get_numerical_input(f"Enter the value for {investment_name}: ")

    investments[investment_name] = investment_value
    print(f"\n{investment_name} of R{investment_value:.2f} has been added successfully.")



#------------Percentage Calculator------------#

# Function to read data from file
def get_calculator_file_path(user_name):
    return os.path.join("data", "Users", user_name, "investment_calculator.txt")


# Function to show investment calculator menu
def percentage_calculator_menu(user_name):
    
    # Construct the file path for investment_calculator.txt in the user's folder
    get_calculator_file_path(user_name)  
    
    # Read existing calculator data from the file
    calculator_data = read_from_file(user_name, "investment_calculator.txt") or {}

    # Assuming original_total_budget is defined somewhere in your code
    original_total_budget = 0

    while True:
        
        # Read existing calculator data from the file
        calculator_data = read_from_file(user_name, "investment_calculator.txt") or {}
        
        print("\nPercentage Calculator:")
        print("1. Create a new investment percentage calculation")
        print("2. Amend or remove investments from current investment calculation data")
        print("3. View investment calculator report")
        print("4. Go back to the main menu")

        sub_choice = input("Enter your choice (1-4): ")

        if sub_choice == "1":
            create_new_investment_calculator(user_name, calculator_data)

        elif sub_choice == "2":
            amend_or_remove_investment_calculator(user_name, calculator_data, original_total_budget)

        elif sub_choice == "3":
            view_investment_calculator_report(calculator_data)

        elif sub_choice == "4":
            break  # Go back to the main menu

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def create_new_investment_calculator(user_name, calculator_data):
    # Function to create new investment calculator
    
    # Construct the file path for investment_calculator.txt in the user's folder
    get_calculator_file_path(user_name)

    # Clear the existing data in the calculator_data
    calculator_data.clear()

    total_budget = float(get_numerical_input("Enter the total investment budget: "))
    remaining_budget = total_budget

    print("\nPercentage Calculator:")
    new_investments = {}

    while True:
        print(f"\nRemaining budget: R{remaining_budget:.2f}/R{total_budget:.2f}")
        print(f"Remaining percentage: {remaining_budget / total_budget * 100:.2f}%")
        print("\nAdd an investment or type 'done' to finish:")
        investment_name = input("Enter the name of the investment: ")

        if investment_name.lower() == 'done':
            # Update the investment_calculator.txt file
            write_to_file(create_user_folder(user_name), "investment_calculator.txt", {"total_budget": total_budget, **new_investments})
            print("\nInvestment calculator has been updated")
            break

        try:
            investment_percentage = float(input(f"Enter the percentage for {investment_name} (remaining: {round(remaining_budget / total_budget * 100, 2)}%): "))
            if  0 <= investment_percentage <= remaining_budget:
                investment_value = (total_budget * investment_percentage) / 100
                if investment_value <= remaining_budget:
                    new_investments[investment_name] = investment_value
                    remaining_budget -= investment_value
                    print(f"\nR{investment_value:.2f} has been allocated to {investment_name} for your investment plan")
                else:
                    print(f"\nInvalid input. The calculated value exceeds the remaining balance.")
            else:
                print(f"\nInvalid input. Percentage must be between 0 and {remaining_budget:.2f}. Percentage exceeds remaining balance.")

        except ValueError:
            print("\nInvalid input. Please enter the new investment name and a valid numerical value for the percentage.")


    print("\nPercentage Calculator Report:")
    print(f"\n{'Total Investment Budget:':<25} R{total_budget:>8.2f}")

    # Calculate and print allocated and unallocated percentages
    allocated_percentage = (total_budget - remaining_budget) / total_budget * 100
    unallocated_percentage = remaining_budget / total_budget * 100

    print(f"{'Allocated Percentage:':<25} R{total_budget - remaining_budget:>8.2f} ({allocated_percentage:.0f}%)")
    print(f"{'Unallocated Percentage:':<25} R{remaining_budget:>8.2f} ({unallocated_percentage:.0f}%)")


    # Print individual investments
    print(f"\n{'Investments':<20} {'Value (R)':>8}")
    print("-" * 50)
    
    total_value = 0
    for investment, value in new_investments.items():
        total_value += value
        percentage = (value / total_budget) * 100
        print(f"{investment:<20} R{value:.2f} ({percentage:.2f}%)")
        
    print(f"\n{'Total':<20} R{total_value:.2f}")

    # Update the investment_calculator.txt file
    write_to_file(create_user_folder(user_name), "investment_calculator.txt", {"total_budget": total_budget, **new_investments})


# Function to amend or remove investment calculator investments
def amend_or_remove_investment_calculator(user_name, calculator_data, original_total_budget):
    
    # Construct the file path for investment_calculator.txt in the user's folder
    calculator_file_path = os.path.join("data", "Users", user_name, "investment_calculator.txt")

    # Read existing calculator data from the file
    calculator_data = read_from_file(user_name, "investment_calculator.txt") or {}

    # Check if there are no investments in the calculator
    if not calculator_data or len(calculator_data) == 1:
        print("\nThere are no investments in the investment calculator available.")
        return

    # Extract total budget from the first line
    total_budget = float(calculator_data.get("total_budget", original_total_budget))
    remaining_budget = total_budget  # Initialize remaining budget

    print("\nAmend or remove investment from the current calculation:")
    print("Choose an investment to amend or remove:")
    
    print(f"\n{'Total budget':<23} R{total_budget:>8.2f}")
    print(f"\n{'Investments':<23} {'Value (R)':>8}")
    print("-" * 50)

    # Print investments excluding 'total_budget' and start enumeration from 1
    for index, (investment, value) in enumerate(list(calculator_data.items())[1:], 1):
        value = float(value)
        percentage = (value / total_budget) * 100
        print(f"{index}. {investment:<20} R{value:>8.2f} ({percentage:.2f}%)")

    choice = get_numerical_input("\nEnter the number of the investment to amend or remove (or '0' to go back): ")

    if choice == "0":
        return

    try:
        choice_index = int(choice)

        selected_investment = list(calculator_data.keys())[choice_index]

        original_value = float(calculator_data[selected_investment])
        original_percentage = (original_value / total_budget) * 100

        allocated_amount = sum(float(value) for key, value in calculator_data.items() if key != "total_budget")
        unallocated_amount = total_budget - allocated_amount

        print(f"\nUnallocated amount: R{unallocated_amount:.2f} ({(unallocated_amount / total_budget) * 100:.2f}%)")

        # Declare max_allowed_value here
        max_allowed_value = (unallocated_amount + original_value) / total_budget * 100

        while True:
            new_value = input(f"Enter the new percentage value for {selected_investment} or 'r' to remove it "
                            f"({max_allowed_value:.2f}% unallocated including {selected_investment} investment): ")

            if new_value.lower() == "r":
                remaining_budget += original_value  # Add back the value to remaining budget
                del calculator_data[selected_investment]
                break

            try:
                new_value = float(new_value)
                max_allowed_value = (unallocated_amount + original_value) / total_budget * 100  # Include original value
                if 0 <= new_value <= max_allowed_value:
                    remaining_budget += original_value  # Add back the original value to remaining budget
                    remaining_budget -= new_value  # Deduct the new value from remaining budget
                    calculator_data[selected_investment] = (total_budget * new_value) / 100
                    print(f"{selected_investment} value has been updated to {new_value:.2f}%.")
                    
                    # Update the investment_calculator.txt file with the modified data
                    write_to_file(create_user_folder(user_name), "investment_calculator.txt", calculator_data)
                    break
                else:
                    print(f"Invalid input. Value must be between 0 and {max_allowed_value:.2f}.")
            except ValueError:
                print("Invalid input. Please enter a valid numerical value for the investment or 'r' to remove it.")

        # Update the investment_calculator.txt file     
        write_to_file(create_user_folder(user_name), "investment_calculator.txt", calculator_data)

    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")
        amend_or_remove_investment_calculator(user_name, calculator_data, original_total_budget)


def view_investment_calculator_report(calculator_data):
    # Function to view investment calculator report
    
    print("\nInvestment Calculator Report:")

    # Extract total budget
    total_budget_raw = calculator_data.get("total_budget")

    if total_budget_raw is None or total_budget_raw.strip() == "":
        total_budget = 0
    else:
        total_budget = float(total_budget_raw)

    # Extract individual investments
    investments = {k: float(v) for k, v in calculator_data.items() if k != "total_budget"}

    # Calculate allocated and unallocated amounts
    allocated_amount = sum(investments.values())
    unallocated_amount = total_budget - allocated_amount

    print(f"\n{'Total budget:':<20} R{total_budget:>8.2f}")

    if total_budget != 0:
        print(f"{'Allocated amount:':<20} R{allocated_amount:>8.2f} ({(allocated_amount / total_budget) * 100:.2f}%)")
        print(f"{'Unallocated amount:':<20} R{unallocated_amount:>8.2f} ({(unallocated_amount / total_budget) * 100:.2f}%)")

    else:
        print("Total budget is zero. Please make sure a credit calculation has been created.")

    print(f"\n{'Investments':<20} {'Value (R)':>8}")
    print("-" * 50)

    # Display individual investments sorted by value (largest to smallest)
    for investment, value in sorted(investments.items(), key=lambda x: x[1], reverse=True):
        percentage = (value / total_budget) * 100
        print(f"{investment:<20} R{value:.2f} ({percentage:.2f}%)")



# ------------------ Generate reports Functions ------------------ #

# Modified generate_report function
def generate_report(current_user):
    user_name = current_user
    debits, other_expenses, credits, investments, income_data = initialize_financial_data(user_name)

    while True:
        print("\nGenerate report:")
        print("1. Income report")
        print("2. Expense report")
        print("3. Credit report")
        print("4. Investment report")
        print("5. Calculate remaining balance")
        print("6. Full finance report")
        print("0. Back to main menu")

        choice = input("Enter your choice (0-5): ")

        if choice == "0":
            return

        elif choice == "1":
            view_income_report(
                income_data["income"],
                income_data["Income_TAX"],
                float(income_data["Income_Less_Tax"]),
                float(income_data["UIF"]),
                float(income_data["TOTAl_NET_INCOME"]))

        elif choice == "2":
            show_expense_report(debits, other_expenses)

        elif choice == "3":
            show_credit_report(credits)

        elif choice == "4":
            show_investment_report(investments)

        elif choice == "5":
            calculate_net_position(income_data, debits, other_expenses, credits, investments)

        elif choice == "6":
            generate_full_report(income_data, debits, other_expenses, credits, investments)

        else:
            print("Invalid choice. Please enter a number between 0 and 6.")



# Function to generate the full report
def generate_full_report(income_data, debits, other_expenses, credits, investments):
    print("\nFull report:\n")

    view_income_report(
        income_data["income"],
        income_data["Income_TAX"],
        float(income_data["Income_Less_Tax"]),
        float(income_data["UIF"]),
        float(income_data["TOTAl_NET_INCOME"]))

    print("\n")
    show_expense_report(debits, other_expenses)

    print("\n")
    show_credit_report(credits)

    print("\n")
    show_investment_report(investments)


# Function to calculate net financial position
def calculate_net_position(income_data, debits, other_expenses, credits, investments):

    # Extract relevant values from income_data
    total_net_income = float(income_data["TOTAl_NET_INCOME"])

    # Calculate total expenses
    total_expenses = sum(float(value) for value in debits.values()) + sum(float(value) for value in other_expenses.values())

    # Calculate total credits
    total_credits = sum(float(value) for value in credits.values())

    # Calculate total investments
    total_investments = sum(float(value) for value in investments.values())

    # Calculate net financial position
    net_position = total_net_income - total_expenses + total_credits - total_investments

    # Print the result
    print("\nBalance breakdown:\n")
    print(f"{'Total Net Income':.<20} R{total_net_income:.2f}")
    print(f"{'Total Expenses':.<20} R{total_expenses:.2f}")
    print(f"{'Total Credits':.<20} R{total_credits:.2f}")
    print(f"{'Total Investments':.<20} R{total_investments:.2f}")
    print(f"\n{'Remaining balance':.<20} R{net_position:.2f}")

    # Check if net_position is below 0
    if net_position < 0:
        print("Your expenses exceed your income")



# ------------------ Main menu Functions ------------------ #

# Function to display the main menu and get user choice
def main_menu(current_user):
    print("\nMain Menu:")
    print("1. Manage Income")
    print("2. Manage Expenses")
    print("3. Manage Credits")
    print("4. Manage Investments")
    print("5. Generate report")
    print("0. Logout")

    choice = input("Enter your choice (0-5): ")
    return choice


# Main loop
while True:
    # Call the authentication function before the main menu
    current_user = authenticate_user()
    if not current_user:
        # Exit the program if authentication fails
        print("Exiting the program. Goodbye!")
        break

    in_main_menu = True
    while in_main_menu:
        # Display the main menu
        choice = main_menu(current_user)

        if choice == "0":
            print(f"Exiting the program. Goodbye {current_user}!")
            in_main_menu = False

        elif choice == "1":
            income_data = manage_income(current_user)

        elif choice == "2":
            manage_expenses(current_user)

        elif choice == "3":
            manage_credits(current_user)

        elif choice == "4":
            manage_investments(current_user)

        elif choice == "5":
            # Pass the necessary arguments to generate_report
            generate_report(current_user)

        else:
            print("Invalid choice. Please enter a number between 0 and 5.")