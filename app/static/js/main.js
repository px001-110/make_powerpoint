let selectedFiles = []

const form = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const fileList = document.getElementById("file-list");
const dropZone = document.getElementById("drop-zone");
const loading = document.getElementById("loading")

// ==============================
// fileInput同期
// ==============================
function syncFileInput() {
    const dt = new DataTransfer();
    selectedFiles.forEach(file => {
        dt.items.add(file)
    });
    fileInput.files = dt.files;
}

// ==============================
// ファイル一覧
// ==============================

function renderFileList() {
    fileList.innerHTML = "";

    selectedFiles.forEach((file, index) => {
        const li = document.createElement("li");
        li.className = "file-item";
        li.dataset.index = index;

        const span = document.createElement("span");
        span.textContent = "≡ " + file.name;

        // 削除ボタン
        const deleteBtn = document.createElement("button");

        deleteBtn.type = "button";
        deleteBtn.textContent = "x";
        deleteBtn.className = "delete-btn";

        deleteBtn.onclick = () => {
            selectedFiles.splice(index, 1);
            syncFileInput();
            renderFileList();
        };

        li.appendChild(span);
        li.appendChild(deleteBtn);

        fileList.appendChild(li);
    });
}

// ==============================
// ファイル選択
// ==============================
fileInput.addEventListener("change", (e) => {

    selectedFiles = [...e.target.files];
    syncFileInput();
    renderFileList();
})

// ==============================
// drag & drop
// ==============================
dropZone.addEventListener("dragenter", e => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragover", e => {
    e.preventDefault();
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
})

dropZone.addEventListener("drop", e => {
    e.preventDefault();
    dropZone.classList.remove("dragover");

    const files = Array.from(e.dataTransfer.files);

    // 新しい配列を作る
    selectedFiles.push(...files);
    syncFileInput();
    renderFileList();
});
// ==============================
// sortable
// ==============================
new Sortable(fileList, {
    animation: 150,
    onEnd: function () {
        const reordered = [];
        fileList.querySelectorAll(".file-item").forEach(item => {
            reordered.push(
                selectedFiles[item.dataset.index]
            );
        });

        selectedFiles = reordered;
        syncFileInput();
        renderFileList();
    }
});

// ==============================
// submit
// ==============================
form.addEventListener("submit", function (e) {
    if (selectedFiles.length === 0) {
        e.preventDefault();
        alert("ファイルを選択してください");
        return;
    }

    loading.style.display = "block";
});
