from pathlib import Path
import re
import shutil

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


def convert(nb_path, py_out=None, html_out=None):
    """Convert a single notebook to .py and .html"""
    nb = nbformat.read(nb_path, as_version=4)
    # ---- .py ----
    if py_out is not None:
        py_code, _ = PythonExporter().from_notebook_node(nb)
        py_out.write_text(py_code, encoding="utf-8")
    # ---- .html ----
    if html_out is not None:
        html, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
        html_out.write_text(html, encoding="utf-8")
    # ---- title ----
    title = first_heading(nb)
    if title is None:
        title = nb.stem
    return title


def create_rst(rst_out, title, stem, html_dir, ipynb_dir):
    rst = rf"""{title}
{'=' * len(title)}

 * `{stem}.html <../{html_dir}/{stem}.html>`_ (view html)\
 * `{stem}.ipynb <../{ipynb_dir}/{stem}.ipynb>`_ (download notebook)

--------------------

.. only:: html

   .. raw:: html

      <iframe src="../{html_dir}/{stem}.html"
              style="width:100%; height:80vh; border:0;"
              loading="lazy"
              referrerpolicy="no-referrer">
      </iframe>"""
    rst_out.write_text(rst, encoding="utf-8")


def main():
    root_dir = Path(__file__).parent.parent.absolute()
    nb_dir = root_dir / "notebooks"
    doc_dir = root_dir / "doc"
    doc_nb_html_sub_dir = "notebooks_html"
    doc_nb_rst_sub_dir = "notebooks_rst"
    doc_nb_ipynb_sub_dir = "notebooks_ipynb"
    doc_nb_html_dir = doc_dir / "extra" / doc_nb_html_sub_dir
    doc_nb_ipynb_dir = doc_dir / "extra" / doc_nb_ipynb_sub_dir
    doc_nb_rst_dir = doc_dir / doc_nb_rst_sub_dir
    test_nb_dir = root_dir / "tests" / "notebooks"

    # converted NBs are written into these directories, make sure they exist
    for dir in [doc_nb_html_dir, doc_nb_rst_dir, doc_nb_ipynb_dir, test_nb_dir]:
        dir.mkdir(exist_ok=True)

    print("Using the following paths:")
    print(f"  root dir:          {root_dir}")
    print(f"  NB dir:            {nb_dir}")
    print(f"  doc dir:           {doc_dir}")
    print(f"  doc NB HTML dir:   {doc_nb_html_dir}")
    print(f"  doc NB RST dir:    {doc_nb_rst_dir}")
    print(f"  doc NB ipynb dir:  {doc_nb_ipynb_dir}")
    print(f"  test NB dir:       {test_nb_dir}")

    # read gallery header
    with open(doc_nb_rst_dir/"README.rst", 'r') as file:
        nb_gallery = file.read()

    # iterate through notebooks
    print("Start notebook conversion:")
    for nb in nb_dir.glob("*.ipynb"):
        # copy to doc
        shutil.copyfile(nb, doc_nb_ipynb_dir / f"{nb.stem}.ipynb")
        # get title and convert to .py and .html
        title = convert(
            nb_path=nb,
            py_out=test_nb_dir / f"{nb.stem}.py",
            html_out=doc_nb_html_dir / f"{nb.stem}.html",
        )
        # create RST file
        create_rst(rst_out=doc_nb_rst_dir / f"{nb.stem}.rst",
                   title=title,
                   stem=nb.stem,
                   html_dir=doc_nb_html_sub_dir,
                   ipynb_dir=doc_nb_ipynb_sub_dir)
        # add to gallery
        nb_gallery += f"\n * `{title} <{doc_nb_rst_sub_dir}/{nb.stem}.html>`_"
        print(f"  ✓ {nb.name}")
    print("DONE")

    # write gallery file
    (doc_dir / "notebook_gallery.rst").write_text(nb_gallery, encoding="utf-8")


if __name__ == "__main__":
    main()
