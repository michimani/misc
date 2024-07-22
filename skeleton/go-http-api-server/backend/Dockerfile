# Build stage
FROM golang:1.22.4-bullseye AS builder

WORKDIR /app

COPY go.* ./

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -installsuffix cgo -o /app/backend ./cmd/backend/...

# Runtime stage
FROM alpine:3.20.1

WORKDIR /app

COPY --from=builder /app/backend .
RUN chmod +x /app/backend

EXPOSE 8080

CMD [ "/app/backend" ]