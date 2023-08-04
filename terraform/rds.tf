# RDS Instance

resource "aws_db_instance" "practice_logs" {
  db_name                = "practicelogs"
  identifier             = "practicelogs"
  instance_class         = "db.t3.micro"
  engine                 = "postgres"
  engine_version         = "14.5"
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
  password_length     = 8
  exclude_punctuation = true
}
