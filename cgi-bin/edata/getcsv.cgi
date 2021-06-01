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

#変数定義 スコープ付き(my使用,環境依存)
my ($string,$value,$name,$pair);
my @pairs;
#POST値の初期化
my %varPOST = (
	'date_s' => '','' => '','date_e' => '','target' => ''
);
#GET値の初期化
my %varGET = ('proc' => '' );

my (@wkBuf,@fileNames);
my ($i,$j,$cnt,$outfile,$wkString,$fileHandle,$fileTime,$dateStart,$dateEnd);
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

switch ($varGET{'proc'}) {
	case 'make' {
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
					if( substr($arrayValue, 0, 4) ne 'data' ){
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

<!-- jQueryUI -->
<script type="text/javascript" src="../jquery/jquery-1.8.3.js"></script>
<script type="text/javascript" src="../jquery/ui/jquery-ui.min.js"></script>
<link type="text/css" rel="stylesheet" href="../jquery/themes/excite-bike/jquery-ui.css" />

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
			</div>
		</form>
	</div>
</div>

<footer id="global_footer">
	<div id="global_footer_area">
		<p class="rc"><a href="http://www.daido.co.jp/">大同特殊鋼株式会社</a></p>
		<p id="copyright" class="lc"><small>Copyright c 大同キャスティングス All rights reserved.</small></p>
	</div>
</footer>

</body>
</html>
EOF

exit(0);
