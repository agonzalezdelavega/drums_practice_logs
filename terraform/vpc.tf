# VPC

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${local.prefix}-vpc-main"
  }
}

resource "aws_subnet" "practice_logs-public-a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${data.aws_region.current.name}a"
  tags = {
    Name = "${local.prefix}-public-a"
  }
  depends_on = [
    aws_vpc.main
  ]
}

resource "aws_subnet" "practice_logs-public-b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${data.aws_region.current.name}b"
  tags = {
    Name = "${local.prefix}-public-b"
  }
  depends_on = [
    aws_vpc.main
  ]
}

resource "aws_subnet" "practice_logs-private-a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.3.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "${data.aws_region.current.name}a"
  tags = {
    Name = "${local.prefix}-private-a"
  }
  depends_on = [
    aws_vpc.main
  ]
}

resource "aws_subnet" "practice_logs-private-b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.4.0/24"
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

resource "aws_eip" "eip1" {}

resource "aws_eip" "eip2" {}

resource "aws_nat_gateway" "nat1" {
  subnet_id     = aws_subnet.practice_logs-public-a.id
  allocation_id = aws_eip.eip1.id
  depends_on = [
    aws_subnet.practice_logs-public-a,
    aws_eip.eip1
  ]
}

resource "aws_nat_gateway" "nat2" {
  subnet_id     = aws_subnet.practice_logs-public-b.id
  allocation_id = aws_eip.eip2.id
  depends_on = [
    aws_subnet.practice_logs-public-b,
    aws_eip.eip2
  ]
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table" "private1" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat1.id
  }
}

resource "aws_route_table" "private2" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat2.id
  }
}

resource "aws_route_table_association" "public1" {
  route_table_id = aws_route_table.public.id
  subnet_id      = aws_subnet.practice_logs-public-a.id
}

resource "aws_route_table_association" "public2" {
  route_table_id = aws_route_table.public.id
  subnet_id      = aws_subnet.practice_logs-public-b.id
}

resource "aws_route_table_association" "private1" {
  route_table_id = aws_route_table.private1.id
  subnet_id      = aws_subnet.practice_logs-private-a.id
}

resource "aws_route_table_association" "private2" {
  route_table_id = aws_route_table.private2.id
  subnet_id      = aws_subnet.practice_logs-private-b.id
}