# please note: this script works in cases where the invoice has the company name (or variations of it) or the company number and there is not a list with company data and its vat number

import csv, re
from pathlib import Path
import pdfplumber

from search import content, normalize

script_dir = Path(__file__).resolve().parent
FOLDER = script_dir / "sample-invoices"

THRESHOLD = 0.7        # minimum score for a name match
COMMON_LIMIT = 50000   # tokens appearing in more rows than this (LIMITED, etc.) are not used to find candidates

rows = [r for r in content[1:] if len(r) > 1]
tokensList = [set(normalize(r[0])) for r in rows] # cuvintele din numele companiilor

def normNumber(n):
    n = n.strip().upper()
    return n.zfill(8) if n.isdigit() else n

byNumber = {normNumber(r[1]): r for r in rows}

index = {}   # token -> list of row positions
for i, tokens in enumerate(tokensList):
    for t in tokens:
        index.setdefault(t, []).append(i)

# extract from PDF
VAT_RE = re.compile(r"\bGB\s?(\d{3})\s?(\d{4})\s?(\d{2})\b", re.IGNORECASE)
NUMBER_RE = re.compile(
    r"Company\s+(?:Reg(?:istration)?\.?\s+)?(?:No\.?|Number)\s*:?\s*([A-Z]{2}\d{6}|\d{8})",
    re.IGNORECASE)
SUFFIX_RE = re.compile(r"\b(LTD|LIMITED|PLC|LLP|CIC)\b", re.IGNORECASE)

def readText(pdfPath):
    with pdfplumber.open(pdfPath) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def vatValid(d):
    total = sum(int(x) * w for x, w in zip(d[:7], (8, 7, 6, 5, 4, 3, 2)))
    check = int(d[7:])
    return (total + check) % 97 == 0 or (total + check + 55) % 97 == 0

def extractVat(text):
    found = {"".join(m.groups()) for m in VAT_RE.finditer(text)}
    valid = [v for v in found if vatValid(v)]
    if valid:
        return "GB" + valid[0], "ok"
    if found:
        return "GB" + next(iter(found)), "invalid VAT check digits"
    return "", "no VAT found"

def extractNumber(text):
    m = NUMBER_RE.search(text)
    return m.group(1).upper() if m else ""

def extractName(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        if line.lower().startswith(("bill to", "customer", "invoice to", "synthetic")):
            continue
        if SUFFIX_RE.search(line):
            return line
    return lines[0] if lines else ""

# matching
def score(q, tokens):
    return len(q & tokens) / len(q) - 0.1 * len(tokens - q)

def searchName(name, top=5):
    q = set(normalize(name))
    if not q:
        return []
    candidates = set()
    for t in q:
        postings = index.get(t, [])
        if len(postings) <= COMMON_LIMIT:
            candidates.update(postings)
    results = []
    for i in candidates:
        s = score(q, tokensList[i])
        if s >= THRESHOLD:
            results.append((s, rows[i]))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top]

def matchCompany(name, number):
    # 1. company number found on the invoice
    if number and normNumber(number) in byNumber:
        row = byNumber[normNumber(number)]
        q = set(normalize(name))
        s = score(q, set(normalize(row[0]))) if q else 1.0
        return row, s, "company number", ("ok" if s >= THRESHOLD else "number/name mismatch")

    # 2. otherwise by name
    matches = searchName(name) if name else []
    if not matches:
        return None, 0, "name", "no match"
    s, row = matches[0]
    if len(matches) > 1 and s - matches[1][0] < 0.05 and matches[1][1][1] != row[1]:
        return row, s, "name", "ambiguous"
    return row, s, "name", "ok"

# index view
# for i, rec in enumerate(index):
#     print(rec)
#     print(index[rec])
#     if i == 5:
#         break


results = []
for pdfPath in sorted(FOLDER.glob("*.pdf")):
    text = readText(pdfPath)
    if not text.strip():
        results.append([pdfPath.name, "", "", "", "", 0, "", "no text (needs OCR)"])
        continue

    vat, vatStatus = extractVat(text)
    nameOnInvoice = extractName(text)
    numberOnInvoice = extractNumber(text)

    row, s, method, status = matchCompany(nameOnInvoice, numberOnInvoice)
    if status == "ok" and vatStatus != "ok":
        status = vatStatus

    results.append([pdfPath.name, nameOnInvoice,
                    row[0] if row else "", row[1] if row else "",
                    vat, round(s, 2), method, status])
    print(pdfPath.name, status)

with open("matches.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file", "name_on_invoice", "matched_name", "company_number",
                "vat_number", "score", "method", "status"])
    w.writerows(results)

# final document: only confirmed rows, without duplicates
final = {}
for r in results:
    if r[7] == "ok":
        final.setdefault((r[2], r[3]), set()).add(r[4])

with open("companies_vat.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["company_name", "company_number", "vat_number"])
    for (name, number), vats in sorted(final.items()):
        if len(vats) > 1:
            print("WARNING: different VAT numbers for", name, vats)
        for v in sorted(vats):
            w.writerow([name, number, v])