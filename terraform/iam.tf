resource "aws_iam_role" "task_execution_role" {
  name               = "${local.prefix}-task-exec-role"
  assume_role_policy = file("./templates/iam/ecs-assume-role-policy.json")
}

resource "aws_iam_policy" "task_execution_role_policy" {
  name   = "${local.prefix}-task-exec-role-policy"
  path   = "/"
  policy = file("./templates/iam/ecs-task-exec-role.json")
}

resource "aws_iam_role_policy_attachment" "task_execution_role_policy_attachment" {
  role       = aws_iam_role.task_execution_role.name
  policy_arn = aws_iam_policy.task_execution_role_policy.arn
}

resource "aws_iam_role" "app_iam_role" {
  name               = "${local.prefix}-api-task"
  assume_role_policy = file("./templates/iam/ecs-assume-role-policy.json")
}

# NAT Instances

resource "aws_iam_role" "nat" {
  name = "${local.prefix}-nat-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = "AssumeLambdaRole"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

data "template_file" "nat_task_role_policy" {
  template = file("./templates/iam/nat-instance-profile.json.tpl")
  vars = {
    aws_region       = data.aws_region.current.name,
    account          = data.aws_caller_identity.current.account_id,
    eip-allocation-a = aws_eip.eip-2a.allocation_id
    eip-allocation-b = aws_eip.eip-2b.allocation_id
  }
}

resource "aws_iam_policy" "nat-iam-policy" {
  name   = "${local.prefix}-nat-policy"
  policy = data.template_file.nat_task_role_policy.rendered
}

resource "aws_iam_role_policy_attachment" "nat-iam-policy-attachment" {
  role       = aws_iam_role.nat.name
  policy_arn = aws_iam_policy.nat-iam-policy.arn
}