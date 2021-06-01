#!/usr/bin/perl
use strict; 
use warnings; 
#use Encode;
use Time::HiRes qw/ gettimeofday /;
use Time::Local;
use Switch;
use Data::Dumper;	#zip化(暗号化)の際に使用
use Jcode;
#文字コード設定,環境に依存
#use utf8;
#binmode(STDOUT, ":utf8");

#設定項目
my $make_zip = '1'; #データのzip化の指定 1 => zip,0 => csv
my $zipPwd = '0d1ad'; #zip化の際のパスワード
my $titleFile = 'title.txt'; #csvファイルの項目見出し
my $inifile = "ini.csv"; #iniファイル(csv形式)の指定

#変数定義 スコープ付き(my使用,環境依存)
my ($string,$value,$name,$pair);
my @pairs;
#POST値の初期化
my %varPOST = (
	'date_s' => '','' => '','date_e' => '','target' => '','pf' => ''
);
#GET値の初期化
my %varGET = ('proc' => '' );

#設定値の初期化
my %settings = (
	'ctrl' => '0'
);

my (@wkBuf,@fileNames,@wkItems);
my ($i,$j,$cnt,$outfile,$wkKey,$wkValue,$wkString,$fileHandle,$fileTime,$dateStart,$dateEnd,$publicForm);
my $debug = 0;
my $wkRecBuf = "";
my $wkBuffer = "";
my @idx = ('proc','date_s','date_e','target');
my (%ret,%res);
my ($arrayKey, $arrayValue);
my ($rets,$filePath,$zipPath);
my $ZIP_CMD = "/usr/bin/zip";
my $UNZIP_CMD = "/usr/bin/unzip";

#時間取得(micro秒単位)
my ($epocSec, $microSec) = gettimeofday();
my ($sec,$min,$hour,$day,$mon,$year) = localtime($epocSec);
my $microTime = sprintf("%d%02d%02d%02d%02d%02d%d",$year + 1900,$mon + 1,$day,$hour,$min,$sec,$microSec);
my $nowDate = sprintf("%d%02d%02d",$year + 1900,$mon + 1,$day);

#POST値の受け渡し
if( $ENV{'REQUEST_METHOD'} eq "POST" ){
	read(STDIN, $string, $ENV{'CONTENT_LENGTH'});
} else {
	$string = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/,$string);
foreach $pair (@pairs){
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$varPOST{$name} = $value;
}

#GET値の受け渡し
$string = $ENV{'QUERY_STRING'};
@pairs = split(/&/,$string);
foreach $pair (@pairs){
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$varGET{$name} = $value;
}

#設定値の読込
my $flg = 1;
open (FILE, $inifile) or $flg = 0;
if( $flg == 1 ){
	my @inilist = <FILE>;
	close(FILE);
	foreach my $wkline( @inilist ){
		chomp $wkline;
		( $wkKey, @wkItems ) = split( /,/, $wkline );
		$settings{$wkKey} = $wkItems[0];
	}
}

if( $varPOST{'pf'} eq '0' || $varPOST{'pf'} eq '1' || $varPOST{'pf'} eq '2' || $varPOST{'pf'} eq '3' || $varPOST{'pf'} eq '4' || $varPOST{'pf'} eq '5' || $varPOST{'pf'} eq '6' || $varPOST{'pf'} eq '7' ){ $settings{'ctrl'} = $varPOST{'pf'}; }
#現在公開中の画面
switch( $settings{'ctrl'} ){
	case 2 {
		$publicForm = "新卒採用のみ受付";
	} case 1 {
		$publicForm = "既卒採用のみ受付";
	} case 7 {
		$publicForm = "プレエントリーのみ受付";
	} case 3 {
		$publicForm = "新卒・既卒採用エントリー受付";
	} case 4 {
		$publicForm = "新規・プレエントリー受付";
	} case 6 {
		$publicForm = "プレエントリー・既卒採用受付";
	} case 5 {
		$publicForm = "新卒・プレエントリー・既卒採用受付";
	} case 0 {
		$publicForm = "エントリー受付なし";
	} else {
		$publicForm = "エントリー受付なし";
	}
}

switch( $varGET{'proc'} ){
	case 'ddel' {
		@fileNames = glob "*.zip";
		foreach $arrayValue (@fileNames) {
			unlink $arrayValue;
		}
		@fileNames = glob "*.csv";
		foreach $arrayValue (@fileNames) {
			$zipPath = $arrayValue;
			if( substr($arrayValue, 0, 3) ne 'ini' ){
				unlink $arrayValue;
			}
		}
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"result":"1"}';
		exit(0);
	} case 'make' {
		#csvファイルの項目見出しを読込
		open $fileHandle,"< $titleFile"or next;
    @wkBuf = <$fileHandle>; #解凍したファイルの内容を一気に変数に読み込み
		$wkRecBuf .= $wkBuf[0];
    close $fileHandle;
		$ret{'result'} = 0;
		$ret{'message'} = '';
		$ret{'target'} = '';
		$i = 0;
		if( $varPOST{'date_s'} ne '' && $varPOST{'date_e'} ne '' ){
			$dateStart = $varPOST{'date_s'};
			($year,$mon,$day) = ($dateStart =~ /(\d{4})\/(\d\d)\/(\d\d)/);
	    $dateStart = timelocal(0,0,0,$day,$mon - 1,$year);
			$dateEnd = $varPOST{'date_e'};
			($year,$mon,$day) = ($dateEnd =~ /(\d{4})\/(\d\d)\/(\d\d)/);
	    $dateEnd = timelocal(59,59,23,$day,$mon - 1,$year);
			if( $make_zip eq '1' ){
				@fileNames = glob "*.zip";
				foreach $arrayValue (@fileNames) {
					$zipPath = $arrayValue;
					if( substr($arrayValue, 0, 4) ne 'data' ){
						$fileTime = (stat($zipPath))[10];
						if( $fileTime >= $dateStart && $fileTime <= $dateEnd ){
							open $fileHandle,"$UNZIP_CMD -p -P $zipPwd $zipPath |"or next;
					    @wkBuf = <$fileHandle>; #解凍したファイルの内容を一気に変数に読み込み
					    close $fileHandle;
							foreach $wkBuffer ( @wkBuf ){
								$wkRecBuf .= $wkBuffer;
							}
							$i = $i + 1;
						}
					}
				}
			} else {
				@fileNames = glob "*.csv";
				foreach $arrayValue (@fileNames) {
					$zipPath = $arrayValue;
					if( substr($arrayValue, 0, 4) ne 'data' && substr($arrayValue, 0, 3) ne 'ini' ){
						$fileTime = (stat($zipPath))[10];
						if( $fileTime >= $dateStart && $fileTime <= $dateEnd ){
							open $fileHandle,"< $zipPath"or next;
					    @wkBuf = <$fileHandle>; #ファイルの内容を一気に変数に読み込み
					    close $fileHandle;
							foreach $wkBuffer ( @wkBuf ){
								$wkRecBuf .= $wkBuffer;
							}
							$i = $i + 1;
						}
					}
				}
			}
			if( $i == 0 ){
				$ret{'result'} = 0;
				$ret{'message'} = '※指定された作成範囲にデータが存在しません。';
			} else {
				$i = 0;
				#Encode(v5.8upper環境)
				#$wkRecBuf = decode('utf-8', $wkRecBuf);
				#$wkRecBuf = encode('Shift_JIS', $wkRecBuf);
				#Jcode.pm仕様
				#$wkRecBuf = Jcode::convert( $wkRecBuf , "sjis", "utf8" );	#書き方1
				#$wkRecBuf = Jcode->new( $wkRecBuf, "utf8")->sjis;	#書き方2
				while( 1 ){
					$i = $i + 1;
					$outfile = 'data'.$microTime . $i;
					open (FILE, '>' . $outfile . '.csv') or next;
					print FILE "$wkRecBuf\n";
					close (FILE);
					if( $make_zip ne "1" ){ $ret{'result'} = 0; }
					last;
				};
				if( $make_zip eq "1" ){
			    $filePath = $outfile . '.csv';
					$zipPath = $outfile . '.zip';
			    #暗号化zip(-e)の作成
			    $rets = system("$ZIP_CMD -P $zipPwd -e -D $zipPath $filePath");
					#zip file作成成功
			    if( $rets == 0 ){
						unlink $filePath;
						$ret{'result'} = 1;
						$ret{'target'} = $zipPath;
					}
				} else {
					$ret{'result'} = 1;
					$ret{'target'} = $filePath;
				}
			}
		} else {
			$ret{'message'} = '※データの作成範囲の日付を正しく入力して下さい。';
		}
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"result":"'.$ret{'result'}.'","message":"'. $ret{'message'} .'","target":"'. $ret{'target'} .'"}';
		exit(0);
	}	case 'del' {
		if( defined($varPOST{'target'}) ){
			if( unlink($varPOST{'target'}) == 0){
				$rets = 0;
			} else {
				$rets = 1;
			}
			print "Content-Type: text/html; charset=UTF-8\n\n"; 
			print '{"result":"'.$rets.'"}';
		}
		exit(0);
	}	case 'pub' {
		$rets = 0;
		while( 1 ){
			open (FILE, '>' . $inifile) or next;
			while( ($wkKey, $wkValue) = each(%settings) ){
				print FILE "$wkKey,$wkValue\n";
			}
			close (FILE);
			$rets = 1;
			last;
		};
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"result":"'.$rets.'","public":"'.$publicForm.'"}';
		exit(0);
	}	else {
	}
}

print "Content-Type: text/html; charset=UTF-8\n\n";
print << "EOF";
<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8" />
<meta name="description" content="大同キャスティングス" />
<meta name="keywords" content="大同キャスティングス" />

<title>エントリーフォーム｜大同キャスティングス</title>

<link rel="stylesheet" href="../css/html5-doctor-reset-stylesheet.css" />
<link rel="stylesheet" href="../css/style.css" />
<link rel="stylesheet" href="../css/edata.css" />

<!-- jQuery,jQueryUI -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js" integrity="sha256-VazP97ZCwtekAsvgPBSUwPFKdrwD3unUfSGVYrahUqU=" crossorigin="anonymous"></script>
<link type="text/css" rel="stylesheet" href="https://code.jquery.com/ui/1.11.4/themes/excite-bike/jquery-ui.css" />

<!-- jQueryMobiscroll2.6 -->
<script src="../jquery/plugin/mobiscroll/js/mobiscroll.core.js" type="text/javascript"></script>
<script src="../jquery/plugin/mobiscroll/js/mobiscroll.datetime.js" type="text/javascript"></script>
<script src="../jquery/plugin/mobiscroll/js/mobiscroll.select.js" type="text/javascript"></script>
<script src="../jquery/plugin/mobiscroll/js/mobiscroll.jqm.js" type="text/javascript"></script>
<script src="../jquery/plugin/mobiscroll/js/mobiscroll.ios.js" type="text/javascript"></script>
<script src="../jquery/plugin/mobiscroll/js/mobiscroll.android.js" type="text/javascript"></script>
<script src="../jquery/plugin/mobiscroll/js/mobiscroll.android-ics.js" type="text/javascript"></script>
<script src="../jquery/plugin/mobiscroll/js/mobiscroll.wp.js" type="text/javascript"></script>
<script src="../jquery/plugin/mobiscroll/js/i18n/mobiscroll.i18n.ja.js" type="text/javascript"></script>
<link href="../jquery/plugin/mobiscroll/css/mobiscroll.core.css" rel="stylesheet" type="text/css" />
<link href="../jquery/plugin/mobiscroll/css/mobiscroll.jqm.css" rel="stylesheet" type="text/css" />
<link href="../jquery/plugin/mobiscroll/css/mobiscroll.android.css" rel="stylesheet" type="text/css" />
<link href="../jquery/plugin/mobiscroll/css/mobiscroll.android-ics.css" rel="stylesheet" type="text/css" />
<link href="../jquery/plugin/mobiscroll/css/mobiscroll.ios.css" rel="stylesheet" type="text/css" />
<link href="../jquery/plugin/mobiscroll/css/mobiscroll.sense-ui.css" rel="stylesheet" type="text/css" />
<link href="../jquery/plugin/mobiscroll/css/mobiscroll.wp.css" rel="stylesheet" type="text/css" />
<link href="../jquery/plugin/mobiscroll/css/mobiscroll.animation.css" rel="stylesheet" type="text/css" />

<!-- PerlがHereDocumentのJavascriptを誤認識してしまうので別ファイル化 -->
<script src="getcsv.js" type="text/javascript"></script>

<script language=javascript>
<!--
//-->
</script>

<style type="text/css">
<!--
/* reset.cssのvertical-align:bottom;指定がMobiscrollに悪影響を与えていた為 */
div.dw-persp * {
	vertical-align:top !important;
}

#buttons{
	margin: 20px auto 0;
	width:124px;
}
.text-notice {
	color:crimson;
	text-size:20px;
}
#msgDDel{
	display:none;
}

-->
</style>

</head>
<body>

<div id="header">
	<div id="header1">
		<img src="../images/logo.jpg" alt="大同キャスティングス" width="248" height="46">
	</div>
</div>

<div id="wp">
	<img src="../images/tag_entry.png" alt="エントリー" width="960" height="31">
	<div id="main">
		<div id="entryNew">
			<form name="frmCSV" id="frmCSV">
				<div id="dlButton">
					<div style="margin:10px 0px;">
						<span>データ日付(開始)&nbsp;&nbsp;&nbsp;&nbsp;</span>
						<input id="date_s" name="date_s" type="text" value="" class="dtpicker" /><br>
					</div>
					<div style="margin:10px 0px;">
						<span >データ日付(終了)&nbsp;&nbsp;&nbsp;&nbsp;</span>
						<input id="date_e" name="date_e" type="text" value="" class="dtpicker" /><br>
					</div>
					<button type="button" id="btnMake">csvデータ作成</button>
					<span id="dispMessage" class=""></span>
				</div>
				<div id="dlLink" style="display:none;">
					<input name="dlFile" id="dlFile" type="hidden" />
					<button type="button" id="btnDownload">DownLoad</button></a><br><br>
					<button type="button" id="btnDelete">データ消去</button><br>
					<span class="">※データはダウンロード完了後、消去して下さい。</span><br>
				</div>
				<div id="dlClose" style="display:none;">
					<span class="">
						※閉じるボタンをクリックするとウインドウを閉じます。(IEのみ)<br>
						　ブラウザを終了させて、処理を完了して下さい。<br>
					</span>
					<button type="button" id="btnClose">閉じる</button>
				</div>
			</form>
		</div>
		<div id="publicSetting">
			<h3>現在公開中の画面</h3>
			<span id="publicForm" class="text_pfs">$publicForm</span>
			<h3>公開画面の変更</h3>
			<form name="frmPublic" id="frmPublic">
				<input type="radio" name="pf" value="5" /><span class="text_pfs">新卒・プレエントリー・既卒採用受付</span><br>
				<input type="radio" name="pf" value="6" /><span class="text_pfs">既卒・プレエントリー受付</span><br>
				<input type="radio" name="pf" value="4" /><span class="text_pfs">新卒・プレエントリー受付</span><br>
				<input type="radio" name="pf" value="3" /><span class="text_pfs">新卒・既卒採用エントリー受付</span><br>
				<input type="radio" name="pf" value="7" /><span class="text_pfs">プレエントリーのみ受付</span><br>
				<input type="radio" name="pf" value="2" /><span class="text_pfs">新卒採用のみ受付</span><br>
				<input type="radio" name="pf" value="1" /><span class="text_pfs">既卒採用のみ受付</span><br>
				<input type="radio" name="pf" value="0" /><span class="text_pfs">エントリー受付なし</span><br>
				<button type="button" id="btnPublic">公開画面を変更する</button></a><br><br>
			</form>
		</div>
		<div id="publicSetting">
			<h3>データの削除</h3>
			<span class="text-notice">※サーバーに保存されているデータを削除します。消した場合、復活は出来ませんので充分に注意して消して下さい!!</span>
			<form name="frmDDel" id="frmDDel">
				「削除」と入力して下さい：<input type="text" id="ddelText" name="ddelText" /><br>
				<input type="checkbox" id="ddel" name="ddel" />データを削除します!!<br>
				<button type="button" id="btnDDel" disabled="disabled">データを削除</button></a><br>
				<div id="msgDDel" class="text-notice">データの削除が完了しました。</div><br>
			</form>
		</div>
	</div>
</div>

<footer id="global_footer">
	<div id="global_footer_area">
		<p class="rc"><a href="http://www.daido.co.jp/">大同特殊鋼株式会社</a></p>
		<p id="copyright" class="lc"><small>Copyright © 大同キャスティングス All rights reserved.</small></p>
	</div>
</footer>

</body>
</html>
EOF

exit(0);
