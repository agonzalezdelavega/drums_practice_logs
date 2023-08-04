variable "prefix" {
  type    = string
  default = "drums-practice-logs"
}

variable "rds_user" {
  type = string
}

variable "dns_zone_name" {
  type = string
}

variable "rds_snapshot_identifier" {
  type    = string
  default = "practicelogs"
}