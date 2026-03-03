package handlers

import (
	"log/slog"
	"net/http"
	"os"
)

func NewHTTPServer(addr string) *http.Server {
	httpsrv := newHTTPServer()

	mux := http.NewServeMux()
	mux.HandleFunc("GET /api/health", httpsrv.health)

	return &http.Server{
		Addr:    addr,
		Handler: mux,
	}
}

type httpServer struct {
	logger *slog.Logger
}

func newHTTPServer() *httpServer {
	return &httpServer{
		logger: slog.New(slog.NewJSONHandler(os.Stdout, nil).WithGroup("http")),
	}
}
