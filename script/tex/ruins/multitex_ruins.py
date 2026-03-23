import json
import os
import re

# Input JSON
json_file = "submissions.json"
output_dir = "theme_tables"
os.makedirs(output_dir, exist_ok=True)

# Escape LaTeX special chars and handle multiline
def latex_escape_multiline(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
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
    lines = text.split("\n")
    lines = [line.strip() for line in lines]
    return " \\newline\n".join(lines)

# Sanitize theme name to a safe filename
def sanitize_filename(name: str) -> str:
    return re.sub(r"[^\w\-]", "_", name)

# Load JSON
with open(json_file, encoding="utf-8") as f:
    data = json.load(f)

# Group by theme
themes = {}
for entry in data:
    theme = entry.get("Select the theme you are contributing to", "Misc")
    themes.setdefault(theme, []).append(entry)

# Generate a .tex table for each theme
for theme, entries in themes.items():
    filename = f"{sanitize_filename(theme)}.tex"
    tex_file = os.path.join(output_dir, filename)
    
    tex = f"\\section*{{{theme}}}\n"
    tex += r"\begin{tabular}{p{0.5\textwidth}|p{0.5\textwidth}}" + "\n"
    
    for i, entry in enumerate(entries):
        orig = latex_escape_multiline(entry.get("Your script in any language", ""))
        eng = latex_escape_multiline(entry.get("Your script in english", ""))
        pseudo = latex_escape_multiline(entry.get("Choose a pseudonym for your dirty page", ""))
        
        orig_cell = f"{orig} \n\\begin{{flushright}}- {pseudo} -\\end{{flushright}}"
        eng_cell = f"{eng} \n\\begin{{flushright}}- {pseudo} -\\end{{flushright}}"
        
        tex += f"{orig_cell} & {eng_cell} \\\\\n"
        if i != len(entries) - 1:
            tex += r"\hline" + "\n"
    
    tex += r"\end{tabular}" + "\n"

    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(tex)
    
    print(f"LaTeX table for theme '{theme}' written to {tex_file}")