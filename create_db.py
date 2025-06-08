import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    """Create the Flight Management Database with all tables and sample data"""
    
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect('flight_management.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist (for clean setup)
    cursor.execute('DROP TABLE IF EXISTS flights')
    cursor.execute('DROP TABLE IF EXISTS pilots')
    cursor.execute('DROP TABLE IF EXISTS destinations')
    
    print("Creating Flight Management Database...")
    
    # CREATE TABLES
    
    # 1. Create DESTINATIONS table
    cursor.execute('''
        CREATE TABLE destinations (
            destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_code VARCHAR(3) UNIQUE NOT NULL,
            city_name VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL,
            timezone VARCHAR(20) NOT NULL,
            terminal_info VARCHAR(100)
        )
    ''')
    
    # 2. Create PILOTS table
    cursor.execute('''
        CREATE TABLE pilots (
            pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            license_no VARCHAR(20) UNIQUE NOT NULL,
            experience_years INTEGER NOT NULL,
            phone VARCHAR(15)
        )
    ''')
    
    # 3. Create FLIGHTS table
    cursor.execute('''
        CREATE TABLE flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number VARCHAR(10) UNIQUE NOT NULL,
            departure_time DATETIME NOT NULL,
            arrival_time DATETIME NOT NULL,
            status VARCHAR(20) DEFAULT 'Scheduled',
            aircraft_type VARCHAR(30) NOT NULL,
            capacity INTEGER NOT NULL,
            pilot_id INTEGER,
            destination_id INTEGER NOT NULL,
            FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id),
            FOREIGN KEY (destination_id) REFERENCES destinations(destination_id)
        )
    ''')
    
    print("Tables created successfully!")
    
    # POPULATE TABLES WITH SAMPLE DATA
    
    # Insert sample DESTINATIONS (15 records)
    destinations_data = [
        ('LHR', 'London', 'United Kingdom', 'GMT+0', 'Terminal 5'),
        ('JFK', 'New York', 'United States', 'EST-5', 'Terminal 4'),
        ('CDG', 'Paris', 'France', 'CET+1', 'Terminal 2E'),
        ('DXB', 'Dubai', 'United Arab Emirates', 'GST+4', 'Terminal 3'),
        ('NRT', 'Tokyo', 'Japan', 'JST+9', 'Terminal 1'),
        ('LAX', 'Los Angeles', 'United States', 'PST-8', 'Terminal B'),
        ('FRA', 'Frankfurt', 'Germany', 'CET+1', 'Terminal 1'),
        ('SIN', 'Singapore', 'Singapore', 'SGT+8', 'Terminal 3'),
        ('SYD', 'Sydney', 'Australia', 'AEST+10', 'Terminal 1'),
        ('HKG', 'Hong Kong', 'Hong Kong', 'HKT+8', 'Terminal 1'),
        ('MAD', 'Madrid', 'Spain', 'CET+1', 'Terminal 4'),
        ('AMS', 'Amsterdam', 'Netherlands', 'CET+1', 'Terminal 3'),
        ('ZUR', 'Zurich', 'Switzerland', 'CET+1', 'Terminal A'),
        ('BOM', 'Mumbai', 'India', 'IST+5:30', 'Terminal 2'),
        ('YYZ', 'Toronto', 'Canada', 'EST-5', 'Terminal 1')
    ]
    
    cursor.executemany('''
        INSERT INTO destinations (airport_code, city_name, country, timezone, terminal_info)
        VALUES (?, ?, ?, ?, ?)
    ''', destinations_data)
    
    # Insert sample PILOTS (12 records)
    pilots_data = [
        ('John', 'Smith', 'ATP001234', 15, '+44-20-1234-5678'),
        ('Sarah', 'Johnson', 'ATP002345', 12, '+44-20-2345-6789'),
        ('Michael', 'Brown', 'ATP003456', 8, '+44-20-3456-7890'),
        ('Emma', 'Davis', 'ATP004567', 10, '+44-20-4567-8901'),
        ('James', 'Wilson', 'ATP005678', 20, '+44-20-5678-9012'),
        ('Lisa', 'Taylor', 'ATP006789', 7, '+44-20-6789-0123'),
        ('David', 'Anderson', 'ATP007890', 18, '+44-20-7890-1234'),
        ('Rachel', 'Thomas', 'ATP008901', 9, '+44-20-8901-2345'),
        ('Robert', 'Jackson', 'ATP009012', 13, '+44-20-9012-3456'),
        ('Helen', 'White', 'ATP010123', 11, '+44-20-0123-4567'),
        ('Mark', 'Harris', 'ATP011234', 16, '+44-20-1234-5670'),
        ('Anna', 'Martin', 'ATP012345', 6, '+44-20-2345-6701')
    ]
    
    cursor.executemany('''
        INSERT INTO pilots (first_name, last_name, license_no, experience_years, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', pilots_data)
    
    # Insert sample FLIGHTS (15 records)
    # Generate realistic flight data
    base_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    flights_data = [
        ('BA101', base_date + timedelta(hours=2), base_date + timedelta(hours=4), 'Scheduled', 'Boeing 737', 180, 1, 1),
        ('BA102', base_date + timedelta(hours=6), base_date + timedelta(hours=14), 'Scheduled', 'Airbus A350', 300, 2, 2),
        ('BA103', base_date + timedelta(hours=10), base_date + timedelta(hours=12), 'Delayed', 'Boeing 777', 350, 3, 3),
        ('BA104', base_date + timedelta(hours=14), base_date + timedelta(hours=22), 'Scheduled', 'Airbus A380', 500, 4, 4),
        ('BA105', base_date + timedelta(hours=18), base_date + timedelta(hours=30), 'Scheduled', 'Boeing 787', 250, 5, 5),
        ('BA106', base_date + timedelta(days=1, hours=2), base_date + timedelta(days=1, hours=14), 'Scheduled', 'Airbus A320', 150, 6, 6),
        ('BA107', base_date + timedelta(days=1, hours=6), base_date + timedelta(days=1, hours=8), 'Scheduled', 'Boeing 737', 180, 7, 7),
        ('BA108', base_date + timedelta(days=1, hours=10), base_date + timedelta(days=1, hours=18), 'Cancelled', 'Airbus A330', 280, 8, 8),
        ('BA109', base_date + timedelta(days=1, hours=14), base_date + timedelta(days=2, hours=2), 'Scheduled', 'Boeing 777', 350, 9, 9),
        ('BA110', base_date + timedelta(days=1, hours=18), base_date + timedelta(days=2, hours=6), 'Scheduled', 'Airbus A350', 300, 10, 10),
        ('BA111', base_date + timedelta(days=2, hours=2), base_date + timedelta(days=2, hours=4), 'Scheduled', 'Boeing 737', 180, 11, 11),
        ('BA112', base_date + timedelta(days=2, hours=6), base_date + timedelta(days=2, hours=8), 'Scheduled', 'Airbus A320', 150, 12, 12),
        ('BA113', base_date + timedelta(days=2, hours=10), base_date + timedelta(days=2, hours=12), 'Scheduled', 'Boeing 787', 250, 1, 13),
        ('BA114', base_date + timedelta(days=2, hours=14), base_date + timedelta(days=3, hours=2), 'Scheduled', 'Airbus A380', 500, 2, 14),
        ('BA115', base_date + timedelta(days=2, hours=18), base_date + timedelta(days=3, hours=6), 'Delayed', 'Boeing 777', 350, 3, 15)
    ]
    
    cursor.executemany('''
        INSERT INTO flights (flight_number, departure_time, arrival_time, status, aircraft_type, capacity, pilot_id, destination_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', flights_data)
    
    # Commit changes
    conn.commit()
    print(f"Database populated with:")
    print(f"- {len(destinations_data)} destinations")
    print(f"- {len(pilots_data)} pilots")
    print(f"- {len(flights_data)} flights")
    
    return conn

def demonstrate_queries():
    """Demonstrate all required SQL queries"""
    
    conn = sqlite3.connect('flight_management.db')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("FLIGHT MANAGEMENT SYSTEM - SQL QUERY DEMONSTRATIONS")
    print("="*60)
    
    # 1. FLIGHT RETRIEVAL QUERIES
    print("\n1. FLIGHT RETRIEVAL QUERIES")
    print("-" * 30)
    
    # 1a. Retrieve flights by destination
    print("\n1a. Flights to London (LHR):")
    cursor.execute('''
        SELECT f.flight_number, f.departure_time, f.arrival_time, f.status, 
               d.city_name, d.airport_code
        FROM flights f
        JOIN destinations d ON f.destination_id = d.destination_id
        WHERE d.airport_code = 'LHR'
    ''')
    for row in cursor.fetchall():
        print(f"Flight {row[0]}: {row[1]} -> {row[2]} | Status: {row[3]} | To: {row[4]} ({row[5]})")
    
    # 1b. Retrieve flights by status
    print("\n1b. All Delayed Flights:")
    cursor.execute('''
        SELECT f.flight_number, f.departure_time, f.status, 
               d.city_name, p.first_name, p.last_name
        FROM flights f
        JOIN destinations d ON f.destination_id = d.destination_id
        JOIN pilots p ON f.pilot_id = p.pilot_id
        WHERE f.status = 'Delayed'
    ''')
    for row in cursor.fetchall():
        print(f"Flight {row[0]}: {row[1]} | Status: {row[2]} | To: {row[3]} | Pilot: {row[4]} {row[5]}")
    
    # 1c. Retrieve flights by departure date
    print("\n1c. Flights departing today:")
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT f.flight_number, f.departure_time, f.arrival_time, 
               d.city_name, f.aircraft_type
        FROM flights f
        JOIN destinations d ON f.destination_id = d.destination_id
        WHERE DATE(f.departure_time) = DATE('now')
        ORDER BY f.departure_time
    ''')
    for row in cursor.fetchall():
        print(f"Flight {row[0]}: {row[1]} -> {row[2]} | To: {row[3]} | Aircraft: {row[4]}")
    
    # 2. SCHEDULE MODIFICATION QUERIES
    print("\n\n2. SCHEDULE MODIFICATION QUERIES")
    print("-" * 32)
    
    # 2a. Update departure time
    print("\n2a. Updating flight BA103 departure time...")
    new_departure = datetime.now() + timedelta(hours=12)
    cursor.execute('''
        UPDATE flights 
        SET departure_time = ? 
        WHERE flight_number = 'BA103'
    ''', (new_departure,))
    
    # Verify the update
    cursor.execute('''
        SELECT flight_number, departure_time, status 
        FROM flights 
        WHERE flight_number = 'BA103'
    ''')
    row = cursor.fetchone()
    print(f"Updated: Flight {row[0]} - New departure: {row[1]} | Status: {row[2]}")
    
    # 2b. Update flight status
    print("\n2b. Updating flight BA108 status from Cancelled to Scheduled...")
    cursor.execute('''
        UPDATE flights 
        SET status = 'Scheduled' 
        WHERE flight_number = 'BA108'
    ''')
    
    cursor.execute('''
        SELECT flight_number, status, departure_time 
        FROM flights 
        WHERE flight_number = 'BA108'
    ''')
    row = cursor.fetchone()
    print(f"Updated: Flight {row[0]} - Status: {row[1]} | Departure: {row[2]}")
    
    # 3. PILOT ASSIGNMENT QUERIES
    print("\n\n3. PILOT ASSIGNMENT QUERIES")
    print("-" * 27)
    
    # 3a. Assign pilot to flight
    print("\n3a. Assigning pilot John Smith to flight BA115...")
    cursor.execute('''
        UPDATE flights 
        SET pilot_id = (SELECT pilot_id FROM pilots WHERE first_name = 'John' AND last_name = 'Smith')
        WHERE flight_number = 'BA115'
    ''')
    
    # 3b. Retrieve pilot schedules
    print("\n3b. John Smith's Flight Schedule:")
    cursor.execute('''
        SELECT f.flight_number, f.departure_time, f.arrival_time, 
               d.city_name, f.status
        FROM flights f
        JOIN destinations d ON f.destination_id = d.destination_id
        JOIN pilots p ON f.pilot_id = p.pilot_id
        WHERE p.first_name = 'John' AND p.last_name = 'Smith'
        ORDER BY f.departure_time
    ''')
    for row in cursor.fetchall():
        print(f"Flight {row[0]}: {row[1]} -> {row[2]} | To: {row[3]} | Status: {row[4]}")
    
    # 3c. All pilots and their assigned flights count
    print("\n3c. All Pilots and Their Flight Assignments:")
    cursor.execute('''
        SELECT p.first_name, p.last_name, p.license_no, 
               COUNT(f.flight_id) as flights_assigned
        FROM pilots p
        LEFT JOIN flights f ON p.pilot_id = f.pilot_id
        GROUP BY p.pilot_id
        ORDER BY flights_assigned DESC
    ''')
    for row in cursor.fetchall():
        print(f"Pilot: {row[0]} {row[1]} | License: {row[2]} | Flights Assigned: {row[3]}")
    
    # 4. DESTINATION MANAGEMENT QUERIES
    print("\n\n4. DESTINATION MANAGEMENT QUERIES")
    print("-" * 33)
    
    # 4a. View all destinations
    print("\n4a. All Destinations:")
    cursor.execute('''
        SELECT airport_code, city_name, country, timezone, terminal_info
        FROM destinations
        ORDER BY country, city_name
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]} - {row[1]}, {row[2]} | Timezone: {row[3]} | Terminal: {row[4]}")
    
    # 4b. Update destination information
    print("\n4b. Updating terminal info for Dubai (DXB)...")
    cursor.execute('''
        UPDATE destinations 
        SET terminal_info = 'Terminal 3 - Concourse A' 
        WHERE airport_code = 'DXB'
    ''')
    
    cursor.execute('''
        SELECT airport_code, city_name, terminal_info 
        FROM destinations 
        WHERE airport_code = 'DXB'
    ''')
    row = cursor.fetchone()
    print(f"Updated: {row[0]} - {row[1]} | New Terminal Info: {row[2]}")
    
    # 5. SUMMARY QUERIES
    print("\n\n5. SUMMARY QUERIES")
    print("-" * 17)
    
    # 5a. Number of flights to each destination
    print("\n5a. Flights Count by Destination:")
    cursor.execute('''
        SELECT d.city_name, d.airport_code, COUNT(f.flight_id) as flight_count
        FROM destinations d
        LEFT JOIN flights f ON d.destination_id = f.destination_id
        GROUP BY d.destination_id
        ORDER BY flight_count DESC, d.city_name
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]} ({row[1]}): {row[2]} flights")
    
    # 5b. Number of flights assigned to each pilot
    print("\n5b. Flights Assigned per Pilot:")
    cursor.execute('''
        SELECT p.first_name, p.last_name, COUNT(f.flight_id) as flights_assigned,
               p.experience_years
        FROM pilots p
        LEFT JOIN flights f ON p.pilot_id = f.pilot_id
        GROUP BY p.pilot_id
        ORDER BY flights_assigned DESC, p.experience_years DESC
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]} {row[1]}: {row[2]} flights | Experience: {row[3]} years")
    
    # 5c. Flight status summary
    print("\n5c. Flight Status Summary:")
    cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM flights
        GROUP BY status
        ORDER BY count DESC
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} flights")
    
    # 5d. Aircraft type usage
    print("\n5d. Aircraft Type Usage:")
    cursor.execute('''
        SELECT aircraft_type, COUNT(*) as usage_count, 
               AVG(capacity) as avg_capacity
        FROM flights
        GROUP BY aircraft_type
        ORDER BY usage_count DESC
    ''')
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} flights | Avg Capacity: {row[2]:.0f}")
    
    # 5e. Upcoming flights (next 24 hours)
    print("\n5e. Upcoming Flights (Next 24 Hours):")
    cursor.execute('''
        SELECT f.flight_number, f.departure_time, d.city_name, 
               p.first_name, p.last_name, f.status
        FROM flights f
        JOIN destinations d ON f.destination_id = d.destination_id
        JOIN pilots p ON f.pilot_id = p.pilot_id
        WHERE f.departure_time BETWEEN datetime('now') AND datetime('now', '+1 day')
        ORDER BY f.departure_time
    ''')
    for row in cursor.fetchall():
        print(f"Flight {row[0]}: {row[1]} | To: {row[2]} | Pilot: {row[3]} {row[4]} | Status: {row[5]}")
    
    # Commit any changes and close
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("All queries executed successfully!")
    print("Database file 'flight_management.db' created and populated.")
    print("="*60)

if __name__ == "__main__":
    # Create and populate the database
    conn = create_database()
    conn.close()
    
    # Demonstrate all the required SQL queries
    demonstrate_queries()
    
    print("\n\nDatabase Setup Complete!")
    print("You can now use this database with your Python CLI application.")
    print("\nKey features implemented:")
    print("✓ Three main tables: pilots, flights, destinations")
    print("✓ 15 destinations, 12 pilots, 15 flights with sample data")
    print("✓ All required query types demonstrated")
    print("✓ Foreign key relationships properly established")
    print("✓ Comprehensive test data for development and testing")