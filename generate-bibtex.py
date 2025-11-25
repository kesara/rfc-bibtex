from pathlib import Path
from requests import get
import xml.etree.ElementTree as ET

RFC_INDEX = "https://www.rfc-editor.org/rfc-index.xml"
BIBTEX_URL_PREFIX = "https://datatracker.ietf.org/doc/"
BIBTEX_URL_SUFFIX = "/bibtex/"
BIBTEX_DIR = "bibtex"
NS = {"RFCi": "https://www.rfc-editor.org/rfc-index"}
BIBTEX = """%%% -*-BibTeX-*-
%%% ===========================================
%%% Generated with github.com/kesara/rfc-bibtex
%%% ===========================================
"""
BIBTEX_FILE = "bibtex.tex"


def strip_zeros(rfc):
    rfc_number = rfc[3:].lstrip("0")
    return f"rfc{rfc_number}"


def get_bibtex(rfc):
    rfc = strip_zeros(rfc)
    filename = f"{BIBTEX_DIR}/{rfc}.bib"

    if Path(filename).exists():
        print(f"{rfc} BibTeX already exists.")
        bibtex = ""
        with open(filename, "r", encoding="utf-8") as file:
            bibtex = file.read()
        return bibtex
    else:
        print(f"Getting BibTeX for {rfc}.")
        url = f"{BIBTEX_URL_PREFIX}{rfc}{BIBTEX_URL_SUFFIX}"
        response = get(url)
        response.raise_for_status()

        with open(filename, "wb") as file:
            file.write(response.content)

        return response.content.decode("utf-8")


def get_rfcs():
    print("Collecting RFC list.")
    response = get(RFC_INDEX)
    response.raise_for_status()
    rfcs = []

    root = ET.fromstring(response.content)

    for doc_id in root.findall(".//RFCi:rfc-entry/RFCi:doc-id", NS):
        rfcs.append(doc_id.text)

    rfcs.sort()

    return rfcs


def save_pickle(data, filename):
    with open(filename, "wb") as file:
        pickle.dump(data, file)


rfcs = get_rfcs()

big_bibtex = BIBTEX

for rfc in rfcs:
    bibtex = get_bibtex(rfc)
    big_bibtex += "\n"
    big_bibtex += bibtex

with open(BIBTEX_FILE, "w", encoding="utf-8") as file:
    file.write(big_bibtex)

print(f"{BIBTEX_FILE} written")
