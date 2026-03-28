# DECISIONS.md

## 1. What is an ODM and why Beanie?
An ODM (Object Document Mapper) lets you work with MongoDB using Python classes
instead of raw query dictionaries. Beanie sits on top of Motor (async MongoDB driver)
and lets you define your data as Document classes — so instead of writing
`{"$set": ...}` queries everywhere, you call `.update()` or `.create()` on objects.
I used Beanie because it integrates naturally with FastAPI's async design and plays
well with Pydantic, which I was already using for validation.

## 2. Why wrap Beanie in a Database class?
If I called Beanie methods directly in each route, I'd be repeating the same logic
in multiple places. The Database class centralizes that logic — save, get, update,
delete — in one spot. If I later need to change how saving works (e.g. add logging),
I only touch one class, not every route file. It also makes routes easier to read.

## 3. What happens if initialize_database() is not called on startup?
Beanie won't know which MongoDB collection maps to which Document class.
Any route that tries to query or insert data would throw an error because the
ODM hasn't been set up. The @app.on_event("startup") hook ensures the DB
is ready before the first request hits any route.

## 4. Event vs EventUpdate — why two classes?
Event is a Beanie Document — it maps to a MongoDB collection and includes all
required fields. EventUpdate is a plain Pydantic BaseModel where every field
is Optional, because when updating you might only want to change one field.
If I used Event for updates, I'd be forced to supply all fields every time,
which defeats the purpose of a PATCH/PUT operation.