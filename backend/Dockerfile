# Could use a smaller one but this is still needed to compile so...
FROM rust:1.53

WORKDIR /app
COPY target/release/backend .
COPY Rocket.toml .
COPY .env .

# Launch from target dir
CMD [ "/app/backend" ]
