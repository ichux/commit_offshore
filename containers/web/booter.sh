#!/bin/sh
set -e

FAKER_MARKER="/opt/.faker_done"

./itsup.py

alembic upgrade head

if [ ! -f "$FAKER_MARKER" ]; then
    python3 generate_data.py
    touch "$FAKER_MARKER"
else
    echo -e "Fake data generation already performed.\n"
fi

echo "Web app will now start ..."
uvicorn app.main:app --host 0.0.0.0 --port 18000 --reload
