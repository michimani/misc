package handlers

import "net/http"

func NewHTTPServer(addr string) *http.Server {
	httpsrv := newHTTPServer()

	mux := http.NewServeMux()
	mux.HandleFunc("/health", httpsrv.health)

	return &http.Server{
		Addr:    addr,
		Handler: mux,
	}
}

type httpServer struct{}

func newHTTPServer() *httpServer {
	return &httpServer{}
}
