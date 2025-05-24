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
