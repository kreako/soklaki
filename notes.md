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

- 8080 is hasura graphql end point port
- 5432 is postgresql port
- 8000 is companion port

### Creation

podman pod create -p 8080:8080 -p 5432:5432 -p 8000:8000 --name sokakli

podman run -d \
    --restart=always \
    --pod sokakli \
    -e POSTGRES_PASSWORD="password" \
    -v ./pgdata/:/var/lib/postgresql/data:z \
    --name sokakli-db \
    postgres

podman run -d \
    --restart=always \
    --pod sokakli \
    -e HASURA_GRAPHQL_DATABASE_URL="postgres://postgres:password@127.0.0.1:5432/postgres" \
    -e HASURA_GRAPHQL_ENABLE_CONSOLE="false" \
    -e HASURA_GRAPHQL_DEV_MODE="true" \
    -e HASURA_GRAPHQL_ENABLED_LOG_TYPES="startup, http-log, webhook-log, websocket-log, query-log" \
    -e HASURA_GRAPHQL_UNAUTHORIZED_ROLE="anonymous" \
    -e HASURA_GRAPHQL_ADMIN_SECRET="hasura admin secret - keep in sync with hasura deployment" \
    --name sokakli-hasura \
    hasura/graphql-engine:v2.0.0-alpha.4

podman run -d \
    --restart=always \
    --pod sokakli \
    --name sokakli-companion \
    sokakli-companion

### Start the pod

$ podman pod start sokakli


### Restart individually

podman stop sokakli-db && podman rm sokakli-db

podman stop sokakli-hasura && podman rm sokakli-hasura

### Run inside the container

podman exec -it sokakli-hasura /bin/bash
