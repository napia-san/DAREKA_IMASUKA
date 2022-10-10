<?php
//DBログイン情報
$dsn = 'mysql:hoge;host=hoge.hoge.jp;charset=utf8';
$user = 'hoge';
$password = 'hohoge';
try {
    $dbh = new PDO($dsn, $user, $password);
    $sql = 'SELECT NAME,ROOM_X,ROOM_Y,ROOM_Z FROM CurrentStatus';
	$statement = $dbh -> query($sql);
	
	//レコード件数取得
	$row_count = $statement->rowCount();
	
	while($row = $statement->fetch()){
		$rows[] = $row;
	}
	
	//データベース接続切断
	$dbh = null;
    
}catch (PDOException $e){
	print('Error:'.$e->getMessage());
	die();
}

?>

<!DOCTYPE html>
<html lang="ja">
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Status</title>
	<meta http-equiv="refresh" content="60" >
	<meta charset="utf-8">
</head>
<body>
	<div class="box">
		<table border="1">
			<th>NAME</th>
			<th>room_X</th>
			<th>room_Y</th>
			<th>room_Z</th>
			<?php 
			foreach($rows as $row){
			?> 
			<tr>
				<td><?php echo htmlspecialchars($row['NAME'],ENT_QUOTES,'UTF-8'); ?></td>
				<td><?php echo htmlspecialchars($row['ROOM_X'],ENT_QUOTES,'UTF-8'); ?></td>
				<td><?php echo htmlspecialchars($row['ROOM_Y'],ENT_QUOTES,'UTF-8'); ?></td>
				<td><?php echo htmlspecialchars($row['ROOM_Z'],ENT_QUOTES,'UTF-8'); ?></td>
			</tr>
			<?php 
			} 
			?>
		</table>
	</div>
</body>
</html>