#!/bin/sh
set -e

FAKER_MARKER="/opt/.faker_done"

./itsup.py

echo "Running database migrations..."
alembic upgrade head
echo -e "Database migrations completed successfully.\n"

if [ ! -f "$FAKER_MARKER" ]; then
    echo "Generating fake data..."
    python3 generate_data.py
    echo "Fake data generation completed."
    touch "$FAKER_MARKER"
else
    echo -e "Fake data generation already performed.\n"
fi

echo "Web app will now start ..."
uvicorn app.main:app --host 0.0.0.0 --port 18000 --reload
