# VPC

resource "aws_vpc" "main" {
  cidr_block           = "192.168.0.0/16"
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${local.prefix}-vpc-main"
  }
}

resource "aws_subnet" "practice_logs-public-2a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "192.168.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${data.aws_region.current.name}a"
  tags = {
    Name = "${local.prefix}-public-a"
  }
  depends_on = [
    aws_vpc.main
  ]
}

resource "aws_subnet" "practice_logs-public-2b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "192.168.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${data.aws_region.current.name}b"
  tags = {
    Name = "${local.prefix}-public-b"
  }
  depends_on = [
    aws_vpc.main
  ]
}

resource "aws_subnet" "practice_logs-private-2a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "192.168.3.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "${data.aws_region.current.name}a"
  tags = {
    Name = "${local.prefix}-private-a"
  }
  depends_on = [
    aws_vpc.main
  ]
}

resource "aws_subnet" "practice_logs-private-2b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "192.168.4.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "${data.aws_region.current.name}b"
  tags = {
    Name = "${local.prefix}-private-b"
  }
  depends_on = [
    aws_vpc.main
  ]
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${local.prefix}-internet-gateway"
  }
  depends_on = [
    aws_vpc.main
  ]
}

# NAT Instance

data "aws_ami" "nat-instance-ami" {
  owners      = ["amazon"]
  most_recent = true
  filter {
    name   = "name"
    values = [var.nat_ami_name] # Must be an Amazon Linux 2023 AMI
  }
}

resource "aws_iam_instance_profile" "nat_instance_profile" {
  name = "${local.prefix}-nat-instances"
  role = aws_iam_role.nat.name
}

resource "aws_network_interface" "nat-2a" {
  subnet_id         = aws_subnet.practice_logs-public-2a.id
  source_dest_check = false
  security_groups   = [aws_security_group.nat.id]
}

resource "aws_eip" "eip-2a" {
  network_interface = aws_network_interface.nat-2a.id
}

resource "aws_launch_template" "nat-2a" {
  name          = "${local.prefix}-nat-2a"
  image_id      = data.aws_ami.nat-instance-ami.id
  instance_type = "t3.nano"
  network_interfaces {
    network_interface_id = aws_network_interface.nat-2a.id
  }
  iam_instance_profile {
    arn = aws_iam_instance_profile.nat_instance_profile.arn
  }
  user_data = filebase64("./templates/scripts/user-data.sh")
}

resource "aws_autoscaling_group" "nat-2a" {
  availability_zones = [aws_subnet.practice_logs-public-2a.availability_zone]
  desired_capacity   = 1
  min_size           = 1
  max_size           = 1
  launch_template {
    id      = aws_launch_template.nat-2a.id
    version = "$Latest"
  }
}

resource "aws_network_interface" "nat-2b" {
  subnet_id         = aws_subnet.practice_logs-public-2b.id
  source_dest_check = false
  security_groups   = [aws_security_group.nat.id]
}

resource "aws_eip" "eip-2b" {
  network_interface = aws_network_interface.nat-2b.id
}

resource "aws_launch_template" "nat-2b" {
  name          = "${local.prefix}-nat-2b"
  image_id      = data.aws_ami.nat-instance-ami.id
  instance_type = "t3.nano"
  network_interfaces {
    network_interface_id = aws_network_interface.nat-2b.id
  }
  iam_instance_profile {
    arn = aws_iam_instance_profile.nat_instance_profile.arn
  }
  user_data = filebase64("./templates/scripts/user-data.sh")
}

resource "aws_autoscaling_group" "nat-2b" {
  availability_zones = [aws_subnet.practice_logs-public-2b.availability_zone]
  desired_capacity   = 1
  min_size           = 1
  max_size           = 1
  launch_template {
    id      = aws_launch_template.nat-2b.id
    version = "$Latest"
  }
}

# Route Tables

resource "aws_route_table" "route-table-public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table" "route-table-private-2a" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block           = "0.0.0.0/0"
    network_interface_id = aws_network_interface.nat-2a.id
  }
}

resource "aws_route_table" "route-table-private-2b" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block           = "0.0.0.0/0"
    network_interface_id = aws_network_interface.nat-2b.id
  }
}

resource "aws_route_table_association" "route-table-association-public-2a" {
  subnet_id      = aws_subnet.practice_logs-public-2a.id
  route_table_id = aws_route_table.route-table-public.id
}

resource "aws_route_table_association" "route-table-association-public-2b" {
  subnet_id      = aws_subnet.practice_logs-public-2b.id
  route_table_id = aws_route_table.route-table-public.id
}

resource "aws_route_table_association" "route-table-association-private-2a" {
  subnet_id      = aws_subnet.practice_logs-private-2a.id
  route_table_id = aws_route_table.route-table-private-2a.id
}

resource "aws_route_table_association" "route-table-association-private-2b" {
  subnet_id      = aws_subnet.practice_logs-private-2b.id
  route_table_id = aws_route_table.route-table-private-2b.id
}