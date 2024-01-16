Terraform and OpenTofu
===

## Overview

This repository contains Terraform and OpenTofu configuration files to deploy some resources on AWS.

## Requirements

- Terraform v1.6.6
- OpenTofu v1.6.0
- aws-provider v5.32.1

## Usage

### Initialize

In case of using Terraform, you need to initialize by the following command.

```bash
cd terraform \
&& terraform init
```

In case of using OpenTofu, you need to initialize by the following command.

```bash
cd opentofu \
&& tofu init
```

### Plan

In case of using Terraform, you need to plan by the following command.

```bash
cd terraform \
&& terraform plan
```

In case of using OpenTofu, you need to plan by the following command.

```bash
cd opentofu \
&& tofu plan
```

### Apply

In case of using Terraform, you need to apply by the following command.

```bash
cd terraform \
&& terraform apply
```

In case of using OpenTofu, you need to apply by the following command.

```bash
cd opentofu \
&& tofu apply
```

### Destroy

In case of using Terraform, you need to destroy by the following command.

```bash
cd terraform \
&& terraform destroy
```

In case of using OpenTofu, you need to destroy by the following command.

```bash
cd opentofu \
&& tofu destroy
```
