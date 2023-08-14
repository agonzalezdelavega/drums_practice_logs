[
    {
        "name": "drums-practice-logs",
        "image": "${app_image}",
        "essential": true,
        "memoryReservation": 512,
        "environment": [
            {"name": "AWS_REGION", "value": "${aws_region}"},
            {"name": "DB_HOST", "value": "${db_host}"},
            {"name": "DB_NAME", "value": "${db_name}"},
            {"name": "DB_USER", "value": "${db_user}"},
            {"name": "DB_PASSWORD", "value": "${db_password}"},
            {"name": "DJANGO_SECRET_KEY", "value": "${django_secret_key}"}
        ],
        "mountPoints": [
            {
                "containerPath": "/usr/src/drums_practice_logs/staticfiles",
                "sourceVolume": "static_volume"
            }
        ],
        "logConfiguration" : {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${log_group_name}",
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
    }
]