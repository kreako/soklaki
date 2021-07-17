FROM rust:1.53

WORKDIR /app

# dummy hack to cache dependencies build
COPY dummy.rs .
COPY Cargo.toml .
RUN sed -i 's#src/main.rs#dummy.rs#' Cargo.toml
RUN cargo build --release

# Now build the complete app
RUN sed -i 's#dummy.rs#src/main.rs#' Cargo.toml
COPY . .
RUN cargo build --release

# Launch from target dir
CMD [ "target/release/backend" ]
