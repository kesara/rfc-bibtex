from bibtexparser import parse_file

BIBTEX_FILE = "bibtex.tex"

try:
    library = parse_file(BIBTEX_FILE)
    if len(library.failed_blocks) > 0:
        print(f"{BIBTEX_FILE} is invalid")
    else:
        print(f"{BIBTEX_FILE} is valid")
except Exception as e:
    print(f"Error: {e}")
    print(f"{BIBTEX_FILE} is invalid")
