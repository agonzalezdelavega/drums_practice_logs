# RDS Instance

resource "aws_db_instance" "practice_logs" {
  db_name                = "practicelogs"
  identifier             = "practicelogs"
  instance_class         = "db.t3.micro"
  engine                 = "mysql"
  engine_version         = "8.0.33"
  username               = var.rds_user
  password               = data.aws_secretsmanager_random_password.db_password.random_password
  port                   = 3306
  allocated_storage      = 20
  skip_final_snapshot    = true
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  apply_immediately      = true
  lifecycle {
    ignore_changes = [
      password
    ]
  }
  depends_on = [
    aws_security_group.rds
  ]
}

resource "aws_db_subnet_group" "db_subnet_group" {
  name = "practice_logs"
  subnet_ids = [
    aws_subnet.practice_logs-private-a.id,
    aws_subnet.practice_logs-private-b.id
  ]
}

# RDS Credentials

data "aws_secretsmanager_random_password" "db_password" {
  password_length     = 16
  exclude_punctuation = true
}

# resource "aws_secretsmanager_secret" "secrets_manager_db_password" {
#   name = "${local.prefix}-password"
# }

# resource "aws_secretsmanager_secret_version" "secrets_manager_db_password_version" {
#   secret_id     = aws_secretsmanager_secret.secrets_manager_db_password.id
#   secret_string = data.aws_secretsmanager_random_password.db_password.random_password
# }