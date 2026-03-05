<html>
<body>

<form action="test.php" method="get">
Tema:
<input type="radio" name="gender" value="female">1
<input type="radio" name="gender" value="male">2
<input type="radio" name="gender" value="other">Other<br>
Pseudonimo: <input type="text" name="email"><br>

<?php
$color = "red";
echo "My car is $color<br>";
echo "My house is $color";
?>

<input type="submit">
</form>

</body>
</html>