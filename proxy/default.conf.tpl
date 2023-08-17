server {
    listen 9000;

    location /static {
        alias /app/static;
    }

    location / {
        uwsgi_pass 127.0.0.1:8000;
        include /etc/nginx/uwsgi_params;
    }
}
