<?php
// ---------- CSV File ----------
$file = 'submissions.csv';
$message = '';

function fputcsv_all_quoted($handle, $fields, $delimiter = ',', $enclosure = '"') {
    $escaped = array_map(function ($field) use ($enclosure) {
        // Escape existing quotes by doubling them
        $field = str_replace($enclosure, $enclosure . $enclosure, $field);
        return $enclosure . $field . $enclosure;
    }, $fields);

    $line = implode($delimiter, $escaped) . "\n";
    fwrite($handle, $line);
}

// ---------- Handle form submission ----------
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input
    $theme = htmlspecialchars(trim($_POST['theme']));
    $pseudonym = htmlspecialchars(trim($_POST['pseudonym']));
    $text_original = htmlspecialchars(trim($_POST['text_original']));
    $text_english = htmlspecialchars(trim($_POST['text_english']));
    $suggestions = htmlspecialchars(trim($_POST['suggestions']));

    // Check duplicates (same pseudonym + same text_original)
    $isDuplicate = false;
    if (file_exists($file)) {
        $rows = array_map('str_getcsv', file($file));
        foreach ($rows as $row) {
            if (count($row) >= 3 && $row[1] === $pseudonym && $row[2] === $text_original) {
                $isDuplicate = true;
                break;
            }
        }
    }


    if ($isDuplicate) {
        $message = "Duplicate submission detected. You have already submitted this text.";
    } else {
        // Append to CSV
        $fp = fopen($file, 'a');
        if ($fp !== false) {
            fputcsv_all_quoted($fp, [$theme, $pseudonym, $text_original, $text_english, $suggestions]);
            fclose($fp);
            $message = "Thank you! Your submission has been saved.";
        } else {
            $message = "Error: Could not save submission.";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Contribution Form</title>

<!-- ---------- Fonts: lineamorta.nl style ---------- -->
<link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;1,400&family=Source+Sans+Pro:wght@400;600&display=swap" rel="stylesheet">

<style>
/* ---------- Body & Form ---------- */
body {
    font-family: 'Merriweather', serif;
    background: #fafafa;
    margin: 0;
    padding: 2em;
    color: #222;
}

form {
    background: #fff;
    max-width: 700px;
    margin: auto;
    padding: 2em;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

h1 {
    font-family: 'Source Sans Pro', sans-serif;
    font-weight: 600;
    font-size: 1.8em;
    margin-bottom: 1em;
    text-align: center;
    letter-spacing: 0.5px;
}

/* ---------- Inputs ---------- */
label {
    display: block;
    margin-top: 1.2em;
    font-weight: 600;
    font-family: 'Source Sans Pro', sans-serif;
}

input[type="text"], textarea, select {
    width: 100%;
    padding: 0.6em;
    margin-top: 0.3em;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-family: 'Merriweather', serif;
    font-size: 1em;
    line-height: 1.4em;
    resize: vertical;
}

input[type="submit"] {
    margin-top: 1.8em;
    padding: 0.7em 2em;
    font-size: 1em;
    border: none;
    background: #222;
    color: #fff;
    border-radius: 4px;
    cursor: pointer;
    font-family: 'Source Sans Pro', sans-serif;
}

input[type="submit"]:hover {
    background: #444;
}

/* ---------- Message ---------- */
.message {
    margin: 1em auto;
    max-width: 700px;
    text-align: center;
    font-weight: 600;
    color: green;
    font-family: 'Source Sans Pro', sans-serif;
}

</style>
</head>
<body>

<h1>Contribution Form</h1>

<?php if (!empty($message)) echo "<div class='message'>$message</div>"; ?>

<form action="" method="post">
    <label for="theme">Theme you are contributing to:</label>
    <select id="theme" name="theme" required>
        <option value="">-- Select a theme --</option>
        <option value="Nature">Nature</option>
        <option value="Technology">Technology</option>
        <option value="Society">Society</option>
        <option value="Art">Art</option>
        <option value="Other">Other</option>
    </select>

    <label for="pseudonym">Pseudonym:</label>
    <input type="text" id="pseudonym" name="pseudonym" required>

    <label for="text_original">Text in your language:</label>
    <textarea id="text_original" name="text_original" rows="7"></textarea>

    <label for="text_english">Text in English:</label>
    <textarea id="text_english" name="text_english" rows="7" required></textarea>

    <label for="suggestions">Suggestions / Comments:</label>
    <textarea id="suggestions" name="suggestions" rows="3"></textarea>

    <input type="submit" value="Submit">
</form>

</body>
</html>