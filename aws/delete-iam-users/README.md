# delete-iam-users

A bash script for bulk-deleting AWS IAM Users, including all of their dependent resources.

## Motivation

IAM's `DeleteUser` API call fails if the user still has any dependent resources
attached — access keys, a login profile, MFA devices, policies, group
memberships, and so on. Cleaning all of that up by hand for even a handful of
users is tedious and error-prone, especially when you're offboarding several
accounts at once (e.g. after an audit, an incident, or a team change).

This script automates that cleanup so a batch of IAM Users can be removed
safely and consistently, with a dry-run mode to preview exactly what would
happen before anything is actually deleted.

## How IAM User deletion works

An IAM User cannot be deleted while any of the following are still attached
to it. The script removes each of these, in order, before calling
`DeleteUser`:

 1. **Access Key** — deactivated, then deleted
 2. **Login Profile** — deleted (the password used for AWS Console login)
 3. **MFA Device** — deactivated; if it's a virtual MFA device, the device
    itself is also deleted
 4. **Signing Certificate** — deleted
 5. **SSH Public Key** — deleted
 6. **Service Specific Credential** — deleted
 7. **Inline Policy** — deleted
 8. **Managed Policy** — detached
 9. **Group** — removed from any groups
10. **Permissions Boundary** — deleted
11. **IAM User** — deleted

Each user is processed independently: if a step fails for one user, the
script moves on to the next user rather than aborting the whole run, and
reports a summary of deleted / skipped / failed users at the end.

## Requirements

- [AWS CLI](https://aws.amazon.com/cli/) installed and available on `PATH`
- Valid AWS credentials (e.g. via `aws configure` or an environment/profile
  setup) with the following IAM permissions:

  ```
  iam:ListAccessKeys, iam:UpdateAccessKey, iam:DeleteAccessKey,
  iam:GetLoginProfile, iam:DeleteLoginProfile,
  iam:ListMFADevices, iam:DeactivateMFADevice, iam:DeleteVirtualMFADevice,
  iam:ListSigningCertificates, iam:DeleteSigningCertificate,
  iam:ListSSHPublicKeys, iam:DeleteSSHPublicKey,
  iam:ListServiceSpecificCredentials, iam:DeleteServiceSpecificCredential,
  iam:ListUserPolicies, iam:DeleteUserPolicy,
  iam:ListAttachedUserPolicies, iam:DetachUserPolicy,
  iam:ListGroupsForUser, iam:RemoveUserFromGroup,
  iam:GetUser, iam:DeleteUserPermissionsBoundary, iam:DeleteUser
  ```

## Usage

```
delete-iam-users.sh [options] <user_name> [user_name ...]
delete-iam-users.sh [options] -f users.txt
```

### Options

| Option      | Description                                                                 |
|-------------|-------------------------------------------------------------------------------|
| `-f FILE`   | File listing IAM User names to delete, one per line (blank lines and lines starting with `#` are ignored) |
| `-p PROFILE`| AWS CLI profile to use                                                      |
| `-r REGION` | Region to use (IAM is global, but useful for unconfigured environments)     |
| `-n`        | Dry-run. Shows the commands that would run without making any changes       |
| `-y`        | Skip the confirmation prompt                                                |
| `-h`        | Show help                                                                    |

### Examples

Preview what would happen (dry-run) for three users using the `prod` profile:

```sh
./delete-iam-users.sh -p prod -n alice bob carol
```

Delete the users listed in `users.txt` using the `prod` profile:

```sh
./delete-iam-users.sh -p prod -f ./users.txt
```

`users.txt` format:

```
# one IAM user name per line
alice
bob
carol
```

Skip the confirmation prompt (useful for non-interactive/automated runs):

```sh
./delete-iam-users.sh -y -p prod -f ./users.txt
```

## Notes

- Without `-n` and `-y`, the script prints the target users and asks for
  confirmation before making any changes.
- A user that doesn't exist is reported as skipped, not as a failure.
- Exit code is `0` if there are no failures, `1` if at least one user failed
  to be processed.
