let files = [];
let format = "docx";
let api = null;

const $ = (id) => document.getElementById(id);

function apiReady(fn) {
  if (api) return fn(api);
  window.addEventListener("pywebviewready", () => {
    api = window.pywebview.api;
    fn(api);
  });
}

function render() {
  const list = $("file-list");
  list.innerHTML = "";
  files.forEach((path, i) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span class="num">${i + 1}</span>
      <span class="name" title="${escapeAttr(path)}">${escapeHtml(path.split(/[\\/]/).pop())}</span>
      <button data-act="up" title="Yukarı" ${i === 0 ? "disabled" : ""}>↑</button>
      <button data-act="down" title="Aşağı" ${i === files.length - 1 ? "disabled" : ""}>↓</button>
      <button data-act="del" class="del" title="Kaldır">×</button>`;
    li.querySelectorAll("button").forEach((b) => {
      b.addEventListener("click", () => {
        const act = b.dataset.act;
        if (act === "up" && i > 0) [files[i - 1], files[i]] = [files[i], files[i - 1]];
        if (act === "down" && i < files.length - 1) [files[i + 1], files[i]] = [files[i], files[i + 1]];
        if (act === "del") files.splice(i, 1);
        render();
      });
    });
    list.appendChild(li);
  });
  $("file-count").textContent = `${files.length} dosya`;
  $("empty").style.display = files.length ? "none" : "block";
  $("convert-btn").disabled = files.length === 0;
  $("preview-btn").disabled = files.length === 0;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function escapeAttr(s) { return escapeHtml(s); }

function status(msg, kind = "") {
  const el = $("status");
  el.textContent = msg;
  el.className = "status " + kind;
}

function addFiles(newFiles) {
  const clean = (newFiles || []).filter((f) => typeof f === "string" && f);
  if (!clean.length) return;
  files = files.concat(clean);
  render();
  status(`${clean.length} dosya eklendi.`, "ok");
}

$("add-btn").addEventListener("click", () => {
  apiReady((a) => a.pick_files().then(addFiles));
});

const dz = $("dropzone");
["dragenter", "dragover"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.add("dragover"); }));
["dragleave", "drop"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.remove("dragover"); }));
dz.addEventListener("drop", () => {
  // Sürükle-bırak desteklenmeyen platformlarda dosya seçiciyi açar
  apiReady((a) => a.pick_files().then(addFiles));
});

$("formats").addEventListener("click", (e) => {
  const btn = e.target.closest(".format");
  if (!btn) return;
  format = btn.dataset.fmt;
  document.querySelectorAll(".format").forEach((b) => b.classList.toggle("active", b === btn));
});

$("convert-btn").addEventListener("click", () => {
  const title = $("title").value;
  const btn = $("convert-btn");
  btn.disabled = true;
  status("Dönüştürülüyor…");
  apiReady((a) => {
    a.convert(files, format, title).then((r) => {
      btn.disabled = false;
      if (r.ok) status(r.msg, "ok");
      else status(r.msg || "Bir hata oluştu.", "err");
    }).catch((e) => {
      btn.disabled = false;
      status("Hata: " + e, "err");
    });
  });
});

$("preview-btn").addEventListener("click", () => {
  status("Önizleme hazırlanıyor…");
  apiReady((a) => {
    a.preview(files).then((r) => {
      if (!r.ok) return status(r.error, "err");
      $("modal-body").innerHTML = r.html;
      $("modal").hidden = false;
      status("");
    });
  });
});
$("close-modal").addEventListener("click", () => { $("modal").hidden = true; });
$("modal").addEventListener("click", (e) => { if (e.target === $("modal")) $("modal").hidden = true; });

window.addEventListener("pywebviewready", () => {
  api = window.pywebview.api;
  render();
});
render();
