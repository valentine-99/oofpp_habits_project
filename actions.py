#!/usr/bin/env python3

import datetime
import sqlite3


class Habitapp:	
	"""	
	A class representing a habit tracker app.
	
	Attributes:
		name (str): The name of the habit.
		frequency (str): The frequency at which the habit should be completed.
		periodicity (str): The periodicity of the habit (e.g. daily, weekly, monthly).
		current_streak (int): The current streak of consecutive completions.
		longest_streak (int): The longest streak of consecutive completions.
		last_completed_date (str): The date when the habit was last completed.
		next_completion_date (str): The date when the habit is next scheduled for completion.
		completion_count (int): The total count of habit completions.
		
	Methods:
		None

	"""
	def __init__(self):
		"""
		Initializes a new instance of the Habitapp class.

		Parameters:
			None

		Returns:
			None
		"""
		self.name = None
		self.frequency = None
		self.periodicity = None
		self.next_completion_date = None
		self.habit_id = 0
		
	def create_habit(self):
		"""
		Menu Item 1 - create_habit() - Creates a new habit by prompting the user for habit details and inserting them into the database.
	
		Parameters:
			name: str
				The name of your habit - e.g. Drink Water
			frequency : int
				How often a habit should be completed in a given day. e.g. "8" (Drink 8 glasses of water a day)
			periodicity : int
				Define when the habit should repeat in days. e.g. "1" (Daily - Drink 8 glasses of water a day[everyday = 1])
	
		Returns:
			That the habit was created successfully.
		"""
		# Connect to db
		conn = sqlite3.connect('habit_tracker.db')
		cur = conn.cursor()		
		
		# Define the name, frequency and periodicity of the habit.
		self.name = input("Enter the name of your habit: ")
		self.frequency = input("How often do you need to do this habit on a given day: ")
		self.periodicity = input("How often do you need to do this habit? Daily = 1, every 2 days = 2, etc. ")
		
		# Set the initial next completion date to today
		next_completion_date = datetime.datetime.now().strftime("%Y-%m-%d")
		
		cur.execute("INSERT INTO habits (habit_name, habit_frequency, habit_period, next_completion_date) VALUES (?, ?, ?, ?)",
					(self.name, self.frequency, self.periodicity, next_completion_date))
		
		conn.commit()
		print(f'Habit {self.name} created!')
		conn.close()
	
	def remove_habit(self):
		"""
		Menu Item 3 - remove_habit() - Removes a habit from the database by prompting the user for the ID of the habit to be removed.
	
		Parameters:
		habit_id : int
			If habit id exists, will remove that habit, and update the ids of remaining habits so there are no gaps in the database.
	
		Returns:
			Printed message that the habit was removed. 
		"""
		self.display_habits()
		
		while True:
			try:
				habit_id = int(input("Enter the ID of the habit you want to remove: "))
				
				# Check if the habit exists in the database
				conn = sqlite3.connect('habit_tracker.db')
				cur = conn.cursor()
				cur.execute("SELECT habit_id FROM habits WHERE habit_id = ?", (habit_id,))
				habit = cur.fetchone()
				
				if habit is None:
					print(f"Habit with ID {habit_id} does not exist!")
					conn.close()
					return
				
				# Delete the habit from the habits table
				cur.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))
				
				# Delete the entries in the completions table as well
				cur.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
				
				# Update the habit IDs for remaining habits
				cur.execute("UPDATE habits SET habit_id = habit_id - 1 WHERE habit_id > ?", (habit_id,))
				
				# Commit the changes and close the connection
				conn.commit()
				conn.close()
				
				print(f"Habit with ID {habit_id} removed successfully!")
				break
			
			except ValueError:
				print("Invalid input! Please enter a valid habit ID.")
		
	def display_habits(self):
		"""
		Menu Item 2 - display_habit() - Retrieves and displays all habits from the database.
	
		Parameters:
			None
	
		Returns:
			List of all habits. 
		"""
		# Connect to the SQLite database
		conn = sqlite3.connect('habit_tracker.db')
		cur = conn.cursor()
		
		# Execute SQL query to fetch all habits from the 'habits' table
		cur.execute("SELECT habit_id, habit_name, habit_frequency, habit_period, next_completion_date FROM habits")
		habits = cur.fetchall()
		
		print("Habit ID | Habit Name | Due | Completion Progress")
		
		# Iterate through each habit
		for habit in habits:
			# Extract habit details
			habit_id, habit_name, habit_frequency, habit_period, next_completion_date = habit
			
			# Calculate the due date and today's date
			due_date = datetime.datetime.strptime(next_completion_date, "%Y-%m-%d").date()
			today = datetime.datetime.now().date()
			
			# Execute SQL query to get the completion count for today for the current habit
			cur.execute("SELECT COUNT(*) FROM completions WHERE habit_id = ? AND date(completion_date) = ?", (habit_id, today.strftime('%Y-%m-%d')))
			completion_count = cur.fetchone()[0]
			
			# Update the next completion date only if the count of completion entries today is equal to the habit frequency
			if completion_count >= habit_frequency:
				next_completion_date = datetime.datetime.now() + datetime.timedelta(days=int(habit_period))
				# Convert to a readable Time format
				next_completion_date = next_completion_date.strftime("%Y-%m-%d")
				# Update the next completion date
				cur.execute("UPDATE habits SET next_completion_date = ? WHERE habit_id = ?", (next_completion_date, habit_id))
				
			# Update due date based on comparison with today's date
			if due_date <= today:
				due_date_str = "Today"
			elif due_date == today + datetime.timedelta(days=1):
				due_date_str = "Tomorrow"
			else:
				due_date_str = due_date.strftime('%Y-%m-%d')
				
			# Calculate completion progress
			completion_progress = f"{completion_count}/{habit_frequency}"
			
			# Print habit details
			print(f"{habit_id}. {habit_name} | Due: {due_date_str} | {completion_progress} | Repeats every ({habit_period}) days")
			
		# Commit all changes after loop
		conn.commit()
		
							
	def complete_habit(self):
		"""
		Menu Item 5 - complete_habit() - Marks a habit as completed by prompting the user for the ID of the habit to be completed.
	
		Parameters:
			habit_id : int
	
		Returns:
			Message that habit was completed and the completion time. Updates completion times and counts in database. 
		"""
		
		#disabling this to see if it works better - Activated again
		self.display_habits()
		
		while True:
			try:
				habit_id = int(input("Enter the ID of the habit you want to complete: "))
				
				# Check if the habit exists in the database
				conn = sqlite3.connect('habit_tracker.db')
				cur = conn.cursor()
				cur.execute("SELECT habit_id, habit_frequency, habit_period FROM habits WHERE habit_id = ?", (habit_id,))
				habit = cur.fetchone()
				
				if habit is None:
					print(f"Habit with ID {habit_id} does not exist!")
					conn.close()
					return
				
				# Get the current date and time
				completion_date = datetime.datetime.now().strftime("%Y-%m-%d")
						
				# Insert the completion record into the completions table
				cur.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)", (habit_id, completion_date))
				
				# Commit the changes and close the connection
				conn.commit()
				conn.close()
				
				print(f"Habit with ID {habit_id} completed on {completion_date}!")
				break
		
			except ValueError:
				print("Invalid input! Please enter a valid habit ID.")
		
	def analyze_habit(self):
		"""
		Menu Item 4 - analyze_habits() - Analyzes and displays the longest streak, current streak, and total completions for each habit.
	
		Parameters:
			None
	
		Returns:
			List of all habits and their longest streaks, current streak, total completions, habits with the same periodicity. 
		"""
		conn = sqlite3.connect('habit_tracker.db')
		cur = conn.cursor()
		
		# Habit stats
		habits_stats = []
		
		# 1. Count total completions for each habit and calculate streaks
		cur.execute("SELECT habit_id, habit_name, habit_frequency, habit_period FROM habits")
		habits = cur.fetchall()
		for habit in habits:
			habit_id, habit_name, habit_frequency, habit_period = habit
			cur.execute("SELECT completion_date FROM completions WHERE habit_id = ? ORDER BY completion_date", (habit_id,))
			dates = [row[0] for row in cur.fetchall()]
			total_completions = len(dates)
			
			# Calculate current streak
			current_streak = 0
			date_check = datetime.datetime.now().date()
			while True:
				cur.execute("SELECT COUNT(*) FROM completions WHERE habit_id = ? AND completion_date = ?", (habit_id, date_check))
				count_for_day = cur.fetchone()[0]
				if count_for_day >= habit_frequency:
					current_streak += 1
					date_check -= datetime.timedelta(days=habit_period)
				else:
					break
				
			# Calculate longest streak
			longest_streak = 0
			temp_streak = 0
			for i in range(len(dates) - 1):
				if (datetime.datetime.strptime(dates[i+1], "%Y-%m-%d").date() - datetime.datetime.strptime(dates[i], "%Y-%m-%d").date()).days == habit_period:
					cur.execute("SELECT COUNT(*) FROM completions WHERE habit_id = ? AND completion_date BETWEEN ? AND ?", (habit_id, dates[i], dates[i+1]))
					count_between_dates = cur.fetchone()[0]
					if count_between_dates >= habit_frequency:
						temp_streak += 1
					else:
						longest_streak = max(longest_streak, temp_streak)
						temp_streak = 0
				else:
					longest_streak = max(longest_streak, temp_streak)
					temp_streak = 0
					
			longest_streak = max(longest_streak, temp_streak) # In case the longest streak is ongoing
			
			habits_stats.append((habit_id, habit_name, total_completions, longest_streak, current_streak))
			
		# Sorting habits by the longest streak
		habits_stats.sort(key=lambda x: x[3], reverse=True)
		best_habit = habits_stats[0]
		print(f"The habit with the best streak is {best_habit[1]} with {best_habit[3]} days. Achieved on the: {datetime.datetime.now().date() - datetime.timedelta(days=best_habit[3]*best_habit[4])}")
		print("--------------------")
		
		# Printing habit stats
		for habit_stat in habits_stats:
			print(f"{habit_stat[0]} | {habit_stat[1]} | Total Completions: {habit_stat[2]} | Longest Streak: {habit_stat[3]} | Current Streak: {habit_stat[4]}")
			
		# 2. Group habits by their periodicity
		print("\nHabits by Periodicity:")
		cur.execute("SELECT habit_period, GROUP_CONCAT(habit_id || ' | ' || habit_name) FROM habits GROUP BY habit_period")
		grouped_habits = cur.fetchall()
		for period, habit_list in grouped_habits:
			print(period)
			print("--------------------")
			print(habit_list)
			print("--------------------")
			
		conn.close()
				
		
	def edit_habit(self):
		"""
		Menu Item 6 - edit_habit - Edits a habit by prompting the user for the ID of the habit to be edited and the new details.
	
		Parameters:
		habit_id : int
			The ID of the habits which you want to change the name, frequency and periodicity. 
		new_name: str
			The new name you want to give the select habit. e.g. Drink Water to Drink Beer. 
		new_frequency: int
			The amount of times you want to complete that habit on a given day. 
		new_periodicity : int
			Define when the habit should repeat in days. e.g. "1" (Daily - Drink 8 glasses of water a day[everyday = 1])
	
		Returns:
			A message that the habit was successfully updated.
		"""
		self.display_habits()
		
		while True:
			try:
				habit_id = int(input("Enter the ID of the habit you want to edit: "))
				
				# Check if the habit exists in the database
				conn = sqlite3.connect('habit_tracker.db')
				cur = conn.cursor()
				cur.execute("SELECT habit_id, habit_name, habit_frequency, habit_period FROM habits WHERE habit_id = ?", (habit_id,))
				habit = cur.fetchone()
				
				if habit is None:
					print(f"Habit with ID {habit_id} does not exist!")
					conn.close()
					return
				
				# Prompt the user for new details
				new_name = input("Enter the new name for the habit: ")
				new_frequency = input("Enter the new frequency for the habit: ")
				new_periodicity = input("Enter the new periodicity for the habit: ")
				
				# Calculate the new next completion date based on the updated periodicity
				next_completion_date = datetime.datetime.now() + datetime.timedelta(days=int(new_periodicity))
				next_completion_date = next_completion_date.strftime("%Y-%m-%d")
				
				# Update the habit details in the database
				cur.execute("UPDATE habits SET habit_name = ?, habit_frequency = ?, habit_period = ?, next_completion_date = ? WHERE habit_id = ?", (new_name, new_frequency, new_periodicity, next_completion_date, habit_id))
				
				# Commit the changes and close the connection
				conn.commit()
				conn.close()
				
				print(f"Habit with ID {habit_id} updated successfully!")
				break
			
			except ValueError:
				print("Invalid input! Please enter a valid habit ID.")