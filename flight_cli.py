#!/usr/bin/env python3
"""
Flight Management System - Command Line Interface
Complete CLI application for airline operations management

This module provides a comprehensive command-line interface for managing:
- Flight schedules and operations
- Pilot assignments and workload tracking  
- Destination and airport information
- System analytics and reporting

Author: [Your Name]
Course: [Course Code]
Assignment: Flight Management Database System
"""

import sqlite3
from datetime import datetime

class FlightManagementCLI:
    """
    Main CLI application class for Flight Management System
    
    Provides menu-driven interface for all database operations including
    CRUD operations for flights, pilots, and destinations.
    """
    
    def __init__(self, db_path='flight_management.db'):
        """
        Initialize CLI application with database connection parameters
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        
    def connect_database(self):
        """
        Establish connection to SQLite database
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create connection to SQLite database file
            self.conn = sqlite3.connect(self.db_path)
            # Enable foreign key constraints for data integrity
            self.conn.execute('PRAGMA foreign_keys = ON')
            return True
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            return False
    
    def close_database(self):
        """
        Close database connection safely
        Ensures proper cleanup of database resources
        """
        if self.conn:
            self.conn.close()
    
    def display_header(self):
        """
        Display application header and branding
        Creates visual separation and professional appearance
        """
        print("\n" + "=" * 60)
        print("🛩️  FLIGHT MANAGEMENT SYSTEM")
        print("=" * 60)
    
    def display_menu(self):
        """
        Display main menu options for user selection
        Each option corresponds to a major system function as required by coursework
        """
        print("\n📋 MAIN MENU:")
        print("1. 🆕 Add a New Flight")               # CRUD: Create operation
        print("2. 🔍 View Flights by Criteria")      # CRUD: Read operations with filtering
        print("3. ✏️  Update Flight Information")     # CRUD: Update operations
        print("4. 👨‍✈️ Assign Pilot to Flight")        # Relationship management
        print("5. 📅 View Pilot Schedule")           # Data retrieval and analysis
        print("6. 🌍 View/Update Destination Information")  # Destination management
        print("7. 📊 View System Statistics")        # Analytics and reporting
        print("0. 🚪 Exit")                         # Application termination
        print("-" * 60)
    
    def get_user_input(self, prompt, input_type=str, required=True, options=None):
        """
        Get validated user input with type checking and validation
        
        Args:
            prompt (str): Input prompt message to display to user
            input_type (type): Expected input type (str, int, float)
            required (bool): Whether input is mandatory
            options (list): Valid options for input validation
            
        Returns:
            Validated user input of specified type
            
        This function handles all user input validation centrally to ensure
        consistent error handling and data quality throughout the application
        """
        while True:
            try:
                user_input = input(f"{prompt}: ").strip()
                
                # Handle empty input validation
                if not user_input and required:
                    print("❌ This field is required. Please enter a value.")
                    continue
                
                # Allow empty input for optional fields
                if not user_input and not required:
                    return None
                
                # Validate against provided options (for dropdown-style inputs)
                if options and user_input not in options:
                    print(f"❌ Invalid option. Choose from: {', '.join(options)}")
                    continue
                
                # Type conversion and validation
                if input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                else:
                    return user_input
                    
            except ValueError:
                print(f"❌ Invalid input. Please enter a valid {input_type.__name__}.")
    
    def validate_datetime(self, date_string):
        """
        Validate and parse datetime string into ISO format
        
        Args:
            date_string (str): User input datetime string
            
        Returns:
            str: ISO formatted datetime string
            
        Raises:
            ValueError: If datetime format is invalid
            
        Supports multiple common datetime formats for user convenience:
        - YYYY-MM-DD HH:MM (most common)
        - YYYY-MM-DD HH:MM:SS (with seconds)
        - YYYY-MM-DD (date only, assumes midnight)
        """
        # Define supported datetime formats in order of preference
        formats = [
            '%Y-%m-%d %H:%M',      # 2024-12-25 14:30
            '%Y-%m-%d %H:%M:%S',   # 2024-12-25 14:30:00
            '%Y-%m-%d'             # 2024-12-25 (assumes midnight)
        ]
        
        # Try each format until one works
        for fmt in formats:
            try:
                dt = datetime.strptime(date_string, fmt)
                return dt.isoformat()  # Convert to ISO format for database storage
            except ValueError:
                continue
        
        # If no format matches, raise descriptive error
        raise ValueError("Invalid date format. Use YYYY-MM-DD HH:MM or YYYY-MM-DD")
    
    # =============================================================================
    # MENU OPTION 1: ADD NEW FLIGHT
    # Implements CREATE operation for flights table
    # =============================================================================
    
    def add_new_flight(self):
        """
        Add a new flight to the database with complete validation
        
        This function implements the CREATE operation for flights, collecting:
        - Flight identification (flight number)
        - Scheduling information (departure/arrival times)
        - Aircraft details (type and capacity)
        - Operational status
        - Destination assignment (required foreign key)
        - Pilot assignment (optional foreign key)
        
        Includes comprehensive validation to ensure data integrity
        """
        print("\n🆕 ADD NEW FLIGHT")
        print("-" * 30)
        
        try:
            cursor = self.conn.cursor()
            
            # Get flight number with uniqueness validation
            flight_number = self.get_user_input("Flight Number (e.g., BA123)")
            
            # Check for duplicate flight numbers (business rule enforcement)
            cursor.execute("SELECT flight_number FROM flights WHERE flight_number = ?", (flight_number,))
            if cursor.fetchone():
                print(f"❌ Flight {flight_number} already exists!")
                return
            
            # Collect and validate scheduling information
            print("\n📅 Flight Scheduling:")
            departure_input = self.get_user_input("Departure Date/Time (YYYY-MM-DD HH:MM)")
            departure_time = self.validate_datetime(departure_input)
            
            arrival_input = self.get_user_input("Arrival Date/Time (YYYY-MM-DD HH:MM)")
            arrival_time = self.validate_datetime(arrival_input)
            
            # Validate logical scheduling (arrival must be after departure)
            if datetime.fromisoformat(arrival_time) <= datetime.fromisoformat(departure_time):
                print("❌ Arrival time must be after departure time!")
                return
            
            # Collect aircraft information
            aircraft_type = self.get_user_input("Aircraft Type (e.g., Boeing 737)")
            capacity = self.get_user_input("Passenger Capacity", int)
            status = self.get_user_input("Status", options=['Scheduled', 'Delayed', 'Cancelled'])
            
            # Display available destinations for user selection
            print("\n🌍 Available Destinations:")
            cursor.execute("SELECT destination_id, airport_code, city_name FROM destinations")
            destinations = cursor.fetchall()
            
            for dest in destinations:
                print(f"  {dest[0]}. {dest[1]} - {dest[2]}")
            
            destination_id = self.get_user_input("Destination ID", int)
            
            # Validate destination exists (foreign key constraint check)
            cursor.execute("SELECT destination_id FROM destinations WHERE destination_id = ?", (destination_id,))
            if not cursor.fetchone():
                print("❌ Invalid destination ID!")
                return
            
            # Optional pilot assignment (demonstrates optional foreign key)
            print("\n👨‍✈️ Available Pilots (optional):")
            cursor.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            pilots = cursor.fetchall()
            
            for pilot in pilots:
                print(f"  {pilot[0]}. {pilot[1]} {pilot[2]}")
            
            # Allow user to skip pilot assignment
            pilot_choice = input("\nPilot ID (press Enter to skip): ").strip()
            pilot_id = int(pilot_choice) if pilot_choice else None
            
            # Validate pilot if provided
            if pilot_id:
                cursor.execute("SELECT pilot_id FROM pilots WHERE pilot_id = ?", (pilot_id,))
                if not cursor.fetchone():
                    print("❌ Invalid pilot ID! Flight will be created without pilot assignment.")
                    pilot_id = None
            
            # Insert new flight record using parameterized query (SQL injection prevention)
            cursor.execute('''
                INSERT INTO flights (flight_number, departure_time, arrival_time, status, 
                                   aircraft_type, capacity, pilot_id, destination_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (flight_number, departure_time, arrival_time, status, aircraft_type, capacity, pilot_id, destination_id))
            
            # Commit transaction to make changes permanent
            self.conn.commit()
            print(f"\n✅ Flight {flight_number} added successfully!")
            
        except ValueError as e:
            # Handle datetime validation errors
            print(f"❌ Input error: {e}")
        except sqlite3.Error as e:
            # Handle database errors (constraints, connection issues, etc.)
            print(f"❌ Database error: {e}")
    
    # =============================================================================
    # MENU OPTION 2: VIEW FLIGHTS BY CRITERIA
    # Implements READ operations with various filtering options
    # =============================================================================
    
    def view_flights_by_criteria(self):
        """
        View flights based on different search criteria
        
        This function demonstrates various SQL query patterns including:
        - JOIN operations to combine related tables
        - WHERE clauses for filtering
        - ORDER BY for result sorting
        - Handling of NULL values in optional relationships
        
        Provides multiple search options as required by coursework:
        - By destination (demonstrates foreign key relationships)
        - By operational status (demonstrates enumerated values)
        - All flights (comprehensive view with all relationships)
        """
        print("\n🔍 VIEW FLIGHTS BY CRITERIA")
        print("-" * 35)
        
        # Present search options to user
        print("Search Options:")
        print("1. By Destination")    # Demonstrates JOIN with destinations table
        print("2. By Status")         # Demonstrates filtering by enumerated values
        print("3. All Flights")       # Demonstrates comprehensive data retrieval
        
        choice = self.get_user_input("Select search option", int)
        
        try:
            cursor = self.conn.cursor()
            
            if choice == 1:
                # Search by destination - demonstrates JOIN operations
                cursor.execute("SELECT airport_code, city_name FROM destinations")
                destinations = cursor.fetchall()
                print("\n🌍 Available Destinations:")
                for dest in destinations:
                    print(f"  {dest[0]} - {dest[1]}")
                
                airport_code = self.get_user_input("Enter airport code").upper()
                
                # Complex JOIN query combining flights, destinations, and pilots
                cursor.execute('''
                    SELECT f.flight_number, f.departure_time, f.status, d.city_name,
                           p.first_name, p.last_name
                    FROM flights f
                    JOIN destinations d ON f.destination_id = d.destination_id
                    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
                    WHERE d.airport_code = ?
                    ORDER BY f.departure_time
                ''', (airport_code,))
                
                results = cursor.fetchall()
                print(f"\n✈️ Flights to {airport_code}:")
                
            elif choice == 2:
                # Search by status - demonstrates filtering with enumerated values
                status = self.get_user_input("Flight Status", options=['Scheduled', 'Delayed', 'Cancelled'])
                
                # JOIN query with status filtering
                cursor.execute('''
                    SELECT f.flight_number, f.departure_time, d.city_name, d.airport_code,
                           p.first_name, p.last_name
                    FROM flights f
                    JOIN destinations d ON f.destination_id = d.destination_id
                    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
                    WHERE f.status = ?
                    ORDER BY f.departure_time
                ''', (status,))
                
                results = cursor.fetchall()
                print(f"\n✈️ {status} Flights:")
                
            elif choice == 3:
                # All flights - comprehensive view demonstrating LEFT JOIN for optional relationships
                cursor.execute('''
                    SELECT f.flight_number, f.departure_time, f.status, d.city_name, d.airport_code,
                           p.first_name, p.last_name
                    FROM flights f
                    JOIN destinations d ON f.destination_id = d.destination_id
                    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
                    ORDER BY f.departure_time
                ''')
                
                results = cursor.fetchall()
                print(f"\n✈️ All Flights:")
            
            else:
                print("❌ Invalid option!")
                return
            
            # Display results with proper NULL handling
            if not results:
                print("   No flights found.")
                return
            
            print(f"\n📊 Found {len(results)} flight(s):")
            for i, flight in enumerate(results, 1):
                # Handle NULL pilot assignments gracefully
                pilot_name = f"{flight[4]} {flight[5]}" if flight[4] else "Unassigned"
                print(f"{i:2d}. {flight[0]} | {flight[1]} | {flight[2]} | To: {flight[3]} | Pilot: {pilot_name}")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    # =============================================================================
    # MENU OPTION 3: UPDATE FLIGHT INFORMATION
    # Implements UPDATE operations for schedule modifications
    # =============================================================================
    
    def update_flight_information(self):
        """
        Update existing flight information with validation
        
        This function demonstrates UPDATE operations including:
        - Record selection and validation
        - Partial updates (updating specific fields)
        - Data validation for updates
        - Transaction commit for persistence
        
        Allows modification of key flight attributes as required by coursework:
        - Flight status (operational changes)
        - Departure time (schedule modifications)
        - Aircraft type (equipment changes)
        """
        print("\n✏️ UPDATE FLIGHT INFORMATION")
        print("-" * 35)
        
        try:
            cursor = self.conn.cursor()
            
            # Display existing flights for user selection
            cursor.execute('''
                SELECT f.flight_id, f.flight_number, f.departure_time, f.status
                FROM flights f
                ORDER BY f.departure_time
            ''')
            
            flights = cursor.fetchall()
            if not flights:
                print("No flights found.")
                return
            
            print("📋 Existing Flights:")
            for flight in flights:
                print(f"  {flight[0]}. {flight[1]} | {flight[2]} | {flight[3]}")
            
            flight_id = self.get_user_input("\nFlight ID to update", int)
            
            # Verify flight exists before attempting update
            cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
            current_flight = cursor.fetchone()
            
            if not current_flight:
                print("❌ Flight not found!")
                return
            
            # Present update options
            print("\n🔧 What would you like to update?")
            print("1. Status")           # Most common operational update
            print("2. Departure Time")   # Schedule modification
            print("3. Aircraft Type")    # Equipment change
            
            update_choice = self.get_user_input("Select option", int)
            
            # Execute specific update based on user choice
            if update_choice == 1:
                # Update flight status - demonstrates enumerated value updates
                new_status = self.get_user_input("New Status", options=['Scheduled', 'Delayed', 'Cancelled'])
                cursor.execute("UPDATE flights SET status = ? WHERE flight_id = ?", (new_status, flight_id))
                
            elif update_choice == 2:
                # Update departure time - demonstrates datetime validation in updates
                new_departure = self.get_user_input("New Departure Time (YYYY-MM-DD HH:MM)")
                departure_time = self.validate_datetime(new_departure)
                cursor.execute("UPDATE flights SET departure_time = ? WHERE flight_id = ?", (departure_time, flight_id))
                
            elif update_choice == 3:
                # Update aircraft type - demonstrates text field updates
                new_aircraft = self.get_user_input("New Aircraft Type")
                cursor.execute("UPDATE flights SET aircraft_type = ? WHERE flight_id = ?", (new_aircraft, flight_id))
            
            else:
                print("❌ Invalid option!")
                return
            
            # Commit transaction to make changes permanent
            self.conn.commit()
            print("✅ Flight updated successfully!")
            
        except ValueError as e:
            # Handle validation errors (e.g., invalid datetime format)
            print(f"❌ Input error: {e}")
        except sqlite3.Error as e:
            # Handle database errors (e.g., constraint violations)
            print(f"❌ Database error: {e}")
    
    # =============================================================================
    # MENU OPTION 4: ASSIGN PILOT TO FLIGHT
    # Implements relationship management between pilots and flights
    # =============================================================================
    
    def assign_pilot_to_flight(self):
        """
        Assign or reassign pilots to flights
        
        This function demonstrates:
        - Foreign key relationship management
        - UPDATE operations on relationship fields
        - Data validation for foreign key constraints
        - LEFT JOIN queries to show current assignments
        
        Supports pilot assignment as required by coursework specification
        """
        print("\n👨‍✈️ ASSIGN PILOT TO FLIGHT")
        print("-" * 30)
        
        try:
            cursor = self.conn.cursor()
            
            # Display flights with current pilot assignments using LEFT JOIN
            cursor.execute('''
                SELECT f.flight_id, f.flight_number, f.departure_time, p.first_name, p.last_name
                FROM flights f
                LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
                ORDER BY f.departure_time
            ''')
            
            flights = cursor.fetchall()
            print("📋 Flights:")
            for flight in flights:
                # Handle NULL pilot assignments
                pilot_name = f"{flight[3]} {flight[4]}" if flight[3] else "Unassigned"
                print(f"  {flight[0]}. {flight[1]} | {flight[2]} | Pilot: {pilot_name}")
            
            flight_id = self.get_user_input("\nFlight ID", int)
            
            # Validate flight exists
            cursor.execute("SELECT flight_number FROM flights WHERE flight_id = ?", (flight_id,))
            if not cursor.fetchone():
                print("❌ Flight not found!")
                return
            
            # Display available pilots
            cursor.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            pilots = cursor.fetchall()
            print("\n👨‍✈️ Available Pilots:")
            for pilot in pilots:
                print(f"  {pilot[0]}. {pilot[1]} {pilot[2]}")
            
            pilot_id = self.get_user_input("\nPilot ID", int)
            
            # Validate pilot exists (foreign key constraint)
            cursor.execute("SELECT first_name, last_name FROM pilots WHERE pilot_id = ?", (pilot_id,))
            pilot_result = cursor.fetchone()
            if not pilot_result:
                print("❌ Pilot not found!")
                return
            
            # Update flight with pilot assignment (foreign key update)
            cursor.execute("UPDATE flights SET pilot_id = ? WHERE flight_id = ?", (pilot_id, flight_id))
            self.conn.commit()
            
            print("✅ Pilot assigned successfully!")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    # =============================================================================
    # MENU OPTION 5: VIEW PILOT SCHEDULE
    # Implements pilot schedule retrieval and workload analysis
    # =============================================================================
    
    def view_pilot_schedule(self):
        """
        View pilot schedules and workload information
        
        This function demonstrates:
        - Complex JOIN queries across multiple tables
        - Data aggregation and analysis
        - Handling of pilots with no flight assignments
        
        Provides pilot schedule viewing as required by coursework
        """
        print("\n📅 VIEW PILOT SCHEDULE")
        print("-" * 25)
        
        try:
            cursor = self.conn.cursor()
            
            # Display available pilots
            cursor.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            pilots = cursor.fetchall()
            print("👨‍✈️ Available Pilots:")
            for pilot in pilots:
                print(f"  {pilot[0]}. {pilot[1]} {pilot[2]}")
            
            pilot_id = self.get_user_input("\nPilot ID", int)
            
            # Validate pilot exists
            cursor.execute("SELECT first_name, last_name FROM pilots WHERE pilot_id = ?", (pilot_id,))
            pilot_info = cursor.fetchone()
            if not pilot_info:
                print("❌ Pilot not found!")
                return
            
            # Retrieve pilot's flight schedule using JOIN operations
            cursor.execute('''
                SELECT f.flight_number, f.departure_time, f.arrival_time, f.status, d.city_name
                FROM flights f
                JOIN destinations d ON f.destination_id = d.destination_id
                WHERE f.pilot_id = ?
                ORDER BY f.departure_time
            ''', (pilot_id,))
            
            flights = cursor.fetchall()
            if not flights:
                print("No flights assigned to this pilot.")
            else:
                print(f"\n📅 Schedule for {pilot_info[0]} {pilot_info[1]}:")
                for i, flight in enumerate(flights, 1):
                    print(f"{i}. {flight[0]} | {flight[1]} → {flight[2]} | {flight[3]} | To: {flight[4]}")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    # =============================================================================
    # MENU OPTION 6: VIEW/UPDATE DESTINATION INFORMATION
    # Implements destination management functionality
    # =============================================================================
    
    def view_update_destinations(self):
        """
        View and update destination information
        
        This function demonstrates:
        - Complex queries with aggregation (COUNT function)
        - LEFT JOIN to include destinations without flights
        - UPDATE operations on destination data
        - GROUP BY operations for statistical analysis
        
        Provides destination management as required by coursework
        """
        print("\n🌍 DESTINATION MANAGEMENT")
        print("-" * 30)
        
        try:
            cursor = self.conn.cursor()
            
            print("Options:")
            print("1. View all destinations")        # READ operation with aggregation
            print("2. Update destination terminal info")  # UPDATE operation
            
            option = self.get_user_input("Select option", int)
            
            if option == 1:
                # Complex query demonstrating LEFT JOIN and GROUP BY
                cursor.execute('''
                    SELECT d.destination_id, d.airport_code, d.city_name, d.country, 
                           d.terminal_info, COUNT(f.flight_id) as flight_count
                    FROM destinations d
                    LEFT JOIN flights f ON d.destination_id = f.destination_id
                    GROUP BY d.destination_id
                    ORDER BY d.city_name
                ''')
                
                destinations = cursor.fetchall()
                print(f"\n🌍 All Destinations:")
                for dest in destinations:
                    print(f"{dest[0]}. {dest[1]} - {dest[2]}, {dest[3]} | Terminal: {dest[4]} | Flights: {dest[5]}")
                
            elif option == 2:
                # Display destinations for selection
                cursor.execute("SELECT destination_id, airport_code, city_name, terminal_info FROM destinations")
                destinations = cursor.fetchall()
                print("\n🌍 Destinations:")
                for dest in destinations:
                    print(f"  {dest[0]}. {dest[1]} - {dest[2]} | Current Terminal: {dest[3]}")
                
                dest_id = self.get_user_input("\nDestination ID to update", int)
                
                # Validate destination exists
                cursor.execute("SELECT destination_id FROM destinations WHERE destination_id = ?", (dest_id,))
                if not cursor.fetchone():
                    print("❌ Destination not found!")
                    return
                
                new_terminal = self.get_user_input("New Terminal Information")
                
                # Execute UPDATE operation
                cursor.execute("UPDATE destinations SET terminal_info = ? WHERE destination_id = ?", 
                             (new_terminal, dest_id))
                self.conn.commit()
                print("✅ Destination updated successfully!")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    # =============================================================================
    # MENU OPTION 7: VIEW SYSTEM STATISTICS
    # Implements analytics and reporting functionality
    # =============================================================================
    
    def view_statistics(self):
        """
        View comprehensive system statistics and analytics
        
        This function demonstrates:
        - Aggregate functions (COUNT, GROUP BY)
        - Complex analytical queries
        - Data summarization and reporting
        - Multiple table relationships
        
        Provides system analytics for operational insights
        """
        print("\n📊 SYSTEM STATISTICS")
        print("-" * 25)
        
        try:
            cursor = self.conn.cursor()
            
            # Basic record counts using COUNT aggregate function
            cursor.execute("SELECT COUNT(*) FROM pilots")
            pilot_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM destinations")
            dest_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM flights")
            flight_count = cursor.fetchone()[0]
            
            print(f"📊 Database Summary:")
            print(f"   👨‍✈️ Total Pilots: {pilot_count}")
            print(f"   🌍 Total Destinations: {dest_count}")
            print(f"   ✈️ Total Flights: {flight_count}")
            
            # Flight status breakdown using GROUP BY
            cursor.execute("SELECT status, COUNT(*) FROM flights GROUP BY status")
            statuses = cursor.fetchall()
            print(f"\n✈️ Flight Status Breakdown:")
            for status in statuses:
                print(f"   {status[0]}: {status[1]} flights")
            
            # Top destinations analysis using complex JOIN and aggregation
            cursor.execute('''
                SELECT d.city_name, d.airport_code, COUNT(f.flight_id) as flight_count
                FROM destinations d
                LEFT JOIN flights f ON d.destination_id = f.destination_id
                GROUP BY d.destination_id
                ORDER BY flight_count DESC
                LIMIT 5
            ''')
            top_destinations = cursor.fetchall()
            print(f"\n🌍 Top Destinations:")
            for dest in top_destinations:
                print(f"   {dest[0]} ({dest[1]}): {dest[2]} flights")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    # =============================================================================
    # MAIN APPLICATION RUNNER
    # Controls overall application flow and user interaction
    # =============================================================================
    
    def run(self):
        """
        Main application loop
        
        This method handles:
        - Database connection management
        - Menu display and user interaction
        - Error handling and graceful shutdown
        - User session management
        
        Implements the main control flow for the CLI application
        """
        # Attempt to establish database connection
        if not self.connect_database():
            print("❌ Failed to connect to database. Please ensure 'flight_management.db' exists.")
            print("💡 Run the database creation script first!")
            return
        
        try:
            # Display welcome message and initialize user session
            self.display_header()
            print("🎉 Welcome to the Flight Management System!")
            
            # Main application loop - continues until user exits
            while True:
                # Display menu and get user choice
                self.display_menu()
                
                try:
                    choice = self.get_user_input("Select an option", int)
                    
                    # Handle user selection with appropriate function calls
                    if choice == 0:
                        # Exit application gracefully
                        print("\n👋 Thank you for using Flight Management System!")
                        print("✈️ Safe travels!")
                        break
                    elif choice == 1:
                        # Menu Option 1: Add new flight (CREATE operation)
                        self.add_new_flight()
                    elif choice == 2:
                        # Menu Option 2: View flights by criteria (READ operations)
                        self.view_flights_by_criteria()
                    elif choice == 3:
                        # Menu Option 3: Update flight information (UPDATE operations)
                        self.update_flight_information()
                    elif choice == 4:
                        # Menu Option 4: Assign pilot to flight (relationship management)
                        self.assign_pilot_to_flight()
                    elif choice == 5:
                        # Menu Option 5: View pilot schedule (data analysis)
                        self.view_pilot_schedule()
                    elif choice == 6:
                        # Menu Option 6: Destination management
                        self.view_update_destinations()
                    elif choice == 7:
                        # Menu Option 7: System statistics and analytics
                        self.view_statistics()
                    else:
                        # Handle invalid menu selections
                        print("❌ Invalid option! Please choose 0-7.")
                    
                    # Pause for user to review results before continuing
                    input("\n🔄 Press Enter to continue...")
                    
                except KeyboardInterrupt:
                    # Handle Ctrl+C gracefully
                    print("\n\n👋 Goodbye!")
                    break
                except Exception as e:
                    # Handle unexpected errors gracefully
                    print(f"❌ An error occurred: {e}")
                    input("Press Enter to continue...")
        
        finally:
            # Ensure database connection is properly closed regardless of how loop exits
            # This is critical for preventing database locks and resource leaks
            self.close_database()

def main():
    """
    Main function to run the CLI application
    
    This function serves as the entry point for the application and performs:
    - Initial system checks and validation
    - Database file existence verification
    - Application initialization and launch
    - Error handling for startup issues
    
    Called when script is run directly (if __name__ == "__main__")
    """
    import os
    
    print("🛩️ Flight Management System - Starting Up...")
    
    # Check if database file exists before attempting to run application
    # This prevents confusing error messages and provides helpful guidance
    if not os.path.exists('flight_management.db'):
        print("❌ Database file 'flight_management.db' not found!")
        print("💡 Please run the database creation script first:")
        print("   python create_clean_db.py")
        print("\n📋 Or make sure you're in the correct directory with the database file.")
        return
    
    print("✅ Database found. Initializing CLI application...")
    
    # Create and run the CLI application instance
    try:
        app = FlightManagementCLI()
        app.run()
    except Exception as e:
        # Handle any unexpected errors during application startup
        print(f"❌ Failed to start application: {e}")
        print("💡 Please check your database file and try again.")

# Python idiom: only run main() when script is executed directly
# This allows the module to be imported without automatically running the application
if __name__ == "__main__":
    main()