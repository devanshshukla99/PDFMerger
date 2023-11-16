import argparse
import ast
import os
import pathlib
import re

from pypdf import PdfMerger, PdfReader, PdfWriter
from rich.console import Console

console = Console()


def parse_range(pages_range):
    if type(pages_range) is str:
        pages_range = ast.literal_eval(pages_range)  # it'll be a list

    out_pages = []
    for page in pages_range:
        # range test
        if re.fullmatch(r"[0-9]+-[0-9]+", page):
            # it is a range, ie lower_range, upper_range
            lower_range, upper_range = re.split("-", page)
            if not lower_range:
                lower_range = "0"
            if not upper_range:
                lower_range = "-1"
            out_pages.append(["select_range", int(lower_range), int(upper_range)])
            console.log(f"It's a range: {int(lower_range)}, {int(upper_range)}")

        elif page is None or page == "-" or page == "":
            out_pages.append(
                [
                    "all",
                ]
            )

        else:
            if "," in page:
                page = re.split(",", page)
            _select_pages = ["select_pages"]
            for x in page:
                _select_pages.append(int(x))
            out_pages.append(_select_pages)
            console.log(f"It's page(s): {_select_pages[1:]}")

    return out_pages


def merger_without_glob(files, output, pages_range=None):
    if not files:
        return False

    pdf_files = files
    console.log("[red]PDF to be merged:[/]", pdf_files)
    if not pages_range:
        console.log("Merging all pages")
        # Create an instance of PdfFileMerger() class
        merger = PdfMerger()

        # Iterate over the list of the file paths
        for pdf_file in pdf_files:
            # Append PDF files
            merger.append(pdf_file)

        # Write out the merged PDF file
        merger.write(output)
        merger.close()
        console.log(f"[red]Merged PDF: [green]{output}[/]")
        console.rule()
        return True

    console.log("Merging selected ranges/pages")

    # If pages_range is given then move page by page
    pages_range = parse_range(pages_range)

    out_pdf = PdfWriter()
    # Iterate over the list of the file paths
    for pdf_file, pages in zip(pdf_files, pages_range):
        pdf = PdfReader(pdf_file)

        # if select_range
        if pages[0] == "select_range":
            console.log(f"selecting range: {pages[1]}, {pages[2]}")
            for index in range(pages[1], pages[2] + 1):
                out_pdf.add_page(pdf.pages[index - 1])

        # if select_pages
        elif pages.pop(0) == "select_pages":
            console.log(f"selecting page(s): {pages}")
            for index in pages:
                out_pdf.add_page(pdf.pages[index - 1])

        # if all pages
        else:
            console.log(f"selecting all page(s): {len(pdf.pages)}")
            for index in range(len(pdf.pages)):
                out_pdf.add_page(pdf.pages[index])

    # Write out the merged PDF file
    with open(output, "wb") as out:
        out_pdf.write(out)

    console.log(f"[red]Merged PDF: [green]{output}[/]")
    console.rule()

    # cleanup
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            console.log(f"rm {pdf_file}")
            os.remove(pdf_file)
    return True


def merger(files, output, pages_range=None):
    pdf_files = []

    if not files:
        return False

    # Check if there are any wild flags, glob usage
    pattern = re.compile(r"^[\w|//]+.\w+$")
    for _file in files:
        if not bool(pattern.fullmatch(_file)):
            files_path = pathlib.Path(_file)
            files_dir = files_path.parent
            files_regex = files_path.name
            pdf_files.extend(files_dir.glob(files_regex))
        else:
            pdf_files.extend(re.split(",|\ ", _file))

    return merger_without_glob(pdf_files, output, pages_range)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", type=str, nargs="*", help="PDF files to be merged [allows regex]")
    parser.add_argument("--output", "-o", type=str, nargs=1, default="out.pdf", help="output file")
    args = parser.parse_args()
    merger(args.files, args.output)
