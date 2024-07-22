package handlers

import "net/http"

func (s *httpServer) health(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	if _, err := w.Write([]byte("healthy")); err != nil {
		w.WriteHeader(http.StatusInternalServerError)
	}
}
