# Privacy-First Habit Tracking App
The main goal of this project is a to provide a simple to use Habit Tracking App. 
It is light-weight and fast. All files get stored locally on your device making it in essence private.
The app has some built in tools to you help you keep track of streaks and records. 

#### Note - The database files are not encrypted, so its possible for these files to be read by any program that can read .db files, but if you have a non-internet connected device this application could run and track all your habits indefintely privately. 

## What tools does it use?
The application uses:
- Python (build on Python 3.11) 
- SQlite3 for managing the database. 

### How can the user interact with the program? 
The interface is a CLI (command-line interface) that is a simple Menu, where the user inputs a number on their keyboard to access that menu item. (1,2,3 etc)

## What does the application do?
The application can:

* create habits
* complete habits (like tick-off)
* provide analytics for habits
* show list of habits
* list habits by periodicity
* display the longest streak of a habit
* delete habits
* built in help-menu
* exit app
* edit a habit and change it name or periodicity and frequency


## How to run the application?
~~~
main.py
~~~

## How to demo the application with 4 weeks of habit data? 
run (and select menu option 1):
~~~
demo.py
~~~
and then run
~~~
main.py
~~~

to remove the demo data, run (and select menu option 2):
~~~
demo.py 
~~~
(this will delete all information saved in the habit tracker app)




## License
MIT License

Copyright (c) 2023 | valentine-99

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
