from rich.console import Console
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file

from api.util import TempDir
from pdfmerger.main import merger_without_glob

app = Flask(__name__)

console = Console()

uploaded_filenames = []
tempdir = None


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        print(request.files)
        files = request.files.getlist("files")
        if not files:
            return "No files uploaded"

        pages_ranges = request.form.getlist("pages-range")
        console.log(pages_ranges)

        with TempDir() as tempdir:
            uploaded_filenames = []
            filenames_for_template = []
            console.log(files)

            for f in files:
                secure_name = secure_filename(f.filename)
                _filename = tempdir + "/" + secure_name
                uploaded_filenames.append(_filename)
                filenames_for_template.append(secure_name)
                f.save(_filename)

            console.log(uploaded_filenames)
            outfile = tempdir + "/" + "out.pdf"
            if merger_without_glob(uploaded_filenames, outfile, pages_ranges):
                return send_file(outfile)

        return "Idk, an issue occured"

    return render_template("index.html")
