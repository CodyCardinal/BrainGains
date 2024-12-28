#!/bin/sh

DATABASE_DIR=$(dirname "$DATABASE_PATH")
mkdir -p "$DATABASE_DIR"

if [ ! -f "$DATABASE_PATH" ]; then
  echo "Database file not found at $DATABASE_PATH. Initializing database..."
  flask db initialize
else
  echo "Database file already exists at $DATABASE_PATH. Skipping initialization."
fi

exec flask run --host=0.0.0.0