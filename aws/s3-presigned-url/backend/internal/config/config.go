package config

import (
	"fmt"
	"os"
)

// Config holds all runtime configuration for the server, loaded from
// environment variables. There are two distinct S3 endpoints because
// presigned URLs are handed to the browser, which cannot resolve the
// docker-compose internal service name: PublicS3Endpoint must be an
// address the browser can reach, while InternalS3Endpoint is used for
// every other S3 call made from inside the backend container.
type Config struct {
	Port               string
	InternalS3Endpoint string
	PublicS3Endpoint   string
	AWSRegion          string
	TmpBucket          string
	StoreBucket        string
	AllowedOrigin      string
}

func Load() (Config, error) {
	cfg := Config{
		Port:               getEnv("PORT", "8080"),
		InternalS3Endpoint: os.Getenv("S3_INTERNAL_ENDPOINT"),
		PublicS3Endpoint:   os.Getenv("S3_PUBLIC_ENDPOINT"),
		AWSRegion:          getEnv("AWS_REGION", "us-east-1"),
		TmpBucket:          os.Getenv("S3_TMP_BUCKET"),
		StoreBucket:        os.Getenv("S3_STORE_BUCKET"),
		AllowedOrigin:      getEnv("ALLOWED_ORIGIN", "http://localhost:5173"),
	}

	var missing []string
	if cfg.InternalS3Endpoint == "" {
		missing = append(missing, "S3_INTERNAL_ENDPOINT")
	}
	if cfg.PublicS3Endpoint == "" {
		missing = append(missing, "S3_PUBLIC_ENDPOINT")
	}
	if cfg.TmpBucket == "" {
		missing = append(missing, "S3_TMP_BUCKET")
	}
	if cfg.StoreBucket == "" {
		missing = append(missing, "S3_STORE_BUCKET")
	}
	if len(missing) > 0 {
		return Config{}, fmt.Errorf("missing required environment variables: %v", missing)
	}

	return cfg, nil
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
