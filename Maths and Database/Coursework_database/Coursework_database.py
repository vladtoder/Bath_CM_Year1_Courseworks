import sqlite3
import datetime
import pandas 

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('airline.db')
curs = conn.cursor()

# Function to create tables
def create_tables():
    curs.execute('''CREATE TABLE IF NOT EXISTS Aircraft (
                    AircraftID INT,
                    Model VARCHAR(15),
                    Capacity INT,
                    PRIMARY KEY (AircraftID)
                )''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Flight (
                    FlightID INT,
                    Aircraft INT,
                    Departure_time DATETIME,
                    Arrival_time DATETIME,
                    Departure_location VARCHAR(30),
                    Arrival_place VARCHAR(30),
                    Status VARCHAR(20),
                    FOREIGN KEY (Aircraft) REFERENCES Aircraft (AircraftID),
                    PRIMARY KEY (FlightID)
                )''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Pilot (
                    PilotID INT,
                    Name VARCHAR(20),
                    License_number VARCHAR(10),
                    Hours_flown INT,
                    PRIMARY KEY (PilotID)
                )''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Pilot_flight (
                    Flight INT,
                    Pilot INT,
                    FOREIGN KEY (Flight) REFERENCES Flight (FlightID),
                    FOREIGN KEY (Pilot) REFERENCES Pilot (PilotID),
                    PRIMARY KEY (Flight, Pilot)
                )''')
    
    # Save (commit) the changes
    conn.commit()

# Function to insert new pilot
def insert_pilot(PilotID, Name, License_number, Hours_flown):
    with conn:
        curs.execute("INSERT INTO Pilot VALUES (:PilotID, :Name, :License_number, :Hours_flown)",
                  {'PilotID': PilotID, 'Name': Name, 'License_number': License_number, 'Hours_flown': Hours_flown})

# Function to insert new aircraft
def insert_aircraft(AircraftID, Model, Capacity):
    with conn:
        curs.execute("INSERT INTO Aircraft VALUES (:AircraftID, :Model, :Capacity)",
                  {'AircraftID': AircraftID, 'Model': Model, 'Capacity': Capacity})

# Function to insert new flight
def insert_flight(FlightID, Aircraft, Departure_time, Arrival_time, Departure_location, Arrival_place, Status):
    with conn:
        curs.execute('''INSERT INTO Flight VALUES (:FlightID, :Aircraft, :Departure_time, :Arrival_time, 
                    :Departure_location, :Arrival_place, :Status)''',
                  {'FlightID': FlightID, 'Aircraft': Aircraft, 'Departure_time': Departure_time,
                   'Arrival_time': Arrival_time, 'Departure_location': Departure_location,
                   'Arrival_place': Arrival_place, 'Status': Status})

# Function to link pilot and flight
def assign_pilot_to_flight(Flight, Pilot):
    with conn:
        # Check if the pilot is already assigned to the flight
        curs.execute("SELECT 1 FROM Pilot_flight WHERE Flight = ? AND Pilot = ?", (Flight, Pilot))
        if curs.fetchone():
            print("This pilot is already assigned to this flight.")
        else:
            curs.execute("INSERT INTO Pilot_flight VALUES (:Flight, :Pilot)", {'Flight': Flight, 'Pilot': Pilot})
            print("Pilot successfully assigned to flight.")

def is_int(value):
    # Check if the given value can be converted to an integer
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_valid_str(value, max_length):
    # Check if the given value is a string within the specified maximum length
    return isinstance(value, str) and len(value) > 0 and len(value) <= max_length

def is_valid_datetime(date_text):
    # Check if the date_text conforms to the 'YYYY-MM-DD HH:MM' format
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

def get_int_input(prompt, exit_code="000"):
    # Repeatedly prompt for an integer input until a valid integer or exit code is entered
    while True:
        print(f"{prompt} (Enter {exit_code} to exit)")
        input_value = input()
        if input_value == exit_code:
            return None  # Exit condition
        if is_int(input_value):
            return int(input_value)
        print("Invalid input. Please enter a valid integer.")

def get_str_input(prompt, max_length, exit_code="000"):
    # Repeatedly prompt for a string input within a maximum length until a valid input or exit code is entered
    while True:
        print(f"{prompt} (max {max_length} characters, Enter {exit_code} to exit)")
        input_value = input()
        if input_value == exit_code:
            return None
        if is_valid_str(input_value, max_length):
            return input_value
        print(f"Invalid input. Please enter a valid string (max {max_length} characters).")

def get_datetime_input(prompt, exit_code="000"):
    # Repeatedly prompt for a date/time input in a specific format until a valid input or exit code is entered
    while True:
        print(f"{prompt} (Enter in 'YYYY-MM-DD HH:MM' format, Enter {exit_code} to exit)")
        input_value = input()
        if input_value == exit_code:
            return None
        if is_valid_datetime(input_value):
            return input_value
        print("Invalid date/time format. Please enter in 'YYYY-MM-DD HH:MM' format.")

def aircraft_exists(AircraftID):
    # Check if an aircraft with the given AircraftID exists in the Aircraft database table
    curs.execute("SELECT 1 FROM Aircraft WHERE AircraftID = ?", (AircraftID,))
    return curs.fetchone() is not None

def flight_exists (FlightID):
    # Check if a flight with the given FlightID exists in the Flight database table
    curs.execute("SELECT 1 FROM Flight WHERE FlightID = ?", (FlightID,))
    return curs.fetchone() is not None 

def pilot_exists (PilotID):
    # Check if a pilot with the given PilotID exists in the Pilot database table
    curs.execute("SELECT 1 FROM Pilot WHERE PilotID = ?", (PilotID,))
    return curs.fetchone() is not None 


# Simple text-based menu
def menu():
    while True:
        print("")
        print("AIRLINE DATABASE MANAGEMENT")
        print("")
        print("0. Show tables")
        print("1. Insert data")
        print("2. Update data")
        print("3. Search data")
        print("4. Delete data")
        print("5. Exit")
        print("")
        choice = input ("Enter choice: ")
        
        
        def display_table_data(table_name):
            try:
                conn = sqlite3.connect('airline.db')
                query = f"SELECT * FROM {table_name}"
                results = pandas.read_sql_query(query, conn)
                conn.close()
                pandas.set_option('display.colheader_justify', 'center')
                if not results.empty:
                    print(results.to_string(index=False))
                else:
                    print(f"No data found in {table_name}.")
            except Exception as e:
                print(f"An error occurred when accessing {table_name}: {e}")
                
        if choice == "0":
            while True:
                print("")
                print("1. Show aircraft table")
                print("2. Show pilot table")
                print("3. Show flight table")
                print("4. Show assigned pilot table")
                print("5. Show all tables")
                print("6. Exit")
                print("")
                choice_show = input("Enter choice:")
                print("")
                
                if choice_show == "1":
                    display_table_data("Aircraft")
                elif choice_show =="2":
                    display_table_data("Pilot")
                elif choice_show =="3":
                    display_table_data("Flight")
                elif choice_show =="4":
                    display_table_data("Pilot_flight")
                elif choice_show =="5":
                    display_table_data("Aircraft")
                    print("")
                    display_table_data("Pilot")
                    print("")
                    display_table_data("Flight")
                    print("")
                    display_table_data("Pilot_flight")
                    print("")
                elif choice_show =="6":
                    break
                else:
                    print("Invalid choice. Please choose a valid option.")
                    continue
                
        
        if choice == "1":
            while True:
                print("")
                print("1. Insert new aircraft")
                print("2. Insert new pilot")
                print("3. Insert new flight")
                print("4. Assign pilot")
                print("5. Exit")
                print("")
                choice_insert = input("Enter choice: ")
                print("")

                if choice_insert == "1":
                    while True:
                        AircraftID = get_int_input("Enter Aircraft ID")
                        if AircraftID is None:  # Exit if user entered "000"
                            break
                        if aircraft_exists(AircraftID):
                            print("Aircraft ID already exists. Please enter a unique Aircraft ID.")
                            continue
                        
                        Model = get_str_input("Enter Aircraft Model", 15)
                        if Model is None:  # Check for exit code after each input
                            break
                        
                        Capacity = get_int_input("Enter Aircraft Capacity")
                        if Capacity is None:
                            break
                        
                        insert_aircraft(AircraftID, Model, Capacity)
                        break

                elif choice_insert == "2":
                    while True:
                        PilotID = get_int_input("Enter Pilot ID")
                        if PilotID is None:
                            break
                        if pilot_exists(PilotID):
                            print("Pilot ID already exists. Please enter a unique Pilot ID.")
                            continue
                    
                        Name = get_str_input("Enter Pilot's Name", 20)
                        if Name is None: 
                            break
                        
                        License_number = get_str_input("Enter License Number", 10)
                        if License_number is None: 
                            break
                        
                        Hours_flown = get_int_input("Enter Hours Flown")
                        if Hours_flown is None: 
                            break
                        
                        insert_pilot(PilotID, Name, License_number, Hours_flown)
                        break
                
                elif choice_insert == "3":

                    # Flight insertion logic
                    while True:
                        FlightID = get_int_input("Enter Flight ID")
                        if FlightID is None: 
                            break
                        if flight_exists(FlightID):
                            print("Flight ID already exists. Please enter a unique Flight ID.")
                            continue
                        
                        Aircraft = get_int_input("Enter Aircraft ID")
                        if Aircraft is None:   
                            break
                        if not aircraft_exists(Aircraft):
                            print("Aircraft does not exist. Please enter an existing Aircraft ID.")
                            break

                        Departure_time = get_datetime_input("Enter Departure Time (YYYY-MM-DD HH:MM)")
                        if Departure_time is None: 
                            break
                        #check later (compare time)
                        Arrival_time = get_datetime_input("Enter Arrival Time (YYYY-MM-DD HH:MM)")
                        if Arrival_time is None: 
                            break

                        Departure_location = get_str_input("Enter Departure Location", 30)
                        if Departure_location is None: 
                            break
                        else:
                            Arrival_place = get_str_input("Enter Arrival Place", 30)
                            if Arrival_place is None and Arrival_place != Departure_location: 
                                break

                        Status = get_str_input("Enter Flight Status", 20)
                        if Status is None: 
                            break

                        insert_flight(FlightID, Aircraft, Departure_time, Arrival_time, Departure_location, Arrival_place, Status)
                        break
                
                elif choice_insert == "4":
                    # Pilot to flight assignment logic
                    Flight = get_int_input("Enter Flight ID")
                    if Flight is None or not flight_exists(Flight):
                        print("Flight does not exist. Please enter an existing Flight ID.")
                        continue

                    Pilot = get_int_input("Enter Pilot ID")
                    if Pilot is None or not pilot_exists(Pilot):
                        print("Pilot does not exist. Please enter an existing Pilot ID.")
                        continue

                    assign_pilot_to_flight(Flight, Pilot)
                    break
                
                elif choice_insert == "5":
                    break

                else:
                    print("Invalid choice. Please choose a valid option.")
                    continue
                
            
        def handle_aircraft_update():
            # Function to handle updates to the Aircraft table
            while True:
                display_table_data("Aircraft")  # Display the current Aircraft data
                id_value = get_int_input("Enter the Aircraft ID that you want to update:")
                if id_value is None:
                    return [], id_value  # Exit the function if the user enters the exit code
                if not aircraft_exists(id_value):
                    print("\nID doesn't exist or invalid data type.")
                    continue
                global table_name, id_field  # Declare global variables for table name and ID field
                table_name, id_field = "Aircraft", "AircraftID"  # Set table name and ID field for Aircraft
                return ["Model", "Capacity"], id_value  # Return the fields to update and the ID

        def handle_pilot_update():
            # Function to handle updates to the Pilot table
            while True:
                display_table_data("Pilot")  # Display the current Pilot data
                id_value = get_int_input("Enter the Pilot ID that you want to update:")
                if id_value is None:
                    return [], None
                if not pilot_exists(id_value):
                    print("\nID doesn't exist or invalid data type.")
                    continue
                global table_name, id_field
                table_name, id_field = "Pilot", "PilotID"  # Set table name and ID field for Pilot
                return ["Name", "License_number", "Hours_flown"], id_value  # Return the fields to update and the ID

        def handle_flight_update():
            # Function to handle updates to the Flight table
            while True:
                display_table_data("Flight")  # Display the current Flight data
                id_value = get_int_input("Enter the Flight ID that you want to update: ")
                if id_value is None:
                    return [], None
                if not flight_exists(id_value):
                    print("\nID doesn't exist or invalid data type.")
                    continue
                global table_name, id_field
                table_name, id_field = "Flight", "FlightID"  # Set table name and ID field for Flight
                return ["Aircraft", "Pilot", "Departure_time", "Arrival_time", "Departure_location", "Arrival_place", "Status"], id_value  # Return the fields to update and the ID

        def get_value_for_field(field):
            # Function to get the new value for a given field
            if field in ["Departure_time", "Arrival_time"]:
                return get_datetime_input(f"Enter the new value for {field}")
            elif field in ["Model", "Name", "License_number", "Departure_location", "Arrival_place", "Status"]:
                return get_str_input(f"Enter the new value for {field}", max_length=30)
            elif field in ["Capacity", "Hours_flown"]:
                return get_int_input(f"Enter the new value for {field}")
            else:
                return input(f"Enter the new value for {field}: ")  # Generic input for other fields

        def update_table(table_name, id_field, id_value, field_to_update, new_value):
            # Function to execute the update operation on the database
            if field_to_update not in ["AircraftID", "PilotID", "FlightID"]:
                curs.execute(f"UPDATE {table_name} SET {field_to_update} = ? WHERE {id_field} = ?", (new_value, id_value))  # Update the database
                conn.commit()  # Commit the changes
                print(f"{field_to_update} has been updated successfully.")
            else:
                print("Updating ID fields is not allowed.")  # Prevent updating of ID fields

        if choice == "2":
            while True:
                print("Select the table you want to update:")
                print("1. Aircraft")
                print("2. Pilot")
                print("3. Flight")
                print("4. Exit")
                choice_update = input("Enter choice: ")

                valid_fields = []
                if choice_update == "1":
                    valid_fields, id_value = handle_aircraft_update()
                elif choice_update == "2":
                    valid_fields, id_value = handle_pilot_update()
                elif choice_update == "3":
                    valid_fields, id_value = handle_flight_update()
                elif choice_update == "4":
                    break
                

                if not valid_fields:
                    continue
                
                while True:
                    field_to_update = input(f"Enter the field you want to update: {', '.join(valid_fields)}\n")
                    if field_to_update not in valid_fields:
                        print("Invalid field. Please enter a valid field (or you exited)")
                        continue
                    else:
                        break

                new_value = get_value_for_field(field_to_update)
                update_table(table_name, id_field, id_value, field_to_update, new_value)
                display_table_data(table_name)
                
                
        def search_pilot(search_term):
            try:
                with conn:
                    # Check if the search term is numeric for exact ID match
                    if search_term.isdigit():
                        query = "SELECT * FROM Pilot WHERE PilotID = ?"
                        params = (search_term,)
                    else:  # Text-based search for other fields
                        query = "SELECT * FROM Pilot WHERE Name LIKE ? OR License_number LIKE ?"
                        params = (f'%{search_term}%', f'%{search_term}%')
                    results = pandas.read_sql_query(query, conn, params=params)
                    pandas.set_option('display.colheader_justify', 'center')
                    if not results.empty:
                        print(results.to_string(index=False))
                    else:
                        print("No matching pilot found.")
            except sqlite3.Error as e:
                print("An error occurred while searching:", e)

        def search_aircraft(search_term):
            try:
                with conn:
                    # Check if the search term is numeric
                    if search_term.isdigit():
                        query = "SELECT * FROM Aircraft WHERE AircraftID = ? OR Capacity = ?"
                        params = (search_term, search_term)
                    else:
                        query = "SELECT * FROM Aircraft WHERE Model LIKE ?"
                        params = (f'%{search_term}%',)
                    results = pandas.read_sql_query(query, conn, params=params)
                    pandas.set_option('display.colheader_justify', 'center')
                    if not results.empty:
                        print(results.to_string(index=False))
                    else:
                        print("No matching aircraft found.")
            except sqlite3.Error as e:
                print("An error occurred while searching:", e)

        def search_flight(search_term):
            try:
                with conn:
                    # Check if the search term is numeric for exact ID match
                    if search_term.isdigit():
                        query = "SELECT * FROM Flight WHERE FlightID = ?"
                        params = (search_term,)
                    else:  # Text-based search for other fields
                        query = "SELECT * FROM Flight WHERE Departure_location LIKE ? OR Arrival_place LIKE ?"
                        params = (f'%{search_term}%', f'%{search_term}%')
                    results = pandas.read_sql_query(query, conn, params=params)
                    pandas.set_option('display.colheader_justify', 'center')
                    if not results.empty:
                        print(results.to_string(index=False))
                    else:
                        print("No matching flight found.")
            except sqlite3.Error as e:
                print("An error occurred while searching:", e)

        def search_pilot_flight(search_term):
            try:
                with conn:
                    query = ("SELECT * FROM Pilot_flight WHERE Flight = ? OR Pilot = ?", (search_term, search_term))
                    results = pandas.read_sql_query(query, conn, params=(search_term, search_term))
                    pandas.set_option('display.colheader_justify', 'center')
                    if not results:
                        print(results.to_string(index=False))
                    else:
                        print("No matching pilot-flight assignment found.")
            except sqlite3.Error as e:
                print("An error occurred while searching:", e)
        
        if choice == "3":  
            print("")
            print("1. Search for aircraft")
            print("2. Search for pilot")
            print("3. Search for flight")
            print("4. Search for assigned pilot to flight")
            print("5. Exit")
            print("")
            choice_search = input("Enter what you want to search for: ")

            if choice_search == "1":
                search_term = input("Enter Aircraft ID, Model or Capacity to search for: ")
                search_aircraft(search_term)
            elif choice_search == "2":
                search_term = input("Enter Pilot ID, Name, License number or Hours flown to search for: ")
                search_pilot(search_term)
            elif choice_search == "3":
                search_term = input("Enter Flight ID, Departure or Arrival location, to search for: ")
                search_flight(search_term)
            elif choice_search == "4":
                search_term = input("Enter Flight ID or Pilot ID for pilot-flight assignment search: ")
                search_pilot_flight(search_term)
            elif choice_search == "5":
                pass  # Exit the search menu
            else:
                print("Invalid choice. Please enter a valid option.")

        
        # Function to delete a row with exception handling
        def delete_row(table_name, id_field, id_value):
            try:
                curs.execute(f"DELETE FROM {table_name} WHERE {id_field} = ?", (id_value,))
                conn.commit()
                if curs.rowcount == 0:
                    print(f"No row found with {id_field} = {id_value} in {table_name}.")
                else:
                    print(f"Row with {id_field} = {id_value} has been deleted from {table_name}.")
            except sqlite3.Error as e:
                print("An error occurred:", e)
                    
        if choice == "4":
            while True:
                print("")
                print("1. Delete data in Aircraft table")
                print("2. Delete data in Pilot table")
                print("3. Delete data in Flight table")
                print("4. Exit")
                print("")
                choice_delete = input("Enter choice: ")

                if choice_delete == "1":
                    while True:
                        display_table_data("Aircraft")
                        aircraft_id = get_int_input("Enter the Aircraft ID of the row you want to delete: ")
                        if aircraft_id is None:
                            break
                        elif aircraft_exists(aircraft_id):
                            delete_row("Aircraft", "AircraftID", aircraft_id)
                        else:
                            print ("This ID doesn't exist.")
                            continue

                elif choice_delete == "2":
                    while True:
                        display_table_data("Pilot")
                        pilot_id = get_int_input("Enter the Pilot ID of the row you want to delete: ")
                        if pilot_id is None:
                            break
                        elif pilot_exists(pilot_id):
                            delete_row("Pilot", "PilotID", pilot_id)
                        else:
                            print ("This ID doesn't exist.")

                elif choice_delete == "3":
                    while True:
                        display_table_data("Flight")
                        flight_id = get_int_input("Enter the Flight ID of the row you want to delete: ")
                        if flight_id is None:
                            break
                        elif not flight_exists(flight_id):
                            delete_row("Flight", "FlightID", flight_id)
                        else:
                            print ("This ID doesn't exist.")

                elif choice_delete == "4":
                    break

                else:
                    print("Invalid choice. Please enter a valid option.")


        if choice == "5":
            break

menu()

# When you're ready to close the connection, it's best practice to use a try block
try:
    conn.close()
except sqlite3.Error as e:
    print("An error occurred while closing the connection:", e)
