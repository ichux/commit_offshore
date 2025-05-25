# Commit Offshore
Pre-requisites:
- Install docker
- Install any SQL client e.g. TablePlus
- Have the docker command setup on your machine

Instructions
- Copy the .env_sample file to .env
- Start the env: docker compose up -d
- Stop the env: docker compose down -v
- PostgreSQL connection string is: `postgresql://offshore:G589cdc227bR@127.0.0.1:16432/offshore`
- `offshore:G589cdc227bR` should match the `POSTGRES_DB:POSTGRES_PASSWORD` in your .env
- the last `/offshore` is your `/POSTGRES_DB`, also in your .env

## API Endpoints

---
## 🧑‍🤝‍🧑 Users API

### 1. `GET /v1/users`

**Params:**

* `skip`: integer (pagination offset)
* `limit`: integer (pagination limit)

**Examples:**

* **Standard pagination (10 users):**
  `skip=0&limit=10` → returns 10 users
* **Pagination beyond data (\~100 users exist):**
  `skip=100&limit=10` → returns empty list
* **Negative limit (invalid):**
  `skip=0&limit=-1` → returns 422 error
* **Negative skip (invalid):**
  `skip=-1&limit=10` → returns 422 error

---

## 📦 Orders API

### 2. `GET /v1/orders`

**Params:**

* `skip`: integer (pagination offset)
* `limit`: integer (pagination limit)
* `user_id`: UUID (optional filter)

**Examples:**

* **All orders (first 10):**
  `skip=0&limit=10`
* **Filter by valid user ID:**
  `user_id=<valid-uuid>&skip=0&limit=5`
* **Filter by invalid user ID:**
  `user_id=00000000-0000-0000-0000-000000000000&skip=0&limit=5` → returns empty list
* **Pagination beyond data (\~200 orders):**
  `skip=200&limit=10` → returns empty list

---

## 💳 Payments API

### 3. `GET /v1/payments`

**Params:**

* `skip`: integer (pagination offset)
* `limit`: integer (pagination limit)

**Examples:**

* **Standard pagination (10 payments):**
  `skip=0&limit=10`
* **Pagination beyond data (\~150 payments):**
  `skip=150&limit=10` → returns empty list

---

## 🧾 Support Tickets API

### 4. `GET /v1/support-tickets`

**Params:**

* `skip`: integer (pagination offset)
* `limit`: integer (pagination limit)

**Examples:**

* **Standard pagination (10 tickets):**
  `skip=0&limit=10`
* **Pagination beyond data (\~50 tickets):**
  `skip=50&limit=10` → returns empty list

### 5. `GET /v1/recent-users`

**Params:**

* `days`: integer (number of recent days)

**Examples:**

* `days=7` → returns users from last 7 days (\~25 expected)
* `days=0` → returns 422 error
* `days=365` → returns all users (\~100)

---

### 6. `GET /v1/orders-by-unresolved-tickets`

**Params:** None

**Returns:** Orders from users with unresolved support tickets (\~10 users)

---

### 7. `GET /v1/total-spent-last-30-days`

**Params:** None

**Returns:** Total spent per user over last 30 days (\~33 successful payments)

---

### 8. `GET /v1/users-with-failed-payments`

**Params:**

* `days`: integer (time window in days)
* `threshold`: integer (minimum number of failed payments)

**Examples:**

* `days=60&threshold=3` → \~5 users
* `days=60&threshold=10` → empty list
* `days=1&threshold=3` → fewer or no users
* `days=60&threshold=-1` → 422 error

---

### 9. `GET /v1/user-order-stats`

**Params:** None
**Returns:** Statistics per user (order count, totals, etc.) for \~100 users
