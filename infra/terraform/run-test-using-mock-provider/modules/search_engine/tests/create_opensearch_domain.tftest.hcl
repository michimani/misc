mock_provider "aws" {
  mock_resource "aws_opensearch_domain" {
    defaults = {}
  }
}

run "create_opensearch_domain" {
  variables {
    env = "test"
    project_name = "test-pj"
    engine_version = "OpenSearch_2.11"
  }

  assert {
    condition = aws_opensearch_domain.main.domain_name == "test-test-pj-os"
    error_message = "Wrong domain name"
  }

  assert {
    condition = aws_opensearch_domain.main.engine_version == "OpenSearch_2.11"
    error_message = "Wrong engine version"
  }
}