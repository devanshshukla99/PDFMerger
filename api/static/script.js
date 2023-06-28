window.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOMContentLoaded")
    uploader_container = document.querySelector("#upload-container")
    if (uploader_container != null) {
        document.getElementById("UploadAddButton").addEventListener("click", function () {
            uploader_container.innerHTML += `<div class="card list-item draggable-card ui-sortable-handle ui-sortable-placeholder">
            <div class="card-body">
                <input type="file" class="form-control" name="files" />
                <input type="text" class="form-control mb-3 w-25" placeholder="range" class="noscroll pages-range"
                    name="pages-range" />
            </div>
        </div>`
        });
    };
    $(".cards-container").sortable();
});
