#!/bin/bash

set -euo pipefail

DB_NAME="${1:-development_db}"

# Check that dependencies are installed
DOCKER_VERSION=$(docker --version)
echo "Docker: ${DOCKER_VERSION}"

FAUNA_SHELL_VERSION=$(fauna --version)
echo "Fauna Shell: ${FAUNA_SHELL_VERSION}"

# Run FaunaDB
docker pull fauna/faunadb
docker run -d --name faunadb -p 8443:8443 -p 8084:8084 fauna/faunadb

# Give the DB time to start up before sending commands
# (wait-for-it doesn't work here, because there's a delay between
# the port being ready and the DB being ready)
sleep 2

# Configure database
fauna add-endpoint http://localhost:8443/ --alias localhost --key secret
fauna create-database ${DB_NAME} --endpoint=localhost

# Create an API key and save it in .env
touch .env

if [ -z "$(cat .env | grep FAUNADB_KEY)" ]
then
  # create-key command includes the line: "  secret: <API token string>"
  FAUNADB_KEY="$(fauna create-key ${DB_NAME} --endpoint=localhost | grep secret: | cut -d " " -f 4)"
  echo "FAUNADB_KEY=${FAUNADB_KEY}" >> .env
fi
