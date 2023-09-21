#!/usr/bin/env python3

import sqlite3
import datetime
import actions
import database



def print_separator():
	"""
	Prints a separator line consisting of dashes.

	Parameters:
		None

	Returns:
		A line with dashes.
	"""
	print("-" * 20)
	
	
def main():
	"""
	The main function that runs the Habit Tracker application.

	Parameters = int
		Pick an integer to access that module within the HabitApp Class, see: actions.py
	"""
	app = actions.Habitapp()
	
	while True:
		print("\nHabit Tracker Menu:")
		print("1. Create a new habit")
		print("2. View all habits")
		print("3. Remove a habit")
		print("4. Analyze habits")
		print("5. Complete a habit")
		print("6. Edit a habit")
		print("7. Help Menu")
		print("8. Exit App")
		
		choice = input("Enter your choice: ")
		
		if choice == "1":
			app.create_habit()
		elif choice == "2":
			app.display_habits()
		elif choice == "3":
			app.remove_habit()
		elif choice == "4":
			app.analyze_habit()
		elif choice == "5":
			app.complete_habit()
		elif choice == "6":
			app.edit_habit()
		elif choice == "7":
			print("Help Docstrings:")
			print("------------------")
			print(app.create_habit.__doc__)
			print_separator()
			print(app.display_habits.__doc__)
			print_separator()
			print(app.remove_habit.__doc__)
			print_separator()
			print(app.analyze_habit.__doc__)
			print_separator()
			print(app.complete_habit.__doc__)
			print_separator()
			print(app.edit_habit.__doc__)
		elif choice == "8":
			print("Exiting Habit Tracker...")
			break
		else:
			print("Invalid choice! Please enter a valid option.")
			
			
		print_separator()  # Print the separator after each interaction
		
if __name__ == "__main__":
	database.initialize_db()
	main()
	