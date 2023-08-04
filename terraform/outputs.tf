output "rds_username" {
  value     = aws_db_instance.practice_logs.username
  sensitive = true
}

output "rds_password" {
  value     = aws_db_instance.practice_logs.password
  sensitive = true
}

output "rds_connection_string" {
  value = aws_db_instance.practice_logs.endpoint
}