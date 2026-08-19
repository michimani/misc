const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:58080";

export interface PrepareResponse {
  uuid: string;
  uploadUrl: string;
  fields: Record<string, string>;
}

export interface CommitFileInput {
  uuid: string;
  fileName: string;
}

export interface CommitResult {
  uuid: string;
  fileName: string;
  status: "committed" | "not_found" | "invalid_file_type" | "error";
}

export interface CommitResponse {
  results: CommitResult[];
}

export interface FileListItem {
  uuid: string;
  fileName: string;
  size: number;
  lastModified: string;
  downloadUrl: string;
}

export interface FileListResponse {
  files: FileListItem[];
}

async function requestJSON<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const res = await fetch(input, init);
  if (!res.ok) {
    throw new Error(`request failed: ${res.status} ${res.statusText}`);
  }
  return (await res.json()) as T;
}

export function prepareUpload(fileName: string): Promise<PrepareResponse> {
  return requestJSON<PrepareResponse>(`${API_BASE_URL}/api/prepare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fileName }),
  });
}

export async function uploadToPresignedUrl(
  uploadUrl: string,
  fields: Record<string, string>,
  file: File
): Promise<void> {
  const formData = new FormData();
  for (const [key, value] of Object.entries(fields)) {
    formData.append(key, value);
  }
  // The Content-Type field is matched against the pre-signed POST policy's
  // condition (fixed to application/pdf), so the browser-detected MIME type
  // is sent as-is instead of being overridden — a non-PDF selection should
  // be rejected by S3 itself rather than silently coerced to pass.
  formData.append("Content-Type", file.type);
  // The file field must come last, per the S3 POST policy form requirements.
  formData.append("file", file);

  const res = await fetch(uploadUrl, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`upload failed: ${res.status} ${res.statusText} ${body}`);
  }
}

export function commitFiles(files: CommitFileInput[]): Promise<CommitResponse> {
  return requestJSON<CommitResponse>(`${API_BASE_URL}/api/commit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ files }),
  });
}

export function fetchFileList(): Promise<FileListResponse> {
  return requestJSON<FileListResponse>(`${API_BASE_URL}/api/file-list`);
}
