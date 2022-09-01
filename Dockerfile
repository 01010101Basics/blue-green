FROM nginx:latest
COPY ./html/* /usr/share/nginx/html/
WORKDIR /usr/share/nginx/html
