[
    {
        "name": "drums-practice-logs",
        "image": "${app_image}",
        "essential": true,
        "memory": 512,
        "environment": [
            {"name": "AWS_REGION", "value": "${aws_region}"},
            {"name": "DB_HOST", "value": "${db_host}"},
            {"name": "DB_NAME", "value": "${db_name}"},
            {"name": "DB_USER", "value": "${db_user}"},
            {"name": "DB_PASSWORD", "value": "${db_password}"},
            {"name": "DJANGO_SECRET_KEY", "value": "${django_secret_key}"},
            {"name": "ALLOWED_HOSTS", "value": "${allowed_hosts}"}
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/app/static",
                "sourceVolume": "static"
            }
        ],
        "logConfiguration" : {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${django_log_group_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "drums-practice-logs",
                "awslogs-create-group": "true"
            }
        },
        "portMappings": [
            {
                "containerPort": 8000,
                "hostPort": 8000,
                "protocol": "tcp"
            }
        ]
    },
    {
        "name": "nginx",
        "image": "${proxy_image}",
        "essential": true,
        "memory": 256,
        "portMappings": [
            {
                "containerPort": 9000,
                "hostPort": 9000,
                "protocol": "tcp"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/app/static",
                "sourceVolume": "static"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${proxy_log_group_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "nginx"
            }
        }
    }
]