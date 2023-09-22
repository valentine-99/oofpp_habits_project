import sqlite3
import datetime
import random

def create_random_habits():
    # Connect to the habit_tracker.db database
    conn = sqlite3.connect('habit_tracker.db')
    cursor = conn.cursor()

    # Create the habits table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS habits
                      (habit_id INTEGER PRIMARY KEY, habit_name TEXT, habit_frequency INTEGER, habit_period INTEGER, next_completion_date DATE)''')

    # List of example habit names
    habit_names = ['Drink water', 'Exercise', 'Read for 15min in book', 'Meditate for 5min', 'Write in journal', 'Eat 3 vegetables', 'Take a 10min walk', 'Eat Pizza', 'Ride Bicycle for 5min', 'Code for 20min']

    # Insert 15 random habits into the habits table
    for _ in range(15):      
        habit_name = random.choice(habit_names)
        habit_frequency = random.randint(1, 3)
        habit_period = random.randint(1, 7)
        next_completion_date = datetime.datetime.now().date()
        cursor.execute("INSERT INTO habits (habit_name, habit_frequency, habit_period, next_completion_date) VALUES (?, ?, ?, ?)", (habit_name, habit_frequency, habit_period, next_completion_date))

    # Create the completions table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS completions
                      (completion_id INTEGER PRIMARY KEY, habit_id INTEGER, completion_date DATE)''')

    # Get all habit IDs from the habits table
    cursor.execute("SELECT habit_id FROM habits")
    habit_ids = [row[0] for row in cursor.fetchall()]

    # Generate random entries for the last 4 weeks for each habit
    for habit_id in habit_ids:
        # Get the current date and time
        current_date = datetime.datetime.now().date()

        # Generate random completion dates for the last 4 weeks
        for _ in range(31):
            completion_date = current_date - datetime.timedelta(days=random.randint(0, 80))
            cursor.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)", (habit_id, completion_date))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def remove_all_habits():
    # Connect to the habit_tracker.db database
    conn = sqlite3.connect('habit_tracker.db')
    cursor = conn.cursor()

    # Delete all rows from the habits table
    cursor.execute("DELETE FROM habits")

    # Delete all rows from the completions table
    cursor.execute("DELETE FROM completions")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def main():
    """
    The main function that runs the Habit Tracker application.
    """

    while True:
        print("\nHabit Tracker Menu:")
        print("1. Create a bunch of habit with 4 weeks of sample data")
        print("2. Remove all habits")
        print("3. Exit App")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_random_habits()
        elif choice == "2":
            remove_all_habits()
        elif choice == "3":
            print("Exiting Habit Tracker...")
            break
        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    main()
