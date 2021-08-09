# Notes

## Frontend creation

npm init @vitejs/app frontend
cd frontend
npm install
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
npx tailwindcss init -p
npm install vuex@next
npm install vue-router@4

## backend containers

### Ports

Take a look at ansible/roles/podman to see if something is missing

- 8080 is hasura graphql end point port
- 5432 is postgresql port
- 8000 is companion port
- 8001 is the exporter
- 8008 is the backend

### Creation

podman pod create -p 8080:8080 -p 5432:5432 -p 8000:8000 -p 8001:8001 --name soklaki

podman run -d \
 --restart=always \
 --pod soklaki \
 -e POSTGRES_PASSWORD="password" \
 -v ./pgdata/:/var/lib/postgresql/data:z \
 --name soklaki-db \
 postgres

podman run -d \
 --restart=always \
 --pod soklaki \
 -e HASURA_GRAPHQL_DATABASE_URL="postgres://postgres:password@127.0.0.1:5432/postgres" \
 -e HASURA_GRAPHQL_ENABLE_CONSOLE="false" \
 -e HASURA_GRAPHQL_DEV_MODE="true" \
 -e HASURA_GRAPHQL_ENABLED_LOG_TYPES="startup, http-log, webhook-log, websocket-log, query-log" \
 -e HASURA_GRAPHQL_UNAUTHORIZED_ROLE="anonymous" \
 -e HASURA_GRAPHQL_ADMIN_SECRET="hasura admin secret - keep in sync with hasura deployment" \
 -e HASURA_GRAPHQL_JWT_SECRET='{"type": "HS256", "key": "biew5Phiz5uoNg7Oobunee0ahd0ohbao"}' \
 --name soklaki-hasura \
 hasura/graphql-engine:v2.0.5

podman run -d \
 --restart=always \
 --pod soklaki \
 --name soklaki-companion \
 soklaki-companion

### Start the pod

$ podman pod start soklaki

### Run the companion for debug

podman run -it --rm \
 --pod soklaki \
 --name soklaki-companion \
 -v ./reports/:/reports:z \
 soklaki-companion

or copy file to the running container :

podman cp src/main.py soklaki-companion:/app/

Rebuild with :

podman build -t soklaki-companion -f ./Dockerfile .

Full command :

podman rm soklaki-companion; podman build -t soklaki-companion -f ./Dockerfile . && podman run -it --rm --pod soklaki --name soklaki-companion -v ./reports/:/reports:z soklaki-companion

### Stop/Delete individually

podman stop soklaki-db && podman rm soklaki-db

podman stop soklaki-hasura && podman rm soklaki-hasura

### Run inside the container

podman exec -it soklaki-hasura /bin/bash

## Ansible

### Installation

#### Ansible

sudo dnf install ansible

### Podman modules

ansible-galaxy collection install containers.podman

### Snaps module

ansible-galaxy collection install community.general

### Selinux module

ansible-galaxy collection install ansible.posix

### Ssh key copy

ssh-copy-id <user>@<ip>

## Supervision

### Prometheus

podman run -p 9090:9090 -v $HOME/prometheus/config:/etc/prometheus/:z prom/prometheus

## Backend

### Todo

When hasura is not anymore in charge :

https://github.com/rust-db/refinery
For Migrations

https://crates.io/crates/barrel
For typed migrations
