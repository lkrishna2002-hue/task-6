# Todo CRUD API (FastAPI + PostgreSQL + Docker)

## 1. What does this application do?

This project is a simple **Todo CRUD API** built with **FastAPI** and **PostgreSQL**, containerized using **Docker** and **Docker Compose**.

You can:

- Create a todo item
- List all todos
- Get a todo by ID
- Update a todo
- Delete a todo

### High-level architecture (ASCII diagram)

```text
+---------------------------+
|        Client (You)       |
|  curl / Postman / browser |
+-------------+-------------+
              |
              v
+-------------+-------------+
|        todo-app (API)     |
|  FastAPI + Uvicorn        |
|  Reads env: DATABASE_URL  |
+-------------+-------------+
              |
              v
+-------------+-------------+
|      todo-db (Postgres)   |
|  Data stored in volume    |
+-------------+-------------+
