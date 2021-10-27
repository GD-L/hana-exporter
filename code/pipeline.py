import argparse
import os
from getpass import getpass
from tkinter import Tk, filedialog
import pandas as pd
from dotenv import load_dotenv
from hdbcli import dbapi

load_dotenv()
default_url = os.getenv("SERVER")
default_port = os.getenv("PORT")


def connection(argv):
    """
    Defines the connection to an SAP HANA server.
    """
    conn = dbapi.connect(address = argv.server,
                        port = argv.port,
                        user=argv.username,
                        password = argv.password)
    print("\n Connected  to " + argv.server + " \n")
    return conn

def execute_query(query,conn):
    """
    Executes a SQL Query against the previously established connection.
    Uses pandas read_sql_query
    """
    data = pd.read_sql_query(query,conn)
    return data

def write_csv(data):
    """
    Writes a .CSV file using tkinter asksaveasfilename dialog
    """
    files = [("CSV", '*.csv'),
            ("All Files","*.*")]
    file_path = filedialog.asksaveasfilename(filetypes=files)
    data.to_csv(file_path, index = False)

def read_input():
    """
    Uses tkinter to read a .txt .sql or other readable file containing a SQL query.
    """
    files = [("Text","*.txt"),("SQL","*.sql"),("All Files","*.*")]
    file_path = filedialog.askopenfilename(filetypes = files)
    read_file = open(file_path, "r", encoding = "UTF-8")
    sql_input = read_file.read()
    return sql_input, file_path



def main(argv):
    """
    To automate this script then fill in the values for server, username, etc
    You will be prompted for any values set to ""

    Server and username can be entered on the command line as well.

    """
    server = ""
    port = ""
    user_name = ""
    password = ""

    root = Tk()
    root.withdraw()

    print(argv)

    if server != "":
        argv.server = server

    if port != "":
        argv.port = port

    if user_name !="":
        argv.username = user_name
    elif argv.username is None:
        argv.username = input("Enter Username: \n")

    if password != "":
        argv.password = password
    elif argv.password is None:
        argv.password = getpass("Enter Password: \n")

    print(argv)
    conn = connection(argv)
    source = input("Would you like to read from a file? (y/n) \n")
    if source.upper() == "Y":
        sql_query, file_path = read_input()
        print("Reading file "+str(file_path))
    else: sql_query = input("Enter SQL Query:")

    data = execute_query(sql_query, conn)

    print_or_export = input("Would you like to export data (y/n)\n")
    if print_or_export.upper() == 'Y':
        write_csv(data)

    else:
        print(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server" ,
                        help = "Server URL",
                        default = default_url,
                        dest = "server", type=str)
    parser.add_argument("-p", "--port" , help = "Port", default = default_port, dest = "port")
    parser.add_argument("-u", "--username", help = "Username", dest = "username", type=str)
    parser.add_argument("-P","--Password", help = "Password", dest = "password")
    args = parser.parse_args()
    main(args)
