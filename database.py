#!/usr/bin/env python3

import sqlite3

def initialize_db():
	
	while True:
		try:
			conn = sqlite3.connect('habit_tracker.db')
			cur = conn.cursor()
			
			#Create the main table that keeps track of all habits
			cur.execute('''CREATE TABLE IF NOT EXISTS habits (
							habit_id INTEGER PRIMARY KEY,
							habit_name TEXT,
							habit_frequency INTEGER,
							habit_period INTEGER,
							next_completion_date DATE
						)''')
			
			#Create the table that logs completed habits
			cur.execute('''CREATE TABLE IF NOT EXISTS completions (
							completion_id INTEGER PRIMARY KEY,
							habit_id INTEGER,
							completion_date DATE,
							FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
						)''')
			#print("Database created successfully")
			break
		
		except ValueError:
			print("There was an error creating the database")
			break
		
#test the connection and database created
		#initialize_db()