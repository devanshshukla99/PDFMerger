let filecard = `<div class="card list-item draggable-card ui-sortable-handle ui-sortable-placeholder">
<button type="button" class="btn-close" onclick="removeParent(event)" aria-label="Close"></button>
<div class="card-body">
    <input type="file" class="form-control" id="files" name="files" aria-label="Select file" required />
    <div class="invalid-feedback">Invalid file | the input file must be a valid PDF. </div>
    <input type="text" class="form-control mb-3 w-25" placeholder="range" class="noscroll pages-range"
        name="pages-range" />
</div>
</div>`

window.addEventListener("DOMContentLoaded", (event) => {
    document.querySelectorAll("filecard").forEach(element => {
        element.innerHTML = filecard
    });

    uploader_container = document.querySelector("#upload-container")
    if (uploader_container != null) {
        document.getElementById("UploadAddButton").addEventListener("click", function () {
            new_filecard = document.createElement("filecard")
            new_filecard.innerHTML = filecard
            new_filecard.classList.add("ui-sortable-handle")
            uploader_container.appendChild(new_filecard)
        });
    };
    $(".cards-container").sortable();

    ApplyBootstrapValidation();
});

function removeParent(event) {
    event.target.parentElement.remove();
};

function ApplyBootstrapValidation() {
    'use strict'
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                document.getElementsByName("files").forEach(element => {
                    if (element.value) {
                        if (!element.value.endsWith(".pdf")) {
                            element.classList.add("is-invalid");
                            event.preventDefault()
                            event.stopPropagation()
                        }
                    }
                });
                form.classList.add('was-validated')
            }, false)
        })
};
