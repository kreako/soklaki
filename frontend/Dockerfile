FROM node:14

WORKDIR /app

# First install dependencies
COPY package*.json .
RUN npm install

# Copy src package
COPY index.html .
COPY tailwind.config.cjs .
COPY vite.config.js .
COPY postcss.config.cjs .
COPY jest.config.mjs .
COPY src .
COPY tests .
COPY public .
COPY tailwindcss-plugins .

# Build
RUN npm run build