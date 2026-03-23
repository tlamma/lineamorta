import json
import os
import re

# ========== CONFIGURATION ==========
# Add all the themes you want to extract here
THEMES = ["Ode all'Oblìo || Ode to Oblivion (Dec 25)"]
# ===================================

######### FUTURE : NEED TO PUT THE A CAPOS ####################

json_file = "submissions.json"

# Escape LaTeX special chars while preserving line breaks
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
    return text


# Load JSON
with open(json_file, encoding="utf-8") as f:
    data = json.load(f)

# Process each theme
for theme_name in THEMES:
    # Filter entries by theme
    theme_key = "Select the theme you are contributing to"
    filtered_entries = [
        entry for entry in data 
        if entry.get(theme_key, "") == theme_name
    ]
    
    if not filtered_entries:
        print(f"No entries found for theme '{theme_name}'")
        continue
    
    # Generate output filename
    output_file = f"{theme_name.lower().replace(' ', '_')}_contributions.tex"
    
    # Generate the \couple commands
    tex_content = ""
    
    for entry in filtered_entries:
        pseudonym = latex_escape_multiline(entry.get("Choose a pseudonym for your dirty page", "Anonymous"))
        original = latex_escape_multiline(entry.get("Your script in any language", ""))
        english = latex_escape_multiline(entry.get("Your script in english", ""))
        
        tex_content += f"\\couple{{{pseudonym}}}{{{original}}}{{{english}}}\n\n"
    
    # Write the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(tex_content)
    
    print(f"LaTeX commands for theme '{theme_name}' written to {output_file}")
    print(f"Total entries processed: {len(filtered_entries)}\n")