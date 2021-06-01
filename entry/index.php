<?php

//処理文字コードの指定
mb_language("Japanese");
mb_internal_encoding("UTF-8");
mb_regex_encoding("UTF-8");

//時刻取得
$dateSerial = time();
$dateString = date('Y/m/d H:i:s', $dateSerial);

//Include,Require
include_once("../manage/subroutine.php");
include_once("../manage/dbinfo.php");

//サニタイジング
$varCOOKIE = sanitize($_COOKIE, 'aKV');
$varSESSION = sanitize($_SESSION, 'aKV');
$varGET = sanitize($_GET, 'aKV');
$varPOST = sanitize($_POST, 'aKV');

//設定項目
$screen_select[1] = "html/index1.html"; //中途採用のみのHOME画面
$screen_select[2] = "html/index2.html"; //新卒採用のみのHOME画面
$screen_select[3] = "html/index3.html"; //新卒・中途採用時のHOME画面
$screen_select[4] = "html/index4.html"; //新卒・プレエントリー採用時のHOME画面
$screen_select[5] = "html/index5.html"; //新卒・プレエントリー・中途採用時のHOME画面
$screen_select[6] = "html/index6.html"; //プレエントリー・中途採用時のHOME画面
$screen_select[7] = "html/index7.html"; //プレエントリーのみのHOME画面
$screen_close = 'closing.html'; //公開期間外の場合に表示する頁のURL
$screen_entry = 'entryform.php';

//file_get_contents ベーシック認証
$url = 'http://' . $_SERVER['SERVER_NAME'] . '/manage/displayget.php';
$screen_json = file_get_contents_ba($url, 'd-cast', 'redcube');

$screen_array = json_decode($screen_json, true);
$screen = $screen_array['template'];

switch( $screen ){
	case '1':
		$output_screen = $screen_select[1];
		break;
	case '2':
		$output_screen = $screen_select[2];
		break;
	case '3':
		$output_screen = $screen_select[3];
		break;
	case '4':
		$output_screen = $screen_select[4];
		break;
	case '5':
		$output_screen = $screen_select[5];
		break;
	case '6':
		$output_screen = $screen_select[6];
		break;
	case '7':
		$output_screen = $screen_select[7];
		break;
	case '0':
	default:
		$output_screen = $screen_close;
		break;
}

$screen_select[1] = "html/index1.html"; //中途採用のみのHOME画面
$screen_select[2] = "html/index2.html"; //新卒採用のみのHOME画面
$screen_select[3] = "html/index3.html"; //新卒・中途採用時のHOME画面
$screen_select[4] = "html/index4.html"; //新卒・プレエントリー採用時のHOME画面
$screen_select[5] = "html/index5.html"; //新卒・プレエントリー・中途採用時のHOME画面
$screen_select[6] = "html/index6.html"; //プレエントリー・中途採用時のHOME画面
$screen_select[7] = "html/index7.html"; //プレエントリーのみのHOME画面

if( $varGET['exp'] == '0' ){
	if( $screen == '2' || $screen == '3' || $screen == '4' || $screen == '5' ) $output_screen = $screen_entry;
} else if( $varGET['exp'] == '1' ){
	if( $screen == '1' || $screen == '3' || $screen == '5' || $screen == '6' ) $output_screen = $screen_entry;
} else if( $varGET['exp'] == '2' ){
	if( $screen == '4' || $screen == '5' || $screen == '6' || $screen == '7' ) $output_screen = $screen_entry;
}

//file_get_contents ベーシック認証
$url = 'http://' . $_SERVER['SERVER_NAME'] . '/entry/' . $output_screen . "?exp={$varGET['exp']}";
$buffer = file_get_contents_ba($url, 'd-cast', 'redcube');
//$buffer = mb_ereg_replace("#####exp#####", $varPOST['exp'], $buffer);
$buffer = mb_ereg_replace("#####[a-zA-Z0-9]{1,}#####", '', $buffer);

echo $buffer . $url;
exit(0);

?>
