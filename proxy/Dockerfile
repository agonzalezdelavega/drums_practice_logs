FROM nginxinc/nginx-unprivileged

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params

USER root

RUN mkdir -p /app/static
RUN chmod 555 /app/static
RUN touch /etc/nginx/conf.d/default.conf
RUN chown nginx:nginx /etc/nginx/conf.d/default.conf

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

USER nginx

CMD ["/entrypoint.sh"]