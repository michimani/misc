#!/bin/sh
set -eu

ENDPOINT="${S3_ENDPOINT:?S3_ENDPOINT is required}"
TMP_BUCKET="${S3_TMP_BUCKET:?S3_TMP_BUCKET is required}"
STORE_BUCKET="${S3_STORE_BUCKET:?S3_STORE_BUCKET is required}"
ALLOWED_ORIGIN="${ALLOWED_ORIGIN:?ALLOWED_ORIGIN is required}"

echo "waiting for floci at ${ENDPOINT}..."
until aws s3 ls --endpoint-url "${ENDPOINT}" >/dev/null 2>&1; do
  sleep 1
done
echo "floci is ready"

for bucket in "${TMP_BUCKET}" "${STORE_BUCKET}"; do
  if aws s3api head-bucket --bucket "${bucket}" --endpoint-url "${ENDPOINT}" >/dev/null 2>&1; then
    echo "bucket ${bucket} already exists"
  else
    aws s3 mb "s3://${bucket}" --endpoint-url "${ENDPOINT}"
    echo "created bucket ${bucket}"
  fi
done

cat <<EOF >/tmp/cors.json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["${ALLOWED_ORIGIN}"],
      "AllowedMethods": ["PUT", "POST", "GET"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag"]
    }
  ]
}
EOF

# The tmp bucket needs CORS so the browser can POST directly to a presigned
# POST URL from the frontend's origin. The store bucket gets the same rule so
# fetch-based downloads of presigned GET URLs would also work, even though
# the file-list page currently only uses plain <a> navigation.
aws s3api put-bucket-cors --bucket "${TMP_BUCKET}" --cors-configuration file:///tmp/cors.json --endpoint-url "${ENDPOINT}"
aws s3api put-bucket-cors --bucket "${STORE_BUCKET}" --cors-configuration file:///tmp/cors.json --endpoint-url "${ENDPOINT}"

echo "bucket setup complete"
