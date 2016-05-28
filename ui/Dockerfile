FROM nginx:stable-alpine

ADD . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/
RUN chown nginx:nginx -R /usr/share/nginx/html
