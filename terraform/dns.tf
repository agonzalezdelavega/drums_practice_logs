data "aws_route53_zone" "zone" {
  name = var.dns_zone_name
}

resource "aws_route53_record" "practice_logs" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "dpl.${data.aws_route53_zone.zone.name}"
  type    = "CNAME"
  ttl     = "300"
  records = [aws_lb.practice_logs_alb.dns_name]
}

resource "aws_acm_certificate" "cert" {
  domain_name       = aws_route53_record.practice_logs.fqdn
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  name    = tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_name
  records = [tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_value]
  type    = tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_type
  zone_id = data.aws_route53_zone.zone.zone_id
  ttl     = 60
}

resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [aws_route53_record.cert_validation.fqdn]
}