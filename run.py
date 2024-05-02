import gspread 
from google.oauth2.service_account import Credentials
#from pprint import pprint - not needed in final

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    '''
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user via the terminal, which must be a string of 6 numbers seperated by commas, the loop will repeatedly request data, until it is valid.

    '''
    while True:

        print("Please enter sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")
        
        data_str = input("Enter your data here: \n")
        # when you use the input method you must have the \n character for it to show in the terminal

        sales_data = data_str.split(",") #remove commas and convert into a list of values
        

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data

def validate_data(values):
    '''
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int or if there arent exactly 6
    '''

    print(values)
    try:
        [int(value) for value in values]
        if len(values) !=6:  
            #if the length of our data is not equal to six
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data : {e}, please try again\n')
        return False
    return True


'''
def update_sales_worksheet(data):
    
    Update sales worksheet, add new row with the list data provided
    
    print("updating sales worksheet....\n")
    sales_worksheet = SHEET.worksheet("sales") # this is the way we access our sheet
    sales_worksheet.append_row(data) # appends a row to the sales sheet
    print("Sales worksheet updated sucessfully \n")

def update_surplus_worksheet(data):
    
    Update surplus worksheet, add new row with the list data provided
    
    print("updating surplus worksheet....\n")
    surplus_worksheet = SHEET.worksheet("surplus") # this is the way we access our sheet
    surplus_worksheet.append_row(data) # appends a row to the sales sheet
    print("surplus worksheet updated sucessfully \n")

the above update_sales_worksheet and update_surplus_worksheet has been replaced by the following:
'''

def update_worksheet(data,worksheet):
    '''
    Recieves a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    '''

    print(f"updating {worksheet} worksheet....\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_surplus_data(sales_row):
    '''
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out

    '''
    print("Calculating surplus data ... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    # the above states we want to get all data from the stock sheet
    stock_row = stock[-1] #use a slice to access last row in stock list
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    '''
    Collects columns of data from sales worksheet, collecting the last 5 entries for each sandwich and returns the data as a list of lists 
    '''
    sales = SHEET.worksheet("sales")
    #column = sales.col_values(3)  
    ''' this returns the data in columns instead of rows (rows and cols start at 1 not 0)'''
    #print(column)
    columns =[]

    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])  # this gets the last 5 values in each column which is what we want
    return columns

def calculate_stock_data(data):
    '''
    Calculate the average stock for each item type, adding 10%
    '''

    print("Calculating Stock data ....\n")

    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column] # convert values into int so we can perform calculations on them
        average = sum(int_column)/ len(int_column)  # gives us the avg from each column
        stock_num = average * 1.1 # adds 10% to avg
        new_stock_data.append(round(stock_num))
    return new_stock_data

def main():

    '''
    Run all program functions (in python functions should be wrapped in a main function)'''

    data = get_sales_data()
    sales_data = [int(num) for num in data]

    update_worksheet(sales_data,"sales") # here we want to update the sales worksheet

    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus") # here we want to update the surplus worksheet
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data,"stock")
print("Welcome to Love Sandwiches Data Automation") #this is where our instructions will be for our game

main()

