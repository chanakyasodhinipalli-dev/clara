async function postFile(file) {
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch("/api/process", { method: "POST", body: fd });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

function renderJSON(el, obj) {
  el.textContent = JSON.stringify(obj, null, 2);
}

function renderTable(el, result) {
  const rows = [];
  function row(k, v) { rows.push(`<tr><td class="border px-2 py-1 font-semibold">${k}</td><td class="border px-2 py-1"><pre class='whitespace-pre-wrap'>${v}</pre></td></tr>`); }
  row("Preprocessor", JSON.stringify(result.preprocessor.data));
  row("Splitter", JSON.stringify(result.splitter.data));
  row("Context", JSON.stringify(result.context.data));
  row("Grouping", JSON.stringify(result.grouping.data));
  row("Merger", JSON.stringify(result.merger.data));
  row("Metadata", JSON.stringify(result.metadata.data));
  row("Classification", JSON.stringify(result.parallel.classification.data));
  row("Summary", JSON.stringify(result.parallel.summary.data));
  el.innerHTML = `<table class="table-auto w-full text-xs border">${rows.join("")}</table>`;
}

function renderDownloads(el, outputs) {
  const links = [];
  if (outputs && outputs.merged_pdf) {
    const url = `/api/file?path=${encodeURIComponent(outputs.merged_pdf)}`;
    links.push(`<a class="underline text-indigo-700" href="${url}">Download Merged PDF</a>`);
  }
  el.innerHTML = links.join(" · ");
}

function renderPDF(el, path) {
  if (!path) { el.innerHTML = "<em>No merged PDF available.</em>"; return; }
  const url = `/api/file?path=${encodeURIComponent(path)}`;
  el.innerHTML = `<object data="${url}" type="application/pdf" width="100%" height="600px">
      <p>PDF preview not supported in this browser. <a class="underline" href="${url}">Download PDF</a></p>
    </object>`;
}

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = document.getElementById("file").files[0];
  if (!file) return;
  const status = document.getElementById("status");
  status.textContent = "Status: uploading & processing...";
  try {
    const resp = await postFile(file);
    status.textContent = "Status: done";
    renderJSON(document.getElementById("jsonOut"), resp);
    renderTable(document.getElementById("tableOut"), resp.result);
    renderDownloads(document.getElementById("downloads"), resp.result.outputs);
    renderPDF(document.getElementById("pdfViewer"), resp.result.outputs.merged_pdf);
  } catch (err) {
    status.textContent = "Status: error";
    document.getElementById("jsonOut").textContent = String(err);
  }
});
