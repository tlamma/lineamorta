import json

# Input and output files
json_file = "submissions.json"
tex_file = "table.tex"

# Function to escape LaTeX special characters and handle multiline
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

# Load JSON
with open(json_file, encoding="utf-8") as f:
    data = json.load(f)

# Start building LaTeX tabular
tex = r"\begin{tabular}{p{0.5\textwidth}|p{0.5\textwidth}}" + "\n"

for i, entry in enumerate(data):
    orig = latex_escape_multiline(entry.get("text_original", ""))
    eng = latex_escape_multiline(entry.get("text_english", ""))
    pseudo = latex_escape_multiline(entry.get("pseudonym", ""))

    orig_cell = f"{orig} \n\\begin{{flushright}}- {pseudo} -\\end{{flushright}}"
    eng_cell = f"{eng} \n\\begin{{flushright}}- {pseudo} -\\end{{flushright}}"

    tex += f"{orig_cell} & {eng_cell} \\\\\n"

    # Add horizontal line except after last entry
    if i != len(data) - 1:
        tex += r"\hline" + "\n"

tex += r"\end{tabular}" + "\n"

# Write to output
with open(tex_file, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"LaTeX table written to {tex_file}")