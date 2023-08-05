# ECS Cluster

resource "aws_ecs_cluster" "main" {
  name = "${var.prefix}-cluster"
}

resource "aws_cloudwatch_log_group" "ecs_task_logs" {
  name = "${var.prefix}-cw-logs"
}

resource "random_string" "django_secret_key" {
  length = 16
}

data "aws_ecr_image" "drums_practice_logs" {
  repository_name = "drums_practice_logs"
  image_tag       = "latest"
}

data "template_file" "ecs_container_definitions" {
  template = file("./templates/ecs/container-definition.json.tpl")
  vars = {
    app_image         = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${data.aws_ecr_image.drums_practice_logs.repository_name}:latest",
    django_secret_key = random_string.django_secret_key.result,
    db_host           = aws_db_instance.practice_logs.address,
    db_name           = aws_db_instance.practice_logs.db_name,
    db_user           = aws_db_instance.practice_logs.username,
    db_password       = aws_db_instance.practice_logs.password,
    log_group_name    = aws_cloudwatch_log_group.ecs_task_logs.name,
    log_group_region  = data.aws_region.current.name,
    allowed_hosts     = aws_route53_record.practice_logs.fqdn
  }
}

resource "aws_ecs_task_definition" "practice_logs" {
  family                   = "${var.prefix}-task-definition-practice-logs"
  container_definitions    = data.template_file.ecs_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.app_iam_role.arn
  volume {
    name = "static"
  }
}

resource "aws_ecs_service" "practice_logs" {
  name             = "${var.prefix}-service"
  cluster          = aws_ecs_cluster.main.name
  task_definition  = aws_ecs_task_definition.practice_logs.family
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "1.4.0"
  network_configuration {
    subnets = [
      aws_subnet.practice_logs-private-a.id,
      aws_subnet.practice_logs-private-b.id,
    ]
    security_groups = [aws_security_group.ecs.id]
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.practice_logs_alb_target_group.arn
    container_name   = "drums_practice_logs"
    container_port   = "8000"
  }
  depends_on = [
    aws_lb_listener.practice_logs_https
  ]
}