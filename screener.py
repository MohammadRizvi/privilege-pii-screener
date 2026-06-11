import os

def find_digit_run(text):
    run = 0
    for char in text:
        if char.isdigit():
            run = run + 1
            if run >= 7:
                return True
        else:
            run = 0
    return False

folder = "docs"

privilege_words = ["attorney", "counsel", "privileged", "confidential", "litigation", "work product", "legal advice"]
results = []
for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue
    path = os.path.join(folder, filename)
    opened = open(path)
    text = opened.read()
    opened.close()

    lower_text = text.lower()
    triggers = []
    privilege_score = 0

    for word in privilege_words:
        count = lower_text.count(word)
        if count > 0:
            privilege_score = privilege_score + count
            triggers.append(word)
    
    pii_score = 0
    at_count = text.count("@")
    if at_count > 0:
        pii_score = pii_score + at_count
        triggers.append("@ symbol")
    if find_digit_run(text):
        pii_score = pii_score + 1
        triggers.append("phone/ID format")
        
    if privilege_score >= 3:
        action = "Privileged"
    elif privilege_score >= 1:
        action = "Potentially Privileged"
    elif pii_score >= 1:
        action = "Needs Further Review"
    else:
        action = "Not Privileged"

    trigger_text = ", ".join(triggers)

    results.append({
        "filename": filename,
        "privilege_score": privilege_score,
        "pii_score": pii_score,
        "triggers": trigger_text,
        "action": action,
    })        
    action_order = {
    "Privileged": 3,
    "Potentially Privileged": 2,
    "Needs Further Review": 1,
    "Not Privileged": 0,
}

results.sort(key=lambda r: action_order[r["action"]], reverse=True)

def print_console_report(results):
    print("Privilege & PII Screener")
    print("Scanned", len(results), "document(s)")
    print("-" * 60)
    for r in results:
        print(r["filename"], "->", r["action"])
        print("  privilege score:", r["privilege_score"], "  PII score:", r["pii_score"])
        if r["triggers"]:
            print("  triggers:", r["triggers"])
        print()

print_console_report(results)

def write_html_report(results):
    action_class = {
        "Privileged": "priv",
        "Potentially Privileged": "priv-maybe",
        "Needs Further Review": "pii",
        "Not Privileged": "clear",
    }

    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Privilege & PII Screener</title>
<style>
body { font-family: Arial, sans-serif; margin: 40px; color: #222; }
h1 { font-size: 22px; }
table { border-collapse: collapse; width: 100%; margin-top: 16px; }
th, td { text-align: left; padding: 10px 14px; border-bottom: 1px solid #ddd; }
th { background: #f4f4f4; }
.priv { background: #f8d0d0; }
.priv-maybe { background: #ffe0b3; }
.pii { background: #fff3b0; }
.clear { background: #d6f5d6; }
.action { font-weight: bold; }
</style>
</head>
<body>
<h1>Privilege &amp; PII Screener</h1>
<p>Scanned """ + str(len(results)) + """ document(s).</p>
<table>
<tr><th>Document</th><th>Action</th><th>Privilege</th><th>PII</th><th>Triggers</th></tr>
"""

    for r in results:
        css = action_class[r["action"]]
        triggers = r["triggers"]
        if triggers == "":
            triggers = "&mdash;"
        html = html + '<tr class="' + css + '">'
        html = html + "<td>" + r["filename"] + "</td>"
        html = html + '<td class="action">' + r["action"] + "</td>"
        html = html + "<td>" + str(r["privilege_score"]) + "</td>"
        html = html + "<td>" + str(r["pii_score"]) + "</td>"
        html = html + "<td>" + triggers + "</td>"
        html = html + "</tr>\n"

    html = html + "</table>\n</body>\n</html>\n"

    out = open("report.html", "w")
    out.write(html)
    out.close()
    print("Wrote dashboard to report.html")

write_html_report(results)
    
    
    

    