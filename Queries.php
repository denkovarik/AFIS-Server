<?php

function openConnection()
{
    $servername = "localhost";
    $username = "admin";
    $password = "1QAZ2wsx3edc!";
    $db = "db_afis_f20";

// Create connection
    $conn = new mysqli($servername, $username, $password, $db) or die("Connection failed: " . $conn->connect_error);
    return $conn;
}
// Check connection
function get_xtyFiles($conn, $f_name)
{
    $query = "SELECT xyt_file FROM Minutiaes";
    if ($results = $conn->query($query)) {
        $myfile = fopen($f_name, "w") or die("Unable to open file!");
        while ($row = $results->fetch_row()) {
            fwrite($myfile, $row[0]);
            fwrite($myfile, "\n");
        }
        fclose($myfile);
    }
    else
        echo "data is empty";

}

// Sample Usage
// $f_name = "xyt_paths.txt";
// touch($f_name);
// chmod($f_name, 0777);
// $connection = openConnection();
// get_xtyFiles($connection, $f_name);
// // Use the file, then delete the file when finished
// unlink($f_name);

?>