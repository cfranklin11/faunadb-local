# faunadb-local
Example code for tutorial for FaunaDB local development

## Quick Setup

- Install [Docker](https://docs.docker.com/get-docker/), so we can run an instance of FaunaDB in a container.
- Install [`fauna-shell`](https://docs.fauna.com/fauna/current/integrations/shell/) to be able to interact with local FaunaDB databases.
- Run `./setup_faunadb.sh` (if you've run the script before, be sure to delete `FAUNADB_KEY` from `.env` before running it again).
  - To set the database name to something other than the default (`development_db`), add it as an argument: `./setup_faunadb.sh my_custom_db_name`.
