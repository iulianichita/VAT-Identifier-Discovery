from pathlib import Path
script_dir = Path(__file__).resolve().parent
file_path = script_dir / "BasicCompanyData-2026-11-01-part1_7" / "BasicCompanyData-2026-11-01-part1_7.csv"

import csv, re

with open(file_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
    content = list(reader)
    
def pp(row):
    for i, column in enumerate(content[0]):
        if len(row[i]) != 0:
            print(column.strip(), ':', row[i])
        

VARIANTS = {
    "LIMITED": ["LTD", "LTD.", "LIM", "LMTD", "LTED", "LIMTED", "LIMITED"],
    "PUBLIC LIMITED COMPANY": ["PLC", "P.L.C.", "PUBLIC LIMITED COMPANY"],
    "LLP": ["LLP", "L.L.P.", "LIMITED LIABILITY PARTNERSHIP"],
    "AND": ["&", "AND", "+"],
    "COMPANY": ["CO", "CO.", "COMP", "COMPANY"],
    "SERVICES": ["SVCS", "SVC", "SERV", "SERVS", "SERVICE", "SERVICES"],
    "BUILDING": ["BLDG", "BLDNG", "BUILDING", "BUILDINGS"],
    "CONSTRUCTION": ["CONSTR", "CONSTRUCTN", "CONST", "CONSTRUCTION"],
    "CONTRACTORS": ["CONTR", "CONTRS", "CONTRACTOR", "CONTRACTORS"],
    "ENGINEERING": ["ENG", "ENGG", "ENGR", "ENGINEERING"],
    "GROUP": ["GRP", "GROUP"],
    "HOLDINGS": ["HLDGS", "HLDG", "HOLDING", "HOLDINGS"],
    "INTERNATIONAL": ["INTL", "INT'L", "INTERNATIONAL"],
    "MANAGEMENT": ["MGMT", "MGT", "MANAGEMENT"],
    "PROPERTY": ["PROP", "PROPERTY", "PROPERTIES", "PROPS"],
    "DEVELOPMENTS": ["DEV", "DEVS", "DEVELOPMENT", "DEVELOPMENTS"],
    "ASSOCIATES": ["ASSOC", "ASSOCS", "ASSOCIATES"],
    "SOLUTIONS": ["SOLNS", "SOLUTION", "SOLUTIONS"],
    "TECHNOLOGY": ["TECH", "TECHNOLOGY", "TECHNOLOGIES"],
    "ELECTRICAL": ["ELEC", "ELECT", "ELECTRICAL"],
    "MAINTENANCE": ["MAINT", "MAINTENANCE"],
}

LOOKUP = {}
for canon, vs in VARIANTS.items():
    for v in vs:
        LOOKUP[re.sub(r"[.,'‘’“”\"()]", "", v)] = canon
        
def normalize(name):
    name = name.upper().replace("&", " AND ")
    name = re.sub(r"[.,'‘’“”\"()!]", "", name)
    name = re.sub(r"[-/]", " ", name)
    return [LOOKUP.get(w, w) for w in name.split()]

def search(value): # value can be company name or company number
    value = value.strip()
    
    # company number
    if value.replace(" ", "").isdigit():
        return [row for row in content
            if row[1] == value.replace(" ", "")]
        
    results = []
    
    # company name
    wordsList = normalize(value)

    for row in content[1:]:
        common = 0
        companyName = normalize(row[0])
        for word in wordsList:
            if word.upper() in companyName:
                common = common + 1
        
        score = common / len(wordsList) - 0.1 * ( len(companyName) - len(wordsList) )
        if score > 0.7:
            results.append(row)
        
    if len(results) == 0:    
        return "There is no company with these details."
    else:
        return results

    
results = search("\" TRIPLE. D\" PROPERTIES LTD.")
for companyDetails in results:
    pp(companyDetails)
    print()
