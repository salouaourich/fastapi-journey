1. Connection Management
I store active WebSocket connections per poll in a dictionary.
When a user disconnects, I catch the error and remove them safely so the server doesn’t crash.
2. State Storage
I used in-memory storage (Python dictionary) because it’s simple for a prototype.
The downside is all data is lost if the server restarts, so a real app should use a database like PostgreSQL.
3. Concurrency
Votes are usually handled one at a time due to Python’s execution model, so it mostly works safely.
But in a real multi-worker setup, race conditions can happen, so a database with transactions would be better.
4. REST vs WebSocket
REST is used for normal voting requests but doesn’t update other users instantly.
WebSockets broadcast changes in real time so all connected clients see updates immediately.