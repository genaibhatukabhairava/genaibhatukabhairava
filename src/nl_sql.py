#Python program to convert natural language to SQL query and execute it.
# Requirements
# python 3.x
# Packages required are
#pip install -U google -generativeai
#pip install pyodbc

import pyodbc
import google.generativeai as genai


# API key for Gemini Generative AI, you can get it from the below link. 
# https://aistudio.google.com/app/apikey

api_key = "AIzaSyBb_ISJob0L_sbQaI0Y9TodCb357Zw7SX"
genai.configure(api_key=api_key)
#api key initialization

model = genai.GenerativeModel("gemini-pro")
#selecting the instance of gemini model and initializing the connection to Gemini

# Connect to MS SQL Server 
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=DESKTOP-OOPRG56\\SQLEXPRESS;'
                      'DATABASE=test;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
#creates a cursor object that allows you to execute SQL queries 


# Function to execute SQL query and fetch results
def execute_query(sql_query):
    """
    Execute SQL query and fetch results from the database.
    
    Args:
    - sql_query (str): SQL query to execute
    
    Returns:
    - list of tuples: Query results
    """
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return result

# Function to format SQL query results
def format_results(results):
    """
    Format SQL query results into a list of dictionaries.
    
    Args:
    - results (list of tuples): Query results
    
    Returns:
    - list of dictionaries: Formatted query results
    """
    columns = [column[0] for column in cursor.description]
    #extracts the column names from the cursor's description attribute and stores them in the columns list.

    formatted_results = []
    #an empty list

    for row in results:
        formatted_row = {}
        for i, value in enumerate(row):
            formatted_row[columns[i]] = value
        formatted_results.append(formatted_row)

    return formatted_results

# Sample prompt for the Generative AI model
prompt = [
    """
    You are an expert in converting English questions to MS SQL query!
    The SQL database has the name EMPLOYEE and has the following columns - EmployeeID, EmployeeName
      , Age, Salary, Gender, Employer
       \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM [Test].[dbo].[Employee] ;
    \nExample 2 - Tell me all the employees of Female gender?, 
    the SQL command will be something like this SELECT * FROM [Test].[dbo].[Employee] where Gender= 'Female'; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Natural language query to be converted to SQL as input to Gemini
user_query = "Show me the average salary of Employees for different Employers"

# Generate SQL query from the natural language query using the Generative AI model
response = model.generate_content([prompt[0], user_query])

print (response.text)

# Execute the generated SQL query
results = execute_query(response.text)

print(results)
#unformatted results from the database

# Format and print the query results
formatted_results = format_results(results)

print("Query Results:")
for row in formatted_results:
    print("------------------------------------")
    for key, value in row.items():
        print(f"{key}: {value}")
    print("------------------------------------")

# Close the database connection
conn.close()
