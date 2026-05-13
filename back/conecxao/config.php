<?php

$host = "localhost";
$username = "root";
$password = "3512";
$database = "startSolidarium";
$conn = new mysqli($host, $username, $password, $database);
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
?>