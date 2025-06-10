# Flight Management System

A comprehensive command-line interface application for managing airline flights, pilots, and destinations using SQLite database.

## Features

- Add new flights with complete scheduling information
- View flights by multiple criteria (destination, status, date)
- Update flight information and schedules
- Assign pilots to flights with workload tracking
- View detailed pilot schedules and availability
- Manage destination information and terminal details
- Comprehensive system statistics and analytics

## Installation

1. Clone this repository
2. Install Python 3.7+ if not already installed
3. Run the database setup script
4. Launch the CLI application

## Usage

### Initial Setup
```bash
# Create the database with sample data
python create_db.py

# Launch the CLI application
python flight_cli.py
Menu Options

Add a New Flight - Create new flight entries with scheduling
View Flights by Criteria - Search and filter flights
Update Flight Information - Modify existing flight details
Assign Pilot to Flight - Manage pilot-flight assignments
View Pilot Schedule - Display pilot workloads and schedules
View/Update Destination Information - Manage airport data
View System Statistics - Database analytics and summaries

Database Schema
The system uses three main tables:

pilots - Pilot credentials and experience data
destinations - Airport and destination information
flights - Flight schedules and operational data

See docs/database_schema.sql for complete schema definitions.
Requirements

Python 3.7+
SQLite3 (included with Python)
No additional dependencies required

Assignment Details
This project was developed for database coursework demonstrating:

Relational database design and implementation
SQL query development and optimization
Python database connectivity using sqlite3
Command-line interface development
CRUD operations and data managemen