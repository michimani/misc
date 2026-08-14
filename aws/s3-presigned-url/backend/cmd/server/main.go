package main

import (
	"context"
	"log"
	"net/http"

	"github.com/michimani/misc/aws/s3-presigned-url/backend/internal/config"
	"github.com/michimani/misc/aws/s3-presigned-url/backend/internal/handler"
	"github.com/michimani/misc/aws/s3-presigned-url/backend/internal/s3client"
)

func main() {
	ctx := context.Background()

	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	clients, err := s3client.New(ctx, cfg)
	if err != nil {
		log.Fatalf("failed to create s3 clients: %v", err)
	}

	h := handler.New(clients, cfg)

	mux := http.NewServeMux()
	mux.HandleFunc("POST /api/prepare", h.Prepare)
	mux.HandleFunc("POST /api/commit", h.Commit)
	mux.HandleFunc("GET /api/file-list", h.FileList)

	addr := ":" + cfg.Port
	log.Printf("listening on %s (tmp bucket=%s, store bucket=%s)", addr, cfg.TmpBucket, cfg.StoreBucket)
	log.Fatal(http.ListenAndServe(addr, withCORS(cfg.AllowedOrigin, mux)))
}

func withCORS(allowedOrigin string, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", allowedOrigin)
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}

		next.ServeHTTP(w, r)
	})
}
