# build
FROM node:16 AS build-stage
WORKDIR /proto_app
COPY package*.json ./
RUN npm install -f
COPY . .
RUN npm run build -f

# runtime
FROM node:16 AS production-stage
WORKDIR /proto_app
COPY --from=build-stage /proto_app/dist ./dist
COPY package*.json ./
RUN npm install --only=production -f
CMD ["npm", "start"]
