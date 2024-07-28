ARG GO_VERSION=1.22.5

# Build stage
FROM golang:${GO_VERSION}-bookworm AS builder

WORKDIR /app

COPY go.* ./

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -installsuffix cgo -o /app/backend ./cmd/backend/...

# Runtime stage
FROM debian:bookworm-slim AS final

WORKDIR /app

COPY --from=builder /app/backend .

EXPOSE 8080

CMD [ "/app/backend" ]