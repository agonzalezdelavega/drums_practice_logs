# ECS Cluster

resource "aws_ecs_cluster" "main" {
  name = "${local.prefix}-cluster"
}

# Logging
resource "aws_cloudwatch_log_group" "ecs_django_logs" {
  name = "${local.prefix}-django-logs"
}

resource "aws_cloudwatch_log_group" "proxy" {
  name = "${local.prefix}-nginx"
}

# Container definition

resource "random_string" "django_secret_key" {
  length = 16
}

data "aws_ecr_image" "drums_practice_logs" {
  repository_name = local.django_image
  image_tag       = "latest"
}


data "aws_ecr_image" "proxy_image" {
  repository_name = local.proxy_image
  image_tag       = "latest"
}

data "template_file" "ecs_container_definitions" {
  template = file("./templates/ecs/container-definition.json.tpl")
  vars = {
    aws_region            = data.aws_region.current.name,
    app_image             = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${data.aws_ecr_image.drums_practice_logs.repository_name}:latest",
    proxy_image           = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${data.aws_ecr_image.proxy_image.repository_name}:latest",
    django_secret_key     = random_string.django_secret_key.result,
    allowed_hosts         = aws_route53_record.app.fqdn,
    db_host               = aws_db_instance.practice_logs.address,
    db_name               = aws_db_instance.practice_logs.db_name,
    db_user               = aws_db_instance.practice_logs.username,
    db_password           = aws_db_instance.practice_logs.password,
    django_log_group_name = aws_cloudwatch_log_group.ecs_django_logs.name,
    proxy_log_group_name  = aws_cloudwatch_log_group.proxy.name
  }
}

resource "aws_ecs_task_definition" "practice_logs" {
  family                   = "${local.prefix}-task-definition-practice-logs"
  container_definitions    = data.template_file.ecs_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 2048
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.app_iam_role.arn
  volume {
    name = "static"
  }
}

# ECS Service

resource "aws_ecs_service" "practice_logs" {
  name             = "${local.prefix}-service"
  cluster          = aws_ecs_cluster.main.name
  task_definition  = aws_ecs_task_definition.practice_logs.family
  desired_count    = 2
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
    container_name   = "nginx"
    container_port   = 9000
  }
}