import sqlite3
import os  
from tkinter import filedialog
from tabulate import tabulate

global file_path
file_path = "C:\\Users\\giasu\\Downloads\\test.db"
def cls():
  # clear the screen
    os.system('cls' if os.name=='nt' else 'clear')
    print("-------------------------------------------------------------------------------------------------")
    print("1. Press (1) Or Type 'newdb' To Create A New Database")
    print("2. Press (2) Or Type 'opendb' To Open A Database")
    print("3. Press (3) Or Type 'newtb' To Create A New Table")
    print("4. Press (4) Or Type 'deltb' To Delete A Table")
    print("5. Press (5) Or Type 'showtb' To Show Details Of A Table")
    print("6. Press (6) Or Type 'cls' To Clear The Screen")
    print("7. Press (7) Or Type 'exit' To Exit The App")
    print("-------------------------------------------------------------------------------------------------")

def create_db(path):
    # create a sqlite database 
    cn = sqlite3.connect(path)
    cn.close()

def save_file():
    # get File path 
    path = filedialog.asksaveasfilename(title = "Create Sqlite Database",defaultextension=".db",filetypes=[("Database File", "*.db"), ("All File", "*.*")])
    return path

def open_file():
    # get file path
    path = filedialog.askopenfilename(title = "Open Sqlite Database",filetypes=[("Database File", "*.db"), ("All File", "*.*")])
    return path

def open_db(path):
    # open a sqlite database :
    cn = sqlite3.connect(path)
    try:
        tables = cn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print("\tTables Name :-")
        i = 1
        for table in tables:
            print(f"{i} {table[0]}")
            columns = cn.execute(f"PRAGMA table_info({table[0]})")
            for colmun in columns:
                print(f"\t{colmun[1]} {colmun[2]} {colmun[3]}")
            i+=1
    except sqlite3.Error as error:
        print(f"\nError : {error}")
    finally:
        if cn:
            cn.close()

def create_tb(db):
    # create table name
    going = True
    i = 0
    tables_dateils = ""
    table_name = input("\nEnter Table Name : ")
    while going:
        col_name = input("\nEnter Column Name: ")
        data_type = input("Enter Data Type: ")
        key = input("Column Is Primary key ? (y/n): ")
        null = input("Column Is Not Null ? (y/n): ")
        tables_dateils+= str(f"{"," if i > 0 else ""} {col_name} {data_type.upper()} {"PRIMARY KEY" if key.lower() == "y" else ""} {"NOT NULL" if null.lower() == "y" else "NULL"}")
        i+=1
        ask = input("Add Another Column in This Table ? (y/n): ")
        if ask.lower() == "n":
            going = False

    cn = sqlite3.connect(db)
    try:
        quary = f"CREATE TABLE IF NOT EXISTs {table_name} ({tables_dateils})"
        cn.execute(quary)
        cn.commit()
    except sqlite3.Error as e:
        print("\n e")
    finally:
        if cn:
            cn.close()

def delete_tb(db):
    # delete a table from database
    table_name = input("\nEnter The Table Name You Want To Delete: ")
    cn = sqlite3.connect(db)
    try:
        cn.execute(f"DROP TABLE {table_name}")
        cn.commit()
    except sqlite3.Error as e:
        print("\t e")
    finally:
        if cn:
            cn.close()

def insert_row(db_path,tb_name):
    #inseart a row in cruent table
    cn = sqlite3.connect(db_path)
    column_list = []
    try:
        columns = cn.execute(f"PRAGMA table_info({tb_name})")
        for column in columns:
            col = input(f"Enter {column[1]}: ")
            column_list.append(col)
        
        column_tup = tuple(column_list)
        quary = f"INSERT INTO {tb_name} VALUES{column_tup}"
        cn.execute(quary)
        cn.commit()
    except sqlite3.Error as e:
        print(f"Error Inseart a Row {e}")
    finally:
        if cn:
            cn.close()

def update_row(db_path,tb_name):
    #update a row 
    cn = sqlite3.connect(db_path)
    value_list =""
    try:
        columns = cn.execute(f"PRAGMA table_info({tb_name})")
        column_names = [column[1] for column in columns]
        col_id = column_names[0]
        ask = input(f"Enter {col_id} To Update The Row: ")
        i = 1
        for column in columns:
            if column[1] == col_id:
                continue
            else:
                row_value = input(f"Enter {column}: ")
                if i > 1:
                    value_list+=f",{column[1]}={row_value}"
                else:
                    value_list+=f"{column[1]}={row_value}"
            i+=1

        quary = f"UPDATE {tb_name} SET {value_list} WHERE({col_id}={int(ask)})"
        cn.execute(quary)
        cn.commit()
    except sqlite3.Error as e:
        print(f"Error Update a Row {e}")
    finally:
        if cn:
            cn.close()
            



def show_rows(db):
    #show all records from a table
    table_name = input("Enter A Table Name: ")
    cn = sqlite3.connect(db)
    try:
        rows  = cn.execute(f"SELECT * FROM {table_name}")
        headers = [header[0] for header in rows.description]
        print(tabulate(rows,headers=headers,tablefmt="grid"))
        print()
        print("Press 1 For Inseart a Row")
        print("Press 2 For Update a Row")
        print("Press 3 For Search a Row")
        print("Press 4 For Delete a Row")
        print("Press 5 For Show All Rows")
        print("Press 6 For Exit This Options")
        cont = True
        while cont:
            ask = input("\nEnter A Option (1/2/3/4/5/6): ")
            match ask:
                case "1":
                    insert_row(file_path,table_name)
                case "2":
                    update_row(file_path,table_name)
                case "3":
                    pass
                case "4":
                    pass
                case "5":
                    rows  = cn.execute(f"SELECT * FROM {table_name}")
                    headers = [header[0] for header in rows.description]
                    print(tabulate(rows,headers=headers,tablefmt="grid"))
                    print()
                case "6":
                    cont = False
                case _:
                    print("Invalid Option !")
    except sqlite3.Error as e:
        print(f"\tError Fatching Rows : {e}")
    finally:
        if cn:
            cn.close()

# main part
cls()
while True:
    print("\n-------------------------------------------------------------------------------------------------")
    if file_path == "":
        print("No Database Selected !")
    else:
        print("Seleted Datbase : ",file_path)
        open_db(file_path)
    print("-------------------------------------------------------------------------------------------------")
    user_input = input("Enter A Command : ")
    match user_input.lower():
        case "newdb":
            file_path = save_file()
            create_db(file_path)
        case "1":
            file_path = save_file()
            create_db(file_path)
        case "opendb":
            file_path = open_file()
        case "2":
            file_path = open_file()
        case "newtb":
            if file_path == "":
                print("\tNo Database Selected!")
            else:
                create_tb(file_path)
        case "3":
            if file_path == "":
                print("\tNo Database Selected!")
            else:
                create_tb(file_path)
        case "deltb":
            if file_path == "":
                print("\tNo Database Selected!")
            else:
                delete_tb(file_path)
        case "4":
            if file_path == "":
                print("\tNo Database Selected!")
            else:
                delete_tb(file_path)
        case "showtb":
            if file_path =="":
                print("\tNo Database Selected!")
            else:
                show_rows(file_path)
        case "5":
            if file_path =="":
                print("\tNo Database Selected!")
            else:
                show_rows(file_path)
        case "cls":
            cls()
        case "6":
            cls()    
        case "exit":
            quit()  
        case "7":
            quit()
        case _:
            print("Invalid Command !")