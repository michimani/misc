#!/usr/bin/env bash
set -euo pipefail

#==============================================================================
# delete-iam-users.sh
#
# Script to bulk-delete specified IAM Users.
# DeleteUser fails if any dependent resources remain attached to the user,
# so this script cleans them up in the following order before deleting.
#
#   1. Access Key                   : Deactivate -> delete
#   2. Login Profile                : Delete (console login password)
#   3. MFA Device                   : Deactivate -> delete the device itself if virtual MFA
#   4. Signing Certificate          : Delete
#   5. SSH Public Key               : Delete
#   6. Service Specific Credential  : Delete
#   7. Inline Policy                : Delete
#   8. Managed Policy               : Detach
#   9. Group                        : Remove from group
#  10. Permissions Boundary         : Delete
#  11. IAM User                     : Delete
#
# Required permissions:
#   iam:ListAccessKeys, iam:UpdateAccessKey, iam:DeleteAccessKey,
#   iam:GetLoginProfile, iam:DeleteLoginProfile,
#   iam:ListMFADevices, iam:DeactivateMFADevice, iam:DeleteVirtualMFADevice,
#   iam:ListSigningCertificates, iam:DeleteSigningCertificate,
#   iam:ListSSHPublicKeys, iam:DeleteSSHPublicKey,
#   iam:ListServiceSpecificCredentials, iam:DeleteServiceSpecificCredential,
#   iam:ListUserPolicies, iam:DeleteUserPolicy,
#   iam:ListAttachedUserPolicies, iam:DetachUserPolicy,
#   iam:ListGroupsForUser, iam:RemoveUserFromGroup,
#   iam:GetUser, iam:DeleteUserPermissionsBoundary, iam:DeleteUser
#==============================================================================

PROGRAM="$(basename "$0")"

DRY_RUN=false
ASSUME_YES=false
USER_FILE=""
AWS_PROFILE_NAME=""
AWS_REGION_NAME=""
declare -a TARGET_USERS=()

#------------------------------------------------------------------------------
# Output
#------------------------------------------------------------------------------
if [[ -t 1 ]]; then
  C_RESET=$'\033[0m'; C_INFO=$'\033[36m'; C_OK=$'\033[32m'
  C_WARN=$'\033[33m'; C_ERR=$'\033[31m'; C_DRY=$'\033[35m'
else
  C_RESET=""; C_INFO=""; C_OK=""; C_WARN=""; C_ERR=""; C_DRY=""
fi

log()      { printf '%s\n' "$*"; }
log_info() { printf '%s[INFO]%s %s\n' "$C_INFO" "$C_RESET" "$*"; }
log_ok()   { printf '%s[ OK ]%s %s\n' "$C_OK" "$C_RESET" "$*"; }
log_warn() { printf '%s[WARN]%s %s\n' "$C_WARN" "$C_RESET" "$*" >&2; }
log_err()  { printf '%s[FAIL]%s %s\n' "$C_ERR" "$C_RESET" "$*" >&2; }
log_dry()  { printf '%s[DRY ]%s %s\n' "$C_DRY" "$C_RESET" "$*"; }

usage() {
  cat <<EOS
Usage:
  ${PROGRAM} [options] <user_name> [user_name ...]
  ${PROGRAM} [options] -f users.txt

Options:
  -f FILE      File listing IAM User names to delete, one per line
               (blank lines and lines starting with # are ignored)
  -p PROFILE   AWS CLI profile to use
  -r REGION    Region to use (IAM is global, but useful for unconfigured environments)
  -n           Dry-run. Shows the commands that would run without making any changes
  -y           Skip the confirmation prompt
  -h           Show this help

Examples:
  ${PROGRAM} -p prod -n alice bob carol
  ${PROGRAM} -p prod -f ./users.txt
EOS
}

#------------------------------------------------------------------------------
# Argument parsing
#------------------------------------------------------------------------------
while getopts ':f:p:r:nyh' opt; do
  case "$opt" in
    f) USER_FILE="$OPTARG" ;;
    p) AWS_PROFILE_NAME="$OPTARG" ;;
    r) AWS_REGION_NAME="$OPTARG" ;;
    n) DRY_RUN=true ;;
    y) ASSUME_YES=true ;;
    h) usage; exit 0 ;;
    :) log_err "Option -$OPTARG requires an argument"; usage; exit 1 ;;
    \?) log_err "Unknown option: -$OPTARG"; usage; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

declare -a AWS_OPTS=(--no-cli-pager --output json)
[[ -n "$AWS_PROFILE_NAME" ]] && AWS_OPTS+=(--profile "$AWS_PROFILE_NAME")
[[ -n "$AWS_REGION_NAME" ]] && AWS_OPTS+=(--region "$AWS_REGION_NAME")

# Load the file if one was specified
if [[ -n "$USER_FILE" ]]; then
  if [[ ! -r "$USER_FILE" ]]; then
    log_err "Cannot read file: ${USER_FILE}"
    exit 1
  fi
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%%#*}"
    line="$(printf '%s' "$line" | tr -d '[:space:]')"
    [[ -n "$line" ]] && TARGET_USERS+=("$line")
  done <"$USER_FILE"
fi

# Add positional arguments
for arg in "$@"; do
  TARGET_USERS+=("$arg")
done

if [[ ${#TARGET_USERS[@]} -eq 0 ]]; then
  log_err "No IAM User specified for deletion"
  usage
  exit 1
fi

command -v aws >/dev/null 2>&1 || { log_err "aws CLI not found"; exit 1; }

#------------------------------------------------------------------------------
# AWS CLI wrappers
#   aws_read : Read-only calls. Runs even in dry-run mode
#   aws_run  : Mutating calls. In dry-run mode, only prints the command
#------------------------------------------------------------------------------
aws_read() {
  aws "${AWS_OPTS[@]}" "$@"
}

aws_run() {
  if [[ "$DRY_RUN" == true ]]; then
    log_dry "aws $*"
    return 0
  fi
  aws "${AWS_OPTS[@]}" "$@" >/dev/null
}

#------------------------------------------------------------------------------
# 1. Access Key : deactivate -> delete
#------------------------------------------------------------------------------
cleanup_access_keys() {
  local user="$1"
  local key_id key_status row
  local -a rows=()

  while IFS=$'\t' read -r key_id key_status; do
    [[ -n "$key_id" ]] && rows+=("${key_id}"$'\t'"${key_status}")
  done < <(aws_read iam list-access-keys --user-name "$user" \
            --query 'AccessKeyMetadata[].[AccessKeyId,Status]' --output text)

  if [[ ${#rows[@]} -eq 0 ]]; then
    log "    Access Key            : none"
    return 0
  fi

  log "    Access Key            : ${#rows[@]} found"
  for row in "${rows[@]}"; do
    IFS=$'\t' read -r key_id key_status <<<"$row"
    log "      - ${key_id} (status: ${key_status})"
    if [[ "$key_status" == "Active" ]]; then
      aws_run iam update-access-key --user-name "$user" \
        --access-key-id "$key_id" --status Inactive || return 1
      log "        deactivated"
    else
      log "        already Inactive, skipping deactivation"
    fi
    aws_run iam delete-access-key --user-name "$user" \
      --access-key-id "$key_id" || return 1
    log "        deleted"
  done
}

#------------------------------------------------------------------------------
# 2. Login Profile
#------------------------------------------------------------------------------
cleanup_login_profile() {
  local user="$1"
  if aws_read iam get-login-profile --user-name "$user" >/dev/null 2>&1; then
    log "    Login Profile         : found -> deleting"
    aws_run iam delete-login-profile --user-name "$user" || return 1
  else
    log "    Login Profile         : none"
  fi
}

#------------------------------------------------------------------------------
# 3. MFA Device
#------------------------------------------------------------------------------
cleanup_mfa_devices() {
  local user="$1" serial count=0
  while IFS= read -r serial; do
    [[ -z "$serial" ]] && continue
    count=$((count + 1))
    log "      - ${serial}"
    aws_run iam deactivate-mfa-device --user-name "$user" \
      --serial-number "$serial" || return 1
    # Virtual MFA serials are ARNs; delete the device itself after deactivating
    if [[ "$serial" == arn:*:mfa/* ]]; then
      aws_run iam delete-virtual-mfa-device --serial-number "$serial" || return 1
    fi
  done < <(aws_read iam list-mfa-devices --user-name "$user" \
            --query 'MFADevices[].SerialNumber' --output text | tr '\t' '\n')
  log "    MFA Device            : ${count} processed"
}

#------------------------------------------------------------------------------
# 4-6. Certificate / SSH Key / Service Specific Credential
#------------------------------------------------------------------------------
cleanup_signing_certificates() {
  local user="$1" cert_id count=0
  while IFS= read -r cert_id; do
    [[ -z "$cert_id" ]] && continue
    count=$((count + 1))
    aws_run iam delete-signing-certificate --user-name "$user" \
      --certificate-id "$cert_id" || return 1
  done < <(aws_read iam list-signing-certificates --user-name "$user" \
            --query 'Certificates[].CertificateId' --output text | tr '\t' '\n')
  log "    Signing Certificate   : ${count} processed"
}

cleanup_ssh_public_keys() {
  local user="$1" ssh_key_id count=0
  while IFS= read -r ssh_key_id; do
    [[ -z "$ssh_key_id" ]] && continue
    count=$((count + 1))
    aws_run iam delete-ssh-public-key --user-name "$user" \
      --ssh-public-key-id "$ssh_key_id" || return 1
  done < <(aws_read iam list-ssh-public-keys --user-name "$user" \
            --query 'SSHPublicKeys[].SSHPublicKeyId' --output text | tr '\t' '\n')
  log "    SSH Public Key        : ${count} processed"
}

cleanup_service_specific_credentials() {
  local user="$1" cred_id count=0
  while IFS= read -r cred_id; do
    [[ -z "$cred_id" ]] && continue
    count=$((count + 1))
    aws_run iam delete-service-specific-credential --user-name "$user" \
      --service-specific-credential-id "$cred_id" || return 1
  done < <(aws_read iam list-service-specific-credentials --user-name "$user" \
            --query 'ServiceSpecificCredentials[].ServiceSpecificCredentialId' \
            --output text | tr '\t' '\n')
  log "    Service Credential    : ${count} processed"
}

#------------------------------------------------------------------------------
# 7-9. Policy / Group
#------------------------------------------------------------------------------
cleanup_inline_policies() {
  local user="$1" policy_name count=0
  while IFS= read -r policy_name; do
    [[ -z "$policy_name" ]] && continue
    count=$((count + 1))
    aws_run iam delete-user-policy --user-name "$user" \
      --policy-name "$policy_name" || return 1
  done < <(aws_read iam list-user-policies --user-name "$user" \
            --query 'PolicyNames[]' --output text | tr '\t' '\n')
  log "    Inline Policy         : ${count} processed"
}

cleanup_attached_policies() {
  local user="$1" policy_arn count=0
  while IFS= read -r policy_arn; do
    [[ -z "$policy_arn" ]] && continue
    count=$((count + 1))
    aws_run iam detach-user-policy --user-name "$user" \
      --policy-arn "$policy_arn" || return 1
  done < <(aws_read iam list-attached-user-policies --user-name "$user" \
            --query 'AttachedPolicies[].PolicyArn' --output text | tr '\t' '\n')
  log "    Managed Policy        : ${count} detached"
}

cleanup_groups() {
  local user="$1" group_name count=0
  while IFS= read -r group_name; do
    [[ -z "$group_name" ]] && continue
    count=$((count + 1))
    aws_run iam remove-user-from-group --user-name "$user" \
      --group-name "$group_name" || return 1
  done < <(aws_read iam list-groups-for-user --user-name "$user" \
            --query 'Groups[].GroupName' --output text | tr '\t' '\n')
  log "    Group                 : removed from ${count}"
}

#------------------------------------------------------------------------------
# 10. Permissions Boundary
#------------------------------------------------------------------------------
cleanup_permissions_boundary() {
  local user="$1" boundary
  boundary="$(aws_read iam get-user --user-name "$user" \
    --query 'User.PermissionsBoundary.PermissionsBoundaryArn' --output text 2>/dev/null || echo 'None')"
  if [[ -n "$boundary" && "$boundary" != "None" ]]; then
    log "    Permissions Boundary  : ${boundary} -> deleting"
    aws_run iam delete-user-permissions-boundary --user-name "$user" || return 1
  else
    log "    Permissions Boundary  : none"
  fi
}

#------------------------------------------------------------------------------
# Process a single user
#------------------------------------------------------------------------------
process_user() {
  local user="$1"

  log ""
  log_info "===== ${user} ====="

  if ! aws_read iam get-user --user-name "$user" >/dev/null 2>&1; then
    log_warn "${user} does not exist. Skipping"
    return 2
  fi

  cleanup_access_keys "$user"                  || return 1
  cleanup_login_profile "$user"                || return 1
  cleanup_mfa_devices "$user"                  || return 1
  cleanup_signing_certificates "$user"         || return 1
  cleanup_ssh_public_keys "$user"              || return 1
  cleanup_service_specific_credentials "$user" || return 1
  cleanup_inline_policies "$user"              || return 1
  cleanup_attached_policies "$user"            || return 1
  cleanup_groups "$user"                       || return 1
  cleanup_permissions_boundary "$user"         || return 1

  aws_run iam delete-user --user-name "$user" || return 1
  log_ok "${user} deleted"
  return 0
}

#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
CALLER="$(aws_read sts get-caller-identity --query 'Arn' --output text 2>/dev/null || true)"
if [[ -z "$CALLER" ]]; then
  log_err "Could not verify AWS credentials. Please check your profile configuration"
  exit 1
fi

log_info "Caller     : ${CALLER}"
log_info "Profile    : ${AWS_PROFILE_NAME:-(default)}"
log_info "Target users: ${#TARGET_USERS[@]}"
for u in "${TARGET_USERS[@]}"; do
  log "  - ${u}"
done
[[ "$DRY_RUN" == true ]] && log_dry "Running in dry-run mode. No changes will be made"

if [[ "$DRY_RUN" == false && "$ASSUME_YES" == false ]]; then
  log ""
  read -r -p "This will delete the IAM Users listed above. Continue? [y/N]: " answer
  if [[ ! "$answer" =~ ^[Yy]$ ]]; then
    log_info "Aborted"
    exit 0
  fi
fi

declare -a DELETED=() SKIPPED=() FAILED=()

for u in "${TARGET_USERS[@]}"; do
  rc=0
  process_user "$u" || rc=$?
  case "$rc" in
    0) DELETED+=("$u") ;;
    2) SKIPPED+=("$u") ;;
    *) FAILED+=("$u"); log_err "Failed to process ${u}" ;;
  esac
done

log ""
log_info "===== Results ====="
log_info "Deleted: ${#DELETED[@]}  Skipped (not found): ${#SKIPPED[@]}  Failed: ${#FAILED[@]}"
if [[ ${#FAILED[@]} -gt 0 ]]; then
  for u in "${FAILED[@]}"; do
    log_err "  - ${u}"
  done
  exit 1
fi
exit 0