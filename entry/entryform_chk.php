<?php

//処理文字コードの指定
mb_language("Japanese");
mb_internal_encoding("UTF-8");
mb_regex_encoding("UTF-8");

//引数受渡
$varPOST = input_format( $_POST, "aKV", "UTF-8", "UTF-8", true, true );
$varGET = input_format( $_GET, "aKV", "UTF-8", "UTF-8", true, true );
$varCOOKIE = input_format( $_COOKIE, "aKV", "UTF-8", "UTF-8", true, true );
$varSERVER = input_format( $_SERVER, "aKV", "UTF-8", "UTF-8", true, true );
$varSESSION = input_format( $_SESSION, "aKV", "UTF-8", "UTF-8", true, true );
//小文字に統一
$varPOST['mail'] = strtolower($varPOST['mail']);

//時刻取得
$date_serial = time();
$date_string = date('Y/m/d H:i:s',$date_serial);
$date_array = getdate($date_serial);

$ret['result'] = true;
if ( $varGET['mode'] == "" || $varGET['mode'] == null) $varGET['mode'] = "all";
switch ( $varGET['mode'] ) {
case "all" :
case "mail" :
	switch ( input_check( $varPOST['mail'], 'mail', 6, 255 ) ) {
	case 0 :
		if( is_null($varSESSION['userid']) || $varSESSION['userid'] == "" ) $varSESSION['userid'] = -1;
		$SQLstr = "select * from GAUCTION_MST_USER where userid = {$varSESSION['userid']}";
		$res = mysql_query($SQLstr);
		if( mysql_num_rows($res) != 1 ){
			if( $varSESSION['userid'] == -1 ){
				$ret['mail'] = "<span class=\"text-error\">メールアドレスを入力して下さい。</span>";
				$ret['result'] = false;
			} else {
				//ログイン情報に誤りがある場合には、ログアウト画面へ
				header ('HTTP/1.1 302 Found');
				header ("Location: $domainSecure[0]logout.php?proc=logout");
				exit(0);
			}
		}
		break;
	case -1 :
		$ret['mail'] = "<span class=\"text-error\">メールアドレスに誤りがあります。</span>";
		$ret['result'] = false;
		$varPOST['mail'] = "";
		break;
	default:
		break;
	}
	if ( $varGET['mode'] != "all" ) break;
case "inquiry" :
	switch ( input_check( $varPOST['inquiry'], 'jp', 0, 0 ) ) {
	case 0 :
		$ret['inquiry'] = "<span class=\"text-error\">ご意見・ご質問を入力して下さい。</span>";
		$ret['result'] = false;
		break;
	case -1 :
		$ret['inquiry'] = "<span class=\"text-error\">ご意見・ご質問に誤りがあります。</span>";
		$ret['result'] = false;
		$varPOST['nickname'] = "";
		break;
	default:
		break;
	}
	if ( $varGET['mode'] != "all" ) break;
default:
	break;
}

if ( $varGET['mode'] != "all" ) {
	$ret['message'] = $ret[$varGET['mode']];
	echo json_encode($ret);
} else {
	return $ret;
}

?>
