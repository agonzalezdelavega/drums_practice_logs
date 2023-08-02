# RDS Instance

data "aws_db_snapshot" "learning_logs" {
  db_instance_identifier = "learninglogs"
  most_recent            = true
}

resource "aws_db_instance" "learning_logs" {
  db_name                = "learninglogs"
  identifier             = "learninglogs"
  instance_class         = "db.t2.micro"
  engine                 = "mysql"
  engine_version         = "8.0.28"
  username               = var.rds_user
  password               = data.aws_secretsmanager_random_password.db_password.random_password
  port                   = 3306
  allocated_storage      = 20
  skip_final_snapshot    = true
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
  snapshot_identifier    = data.aws_db_snapshot.learning_logs.id
  vpc_security_group_ids = [aws_security_group.rds.id]
  apply_immediately      = true
  lifecycle {
    ignore_changes = [
      password
    ]
  }
  tags = {
    application = "learning-logs"
  }
  depends_on = [
    data.aws_db_snapshot.learning_logs
  ]
}

resource "aws_db_subnet_group" "db_subnet_group" {
  name = "learning_logs"
  subnet_ids = [
    aws_subnet.ll-private-1.id,
    aws_subnet.ll-private-2.id
  ]
}

# Security Group

resource "aws_security_group" "rds" {
  name   = "${var.prefix}-rds"
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.prefix}-rds"
  }
  timeouts {
    delete = "5m"
  }
}

resource "aws_security_group_rule" "mysql_ingress_lambda" {
  type              = "ingress"
  from_port         = 3306
  to_port           = 3306
  protocol          = "TCP"
  security_group_id = aws_security_group.rds.id
  cidr_blocks = [
    aws_subnet.ll-private-1.cidr_block,
    aws_subnet.ll-private-2.cidr_block
  ]
  depends_on = [
    aws_security_group.bastion-host
  ]
}

resource "aws_security_group_rule" "mysql_ingress_bastion" {
  type                     = "ingress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "TCP"
  security_group_id        = aws_security_group.rds.id
  source_security_group_id = aws_security_group.bastion-host.id
  depends_on = [
    aws_security_group.bastion-host
  ]
}

# RDS Credentials

data "aws_secretsmanager_random_password" "db_password" {
  password_length     = 8
  exclude_punctuation = true
}

resource "aws_ssm_parameter" "db_credentials" {
  name = "learning_logs_db_credentials"
  type = "SecureString"
  value = jsonencode({
    engine   = aws_db_instance.learning_logs.engine
    username = aws_db_instance.learning_logs.username
    password = aws_db_instance.learning_logs.password
    host     = aws_db_instance.learning_logs.endpoint
    dbname   = aws_db_instance.learning_logs.db_name
    port     = aws_db_instance.learning_logs.port
  })
  lifecycle {
    ignore_changes = [
      insecure_value
    ]
  }
}