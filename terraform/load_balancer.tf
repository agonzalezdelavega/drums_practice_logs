resource "aws_lb" "practice_logs_alb" {
  name               = "${local.prefix}-lb"
  load_balancer_type = "application"
  subnets = [
    aws_subnet.practice_logs-public-2a.id,
    aws_subnet.practice_logs-public-2b.id
  ]
  security_groups = [aws_security_group.lb.id]
}

resource "aws_lb_target_group" "practice_logs_alb_target_group" {
  name        = "${local.prefix}-target-group"
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"
  port        = 9000
  health_check {
    path    = "/health"
    port    = 9000
    matcher = 200
  }
  # stickiness {
  #   type        = "app_cookie"
  #   cookie_name = "drums_practice_logs"
  #   enabled     = true
  # }
}

resource "aws_lb_listener" "app_http" {
  load_balancer_arn = aws_lb.practice_logs_alb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type = "redirect"
    redirect {
      port        = 443
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "app_https" {
  load_balancer_arn = aws_lb.practice_logs_alb.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate_validation.cert.certificate_arn
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.practice_logs_alb_target_group.arn
  }
}