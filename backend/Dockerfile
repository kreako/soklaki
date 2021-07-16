FROM rust:1.53

WORKDIR /app

COPY . .

RUN cargo install --path .

CMD [ "backend" ]
