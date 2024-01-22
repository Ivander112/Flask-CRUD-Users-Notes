# Flask + SQLAlchemy + Alembic Boilerplate

This is a sample project of Async Web API with Flask + SQLAlchemy 2.0 + Alembic.
It includes asynchronous DB access using asyncpg and test code.

See [reference](https://github.com/rhoboro/async-fastapi-sqlalchemy/tree/main).

Other References
- [Flask Docs](https://flask.palletsprojects.com/en/3.0.x/)
- [Gunicorn](https://gunicorn.org/)
- [SQL Alchemy](https://docs.sqlalchemy.org/en/20/orm/index.html)
- [SQL Alchemy - PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

# Setup

## Install

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

## Setup a database and create tables

```shell
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=root \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgdata:/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  postgres:15.2-alpine

# Cleanup database
# $ docker stop db
# $ docker rm db
# $ docker volume rm pgdata

(venv) $ APP_CONFIG_FILE=local python3 app/main.py migrate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a8483365f505, initial_empty
INFO  [alembic.runtime.migration] Running upgrade a8483365f505 -> 24104b6e1e0c, add_tables
```

# Run

```shell
(venv) $ APP_CONFIG_FILE=local python3 app/main.py api
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000 (92311)
[INFO] Using worker: sync
[INFO] Booting worker with pid: 92315
```

# Test

```shell
(venv) $ python3 -m pytest
```

# Create Migration

```shell
(venv) $ cd app/migrations
(venv) alembic revision -m "<name_of_migration_file>"
```
<br>
<br>


[## CRUD API Notes

Adding a method for notes endpoint with function:

-   Create new note with created_by from user_id in JWT token
    
-   Request all notes with pagination. Using filter by user_id in JWT token and notes that have not been deleted
    
-   Request One Notes with validated if user_id in JWT token was the one who created the note
    
-   Update existing note
    
-   Delete Notes (set deleted_at and Deleted By)

### Add note

# Add Note

http://127.0.0.1:8000/api/v1/notes/add

## Request

### Request URL

-   Method: POST
    
-   URL: `http://127.0.0.1:8000/api/v1/notes/add`
    

### Request Body

-   Type: Raw
    
-   Payload:
    
    JSON
    
    ```json
        {
            "title": "",
            "content": ""
        }
    ```
    

## Response

-   Status: 200 OK
    
-   Data:
    
    JSON
    
    ```json
         {
            "data": {
                "content": "",
                "created_at": "",
                "created_by": 0,
                "deleted_at": null,
                "deleted_by": null,
                "note_id": 0,
                "title": "",
                "updated_at": null,
                "updated_by": null
            },
            "message": "",
            "status": ""
        }
    ```
Body

```json
{
  "title": "deleted_gang",
  "content": "deleted_rules"
}
```

### Get All Note (Pagination)

http://127.0.0.1:8000/api/v1/notes/?page=2&item_per_page=1&filter_by_user_id=false

This endpoint makes an HTTP GET request to retrieve notes. It accepts query parameters including page number, items per page, and a filter by user ID flag. The last call to this request did not include a request body.

### Query Parameters

-   `page`: The page number for paginated results.
    
-   `item_per_page`: The number of items to be included per page.
    
-   `filter_by_user_id`: A flag to filter the notes by user ID.
    

### Response

The response will have JSON object with the `data`, `message`, and `status` fields. The `data` object contains `meta` information and an array of `records` representing the notes. Each record includes details such as content, title, creation and update timestamps, and user IDs.

Example Response:

```json
{
    "data": {
        "meta": {
            "item_per_page": 0,
            "page": 0,
            "total_item": 0,
            "total_page": 0
        },
        "records": [
            {
                "content": "",
                "created_at": "",
                "created_by": 0,
                "deleted_at": null,
                "deleted_by": null,
                "note_id": 0,
                "title": "",
                "updated_at": "",
                "updated_by": 0
            }
        ]
    },
    "message": "",
    "status": ""
}
```
Query Params

page  2

item_per_page   1

filter_by_user_id   false

### Get one note

http://127.0.0.1:8000/api/v1/notes/49

This endpoint makes an HTTP GET request to retrieve the details of a specific note. The request should include the note ID in the URL path.

No request body is required for this endpoint.

### Response

-   The response will include the details of the note such as content, title, creation and update timestamps, and the IDs of the creator and updater.
    
-   The "message" and "status" fields may be empty in the response.

### Update Note

http://127.0.0.1:8000/api/v1/notes/49
## Update Note

This endpoint allows the user to update a specific note by sending an HTTP PUT request to the specified URL.

### Request Body

-   The request should include a raw JSON payload in the request body with the following parameters:
    
    -   `title` (string, required): The updated title of the note.
        
    -   `content` (string, required): The updated content of the note.
        

Example:

Example:

JSON

```json
{
  "title": "Updated Title",
  "content": "Updated Content"
}
```
### Response

-   Upon a successful update, the API will respond JSON object containing the updated note details:
    
    -   `note_id` (integer): The unique identifier of the updated note.
        
    -   `title` (string): The updated title of the note.
        
    -   `content` (string): The updated content of the note.
        
    -   `created_at` (string): Timestamp of the note creation.
        
    -   `updated_at` (string): Timestamp of the last update.
        
    -   `created_by` (integer): User ID of the note creator.
        
    -   `updated_by` (integer): User ID of the user who last updated the note.
        
    -   `deleted_at` (string): Timestamp of note deletion, if applicable.
        
    -   `deleted_by` (integer): User ID of the user who deleted the note, if applicable.
        
-   Additionally, the response may include:
    
    -   `message` (string): Any additional information or message from the server.
        
    -   `status` (string): The status of the response.
  
  Example Response:

JSON

```json
{
  "data": {
    "note_id": 123,
    "title": "Updated Title",
    "content": "Updated Content",
    "created_at": "2022-01-01T12:00:00Z",
    "updated_at": "2022-01-02T10:00:00Z",
    "created_by": 456,
    "updated_by": 456,
    "deleted_at": null,
    "deleted_by": null
  },
  "message": "Note updated successfully",
  "status": "success"
}
```
Body raw  (json)

```json
{
    "title": "Deleted fast",
    "content": "Deleted content"
}
```


### Delete Note

http://127.0.0.1:8000/api/v1/notes/50

This endpoint sends an HTTP DELETE request to [http://127.0.0.1:8000/api/v1/notes/63](http://127.0.0.1:8000/api/v1/notes/63) to delete a specific note. The request does not contain any payload in the raw request body.

  Example Response:

```json
{
    "data": {
        "content": "test2fe5",
        "created_at": "Mon, 22 Jan 2024 12:20:39 GMT",
        "created_by": 3,
        "deleted_at": "Mon, 22 Jan 2024 15:27:15 GMT",
        "deleted_by": 1,
        "note_id": 63,
        "title": "test453",
        "updated_at": null,
        "updated_by": null
    },
    "message": "success delete user",
    "status": "success"
}](https://github.com/Ivander112/btj-academy-python-flask-Ivander-A.-W.)https://github.com/Ivander112/btj-academy-python-flask-Ivander-A.-W.
