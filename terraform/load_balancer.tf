resource "aws_lb" "practice_logs_alb" {
  name               = "${var.prefix}-lb"
  load_balancer_type = "application"
  subnets = [
    aws_subnet.practice_logs-public-a.id,
    aws_subnet.practice_logs-public-b.id,
  ]
  security_groups = [aws_security_group.lb.id]
}

resource "aws_lb_target_group" "practice_logs_alb_target_group" {
  name        = "${var.prefix}-lb-tg"
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"
  port        = 8000
  health_check {
    path = "/"
  }
}

resource "aws_lb_listener" "practice_logs_http" {
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

resource "aws_lb_listener" "practice_logs_https" {
  load_balancer_arn = aws_lb.practice_logs_alb.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate_validation.cert.certificate_arn
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.practice_logs_alb_target_group.arn
  }
}
