FROM node:14

WORKDIR /app

# First install dependencies
COPY package*.json .
RUN npm install

# Copy src package
COPY . .

# Build
RUN npm run build

ENTRYPOINT [ "/bin/bash", "-c" ]
CMD [ "cp", "-rf", "/app/dist/*", "/dist" ]