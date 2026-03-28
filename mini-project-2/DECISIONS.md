# DECISIONS.md

## 1. What is an ODM and why Beanie?
An ODM lets us use Python classes instead of writing MongoDB queries manually.  
Beanie works well with FastAPI and Pydantic, so it makes coding easier and cleaner.

## 2. Why wrap Beanie in a Database class?
To avoid repeating the same code in different routes.  
All database actions are in one place, which makes the code easier to manage and update.

## 3. What happens if initialize_database() is not called?
Beanie will not be connected to MongoDB.  
This means any database operation will fail because the models are not initialized.

## 4. Event vs EventUpdate — why two classes?
Event is used to store full data in the database.  
EventUpdate is used for updates where fields are optional, so we can change only what we need.