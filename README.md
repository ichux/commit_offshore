# Commit Offshore
Here are lists of some assumptions made and good to know
1. You are working on a Linux-like OS
2. Makefile works on your PC, else: sudo apt install -y make
3. **docker compose** is your command, else, use **docker-compose**
4. If anything in the **Makefile** didn't work for you, copy and paste on your command line
5. You can't edit generated migration files on some OS, but you can from inside the container

Follow through to set up your whole project.
```bash
# create your env to taste
1. make e

# build your project: see Assumption 3, in case you need to change your command
2. make b

# run the migration
3. make uh

# generate initial data
4. make gd

# run tests
5. make ts
```

# Work with models/data
```bash
1. edit your models.py e.g.

class Diet(Base, TimestampMixin):
    __tablename__ = "diets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

# generate migration file: be free to change 'known diet' to taste.
2. make ai i='known diet'

# how sql for alembic upgrade head
3. make uhs

# run the migration
4. make uh
```

# Normal URLS, even with edge cases
```bash
#GET /v1/users - Standard pagination (10 users)
curl "http://127.0.0.1:18008/v1/users?skip=0&limit=10" -H "Accept: application/json"

#GET /v1/users - Test pagination beyond data (expect empty list, ~100 users exist)
curl "http://127.0.0.1:18008/v1/users?skip=100&limit=10" -H "Accept: application/json"

#GET /v1/users - Test negative limit (expect 422 error)
curl "http://127.0.0.1:18008/v1/users?skip=0&limit=-1" -H "Accept: application/json"

#GET /v1/users - Test negative skip (expect 422 error)
curl "http://127.0.0.1:18008/v1/users?skip=-1&limit=10" -H "Accept: application/json"

#GET /v1/orders - All orders (10 orders)
curl "http://127.0.0.1:18008/v1/orders?skip=0&limit=10" -H "Accept: application/json"

#GET /v1/orders - Filter by valid user_id (replace with a real user_id from your database)
curl "http://127.0.0.1:18008/v1/orders?user_id=550e8400-e29b-41d4-a716-446655440000&skip=0&limit=5" -H "Accept: application/json"

#GET /v1/orders - Filter by invalid user_id (expect empty list) - (replace with a real user_id from your database)
curl "http://127.0.0.1:18008/v1/orders?user_id=00000000-0000-0000-0000-000000000000&skip=0&limit=5" -H "Accept: application/json"

#GET /v1/orders - Test pagination beyond data (expect empty list, ~200 orders exist)
curl "http://127.0.0.1:18008/v1/orders?skip=200&limit=10" -H "Accept: application/json"

#GET /v1/payments - Standard pagination (10 payments)
curl "http://127.0.0.1:18008/v1/payments?skip=0&limit=10" -H "Accept: application/json"

#GET /v1/payments - Test pagination beyond data (expect empty list, ~150 payments exist)
curl "http://127.0.0.1:18008/v1/payments?skip=150&limit=10" -H "Accept: application/json"

#GET /v1/support-tickets - Standard pagination (10 tickets)
curl "http://127.0.0.1:18008/v1/support-tickets?skip=0&limit=10" -H "Accept: application/json"

#GET /v1/support-tickets - Test pagination beyond data (expect empty list, ~50 tickets exist)
curl "http://127.0.0.1:18008/v1/support-tickets?skip=50&limit=10" -H "Accept: application/json"
```

# Optional APIs
```bash
#GET /v1/recent-users - Users created in the last 7 days (expect ~25 users)
curl "http://127.0.0.1:18008/v1/recent-users?days=7" -H "Accept: application/json"

#GET /v1/recent-users - Test with days=0 (expect 422 error)
curl "http://127.0.0.1:18008/v1/recent-users?days=0" -H "Accept: application/json"

#GET /v1/recent-users - Test with large days (expect all ~100 users)
curl "http://127.0.0.1:18008/v1/recent-users?days=365" -H "Accept: application/json"

#GET /v1/orders-by-unresolved-tickets - Orders from users with unresolved tickets (expect orders from ~10 users)
curl "http://127.0.0.1:18008/v1/orders-by-unresolved-tickets" -H "Accept: application/json"

#GET /v1/total-spent-last-30-days - Total spent per user in last 30 days (expect ~33 successful payments)
curl "http://127.0.0.1:18008/v1/total-spent-last-30-days" -H "Accept: application/json"

#GET /v1/users-with-failed-payments - Users with >3 failed payments in last 60 days (expect ~5 users)
curl "http://127.0.0.1:18008/v1/users-with-failed-payments?days=60&threshold=3" -H "Accept: application/json"

#GET /v1/users-with-failed-payments - Test high threshold (expect empty list)
curl "http://127.0.0.1:18008/v1/users-with-failed-payments?days=60&threshold=10" -H "Accept: application/json"

#GET /v1/users-with-failed-payments - Test short time range (expect fewer or no users)
curl "http://127.0.0.1:18008/v1/users-with-failed-payments?days=1&threshold=3" -H "Accept: application/json"

#GET /v1/users-with-failed-payments - Test negative threshold (expect 422 error)
curl "http://127.0.0.1:18008/v1/users-with-failed-payments?days=60&threshold=-1" -H "Accept: application/json"

#GET /v1/user-order-stats - User order statistics (expect ~100 users with varied stats)
curl "http://127.0.0.1:18008/v1/user-order-stats" -H "Accept: application/json"
```