FROM nginx:stable-alpine

ADD . /usr/share/nginx/html
COPY nginx.conf /etc/ngingx/nginx.conf
RUN chown nginx:nginx -R /usr/share/nginx/html
