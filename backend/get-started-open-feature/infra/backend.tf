terraform {
  backend "local" {
    path = "feature-flags.tfstate"
  }
}