
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>JShipp Traffic Recorder</title>
  </head>
  <body>
	<?php
	
	
	
$servername = "localhost";
$username = "sniffer";
$password = "sniffer";
$dbname = "traffic";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}
//echo "Connected successfully";

if (isset($_GET["day"])){
	echo "Report for day " . $_GET["day"] . "<br>";
	
	$sql = "select to_ip, round(sum(sum_size)/1000000000,1) as GB from reports where day=" . $_GET["day"] . " group by to_ip having sum(sum_size)>50000000 order by sum(sum_size) desc;";
	$result = $conn->query($sql);

	echo"<table border=1><tr><td>Dest IP</td><td>GB</td></tr>";
	while($row = $result->fetch_assoc()) {
			echo "<tr><td>" . $row["to_ip"]. "</td><td>" . $row["GB"] . "</td><td>" . str_repeat("l",$row["GB"]) . "</td></tr>";
			}
	echo"</table>";
	}
elseif (isset($_GET["today"])){
	$sql = "select dayofyear(curdate()) as day";
	$result = $conn->query($sql);
	$row = $result->fetch_assoc();
	$day = $row["day"];
	echo "Report for today (" . $day . ")<br>";

	$sql = "select to_ip, round(sum(size)/1000000000,1) as GB from data where day=" . $day . " group by to_ip having sum(size)>50000000 order by sum(size) desc;";
	$result = $conn->query($sql);

	echo"<table border=1><tr><td>Dest IP</td><td>GB</td></tr>";
	while($row = $result->fetch_assoc()) {
			echo "<tr><td>" . $row["to_ip"]. "</td><td>" . $row["GB"] . "</td><td>" . str_repeat("l",$row["GB"]) . "</td></tr>";
			}
	echo"</table>";
	}
elseif (isset($_GET["first"])){
	echo "Report for day " . $_GET["first"] . " to " . $_GET["last"] . "<br>";
	
	$sql = "select to_ip, round(sum(sum_size)/1000000000,1) as GB from reports where day>=" . $_GET["first"] . " and day<=" . $_GET["last"] . " group by to_ip having sum(sum_size)>50000000 order by sum(sum_size) desc;";
	//echo $sql . "<br>";
	$result = $conn->query($sql);

	echo"<table border=1><tr><td>Dest IP</td><td>GB</td></tr>";
	while($row = $result->fetch_assoc()) {
			echo "<tr><td>" . $row["to_ip"]. "</td><td>" . $row["GB"] . "</td><td>" . str_repeat("l",$row["GB"]) . "</td></tr>";
			}
	echo"</table>";	
	}
else{
	echo "<form method=get>";
	echo "Custom Range:<br>";
	echo "First Day <input type=text name=first /></br>";
	echo "Last Day <input type=text name=last /></br>";
	echo "<input type=submit value=Submit />";
	echo "</form><br>";
	
	echo "Daily Summary<br>";

	$sql = "select day, round(sum(sum_size)/1000000000,1) as GB from reports group by day order by day desc;";
	$result = $conn->query($sql);

	echo"<table border=1><tr><td>DAY</td><td>GB</td></tr>";
	echo"<tr><td>Today</td><td><a href=?today=1>Click</a></td></tr>";
	while($row = $result->fetch_assoc()) {
		echo "<tr><td><a href=?day=" . $row["day"] . ">" . $row["day"]. "</a></td><td>" . $row["GB"] . "</td><td>" . str_repeat("l",$row["GB"]) . "</td></tr>";
			}
	echo"</table><br>";
	}



	?>
  </body>
</html>

