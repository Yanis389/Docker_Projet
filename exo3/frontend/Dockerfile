FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY index.html.template index.html.template
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY .env .

RUN apk add --no-cache bash gettext \
 && envsubst < index.html.template > index.html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
