resource "aws_evidently_project" "main" {
  name = "${local.env}-${var.project_name}-project"

  tags = local.tags
}

# Features that has boolean value
resource "aws_evidently_feature" "feature_flag" {
  for_each = var.features

  project     = aws_evidently_project.main.name
  name        = each.key
  description = each.value.description

  dynamic "variations" {
    for_each = local.bool_variations
    iterator = v

    content {
      name = v.key
      value {
        bool_value = v.value
      }
    }
  }

  default_variation = each.value.default_variation

  entity_overrides = each.value.overrides

  lifecycle {
    ignore_changes = [
      default_variation,
    ]
  }
}

# Features that has string value
