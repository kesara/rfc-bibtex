from requests import get
import xml.etree.ElementTree as ET

RFC_INDEX = "https://www.rfc-editor.org/rfc-index.xml"
BIBTEX_URL_PREFIX = "https://datatracker.ietf.org/doc/"
BIBTEX_URL_SUFFIX = "/bibtex/"
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
    print(f"Getting BibTeX for {rfc}.")
    url = f"{BIBTEX_URL_PREFIX}{rfc}{BIBTEX_URL_SUFFIX}"
    response = get(url)
    response.raise_for_status()

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


rfcs = get_rfcs()
bibtex = BIBTEX

for rfc in rfcs:
    bibtex += "\n"
    bibtex += get_bibtex(rfc)

with open(BIBTEX_FILE, "w", encoding="utf-8") as file:
    file.write(bibtex)
