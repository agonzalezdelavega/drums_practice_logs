variable "prefix" {
  type    = string
  default = "learning_logs"
}

variable "rds_user" {
  type = string
}

variable "rds_snapshot_identifier" {
  type    = string
  default = "learninglogs"
}