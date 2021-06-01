<?php

$dbInst = 'here2';
$dbUser = 'here2';
$dbPass =  'otXwUH9ZA7Mn';
$pdo = dbconnect( $dbInst, $dbUser, $dbPass );

$preparedSQL = "show character set";
$query = $pdo->prepare($preparedSQL);
$query->execute();
$datas = $query->fetchAll( PDO::FETCH_ASSOC );

//データベースに接続
function dbconnect( $dbInst, $dbUser, $dbPass ,$charset = 'utf8mb4', $host = false ) {
	$dsn = 'mysql:dbname=' . $dbInst . ';host=' . $host . ';';
	//$dsn = 'mysql:dbname=' . $dbInst . ';host=' . $host . ';charset='.$charset . ";"; //PHP5.3.6以降の文字コード指定付
	$options = array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET CHARACTER SET 'utf8mb4'"); //PHP5.3.6未満の文字コード指定
	//$options = array();
	try{
		$pdo = new PDO($dsn, $dbUser, $dbPass, $options);
	} catch (PDOException $err) {
		print('Connection failed:'.$err->getMessage());
		return false;
	}
	//属性設定、静的プレースホルダを使用
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); //Catch Exception
	$pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
	$pdo->setAttribute(PDO::MYSQL_ATTR_USE_BUFFERED_QUERY, true); //mysqlベースのコード(fetchallではなくfetchの連続使用)
	return $pdo;
}

?>
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>文字コード</title>
</head>
<body>
<h1>CharacterSets <?php echo htmlentities('🍤🐢🍛🐾🍖☂🚬♨ˡ̩˙̮̑͞͡˓̱ͯ˙̮̑͏͜ˉ̀ᵓ̗ͮ̕ ˡ̩ˊ̮̑͞͡˓̨̨ͯˋ̮̑͏͜ˉ̀ᵓ̗ͮ̕ ⁽⁾⁽⁾⁻ ˡ̩ᵋ́͞͡˓̱ᵋ͏͜ʹ̀ᵓ̗ͮ̕ ˡ̩˙̮̑͞͡˓̯ͯ˙̮̑͏͜ˉ̀ᵓ̗ͮ̕((̵̵́ ̆̂̑͟˚̩̮ ̆̂̑)̵̵̀) ((̵̵́ ̆͒͟˚̩̭ ̆͒)̵̵̀) ((̵̵́ ̆ͯ̑͟˚̨̨̩ ̆ͯ̑)̵̵̀) ((̵̵́ ̆́̑͟˚̩̮ ̆̀̑)̵̵̀)"A＆ん'); ?></h1>
<?php
asort( $datas );
foreach( $datas as $data ){
	echo "{$data['Charset']} => {$data['Default collation']}<br>\n";
}
?>
</body>
</html>
