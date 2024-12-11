resource "launchdarkly_project" "main" {
  key  = local.project_name
  name = local.project_name

  environments {
    key   = "test"
    name  = "Test"
    color = "F5A623"
  }

  tags = [
    "terraform",
    "test",
  ]
}


resource "launchdarkly_feature_flag" "main" {
  project_key = launchdarkly_project.main.key
  key         = local.feature_name
  name        = local.feature_name
  description = "Feature flag for ${local.feature_name}"

  variation_type = "boolean"

  variations {
    value = false
    name  = "Disabled"
  }
  variations {
    value = true
    name  = "Enabled"
  }

  defaults {
    on_variation  = 0
    off_variation = 1
  }

  tags = ["terraform", "test"]
}

resource "launchdarkly_feature_flag_environment" "main" {
  flag_id = launchdarkly_feature_flag.main.id
  env_key = launchdarkly_project.main.environments[0].key

  on = true

  targets {
    values    = ["user-1"]
    variation = 1
  }

  fallthrough {
    variation = 0
  }

  off_variation = 0
}
