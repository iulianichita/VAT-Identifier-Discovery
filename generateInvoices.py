from pathlib import Path
script_dir = Path(__file__).resolve().parent
file_path = script_dir / "BasicCompanyData-2026-11-01-part1_7" / "BasicCompanyData-2026-11-01-part1_7.csv"

import csv, random
from datetime import date, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

with open(file_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
    content = list(reader)
    
OUT = script_dir / "sample-invoices"

SAMPLE = [(row[0], row[1]) for index, row in enumerate(content[1:199:2])]

# print(SAMPLE[:5])

# invoice variation
SWAPS = {"LIMITED": ["LTD", "LTD.", "Limited", "Ltd", "LIMITED"],
        "SERVICES": ["SVCS", "Svcs", "Services", "SERVICES"],
        "BUILDING": ["BLDG", "Building", "BUILDING"],
        "CONSTRUCTION": ["CONSTR", "Construction", "CONSTRUCTION"],
        "CONTRACTORS": ["CONTR", "Contractors", "CONTRACTORS"],
        "ENGINEERING": ["ENG", "Engineering", "ENGINEERING"],
        "MANAGEMENT": ["MGMT", "Management", "MANAGEMENT"],
        "PROPERTIES": ["PROPS", "Properties", "PROPERTIES"],
        "DEVELOPMENTS": ["DEVS", "Developments", "DEVELOPMENTS"],
        "TECHNOLOGY": ["TECH", "Technology", "TECHNOLOGY"],
        "HOLDINGS": ["HLDGS", "Holdings", "HOLDINGS"],
        "GROUP": ["GRP", "Group", "GROUP"], "&": ["&", "AND", "and"]}


def vatNumber():
    d = [random.randint(0, 9) for _ in range(7)]
    total = sum(x * w for x, w in zip(d, (8, 7, 6, 5, 4, 3, 2)))
    check = 97 - (total % 97)
    return "".join(map(str, d)) + f"{check:02d}"

def vary(name):
    out = []
    for w in name.split():
        out.append(random.choice(SWAPS[w]) if w in SWAPS and random.random() < 0.8 else w)
    s = " ".join(out)
    return s if random.random() < 0.5 else s.title() if random.random() < 0.5 else s

def formatVat(v):
    return random.choice([f"GB{v}", f"GB {v}", f"GB {v[:3]} {v[3:7]} {v[7:]}", f"GB{v[:3]} {v[3:7]} {v[7:]}"])

def draw(path, supplier, comp_no, vat):
    c = canvas.Canvas(str(path), pagesize=A4); W, H = A4
    c.setFont("Helvetica-Bold", 16); c.drawString(20*mm, H-25*mm, supplier)
    c.setFont("Helvetica", 9)
    for i, ln in enumerate([f"{random.randint(1,99)} Example Street", random.choice(["Leeds","Bristol","Cardiff","Glasgow","Norwich"]),
                            f"AB{random.randint(1,9)} {random.randint(1,9)}XY (sample address)"]):
        c.drawString(20*mm, H-(31+5*i)*mm, ln)
    c.drawString(20*mm, H-48*mm, f"VAT Reg No: {formatVat(vat)}")
    if random.random() < .7:
        c.drawString(20*mm, H-53*mm, f"Company Reg No: {comp_no}")
    c.setFont("Helvetica", 10)
    d = date(2026, 1, 1) + timedelta(days=random.randint(0, 300))
    c.drawRightString(W-20*mm, H-33*mm, f"Invoice No: INV-{random.randint(1000,99999)}")
    c.drawRightString(W-20*mm, H-39*mm, f"Date: {d:%d/%m/%Y}")
    c.drawString(20*mm, H-75*mm, "Bill to: Sample Customer Ltd, 1 Test Road, London")
    y = H-95*mm; c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, y, "Description"); c.drawRightString(W-20*mm, y, "Net (GBP)")
    c.setFont("Helvetica", 10); net = 0
    for item in random.sample(["Labour","Materials","Site visit","Consultancy","Equipment hire","Call-out fee"], 3):
        y -= 7*mm; amt = round(random.uniform(80, 1500), 2); net += amt
        c.drawString(20*mm, y, item); c.drawRightString(W-20*mm, y, f"{amt:,.2f}")
    vat_amt = round(net*.2, 2)
    y -= 14*mm
    for lab, val in [("Net total", net), ("VAT @ 20%", vat_amt), ("TOTAL", net+vat_amt)]:
        c.drawString(W-70*mm, y, lab); c.drawRightString(W-20*mm, y, f"{val:,.2f}"); y -= 6*mm
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(20*mm, 15*mm, "SYNTHETIC TEST DOCUMENT - not a real invoice; VAT number is fictional.")
    c.save()
    

# generate invoices
for i, (companyName, companyNumber) in enumerate(SAMPLE, 1):
    shownName = vary(companyName)
    no = f"invoice_{i:03d}.pdf"
    draw(OUT / no, shownName, companyNumber, vatNumber())