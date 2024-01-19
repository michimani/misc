
run "create_a_boolean_feature_flag" {
  variables {
    env = "test"
    project_name = "test-pj"
    features = {
      sushi = {
        description = "sushi is good"
        default_variation = "true"
        overrides = {}
      }
    }
  }

  assert {
    condition = aws_evidently_project.main.name == "test-test-pj-project"
    error_message = "Wrong project name"
  }

  assert {
    condition     = aws_evidently_feature.feature_flag["sushi"].name == "sushi"
    error_message = "Wrong feature value"
  }

  assert {
    condition = aws_evidently_feature.feature_flag["sushi"].default_variation == "true"
    error_message = "Wrong default variation"
  }
}

run "create_two_boolean_feature_flags" {
    variables {
    env = "test"
    project_name = "test-pj"
    features = {
      sushi = {
        description = "sushi is good"
        default_variation = "true"
        overrides = {}
      },
      niku = {
        description = "niku is good"
        default_variation = "false"
        overrides = {}
      }
    }
  }


  assert {
    condition = aws_evidently_project.main.name == "test-test-pj-project"
    error_message = "Wrong project name"
  }

  assert {
    condition     = aws_evidently_feature.feature_flag["sushi"].name == "sushi"
    error_message = "Wrong feature value"
  }

  assert {
    condition = aws_evidently_feature.feature_flag["sushi"].default_variation == "true"
    error_message = "Wrong default variation"
  }

  assert {
    condition     = aws_evidently_feature.feature_flag["niku"].name == "niku"
    error_message = "Wrong feature value"
  }

  assert {
    condition = aws_evidently_feature.feature_flag["niku"].default_variation == "false"
    error_message = "Wrong default variation"
  }
}