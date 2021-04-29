#import numpy as np
#import pathlib2

import argparse
import sys
from getpass import getpass
from dotenv import load_dotenv
import os

import pandas as pd
from hdbcli import dbapi

# importing all files  from tkinter
from tkinter import * 
from tkinter import ttk
  
# import only asksaveasfile from filedialog
# which is used to save file in any extension
from tkinter import filedialog

load_dotenv()
default_url = os.getenv("SERVER")
default_port = os.getenv("PORT")


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server" , help = "Server URL",default=default_url, dest = "server", type=str)
parser.add_argument("-p", "--port" , help = "Port",default=default_port, dest = "port")
parser.add_argument("-u", "--username", help = "Username", dest = "username", type=str)
parser.add_argument("-P","--Password", help = "Password", dest = "password")
args = parser.parse_args()

def connection(server,port,username,password):
    conn = dbapi.connect(address = args.server, port = args.port, user=args.username, password = args.password)
    print("\n Connected \n")
    return(conn)

def execute_query(query,conn):
    data = pd.read_sql_query(query,conn)
    #print(data.head(100))
    return(data)

def write_csv(data):
    files = [("CSV", '*.csv'),
            ("All Files","*.*")]
    file_path = filedialog.asksaveasfilename(filetypes=files)
    data.to_csv(file_path, index = False)

def read_input():
    files = [("Text","*.txt"),("SQL","*.sql"),("All Files","*.*")]
    file_path = filedialog.askopenfilename(filetypes = files)
    read_file = open(file_path,"r")
    sql_input = read_file.read()
    return(sql_input)



def main():
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
    
    if len(sys.argv)==4:
        args.server = sys.argv[1]
        args.port = sys.argv[2]
        args.username = sys.argv[3]
        args.password = sys.argv[4]

    print(args)
    print("UN: " + user_name)

    if server == "" and args.server == None:
        args.server = input("Server:\n")
    
    if port == "" and args.port == None:
        args.port = input("Port: \n")

    if user_name == "" and args.username == None:
        args.username = input("Username:\n")
    elif user_name != "" and args.username == None:
        args.username = user_name
    else:
        args.username
    
    if password == "" and args.password == None:
        args.password = getpass("Password:\n")
    elif password != "" and args.password == None:
        args.password = password
    else: 
        args.password

    conn = connection(args.server,args.port,args.username,args.password)
    source = input("Would you like to read from a file? (y/n) \n")
    if source.upper() == "Y":
        sql_query = read_input()
    else: sql_query = input("Enter SQL Query:")

    data = execute_query(sql_query, conn)

    print_or_export = input("Would you like to export data (y/n)\n")
    if print_or_export.upper() == 'Y':
        write_csv(data)

    else:
        print(data)

if __name__ == "__main__":
    main()
