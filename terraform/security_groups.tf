# Load Balancer

resource "aws_security_group" "lb" {
  name   = "${local.prefix}-elb"
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.practice_logs-private-2a.cidr_block,
      aws_subnet.practice_logs-private-2b.cidr_block
    ]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# NAT Instances

resource "aws_security_group" "nat" {
  name   = "${local.prefix}-nat"
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_vpc_security_group_ingress_rule" "nat_ingress_elb" {
  security_group_id            = aws_security_group.nat.id
  referenced_security_group_id = aws_security_group.lb.id
  from_port                    = 9000
  to_port                      = 9000
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "nat_ingress_ecs" {
  security_group_id            = aws_security_group.nat.id
  referenced_security_group_id = aws_security_group.ecs.id
  from_port                    = 9000
  to_port                      = 9000
  ip_protocol                  = "tcp"
}

# ECS 

resource "aws_security_group" "ecs" {
  name   = "${local.prefix}-ecs-service"
  vpc_id = aws_vpc.main.id
  egress {
    from_port = 3306
    to_port   = 3306
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.practice_logs-private-2a.cidr_block,
      aws_subnet.practice_logs-private-2b.cidr_block
    ]
  }
  ingress {
    from_port       = 9000
    to_port         = 9000
    protocol        = "tcp"
    security_groups = [aws_security_group.lb.id]
  }
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_vpc_security_group_ingress_rule" "ecs_ingress_nat" {
  security_group_id            = aws_security_group.ecs.id
  referenced_security_group_id = aws_security_group.nat.id
  from_port                    = 9000
  to_port                      = 9000
  ip_protocol                  = "tcp"
}

# RDS

resource "aws_security_group" "rds" {
  name   = "${local.prefix}-rds"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "TCP"
    security_groups = [aws_security_group.ecs.id]
  }

  timeouts {
    delete = "5m"
  }
}
