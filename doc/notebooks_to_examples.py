from pathlib import Path
import re

import nbformat
from nbconvert import PythonExporter, HTMLExporter

HEADING_RE = re.compile(r'^\s*#{1,6}\s+(.*\S)\s*$')


def first_heading(nb):
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        for line in cell.source.splitlines():
            m = HEADING_RE.match(line)
            if m:
                return m.group(1).strip()
    return None


def convert(nb_path: Path, py_out: Path, html_out: Path):
    """Convert a single notebook to .py and .html"""
    nb = nbformat.read(nb_path, as_version=4)
    # ---- .py ----
    py_code, _ = PythonExporter().from_notebook_node(nb)
    py_out.write_text(py_code, encoding="utf-8")
    # ---- .html ----
    html, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
    html_out.write_text(html, encoding="utf-8")
    # ---- title ----
    title = first_heading(nb)
    if title is None:
        title = nb.stem
    return title


def main():
    root_dir = Path(__file__).parent.absolute()
    nb_dir = root_dir.parent / "notebooks"
    py_dir = root_dir.parent / "tests" / "notebooks"
    doc_dir = root_dir
    html_static_dir = doc_dir / "extra" / "notebooks"
    html_ref_dir = "notebooks"
    py_dir.mkdir(exist_ok=True)
    html_static_dir.mkdir(exist_ok=True)

    with open(nb_dir/"README.rst", 'r') as file:
        nb_gallery = file.read()

    for nb in nb_dir.glob("*.ipynb"):
        title = convert(
            nb_path=nb,
            py_out=py_dir / f"{nb.stem}.py",
            html_out=html_static_dir / f"{nb.stem}.html",
        )
        nb_gallery += f"\n * `{title} <{html_ref_dir}/{nb.stem}.html>`_"
        print(f"✓ {nb.name}")

    (doc_dir / "notebook_gallery.rst").write_text(nb_gallery, encoding="utf-8")


if __name__ == "__main__":
    main()
