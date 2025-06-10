

import sqlite3
import sys
from datetime import datetime, timedelta

class FlightManagementCLI:
    def __init__(self, db_path='flight_management.db'):
        """Initialize the CLI application"""
        self.db_path = db_path
        self.conn = None
        
    def connect_database(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute('PRAGMA foreign_keys = ON')
            return True
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            return False
    
    def close_database(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def display_header(self):
        """Display application header"""
        print("\n" + "=" * 60)
        print("🛩️  FLIGHT MANAGEMENT SYSTEM")
        print("=" * 60)
    
    def display_menu(self):
        """Display main menu options"""
        print("\n📋 MAIN MENU:")
        print("1. 🆕 Add a New Flight")
        print("2. 🔍 View Flights by Criteria")
        print("3. ✏️  Update Flight Information")
        print("4. 👨‍✈️ Assign Pilot to Flight")
        print("5. 📅 View Pilot Schedule")
        print("6. 🌍 View/Update Destination Information")
        print("7. 📊 View System Statistics")
        print("0. 🚪 Exit")
        print("-" * 60)
    
    def get_user_input(self, prompt, input_type=str, required=True, options=None):
        """Get validated user input"""
        while True:
            try:
                user_input = input(f"{prompt}: ").strip()
                
                if not user_input and required:
                    print("❌ This field is required. Please enter a value.")
                    continue
                
                if not user_input and not required:
                    return None
                
                if options and user_input not in options:
                    print(f"❌ Invalid option. Choose from: {', '.join(options)}")
                    continue
                
                if input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                else:
                    return user_input
                    
            except ValueError:
                print(f"❌ Invalid input. Please enter a valid {input_type.__name__}.")
    
    def validate_datetime(self, date_string):
        """Validate and parse datetime string"""
        formats = [
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_string, fmt)
                return dt.isoformat()
            except ValueError:
                continue
        
        raise ValueError("Invalid date format. Use YYYY-MM-DD HH:MM or YYYY-MM-DD")
    
    def add_new_flight(self):
        """Add a new flight to the database"""
        print("\n🆕 ADD NEW FLIGHT")
        print("-" * 30)
        
        try:
            cursor = self.conn.cursor()
            
            flight_number = self.get_user_input("Flight Number (e.g., BA123)")
            
            # Check if flight number already exists
            cursor.execute("SELECT flight_number FROM flights WHERE flight_number = ?", (flight_number,))
            if cursor.fetchone():
                print(f"❌ Flight {flight_number} already exists!")
                return
            
            departure_input = self.get_user_input("Departure Date/Time (YYYY-MM-DD HH:MM)")
            departure_time = self.validate_datetime(departure_input)
            
            arrival_input = self.get_user_input("Arrival Date/Time (YYYY-MM-DD HH:MM)")
            arrival_time = self.validate_datetime(arrival_input)
            
            aircraft_type = self.get_user_input("Aircraft Type (e.g., Boeing 737)")
            capacity = self.get_user_input("Passenger Capacity", int)
            status = self.get_user_input("Status", options=['Scheduled', 'Delayed', 'Cancelled'])
            
            # Show destinations
            print("\n🌍 Available Destinations:")
            cursor.execute("SELECT destination_id, airport_code, city_name FROM destinations")
            destinations = cursor.fetchall()
            
            for dest in destinations:
                print(f"  {dest[0]}. {dest[1]} - {dest[2]}")
            
            destination_id = self.get_user_input("Destination ID", int)
            
            # Show pilots
            print("\n👨‍✈️ Available Pilots (optional):")
            cursor.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            pilots = cursor.fetchall()
            
            for pilot in pilots:
                print(f"  {pilot[0]}. {pilot[1]} {pilot[2]}")
            
            pilot_choice = input("\nPilot ID (press Enter to skip): ").strip()
            pilot_id = int(pilot_choice) if pilot_choice else None
            
            # Insert new flight
            cursor.execute('''
                INSERT INTO flights (flight_number, departure_time, arrival_time, status, 
                                   aircraft_type, capacity, pilot_id, destination_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (flight_number, departure_time, arrival_time, status, aircraft_type, capacity, pilot_id, destination_id))
            
            self.conn.commit()
            print(f"\n✅ Flight {flight_number} added successfully!")
            
        except ValueError as e:
            print(f"❌ Input error: {e}")
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def view_flights_by_criteria(self):
        """View flights based on different criteria"""
        print("\n🔍 VIEW FLIGHTS BY CRITERIA")
        print("-" * 35)
        
        print("Search Options:")
        print("1. By Destination")
        print("2. By Status")
        print("3. All Flights")
        
        choice = self.get_user_input("Select search option", int)
        
        try:
            cursor = self.conn.cursor()
            
            if choice == 1:
                cursor.execute("SELECT airport_code, city_name FROM destinations")
                destinations = cursor.fetchall()
                print("\n🌍 Available Destinations:")
                for dest in destinations:
                    print(f"  {dest[0]} - {dest[1]}")
                
                airport_code = self.get_user_input("Enter airport code").upper()
                
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
                status = self.get_user_input("Flight Status", options=['Scheduled', 'Delayed', 'Cancelled'])
                
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
            
            if not results:
                print("   No flights found.")
                return
            
            print(f"\n📊 Found {len(results)} flight(s):")
            for i, flight in enumerate(results, 1):
                pilot_name = f"{flight[4]} {flight[5]}" if flight[4] else "Unassigned"
                print(f"{i:2d}. {flight[0]} | {flight[1]} | {flight[2]} | To: {flight[3]} | Pilot: {pilot_name}")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def update_flight_information(self):
        """Update existing flight information"""
        print("\n✏️ UPDATE FLIGHT INFORMATION")
        print("-" * 35)
        
        try:
            cursor = self.conn.cursor()
            
            # Show existing flights
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
            
            cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
            current_flight = cursor.fetchone()
            
            if not current_flight:
                print("❌ Flight not found!")
                return
            
            print("\n🔧 What would you like to update?")
            print("1. Status")
            print("2. Departure Time")
            print("3. Aircraft Type")
            
            update_choice = self.get_user_input("Select option", int)
            
            if update_choice == 1:
                new_status = self.get_user_input("New Status", options=['Scheduled', 'Delayed', 'Cancelled'])
                cursor.execute("UPDATE flights SET status = ? WHERE flight_id = ?", (new_status, flight_id))
                
            elif update_choice == 2:
                new_departure = self.get_user_input("New Departure Time (YYYY-MM-DD HH:MM)")
                departure_time = self.validate_datetime(new_departure)
                cursor.execute("UPDATE flights SET departure_time = ? WHERE flight_id = ?", (departure_time, flight_id))
                
            elif update_choice == 3:
                new_aircraft = self.get_user_input("New Aircraft Type")
                cursor.execute("UPDATE flights SET aircraft_type = ? WHERE flight_id = ?", (new_aircraft, flight_id))
            
            else:
                print("❌ Invalid option!")
                return
            
            self.conn.commit()
            print("✅ Flight updated successfully!")
            
        except ValueError as e:
            print(f"❌ Input error: {e}")
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def assign_pilot_to_flight(self):
        """Assign pilot to flight"""
        print("\n👨‍✈️ ASSIGN PILOT TO FLIGHT")
        print("-" * 30)
        
        try:
            cursor = self.conn.cursor()
            
            # Show flights
            cursor.execute('''
                SELECT f.flight_id, f.flight_number, f.departure_time, p.first_name, p.last_name
                FROM flights f
                LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
                ORDER BY f.departure_time
            ''')
            
            flights = cursor.fetchall()
            print("📋 Flights:")
            for flight in flights:
                pilot_name = f"{flight[3]} {flight[4]}" if flight[3] else "Unassigned"
                print(f"  {flight[0]}. {flight[1]} | {flight[2]} | Pilot: {pilot_name}")
            
            flight_id = self.get_user_input("\nFlight ID", int)
            
            # Show pilots
            cursor.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            pilots = cursor.fetchall()
            print("\n👨‍✈️ Available Pilots:")
            for pilot in pilots:
                print(f"  {pilot[0]}. {pilot[1]} {pilot[2]}")
            
            pilot_id = self.get_user_input("\nPilot ID", int)
            
            cursor.execute("UPDATE flights SET pilot_id = ? WHERE flight_id = ?", (pilot_id, flight_id))
            self.conn.commit()
            
            print("✅ Pilot assigned successfully!")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def view_pilot_schedule(self):
        """View pilot schedules"""
        print("\n📅 VIEW PILOT SCHEDULE")
        print("-" * 25)
        
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            pilots = cursor.fetchall()
            print("👨‍✈️ Available Pilots:")
            for pilot in pilots:
                print(f"  {pilot[0]}. {pilot[1]} {pilot[2]}")
            
            pilot_id = self.get_user_input("\nPilot ID", int)
            
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
                print(f"\n📅 Schedule:")
                for i, flight in enumerate(flights, 1):
                    print(f"{i}. {flight[0]} | {flight[1]} → {flight[2]} | {flight[3]} | To: {flight[4]}")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def view_update_destinations(self):
        """View and update destinations"""
        print("\n🌍 DESTINATION MANAGEMENT")
        print("-" * 30)
        
        try:
            cursor = self.conn.cursor()
            
            print("Options:")
            print("1. View all destinations")
            print("2. Update destination terminal info")
            
            option = self.get_user_input("Select option", int)
            
            if option == 1:
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
                cursor.execute("SELECT destination_id, airport_code, city_name, terminal_info FROM destinations")
                destinations = cursor.fetchall()
                print("\n🌍 Destinations:")
                for dest in destinations:
                    print(f"  {dest[0]}. {dest[1]} - {dest[2]} | Current Terminal: {dest[3]}")
                
                dest_id = self.get_user_input("\nDestination ID to update", int)
                new_terminal = self.get_user_input("New Terminal Information")
                
                cursor.execute("UPDATE destinations SET terminal_info = ? WHERE destination_id = ?", 
                             (new_terminal, dest_id))
                self.conn.commit()
                print("✅ Destination updated successfully!")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def view_statistics(self):
        """View system statistics"""
        print("\n📊 SYSTEM STATISTICS")
        print("-" * 25)
        
        try:
            cursor = self.conn.cursor()
            
            # Basic counts
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
            
            # Flight status breakdown
            cursor.execute("SELECT status, COUNT(*) FROM flights GROUP BY status")
            statuses = cursor.fetchall()
            print(f"\n✈️ Flight Status Breakdown:")
            for status in statuses:
                print(f"   {status[0]}: {status[1]} flights")
            
            # Top destinations
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
    
    def run(self):
        """Main application loop"""
        if not self.connect_database():
            print("❌ Failed to connect to database. Please ensure 'flight_management.db' exists.")
            print("💡 Run the database creation script first!")
            return
        
        try:
            self.display_header()
            print("🎉 Welcome to the Flight Management System!")
            
            while True:
                self.display_menu()
                
                try:
                    choice = self.get_user_input("Select an option", int)
                    
                    if choice == 0:
                        print("\n👋 Thank you for using Flight Management System!")
                        print("✈️ Safe travels!")
                        break
                    elif choice == 1:
                        self.add_new_flight()
                    elif choice == 2:
                        self.view_flights_by_criteria()
                    elif choice == 3:
                        self.update_flight_information()
                    elif choice == 4:
                        self.assign_pilot_to_flight()
                    elif choice == 5:
                        self.view_pilot_schedule()
                    elif choice == 6:
                        self.view_update_destinations()
                    elif choice == 7:
                        self.view_statistics()
                    else:
                        print("❌ Invalid option! Please choose 0-7.")
                    
                    input("\n🔄 Press Enter to continue...")
                    
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ An error occurred: {e}")
                    input("Press Enter to continue...")
        
        finally:
            self.close_database()

def main():
    """Main function to run the CLI application"""
    import os
    
    # Check if database exists
    if not os.path.exists('flight_management.db'):
        print("❌ Database file 'flight_management.db' not found!")
        print("💡 Please run the database creation script first:")
        print("   python create_clean_db.py")
        return
    
    # Run the CLI application
    app = FlightManagementCLI()
    app.run()

if __name__ == "__main__":
    main()