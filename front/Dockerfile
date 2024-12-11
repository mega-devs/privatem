FROM node:16 as build-stage
WORKDIR /proto_app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build