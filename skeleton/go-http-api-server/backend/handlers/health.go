package handlers

import "net/http"

func (s *httpServer) health(w http.ResponseWriter, r *http.Request) {
	s.logger.Info("health check")
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:5174")

	w.WriteHeader(http.StatusOK)
	if _, err := w.Write([]byte("healthy")); err != nil {
		s.logger.Error("failed to write response", "error", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	s.logger.Info("health check response sent")
}
