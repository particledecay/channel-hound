#!/bin/bash

# BEGIN EDITABLE VALUES
PG_USER=postgres
PG_HOST=localhost
PG_PORT=5432
# END EDITABLE VALUES

docker_wrap=false
if [ ! -x $(which psql) ]
then
  if [ -x $(which docker) ]
  then
    docker_wrap=true
  else
    echo "no 'psql' command found, and docker not installed for fallback use"
    exit 1
  fi
fi

cmd=
if [ $docker_wrap = true ]
then
  docker_pg_host=$PG_HOST
  if [[ "${PG_HOST}" == "localhost" ]]
  then
    docker_pg_host=172.17.0.1
  fi
  cmd="docker run postgres psql -U ${PG_USER} -h ${docker_pg_host} -p ${PG_PORT} -c"
else
  cmd="psql -U ${PG_USER} -h ${PG_HOST} -p ${PG_PORT} -c"
fi

# install extension
${cmd} "CREATE EXTENSION pg_trgm"

# create user
${cmd} "CREATE ROLE houndadmin WITH PASSWORD '${PG_PASS:-houndH0uNd}'"
${cmd} "ALTER ROLE houndadmin WITH LOGIN"

# create database
${cmd} "CREATE DATABASE channel_hound"

# grant
${cmd} "GRANT ALL PRIVILEGES ON DATABASE channel_hound TO houndadmin"
