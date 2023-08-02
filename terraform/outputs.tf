output "rds_username" {
  value     = aws_db_instance.learning_logs.username
  sensitive = true
}

output "rds_password" {
  value     = aws_db_instance.learning_logs.password
  sensitive = true
}

output "rds_connection_string" {
  value = aws_db_instance.learning_logs.endpoint
}

output "bastion_public_ip" {
  value = length(aws_instance.bastion-host) != 0 ? aws_instance.bastion-host[0].public_ip : ""
}

output "lambda_layer" {
  value = aws_lambda_layer_version.mysql_layer.arn
}

output "lambda_security_group" {
  value = aws_security_group.lambda.id
}

output "subnet_ids" {
  value = [aws_subnet.ll-private-1.id, aws_subnet.ll-private-2.id]
}