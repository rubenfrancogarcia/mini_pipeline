# Ticket Sales Pipeline Mini Project

Loads third-party ticket sales from a CSV into a MySQL database (running in
Docker), then lets you query it through an interactive command-line menu.

## Setup

1. Create a `.env` file in the project root:

   ```
   MYSQL_ROOT_PASSWORD=password
   MYSQL_DATABASE=ticket_db
   MYSQL_USER=app_user
   MYSQL_USER_PASSWORD=password
   ```

   `MYSQL_USER` must **not** be `root`: MySQL refuses to create a user named
   root from these variables and the container will exit on first start.

2. Create a virtual environment and install dependencies:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

## Run the database

```powershell
docker compose --env-file .env -f docker_compose.yml up -d
```

Verify it is up:

```powershell
docker compose -f docker_compose.yml logs -f db
```

Wait for `ready for connections` before running the app.

## Run the app

```powershell
.\.venv\Scripts\python.exe main.py
```

On start it connects to the database, creates the `ticket` table if needed,
and loads the CSV (only if the table is empty). Then it shows a menu:

| Option | What it does                              |
| ------ | ----------------------------------------- |
| 1      | Top 3 events by tickets sold              |
| 2      | Revenue by city                           |
| 3      | Tickets for a customer (prompts for an id) |
| 4      | Least popular 3 events by tickets sold    |
| 5      | Return all results                        |
| q      | Quit                                      |

Queries that return nothing print a "no results" message.

## Project layout

- `main.py` - opens the DB connection, loads the CSV, starts the menu
- `CLIService.py` - the menu loop; maps each choice to a query method
- `DBUtils.py` - connection, table creation, CSV load, and the queries
- `tickets.py` - `ticket` dataclass and CSV row parsing/validation
- `docker_compose.yml` - MySQL container and `db_data` volume

## Troubleshooting

**`Unknown database 'ticket_db'`**: the data volume was created earlier without
the database. Deleting the container does not delete the volume, and MySQL only
creates the database on the first start with an empty volume. Reset it
(this deletes all data in the DB; it is reloaded from the CSV on the next run):

```powershell
docker compose -f docker_compose.yml down -v
docker compose --env-file .env -f docker_compose.yml up -d
```

**Connection refused right after `up -d`**: MySQL takes a few seconds to
initialise. Check the logs for `ready for connections` and retry.
