import {
  prepareUpload,
  uploadToPresignedUrl,
  commitFiles,
  fetchFileList,
  type FileListItem,
} from "./api";

type UploadStatus = "uploading" | "done" | "error";

interface UploadItem {
  file: File;
  uuid?: string;
  status: UploadStatus;
  error?: string;
}

type View = "upload" | "list";

let view: View = "upload";
let uploadItems: UploadItem[] = [];
let committing = false;

const app = document.querySelector<HTMLDivElement>("#app")!;

function render(): void {
  if (view === "upload") {
    renderUploadView();
  } else {
    renderListView();
  }
}

function renderUploadView(): void {
  const allDone = uploadItems.length > 0 && uploadItems.every((i) => i.status === "done");

  app.innerHTML = `
    <div class="page">
      <h1>ファイルアップロード</h1>
      <input type="file" id="file-input" multiple />
      <ul class="upload-list">
        ${uploadItems
          .map(
            (item) => `
          <li class="upload-item status-${item.status}">
            <span class="file-name">${escapeHtml(item.file.name)}</span>
            <span class="status">${statusLabel(item)}</span>
          </li>`
          )
          .join("")}
      </ul>
      <button id="register-btn" ${allDone && !committing ? "" : "disabled"}>
        ${committing ? "登録中..." : "登録"}
      </button>
    </div>
  `;

  const fileInput = document.querySelector<HTMLInputElement>("#file-input")!;
  fileInput.addEventListener("change", onFilesSelected);

  const registerBtn = document.querySelector<HTMLButtonElement>("#register-btn")!;
  registerBtn.addEventListener("click", onRegisterClick);
}

function statusLabel(item: UploadItem): string {
  switch (item.status) {
    case "uploading":
      return "アップロード中...";
    case "done":
      return "完了";
    case "error":
      return `失敗: ${item.error ?? ""}`;
  }
}

let uploadGeneration = 0;

async function onFilesSelected(e: Event): Promise<void> {
  const input = e.target as HTMLInputElement;
  const files = Array.from(input.files ?? []);
  if (files.length === 0) return;

  const generation = ++uploadGeneration;
  uploadItems = files.map((file) => ({ file, status: "uploading" as UploadStatus }));
  render();

  await Promise.all(uploadItems.map((item, index) => uploadOne(item, index, generation)));
  render();
}

async function uploadOne(item: UploadItem, index: number, generation: number): Promise<void> {
  let updated: UploadItem;
  try {
    const { uuid, uploadUrl } = await prepareUpload(item.file.name);
    await uploadToPresignedUrl(uploadUrl, item.file);
    updated = { ...item, uuid, status: "done" };
  } catch (err) {
    updated = {
      ...item,
      status: "error",
      error: err instanceof Error ? err.message : String(err),
    };
  }
  if (generation !== uploadGeneration) return;
  uploadItems[index] = updated;
  render();
}

async function onRegisterClick(): Promise<void> {
  committing = true;
  render();

  try {
    const { results } = await commitFiles(
      uploadItems
        .filter((i): i is UploadItem & { uuid: string } => i.status === "done" && !!i.uuid)
        .map((i) => ({ uuid: i.uuid, fileName: i.file.name }))
    );
    committing = false;

    const failed = results.filter((r) => r.status !== "committed");
    if (failed.length > 0) {
      alert(
        `登録に失敗したファイルがあります:\n${failed
          .map((f) => `${f.fileName}: ${f.status}`)
          .join("\n")}`
      );
      render();
      return;
    }

    uploadItems = [];
    view = "list";
    render();
    await loadFileList();
  } catch (err) {
    committing = false;
    alert(`登録に失敗しました: ${err instanceof Error ? err.message : String(err)}`);
    render();
  }
}

let fileListItems: FileListItem[] = [];
let fileListLoading = false;

async function loadFileList(): Promise<void> {
  fileListLoading = true;
  render();
  try {
    const res = await fetchFileList();
    fileListItems = res.files;
  } finally {
    fileListLoading = false;
    render();
  }
}

function renderListView(): void {
  app.innerHTML = `
    <div class="page">
      <h1>登録済みファイル一覧</h1>
      <button id="back-btn">アップロードに戻る</button>
      ${fileListLoading ? "<p>読み込み中...</p>" : renderFileTable()}
    </div>
  `;

  document.querySelector<HTMLButtonElement>("#back-btn")!.addEventListener("click", () => {
    view = "upload";
    render();
  });
}

function renderFileTable(): string {
  if (fileListItems.length === 0) {
    return "<p>ファイルがありません。</p>";
  }
  return `
    <table>
      <thead>
        <tr><th>ファイル名</th><th>サイズ</th><th>更新日時</th><th></th></tr>
      </thead>
      <tbody>
        ${fileListItems
          .map(
            (f) => `
          <tr>
            <td>${escapeHtml(f.fileName)}</td>
            <td>${formatSize(f.size)}</td>
            <td>${escapeHtml(f.lastModified)}</td>
            <td><a href="${f.downloadUrl}" target="_blank" rel="noopener noreferrer">ダウンロード</a></td>
          </tr>`
          )
          .join("")}
      </tbody>
    </table>
  `;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB"];
  let value = bytes / 1024;
  let unitIndex = 0;
  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024;
    unitIndex++;
  }
  return `${value.toFixed(1)} ${units[unitIndex]}`;
}

function escapeHtml(value: string): string {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

render();
