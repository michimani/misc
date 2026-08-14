package s3client

import (
	"context"

	"github.com/aws/aws-sdk-go-v2/aws"
	awsconfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/credentials"
	"github.com/aws/aws-sdk-go-v2/service/s3"

	"github.com/michimani/misc/aws/s3-presigned-url/backend/internal/config"
)

// Clients bundles the two S3 clients the backend needs: Internal talks to
// floci over the docker-compose network and is used for every server-side
// operation (copy, delete, list); Presign talks to floci's browser-facing
// address and is used only to mint presigned URLs, since the signed host
// must be one the browser can actually resolve.
type Clients struct {
	Internal *s3.Client
	Presign  *s3.PresignClient
}

func New(ctx context.Context, cfg config.Config) (*Clients, error) {
	awsCfg, err := awsconfig.LoadDefaultConfig(ctx,
		awsconfig.WithRegion(cfg.AWSRegion),
		awsconfig.WithCredentialsProvider(
			credentials.NewStaticCredentialsProvider("test", "test", ""),
		),
	)
	if err != nil {
		return nil, err
	}

	internal := s3.NewFromConfig(awsCfg, func(o *s3.Options) {
		o.BaseEndpoint = aws.String(cfg.InternalS3Endpoint)
		o.UsePathStyle = true
	})

	forPresign := s3.NewFromConfig(awsCfg, func(o *s3.Options) {
		o.BaseEndpoint = aws.String(cfg.PublicS3Endpoint)
		o.UsePathStyle = true
	})

	return &Clients{
		Internal: internal,
		Presign:  s3.NewPresignClient(forPresign),
	}, nil
}
