# DECISIONS

## Field Types

I used integer for id because each patient must have a unique identifier.

The name field uses string with min_length to ensure the name is not empty.

Age is constrained with gt and lt to prevent unrealistic ages.

Appointments is a list because one patient can have multiple appointments.

## Validation Rules

min_length ensures names are not too short.

Age validation prevents negative ages or unrealistic values.

Enum ensures appointment type can only be specific values.

## Async Endpoint

The GET /patients/ endpoint uses asyncio.sleep(1) to simulate a real database request delay.


## Database

### 1. What is `@contextmanager` and why do we use it instead of a plain function here?

`@contextmanager` is a decorator that lets us use a function with the `with` statement.
In `managed_db()`, it opens the database connection, yields it to the endpoint, and
automatically closes it when done — even if an error occurs. A plain function cannot
guarantee this cleanup, so we use `@contextmanager` to avoid leaving connections open.

### 2. What does `check_same_thread=False` do and why is it necessary in a FastAPI application?

SQLite normally only allows the thread that created the connection to use it.
FastAPI handles requests across multiple threads, so without this setting SQLite
would throw an error. Setting it to `False` allows cross-thread access, which is
safe here because each request opens and closes its own connection via `managed_db()`.

### 3. What happens to your data when the server restarts — with the old list vs. with SQLite?

With the old Python list, all data was stored in memory and lost every time the
server restarted. With SQLite, data is saved to a file called `sqlite.db` on disk,
so it remains after restarts. This makes SQLite a real persistent storage solution
unlike the in-memory list.