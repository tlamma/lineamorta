import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/forms.responses.readonly',
    'https://www.googleapis.com/auth/forms.body.readonly'
]

creds = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=SCOPES
)

service = build('forms', 'v1', credentials=creds)

form_id = "1rF_O1pMN4dOk_xpaH_P_kM_b5qptM1gibWRPrV6dWX0"

# --- Get form metadata ---
form = service.forms().get(formId=form_id).execute()
items = form.get("items", [])
qid_to_title = {}
for item in items:
    question = item.get("questionItem", {}).get("question")
    if question:
        qid = question.get("questionId")
        title = item.get("title", f"Question {qid}")
        qid_to_title[qid] = title

# --- Fetch responses ---
responses = service.forms().responses().list(formId=form_id).execute()
raw = responses.get("responses", [])

# --- Flatten responses ---
rows = []
for r in raw:
    answers = r.get("answers", {})
    flat = {"Timestamp": r.get("createTime")}
    for qid, q_title in qid_to_title.items():
        ans = answers.get(qid, {})
        value = ""
        if "textAnswers" in ans:
            txt_list = ans["textAnswers"].get("answers", [])
            if txt_list:
                value = txt_list[0].get("value", "")
        elif "choiceAnswers" in ans:
            value = ", ".join(ans["choiceAnswers"].get("values", []))
        elif "fileUploadAnswers" in ans:
            files = ans["fileUploadAnswers"].get("answers", [])
            value = ", ".join([f.get("fileId", "") for f in files])
        flat[q_title] = value
    rows.append(flat)

# --- Write CSV safely ---
fieldnames = ["Timestamp"] + list(qid_to_title.values())
with open("form_responses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames,
        quoting=csv.QUOTE_ALL  # <-- ensures all fields are wrapped in quotes
    )
    writer.writeheader()
    for row in rows:
        # Ensure all fields exist
        safe_row = {fn: row.get(fn, "") for fn in fieldnames}
        writer.writerow(safe_row)

print("CSV saved as form_responses.csv")
