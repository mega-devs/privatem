FROM nginx:stable-alpine as production-stage
WORKDIR /nginx
COPY --from=build-stage /proto_app/dist /usr/share/nginx/html
COPY ../default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]