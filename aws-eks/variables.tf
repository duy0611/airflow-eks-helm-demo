#
# Variables Configuration
#

variable "cluster-name" {
  default = "terraform-eks-demo"
  type    = "string"
}

variable "profile" {
  default = "valuemotive"
  type    = "string"
}

variable "ec2-instance-type" {
  default = "t2.medium"
  type    = "string"
  description = "EC2 Instance Type, e.g. t2.medium, m4.large, m5.large"
}