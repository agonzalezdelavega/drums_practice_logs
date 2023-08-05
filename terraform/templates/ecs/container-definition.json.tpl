[
    {
        "name": "nasa-apod",
        "image": "${app_image}",
        "essential": true,
        "memoryReservation": 256,
        "environment": [
            {"name": "AWS_REGION", "value": "${aws_region}"},
            {"name": "COGNITO_URL", "value": "${cognito_url}"},
            {"name": "COGNITO_CLIENT_ID", "value": "${cognito_client_id}"},
            {"name": "USER_POOL_ID", "value": "${user_pool_id}"},
            {"name": "DYNAMO_DB_SESSIONS_TABLE_NAME", "value": "${dynamo_db_sessions_table_name}"},
            {"name": "DYNAMO_DB_SESSIONS_TABLE_PARTITION_KEY", "value": "${dynamo_db_sessions_partition_key}"},
            {"name": "DYNAMO_DB_FAVORITES_TABLE_NAME", "value": "${dynamo_db_favorites_table_name}"},
            {"name": "DYNAMO_DB_FAVORITES_TABLE_PARTITION_KEY", "value": "${dynamo_db_favorites_partition_key}"},
            {"name": "DYNAMO_DB_TABLE_ENDPOINT", "value": "${dynamo_db_endpoint}"},
            {"name": "EXPRESS_SECRET", "value": "${express_session_secret}"},
            {"name": "API_KEY", "value": "${api_key}"}
        ],
        "logConfiguration" : {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${log_group_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "apod-webapp",
                "awslogs-create-group": "true"
            }
        },
        "portMappings": [
            {
                "containerPort": 3000,
                "hostPort": 3000
            }
        ]
    }
]