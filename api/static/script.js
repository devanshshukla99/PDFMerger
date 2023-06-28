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
    document.querySelectorAll(".btn-close").forEach(element => {
        element.addEventListener("click", event => {
            console.log(event.target.parentElement)
            event.target.parentElement.remove();
        })
    });
    (function () {
        'use strict'
        console.log("validator")
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
    })()
});
