resource "aws_s3_bucket" "this" {
  bucket = "${local.name}-data"
  tags   = local.tags
}