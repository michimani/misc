package handler

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"sort"
	"strings"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/smithy-go"
	"github.com/google/uuid"

	"github.com/michimani/misc/aws/s3-presigned-url/backend/internal/config"
	"github.com/michimani/misc/aws/s3-presigned-url/backend/internal/s3client"
)

const presignExpiry = 15 * time.Minute

// maxUploadBytes and allowedContentType are enforced up front via the
// pre-signed POST policy conditions (content-length-range / Content-Type),
// so S3 itself rejects an oversized or wrong-type upload before the object
// is even written to the tmp bucket.
const maxUploadBytes = 500 * 1024 * 1024 // 500MB
const allowedContentType = "application/pdf"

// pdfMagicNumber is the byte sequence every PDF file starts with. Commit
// still checks this because the POST policy's Content-Type condition only
// constrains the *declared* form field, which the client controls and can
// lie about; this is the check against the actual file bytes.
var pdfMagicNumber = []byte("%PDF-")

type Handler struct {
	s3  *s3client.Clients
	cfg config.Config
}

func New(clients *s3client.Clients, cfg config.Config) *Handler {
	return &Handler{s3: clients, cfg: cfg}
}

// --- POST /api/prepare ---

type prepareRequest struct {
	FileName string `json:"fileName"`
}

type prepareResponse struct {
	UUID      string            `json:"uuid"`
	UploadURL string            `json:"uploadUrl"`
	Fields    map[string]string `json:"fields"`
}

func (h *Handler) Prepare(w http.ResponseWriter, r *http.Request) {
	var req prepareRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	if strings.TrimSpace(req.FileName) == "" {
		writeError(w, http.StatusBadRequest, "fileName is required")
		return
	}

	id := uuid.NewString()

	out, err := h.s3.Presign.PresignPostObject(r.Context(), &s3.PutObjectInput{
		Bucket: aws.String(h.cfg.TmpBucket),
		Key:    aws.String(id),
	}, func(o *s3.PresignPostOptions) {
		o.Expires = presignExpiry
		o.Conditions = []any{
			[]any{"content-length-range", 0, maxUploadBytes},
			map[string]string{"Content-Type": allowedContentType},
		}
	})
	if err != nil {
		log.Printf("presign post object failed: %v", err)
		writeError(w, http.StatusInternalServerError, "failed to create upload URL")
		return
	}

	writeJSON(w, http.StatusOK, prepareResponse{
		UUID:      id,
		UploadURL: out.URL,
		Fields:    out.Values,
	})
}

// --- POST /api/commit ---

type commitItem struct {
	UUID     string `json:"uuid"`
	FileName string `json:"fileName"`
}

type commitRequest struct {
	Files []commitItem `json:"files"`
}

type commitResult struct {
	UUID     string `json:"uuid"`
	FileName string `json:"fileName"`
	Status   string `json:"status"`
}

type commitResponse struct {
	Results []commitResult `json:"results"`
}

func (h *Handler) Commit(w http.ResponseWriter, r *http.Request) {
	var req commitRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	if len(req.Files) == 0 {
		writeError(w, http.StatusBadRequest, "files must not be empty")
		return
	}

	results := make([]commitResult, 0, len(req.Files))
	for _, f := range req.Files {
		result := commitResult{UUID: f.UUID, FileName: f.FileName}

		if strings.TrimSpace(f.UUID) == "" || strings.TrimSpace(f.FileName) == "" {
			result.Status = "error"
			results = append(results, result)
			continue
		}

		isPDF, err := h.isTmpObjectPDF(r.Context(), f.UUID)
		if err != nil {
			if isNotFound(err) {
				result.Status = "not_found"
			} else {
				log.Printf("magic number check failed for uuid %s: %v", f.UUID, err)
				result.Status = "error"
			}
			results = append(results, result)
			continue
		}
		if !isPDF {
			result.Status = "invalid_file_type"
			results = append(results, result)
			continue
		}

		destKey := f.UUID + "/" + f.FileName
		copySource := h.cfg.TmpBucket + "/" + url.PathEscape(f.UUID)

		_, err = h.s3.Internal.CopyObject(r.Context(), &s3.CopyObjectInput{
			Bucket:     aws.String(h.cfg.StoreBucket),
			Key:        aws.String(destKey),
			CopySource: aws.String(copySource),
		})
		if err != nil {
			if isNotFound(err) {
				result.Status = "not_found"
			} else {
				log.Printf("copy object failed for uuid %s: %v", f.UUID, err)
				result.Status = "error"
			}
			results = append(results, result)
			continue
		}

		if _, err := h.s3.Internal.DeleteObject(r.Context(), &s3.DeleteObjectInput{
			Bucket: aws.String(h.cfg.TmpBucket),
			Key:    aws.String(f.UUID),
		}); err != nil {
			log.Printf("delete tmp object failed for uuid %s (already copied to store bucket): %v", f.UUID, err)
		}

		result.Status = "committed"
		results = append(results, result)
	}

	writeJSON(w, http.StatusOK, commitResponse{Results: results})
}

// isTmpObjectPDF checks the file type by reading only the leading bytes of
// the tmp object via a ranged GetObject, instead of buffering the whole
// (potentially large) file into memory just to inspect its magic number.
func (h *Handler) isTmpObjectPDF(ctx context.Context, objectUUID string) (bool, error) {
	out, err := h.s3.Internal.GetObject(ctx, &s3.GetObjectInput{
		Bucket: aws.String(h.cfg.TmpBucket),
		Key:    aws.String(objectUUID),
		Range:  aws.String(fmt.Sprintf("bytes=0-%d", len(pdfMagicNumber)-1)),
	})
	if err != nil {
		return false, err
	}
	defer out.Body.Close()

	head := make([]byte, len(pdfMagicNumber))
	n, err := io.ReadFull(out.Body, head)
	if err != nil && !errors.Is(err, io.ErrUnexpectedEOF) && !errors.Is(err, io.EOF) {
		return false, err
	}

	return bytes.Equal(head[:n], pdfMagicNumber), nil
}

func isNotFound(err error) bool {
	var apiErr smithy.APIError
	if errors.As(err, &apiErr) {
		code := apiErr.ErrorCode()
		return code == "NoSuchKey" || code == "NotFound"
	}
	return false
}

// --- GET /api/file-list ---

type fileListItem struct {
	UUID         string `json:"uuid"`
	FileName     string `json:"fileName"`
	Size         int64  `json:"size"`
	LastModified string `json:"lastModified"`
	DownloadURL  string `json:"downloadUrl"`
}

type fileListResponse struct {
	Files []fileListItem `json:"files"`
}

func (h *Handler) FileList(w http.ResponseWriter, r *http.Request) {
	out, err := h.s3.Internal.ListObjectsV2(r.Context(), &s3.ListObjectsV2Input{
		Bucket: aws.String(h.cfg.StoreBucket),
	})
	if err != nil {
		log.Printf("list objects failed: %v", err)
		writeError(w, http.StatusInternalServerError, "failed to list files")
		return
	}

	files := make([]fileListItem, 0, len(out.Contents))
	for _, obj := range out.Contents {
		key := aws.ToString(obj.Key)
		parts := strings.SplitN(key, "/", 2)
		if len(parts) != 2 {
			continue
		}
		id, fileName := parts[0], parts[1]

		downloadURL, err := h.s3.Presign.PresignGetObject(r.Context(), &s3.GetObjectInput{
			Bucket: aws.String(h.cfg.StoreBucket),
			Key:    aws.String(key),
		}, s3.WithPresignExpires(presignExpiry))
		if err != nil {
			log.Printf("presign get object failed for key %s: %v", key, err)
			continue
		}

		var lastModified string
		if obj.LastModified != nil {
			lastModified = obj.LastModified.Format(time.RFC3339)
		}

		files = append(files, fileListItem{
			UUID:         id,
			FileName:     fileName,
			Size:         aws.ToInt64(obj.Size),
			LastModified: lastModified,
			DownloadURL:  downloadURL.URL,
		})
	}

	sort.Slice(files, func(i, j int) bool { return files[i].LastModified > files[j].LastModified })

	writeJSON(w, http.StatusOK, fileListResponse{Files: files})
}

// --- helpers ---

func writeJSON(w http.ResponseWriter, status int, body any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(body); err != nil {
		log.Printf("failed to write json response: %v", err)
	}
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]string{"error": message})
}
