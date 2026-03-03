package main

import (
	"log"
	"os"

	"github.com/michimani/misc/skeleton/go-http-api-server/backend/handlers"
)

func main() {
	addr, exists := os.LookupEnv("API_SEVER_ADDR")
	if !exists {
		addr = ":8080"
	}

	srv := handlers.NewHTTPServer(addr)
	log.Fatal(srv.ListenAndServe())
}
