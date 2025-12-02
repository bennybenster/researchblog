import sys
import subprocess
from pathlib import Path
import yaml
import tempfile
import shutil

# CONFIG: adjust these paths for your system
BASE_PATHS = [
    Path(r"C:\Users\Ben\OneDrive - University of St Andrews\Supervision channel for Benjiman\Thematic Analysis Project Writing Files")
    Path(r"~\writing").expanduser()       
]

bib = None
csl = None

for base in BASE_PATHS:
    bib_candidate = base / "MyLibrary.bib"
    csl_candidate = base / "journal-of-english-for-academic-purposes.csl"

    if bib_candidate.exists() and csl_candidate.exists():
        bib = str(bib_candidate)
        csl = str(csl_candidate)
        break

if bib is None:
    raise FileNotFoundError(
        "Could not find .bib and .csl in any expected locations:\n" +
        "\n".join(str(p) for p in BASE_PATHS)
    )

BIBLIOGRAPHY = bib
CSL_FILE = csl

REPO_ROOT = Path(__file__).parent
SOURCE_DIR = REPO_ROOT / "source"
POSTS_DIR = REPO_ROOT / "_posts"


def parse_source(path: Path):
    text = path.read_text(encoding="utf-8")

    if not text.strip().startswith("---"):
        raise ValueError("Source file must start with YAML front matter (---).")

    # Split YAML front matter and body
    parts = text.split("---", 2)
    # parts[0] is empty before first ---
    yaml_text = parts[1]
    body = parts[2]

    meta = yaml.safe_load(yaml_text)
    if "title" not in meta or "date" not in meta:
        raise ValueError("YAML must contain at least 'title' and 'date' fields.")

    # Tags/slug optional
    meta.setdefault("tags", [])
    meta.setdefault("slug", meta["title"].lower().replace(" ", "-"))

    return meta, body


def run_pandoc_on_body(body_text: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        src = tmpdir / "body.md"
        out = tmpdir / "body_processed.md"
        src.write_text(body_text, encoding="utf-8")

        cmd = [
            "pandoc",
            str(src),
            "-f", "markdown",
            "-t", "html",
            "--citeproc",
            "--bibliography", BIBLIOGRAPHY,
            "--csl", CSL_FILE,
            "-o", str(out),
        ]

        subprocess.check_call(cmd)
        return out.read_text(encoding="utf-8")


def build_post(source_path: Path):
    meta, body = parse_source(source_path)
    processed_body = run_pandoc_on_body(body)

    date = str(meta["date"])  # e.g. 2025-03-01
    slug = meta["slug"]
    filename = f"{date}-{slug}.md"
    out_path = POSTS_DIR / filename

    # Build Jekyll front matter
    front_matter = {
        "layout": "single",
        "title": meta["title"],
        "date": date,
        "tags": meta.get("tags", []),
    }

    fm_text = "---\n" + yaml.safe_dump(front_matter, sort_keys=False) + "---\n\n"
    out_path.write_text(fm_text + processed_body, encoding="utf-8")
    print(f"Built post: {out_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python build_post.py source/your-file.md")
        sys.exit(1)

    source_arg = Path(sys.argv[1])
    if not source_arg.is_absolute():
        source_arg = REPO_ROOT / source_arg

    if not source_arg.exists():
        print(f"Source file not found: {source_arg}")
        sys.exit(1)

    build_post(source_arg)


if __name__ == "__main__":
    main()
