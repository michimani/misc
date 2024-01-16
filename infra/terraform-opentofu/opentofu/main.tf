resource "aws_evidently_project" "main" {
  name = "opentofu-project"
}

# Features that has boolean value
resource "aws_evidently_feature" "bool_feature" {
  project = aws_evidently_project.main.name
  name    = "bool-feature"

  variations {
    name = "true"
    value {
      bool_value = true
    }
  }


  default_variation = "true"

  lifecycle {
    ignore_changes = [
      default_variation,
    ]
  }
}
