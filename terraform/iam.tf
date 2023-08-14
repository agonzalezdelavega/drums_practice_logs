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
