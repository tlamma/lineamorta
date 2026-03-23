import csv

# Input CSV and output LaTeX
csv_file = "submissions.csv"
tex_file = "table.tex"

# Escape LaTeX special characters and handle multiline
def latex_escape_multiline(text: str) -> str:
    if not text:
        return ""
    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Escape LaTeX special characters
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Convert newlines to LaTeX line breaks
    lines = text.split("\n")
    lines = [line.strip() for line in lines]
    return " \\\\\n".join(lines)

# Read CSV
data = []
with open(csv_file, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# Start LaTeX table
tex = r"\begin{tabular}{p{0.5\textwidth}|p{0.5\textwidth}}" + "\n"

for i, entry in enumerate(data):
    orig = latex_escape_multiline(entry.get("text_original", ""))
    eng = latex_escape_multiline(entry.get("text_english", ""))
    pseudo = latex_escape_multiline(entry.get("pseudonym", ""))

    orig_cell = f"{orig} \n\\begin{{flushright}}- {pseudo} -\\end{{flushright}}"
    eng_cell = f"{eng} \n\\begin{{flushright}}- {pseudo} -\\end{{flushright}}"

    tex += f"{orig_cell} & {eng_cell} \\\\\n"

    # Add horizontal line except after last row
    if i != len(data) - 1:
        tex += r"\hline" + "\n"

tex += r"\end{tabular}" + "\n"

# Write LaTeX output
with open(tex_file, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"LaTeX table written to {tex_file}")