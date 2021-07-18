# Could use a smaller one but this is still needed to compile so...
FROM rust:1.53

WORKDIR /app
COPY target/release/backend /app
COPY Rocket.toml /app
COPY .env /app

# Launch from target dir
CMD [ "/app/backend" ]
