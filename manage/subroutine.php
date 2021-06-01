<?php

//処理文字コードの指定
mb_language("Japanese");
mb_internal_encoding("UTF-8");
mb_regex_encoding("UTF-8");

//時刻取得
$dateSerial = time();
$dateString = date('Y/m/d H:i:s', $dateSerial);

//Basic認証下のfile_get_contents
function file_get_contents_ba( $url, $act = '', $pwd = '' ) {
	if( $act == '' && $pwd == ''){
		return file_get_contents($url);
	}	else {
		$basic = array('User-Agent: My User Agent 1.0', 'Authorization: Basic '.base64_encode("{$act}:{$pwd}"),);
		$options = array('http' => array('header' => implode("\r\n", $basic )));
		return file_get_contents($url, false, stream_context_create($options));
	}
}

//初期設定済かの状態を取得(管理者)
function initializedcheck( $pdo ) {
	if( ! $pdo ) return false;
	$preparedSQL = "select * from DCAST_USER_MST";
	$query = $pdo->prepare($preparedSQL);
	$query->execute();
	if( $query->rowCount() == 1 ) return true;
	$query->closeCursor(); //SQLの再実行可能に
	//DCAST_USER_MSTに登録されているデータが1件以外のな場合、テーブルを空に
	$preparedSQL = "TRUNCATE DCAST_USER_MST";
	$query = $pdo->prepare($preparedSQL);
	$query->execute();
	return false;
}

//ログイン状態を取得(管理者)
function logincheck( $loginid, $password, $pdo, $chkonly = false ) {
	if( is_null( $password ) ) return false;
	if( ! $pdo ) return false;
	$preparedSQL = "select * from DCAST_USER_MST where account = :loginid";
	$query = $pdo->prepare($preparedSQL);
	$query->bindParam( ':loginid', $loginid, PDO::PARAM_STR );
	$query->execute();
	if( $query->rowCount() != 1 ) return false;
	$datas = $query->fetchAll( PDO::FETCH_ASSOC );
	$data = $datas[0];
	if( pwd_verify( $password, $data['passwordhash'], $pdo ) ){
		//セッションからログイン情報を保存
		$_SESSION['loginid'] = $loginid;
		$_SESSION['password'] = $password;
		return true;
	} else {
		if( ! $chkonly ){
			//セッションからログイン情報を抹消
			$_SESSION['loginid'] = '';
			$_SESSION['password'] = '';
		}
		return false;
	}
}

//PHP5.5 password_hash互換自作関数('17/01/31現在 PASSWORD_BCRYPT,PASSWORD_DEFAULT共に互換)
function pwd_hash( $pass_org ){
	//saltは自動生成ではなく、2文字のランダム(saltを指定しない場合saltは自動生成されmd5になる)
	$salts = str_split('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789./',1);
	$salt = $salts[rand(0,63)] . $salts[rand(0,63)];
	return crypt($pass_org,$salt);
}

//PHP5.5 password_check互換自作関数('17/01/31現在 PASSWORD_BCRYPT,PASSWORD_DEFAULT共に互換)
function pwd_verify( $pass_org,$pass_hash ){
	if( crypt($pass_org,$pass_hash) === $pass_hash ){
		return true;
	} else {
		return false;
	}
}

function space_trim( $str ){
	//行頭の半角、全角スペースを、空文字に置き換える
	$str = preg_replace('/^[ 　]+/u', '', $str);
	//末尾の半角、全角スペースを、空文字に置き換える
	$str = preg_replace('/[ 　]+$/u', '', $str);
	return $str;
}
//サニタイジング
function sanitize( $value, $kana = false ){
	if( is_array( $value ) ){
		foreach( $value as $wkKey => $wkValue ){
			if( is_array( $wkValue ) ){
				foreach( $wkValue as $wkKey2 => $wkValue2 ){
					$value[$wkKey][$wkKey2] = htmlspecialchars($wkValue2, ENT_QUOTES, 'UTF-8');
					if( $kana ) $value[$wkKey][$wkKey2] = mb_convert_kana( $value[$wkKey][$wkKey2], $kana );
				}
			} else {
				$value[$wkKey] = htmlspecialchars($wkValue, ENT_QUOTES, 'UTF-8');
				if( $kana ) $value[$wkKey] = mb_convert_kana( $value[$wkKey], $kana );
			}
		}
	} else {
		$value = htmlspecialchars($Value, ENT_QUOTES, 'UTF-8');
		if( $kana ) $value = mb_convert_kana( $value, $kana );
	}
	return $value;
}

//データベースに接続
function dbconnect( $dbInst, $dbUser, $dbPass ,$charset = 'UTF-8', $host = false ) {
	$dsn = 'mysql:dbname=' . $dbInst . ';host=' . $host . ';';
	//$dsn = 'mysql:dbname=' . $dbInst . ';host=' . $host . ';charset='.$charset . ";"; //PHP5.3.6以降の文字コード指定付
	$options = array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET CHARACTER SET 'utf8'"); //PHP5.3.6未満の文字コード指定
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
