#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);
use strict;
use warnings;
#use Encode;
use Jcode;
use Time::HiRes qw/ gettimeofday /;
use Switch;
use Data::Dumper;	#zip化(暗号化)の際に使用
#文字コード設定,環境に依存
#use utf8;
#binmode(STDOUT, ":utf8");

#設定項目
my $dataYear = 2017; #データ年度
my $inifile = "edata/ini.csv"; #iniファイル(csv形式)の指定
my $homepage = 'closing.html'; #公開期間外の場合に表示する頁のURL
my $make_zip = '0'; #データのzip化の指定 1 => zip,0 => csv
my $zipPwd = '0d1ad'; #zip化の際のパスワード
my $mailSend = '1'; #メール送信の指定 1 => メール送信,0 => メール送信しない
my $textMail = '';
my $replyMail = '';
#my $addressMail = 'SAIYOU@d-cast.jp';
my $addressMail = 'it-t@redcube.jp';
my $nameMail = '株式会社大同キャスティングス';
my $textFile = './mail/entry.txt';
my $replyFile = './mail/reply.txt';

#my $publicDate_s = 20131105;	#この頁の公開期間(開始日付 ※yyyymmddの数値のみの形式で)
#my $publicDate_e = 20140930;	#この頁の公開期間(終了日付 ※yyyymmddの数値のみの形式で)

#設定項目 スマートフォン用メッセージID
my %spMsgId = (
	'namefamily' => 'namefamilyErr','namefirst' => 'namefirstErr','rubyfamily' => 'rubyfamilyErr','rubyfirst' => 'rubyfirstErr',
	'birthyear' => 'birthdayErr','birthmon' => 'birthdayErr','birthday' => 'birthdayErr','graduateyear' => 'graduateyearErr','graduatemon' => 'graduateyearErr',
	'schoolgrade' => 'schoolgradeErr','schoolkind' => 'schoolkindErr','schoolname' => 'schoolnameErr','schoolfaculty' => 'schoolfacultyErr','zip' => 'zipErr','emgzip' => 'emgzipErr','phone' => 'phoneErr','phonecell' => 'phonecellErr',
	'emgphone' => 'emgphoneErr','mailpc' => 'mailErr','mailcell' => 'mailcellErr'
);

if( $mailSend eq '1' ){
	open(IN, "<".$textFile);
	read(IN, $textMail, (-s "$textFile")); #ファイルの内容を一気に変数に読み込み
	close IN;
	open(IN, "<".$replyFile);
	read(IN, $replyMail, (-s "$replyFile")); #ファイルの内容を一気に変数に読み込み
	close IN;
}
my $preDisp = << 'EOF';
				<tr>
					<th colspan="2" class="line2"><hr></th>
					<td class="line3"><hr>
						<span class="cap2">※以下の項目の記載は自由です。<br>※3月1日以降、正式エントリーに移行致します。</span><br>
					</td>
				</tr>

EOF

#変数定義 スコープ付き(my使用,環境依存)
my ($string,$value,$name,$pair);
my @pairs;
#GET値の初期化
my %varGET = ('exp' => '');
#POST値の初期化
my %varPOST = (
	'mode' => '','namefamily' => '','namefirst' => '','rubyfamily' => '','rubyfirst' => '',
	'birthyear' => '','birthmon' => '','birthday' => '','mailpc' => '','mailcell' => '',
	'zip' => '','add' => '','phone' => '','phonecell' => '','emgclass' => '','emgzip' => '','emgadd' => '','emgphone' => '',
	'schoolgrade' => '','schoolname' => '','schoolfaculty' => '','schoolkind' => '','graduateyear' => '','graduatemon' => '',
	'license' => '','intro' => '','etc' => '','exp' => '','sp' => ''
);
#POST値(エスケープ)の初期化
my %escPOST = (
	'mode' => '','namefamily' => '','namefirst' => '','rubyfamily' => '','rubyfirst' => '',
	'birthyear' => '','birthmon' => '','birthday' => '','mailpc' => '','mailcell' => '',
	'zip' => '','add' => '','phone' => '','phonecell' => '','emgclass' => '','emgzip' => '','emgadd' => '','emgphone' => '',
	'schoolgrade' => '','schoolname' => '','schoolfaculty' => '','schoolkind' => '','graduateyear' => '','graduatemon' => '',
	'license' => '','intro' => '','etc' => '','exp' => '','sp' => ''
);
#POST値(サニタイズ)の初期化
my %sntPOST = (
	'mode' => '','namefamily' => '','namefirst' => '','rubyfamily' => '','rubyfirst' => '',
	'birthyear' => '','birthmon' => '','birthday' => '','mailpc' => '','mailcell' => '',
	'zip' => '','add' => '','phone' => '','phonecell' => '','emgclass' => '','emgzip' => '','emgadd' => '','emgphone' => '',
	'schoolgrade' => '','schoolname' => '','schoolfaculty' => '','schoolkind' => '','graduateyear' => '','graduatemon' => '',
	'license' => '','intro' => '','etc' => '','exp' => '','sp' => ''
);


#設定値の初期化
my %settings = (
	'ctrl' => '0'
);

my ($defBirthyear,$defBirthmon,$defBirthday);
my ($wkBuf,$defGraduateyear,$defGraduatemon);
my ($i,$j,$cnt,$outfile,$wkString,$wkKey,$wkValue,@wkItems);
my ($dispLicense,$dispIntro,$dispEtc);
my $debug = 0;
my $wkRecBuf = "";
my @idx = ('exp','namefamily','namefirst','rubyfamily','rubyfirst','birthyear','birthmon','birthday','mailpc','mailcell',
	'zip','add','phone','phonecell','emgzip','emgadd','emgphone','schoolgrade','schoolname','schoolfaculty','schoolkind',
	'graduateyear','graduatemon','license','intro','etc','dataYear','dataDate','sp');
my @jpidx = ('namefamily','namefirst','add','emgadd','schoolname','schoolfaculty','license','intro','etc');
my (%ret,%res,%mail,%retHash,$retjson);
my ($arrayKey, $arrayValue);
my ($dispAdd,$dispEmgclass,$dispEmgadd,$dispSchoolname,$dispSchoolfaculty);
my ($rets,$filePath,$zipPath);
my $ZIP_CMD = "/usr/bin/zip";
my $UNZIP_CMD = "/usr/bin/unzip";
my ($jsDisp,$jsDef,$btnimg,$btnimgh);
$jsDef = "";

#時間取得(micro秒単位)
my ($epocSec, $microSec) = gettimeofday();
my ($sec,$min,$hour,$day,$mon,$year) = localtime($epocSec);
my $microTime = sprintf("%d%02d%02d%02d%02d%02d%06d",$year + 1900,$mon + 1,$day,$hour,$min,$sec,$microSec);
my $nowDate = sprintf("%d%02d%02d",$year + 1900,$mon + 1,$day);
my $nowDateS = sprintf("%d",$year + 1900).'/'.sprintf("%02d",$mon + 1).'/'.sprintf("%02d",$day).' '.sprintf("%02d",$hour).':'.sprintf("%02d",$min).':'.sprintf("%02d",$sec);

#公開期間の判定
#if( $nowDate < $publicDate_s || $nowDate > $publicDate_e ){
#	#print "HTTP/1.1 302 Found\n\n"; 
#	print "Location: ".$homepage."\n\n"; 
#	exit(0);
#}

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

#データ年度設定
$varPOST{'dataYear'} = $dataYear;
#データ作成年月
$varPOST{'dataDate'} = $nowDateS;

#UTF8 全角チルダ,全角ハイフン問題対応,サニタイジング&エスケープ
$cnt = @jpidx;
for( $j = 0; $j < $cnt ; $j++ ) {
	$varPOST{$jpidx[$j]} = exchangech($varPOST{$jpidx[$j]});
}
$cnt = @idx;
for( $j = 0; $j < $cnt ; $j++ ) {
	$escPOST{$idx[$j]} = $varPOST{$idx[$j]};
	$escPOST{$idx[$j]} =~ s/\"/&quot;/g;
	$sntPOST{$idx[$j]} = $varPOST{$idx[$j]};
	$sntPOST{$idx[$j]} =~ s/</&lt;/g;
	$sntPOST{$idx[$j]} =~ s/>/&gt;/g;
}

#if( $varPOST{'mode'} eq 'conf' || $varPOST{'mode'} eq 'regist' ){
#	#新卒,既卒の区分チェック
#	if( $varPOST{'exp'} ne '1' && $varPOST{'exp'} ne '0' ){
#		#新卒,既卒の区分の入力がない場合、全て既卒扱い
#		$varPOST{'exp'} = 1;
#	}
#}
if( $varPOST{'exp'} eq '1' || $varPOST{'exp'} eq '0' ){
	$preDisp = '';
}

#%varPOST = %varGET;
switch ($varPOST{'mode'}) {
	case 'namefamily' {
		%ret = &chk_namefamily($varPOST{'namefamily'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		#print '{"'.$varPOST{'mode'}.'":"'.$ret{'namefamily'}.'"}';
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'namefamily'}.'","debug":"'.$debug.'"}';
		exit(0);
	} case 'namefirst' {
		%ret = &chk_namefirst($varPOST{'namefirst'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'namefirst'}.'"}';
		exit(0);
	} case 'rubyfamily' {
		%ret = &chk_rubyfamily($varPOST{'rubyfamily'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'rubyfamily'}.'"}';
		exit(0);
	} case 'rubyfirst' {
		%ret = &chk_rubyfirst($varPOST{'rubyfirst'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'rubyfirst'}.'"}';
		exit(0);
	} case 'birthyear' {
		%ret = &chk_birthyear($varPOST{'birthyear'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'birthyear'}.'"}';
		exit(0);
	} case 'birthmon' {
		%ret = &chk_birthmon($varPOST{'birthmon'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'birthmon'}.'"}';
		exit(0);
	} case 'birthday' {
		%ret = &chk_birthday($varPOST{'birthday'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'birthday'}.'"}';
		exit(0);
	} case 'graduateyear' {
		%ret = &chk_graduateyear($varPOST{'graduateyear'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'graduateyear'}.'"}';
		exit(0);
	} case 'graduatemon' {
		%ret = &chk_graduatemon($varPOST{'graduatemon'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'graduatemon'}.'"}';
		exit(0);
	} case 'schoolname' {
		%ret = &chk_schoolname($varPOST{'schoolname'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'schoolname'}.'"}';
		exit(0);
	} case 'schoolfaculty' {
		%ret = &chk_schoolfaculty($varPOST{'schoolfaculty'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'schoolfaculty'}.'"}';
		exit(0);
	} case 'zip' {
		%ret = &chk_zip($varPOST{'zip'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'zip'}.'"}';
		exit(0);
	} case 'emgzip' {
		%ret = &chk_emgzip($varPOST{'emgzip'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'emgzip'}.'"}';
		exit(0);
	} case 'add' {
		%ret = &chk_add($varPOST{'add'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'add'}.'"}';
		exit(0);
	} case 'phone' {
		if( $varPOST{'sp'} eq '1' ){
			%ret = &chk_nphone($varPOST{'phone'});
			print "Content-Type: text/html; charset=UTF-8\n\n"; 
			print '{"'.$varPOST{'mode'}.'":"'.$ret{'phone'}.'"}';
		} else {
			%ret = &chk_phone($varPOST{'phone'});
			print "Content-Type: text/html; charset=UTF-8\n\n"; 
			print '{"'.$varPOST{'mode'}.'":"'.$ret{'phone'}.'"}';
		}
		exit(0);
	} case 'phonecell' {
		if( $varPOST{'sp'} eq '1' ){
			%ret = &chk_nphonecell($varPOST{'phonecell'});
			print "Content-Type: text/html; charset=UTF-8\n\n"; 
			print '{"'.$varPOST{'mode'}.'":"'.$ret{'phonecell'}.'"}';
		} else {
			%ret = &chk_phonecell($varPOST{'phonecell'});
			print "Content-Type: text/html; charset=UTF-8\n\n"; 
			print '{"'.$varPOST{'mode'}.'":"'.$ret{'phonecell'}.'"}';
		}
		exit(0);
	} case 'emgphone' {
		if( $varPOST{'sp'} eq '1' ){
			%ret = &chk_nemgphone($varPOST{'emgphone'});
			print "Content-Type: text/html; charset=UTF-8\n\n"; 
			print '{"'.$varPOST{'mode'}.'":"'.$ret{'emgphone'}.'"}';
		} else {
			%ret = &chk_emgphone($varPOST{'emgphone'});
			print "Content-Type: text/html; charset=UTF-8\n\n"; 
			print '{"'.$varPOST{'mode'}.'":"'.$ret{'emgphone'}.'"}';
		}
		exit(0);
	} case 'mailpc' {
		%ret = &chk_mailpc($varPOST{'mailpc'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'mailpc'}.'"}';
		exit(0);
	} case 'mailcell' {
		%ret = &chk_mailcell($varPOST{'mailcell'});
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print '{"'.$varPOST{'mode'}.'":"'.$ret{'mailcell'}.'"}';
		exit(0);
	}	else {
	}
}
#各項目チェック処理(AJAX)の場合は、ここまでで確実に終了になります。

#全入力チェック
my $chk = 0;
%ret = ();
%res = &chk_namefamily($varPOST{'namefamily'});
%ret = (%ret ,%res);
%res = &chk_namefirst($varPOST{'namefirst'});
%ret = (%ret ,%res);
%res = &chk_rubyfamily($varPOST{'rubyfamily'});
%ret = (%ret ,%res);
%res = &chk_rubyfirst($varPOST{'rubyfirst'});
%ret = (%ret ,%res);
%res = &chk_birthyear($varPOST{'birthyear'});
%ret = (%ret ,%res);
%res = &chk_birthmon($varPOST{'birthmon'});
%ret = (%ret ,%res);
%res = &chk_birthday($varPOST{'birthday'});
%ret = (%ret ,%res);
%res = &chk_graduateyear($varPOST{'graduateyear'});
%ret = (%ret ,%res);
%res = &chk_graduatemon($varPOST{'graduatemon'});
%ret = (%ret ,%res);
%res = &chk_schoolname($varPOST{'schoolname'});
%ret = (%ret ,%res);
%res = &chk_schoolfaculty($varPOST{'schoolfaculty'});
%ret = (%ret ,%res);
%res = &chk_schoolgrade($varPOST{'schoolgrade'});
%ret = (%ret ,%res);
%res = &chk_schoolkind($varPOST{'schoolkind'});
%ret = (%ret ,%res);
%res = &chk_zip($varPOST{'zip'});
%ret = (%ret ,%res);
%res = &chk_emgzip($varPOST{'emgzip'});
%ret = (%ret ,%res);
%res = &chk_add($varPOST{'add'});
%ret = (%ret ,%res);
if( $varPOST{'sp'} eq '1' ){
	%res = &chk_nphone($varPOST{'phone'});
	%ret = (%ret ,%res);
	%res = &chk_nphonecell($varPOST{'phonecell'});
	%ret = (%ret ,%res);
	%res = &chk_nemgphone($varPOST{'emgphone'});
	%ret = (%ret ,%res);
} else {
	%res = &chk_phone($varPOST{'phone'});
	%ret = (%ret ,%res);
	%res = &chk_phonecell($varPOST{'phonecell'});
	%ret = (%ret ,%res);
	%res = &chk_emgphone($varPOST{'emgphone'});
	%ret = (%ret ,%res);
}
%res = &chk_mailpc($varPOST{'mailpc'});
%ret = (%ret ,%res);
%res = &chk_mailcell($varPOST{'mailcell'});
%ret = (%ret ,%res);

$chk = 1;
#メールエラー表示用処理
my $chkX = 0;
while( ($arrayKey, $arrayValue) = each %ret ){
	if( $arrayKey ne "defBirthyear" && $arrayKey ne "defBirthmon" && $arrayKey ne "defBirthday" && $arrayKey ne "defGraduateyear" && $arrayKey ne "defGraduatemon" ){
		if( $arrayValue ne "1" ){
			$chk = 0;
			if( $varPOST{'mode'} eq "conf" ){
				if( $arrayKey eq 'mailpc' || $arrayKey eq 'mailcell' ){
					$jsDef = $jsDef . "\$('#mailErr').css('display','inline');\n"
				} else {
					$jsDef = $jsDef . "\$('#" . $arrayKey . "Err').css('display','inline');\n"
				}
			}
		}
	}
}

#バグの原因不明のため、入力値の保全
$sntPOST{'mailcellX'} = $sntPOST{'mailcell'};

#複合条件他のチェック
if( $varPOST{'mode'} eq "conf" ){
	if( $varPOST{'zip'} eq "" ){
		$chk = 0;
		$jsDef = $jsDef . "\$('#zipErr').css('display','inline');\n"
	}
	if( $varPOST{'phone'} eq "" && $varPOST{'phonecell'} eq "" ){
		$chk = 0;
		$jsDef = $jsDef . "\$('#phoneErr').css('display','inline');\n"
	}
	if( $varPOST{'mailpc'} eq "" && $varPOST{'mailcell'} eq "" ){
		$chk = 0;
		$jsDef = $jsDef . "\$('#mailErr').css('display','inline');\n"
	}
	if( $varPOST{'emgclass'} ne "1" && ( $varPOST{'emgzip'} eq "" || $varPOST{'emgadd'} eq "" || $varPOST{'emgphone'} eq "" )){
		$chk = 0;
		$jsDef = $jsDef . "\$('#emgclassErr').css('display','inline');\n";
	}
} elsif( $varPOST{'mode'} eq "sc" || $varPOST{'mode'} eq "sm" ){
	#戻り値用項目を初期化
	%retHash = ('result' => '0' ); #戻り値用項目初期化
	#複合条件-スマホ用処理
	if( $varPOST{'zip'} eq "" ){
		$chk = 0;
		%res = ( 'zipErr' =>  '' );
		%retHash = (%retHash ,%res);
	}
	if( $varPOST{'phone'} eq "" && $varPOST{'phonecell'} eq "" ){
		$chk = 0;
		%res = ( 'phoneinputErr' =>  '' );
		%retHash = (%retHash ,%res);
	}
	if( $varPOST{'mailpc'} eq "" && $varPOST{'mailcell'} eq "" ){
		$chk = 0;
		%res = ( 'mailinputErr' =>  '' );
		%retHash = (%retHash ,%res);
	}
	if( $varPOST{'emgclass'} ne "1" && ( $varPOST{'emgzip'} eq "" || $varPOST{'emgadd'} eq "" || $varPOST{'emgphone'} eq "" )){
		$chk = 0;
		%res = ( 'emgclassErr' =>  '' );
		%retHash = (%retHash ,%res);
	}
	#エラーが有ればメッセージ表示用のIDを返す
	if( $chk == 0 ){
		while( ($arrayKey, $arrayValue) = each %ret ){
			if( $arrayValue ne '1' ){
				%res = ( $spMsgId{$arrayKey} =>  '' );
				%retHash = (%retHash ,%res);
			}
		}
		delete $retHash{''};
		$retjson = '{';
		while( ($arrayKey, $arrayValue) = each %retHash ){
			$retjson .= '"' . $arrayKey . '":"' . $arrayValue.'",';
		}
		$retjson = substr( $retjson, 0, -1 ) . '}';
		print "Content-Type: text/html; charset=UTF-8\n\n"; 
		print $retjson;
		exit(0);
	} else {
		#エラーが無ければ入力された値を適正な形に変換して返す
		if( $varPOST{'mode'} eq "sc" ){
			$res{'result'} = '1';
			%sntPOST = (%sntPOST ,%res);
			$sntPOST{'license'} =~ s/\n/<br>/g;
			$sntPOST{'license'} =~ s/[\r|\n]//g;
			$sntPOST{'intro'} =~ s/\n/<br>/g;
			$sntPOST{'intro'} =~ s/[\r|\n]//g;
			$sntPOST{'etc'} =~ s/\n/<br>/g;
			$sntPOST{'etc'} =~ s/[\r|\n]//g;
			$sntPOST{'mailcell'} = $sntPOST{'mailcellX'}; #原因不明のバグ対応の為、保全した入力値を戻す
			delete $sntPOST{''};
			$retjson = '{';
			while( ($arrayKey, $arrayValue) = each %sntPOST ){
				$retjson = $retjson . '"' . $arrayKey . '":"' . $arrayValue.'",';
			}
			$retjson = substr( $retjson, 0, -1 ) . '}';
			print "Content-Type: text/html; charset=UTF-8\n\n"; 
			print $retjson;
			exit(0);
		} else {
		#エラーが無ければメール送信
			$wkString = '#####emgcall#####';
			if( $varPOST{'emgclass'} eq "1" ){
				$varPOST{'emgadd'} = '';
				$varPOST{'emgzip'} = '';
				$varPOST{'emgphone'} = '';
				$textMail =~ s/$wkString/上記と同じ/;
				$replyMail =~ s/$wkString/上記と同じ/;
			} else {
				$textMail =~ s/$wkString/ /;
				$replyMail =~ s/$wkString/ /;
			}
			$cnt = @idx;
			for( $j = 0; $j < $cnt ; $j++ ) {
				$wkString = $varPOST{$idx[$j]};
				$wkString =~ s/\\\"/\"\"/g;
				$wkRecBuf = $wkRecBuf.'"'. $wkString .'",';
				$wkString = '#####' . $idx[$j] . '#####';
				$textMail =~ s/$wkString/$varPOST{$idx[$j]}/;
				$replyMail =~ s/$wkString/$varPOST{$idx[$j]}/;
			}
			$wkString = '#####expl#####';
			if( $varPOST{'exp'} eq '1' ){
				$textMail =~ s/$wkString/既卒/;
				$replyMail =~ s/$wkString/既卒/;
			} elsif ( $varPOST{'exp'} eq '2' ){
				$textMail =~ s/$wkString/プレエントリー/;
				$replyMail =~ s/$wkString/プレプレエントリー/;
			} else {
				$textMail =~ s/$wkString/新卒/;
				$replyMail =~ s/$wkString/新卒/;
			}
			$wkRecBuf = substr($wkRecBuf,0,-1);
			chdir('edata');
			$i = 0;
			while( 1 ){
				$i = $i + 1;
				$outfile = $microTime . $i;
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
				}
			} else {
				$ret{'result'} = 1;
			}
			if( $mailSend eq '1' ){
				$mail{'from_name'}	= $varPOST{'namefamily'}." ".$varPOST{'namefirst'};
				if( $varPOST{'mailpc'} ne '' ){
					$mail{'from_mail'} = $varPOST{'mailpc'};
				} else {
					$mail{'from_mail'} = $varPOST{'mailcell'};
				}
				$mail{'to_mail'} = $addressMail;
				$mail{'to_name'} = $nameMail;
				$mail{'message'} = $textMail;
				$mail{'subject'}	= 'エントリーを受け付けました';
				$rets = &sendMail(%mail);
				$mail{'from_mail'} = $addressMail;
				$mail{'from_name'} = $nameMail;
				$mail{'to_name'}	= $varPOST{'namefamily'}." ".$varPOST{'namefirst'};
				if( $varPOST{'mailpc'} ne '' ){
					$mail{'to_mail'} = $varPOST{'mailpc'};
				} else {
					$mail{'to_mail'} = $varPOST{'mailcell'};
				}
				$mail{'message'} = $replyMail;
				$mail{'subject'}	= '【大同キャスティングス】エントリーを受け付けました';
				$rets = &sendMail(%mail);
			}
			print "Content-Type: text/html; charset=UTF-8\n\n";
			print "{\"result\":".$ret{'result'}."}";
			exit(0);
		}
	}
}

# <span id="namefamilyErr" class="msgErr">※姓が未入力もしくは入力内容に誤りがあります。<br></span>
# <span id="namefirstErr" class="msgErr">※名が未入力もしくは入力内容に誤りがあります。<br></span>
# <span id="rubyfamilyErr" class="msgErr">※せいが未入力もしくは入力内容に誤りがあります。<br></span>
# <span id="rubyfirstErr" class="msgErr">※めいが未入力もしくは入力内容に誤りがあります。<br></span>
# <span id="birthdayErr" class="msgErr">※生年月日を正しく選択して下さい。<br></span>
# <span id="mailinputErr" class="msgErr">※どちらかは必ず入力してください。</span><br>
# <span id="mailErr" class="msgErr">※メールアドレスを正しく入力して下さい。<br></span>
# <span id="mailcellErr" class="msgErr">※携帯メールアドレスを正しく入力して下さい。<br></span>
# <span id="zipErr" class="msgErr">※郵便番号が未入力もしくは入力内容に誤りがあります。<br></span>
# <span id="addErr" class="msgErr">※住所を正しく入力して下さい。<br></span>
# <span id="phonecellErr" class="msgErr">※携帯電話番号を正しく入力して下さい。<br></span>
# <span id="phoneinputErr" class="msgErr">※電話番号のどちらかは必ず入力してください。</span><br>
# <span id="phoneErr" class="msgErr">※電話番号を正しく入力して下さい。<br></span>
# <span id="emgclassErr" class="msgErr">※休暇中の連絡先を正しく入力して下さい。<br></span>
# <span id="emgzipErr" class="msgErr">※郵便番号が未入力もしくは入力内容に誤りがあります。<br></span>
# <span id="emgaddErr" class="msgErr">※住所を正しく入力して下さい。<br></span>
# <span id="emgphoneErr" class="msgErr">※電話番号を正しく入力して下さい。<br></span>
# <span id="schoolgradeErr" class="msgErr">※学校種別を正しく選択して下さい。<br></span>
# <span id="schoolnameErr" class="msgErr">※学校名を正しく入力して下さい。<br></span>
# <span id="schoolfacultyErr" class="msgErr">※学部・学科名を正しく入力して下さい。<br></span>
# <span id="schoolkindErr" class="msgErr">※理系・文系を正しく選択して下さい。<br></span>
# <span id="graduateyearErr" class="msgErr">※卒業予定年月を正しく選択して下さい。<br></span>

#%varPOST = %varGET;
switch ($varPOST{'mode'}) {
	case 'regist' {
		$ret{'result'} = 0;
		if( $chk == 1 ){
			$wkString = '#####emgcall#####';
			if( $varPOST{'emgclass'} eq "1" ){
				$varPOST{'emgadd'} = '';
				$varPOST{'emgzip'} = '';
				$varPOST{'emgphone'} = '';
				$textMail =~ s/$wkString/上記と同じ/;
				$replyMail =~ s/$wkString/上記と同じ/;
			} else {
				$textMail =~ s/$wkString/ /;
				$replyMail =~ s/$wkString/ /;
			}
			$cnt = @idx;
			for( $j = 0; $j < $cnt ; $j++ ) {
				$wkString = $varPOST{$idx[$j]};
				$wkString =~ s/\\\"/\"\"/g;
				$wkRecBuf = $wkRecBuf.'"'. $wkString .'",';
				$wkString = '#####' . $idx[$j] . '#####';
				$textMail =~ s/$wkString/$varPOST{$idx[$j]}/;
				$replyMail =~ s/$wkString/$varPOST{$idx[$j]}/;
			}
			$wkString = '#####expl#####';
			if( $varPOST{'exp'} eq '1' ){
				$textMail =~ s/$wkString/既卒/;
				$replyMail =~ s/$wkString/既卒/;
			} elsif ( $varPOST{'exp'} eq '2' ){
				$textMail =~ s/$wkString/プレエントリー/;
				$replyMail =~ s/$wkString/プレプレエントリー/;
			} else {
				$textMail =~ s/$wkString/新卒/;
				$replyMail =~ s/$wkString/新卒/;
			}
			$wkRecBuf = substr($wkRecBuf,0,-1);
			chdir('edata');
			$i = 0;
			while( 1 ){
				$i = $i + 1;
				$outfile = $microTime . $i;
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
				}
			} else {
				$ret{'result'} = 1;
			}
			if( $mailSend eq '1' ){
				$mail{'from_name'}	= $varPOST{'namefamily'}." ".$varPOST{'namefirst'};
				if( $varPOST{'mailpc'} ne '' ){
					$mail{'from_mail'} = $varPOST{'mailpc'};
				} else {
					$mail{'from_mail'} = $varPOST{'mailcell'};
				}
				$mail{'to_mail'} = $addressMail;
				$mail{'to_name'} = $nameMail;
				$mail{'message'} = $textMail;
				$mail{'subject'}	= 'エントリーを受け付けました';
				$rets = &sendMail(%mail);
				$mail{'from_mail'} = $addressMail;
				$mail{'from_name'} = $nameMail;
				$mail{'to_name'}	= $varPOST{'namefamily'}." ".$varPOST{'namefirst'};
				if( $varPOST{'mailpc'} ne '' ){
					$mail{'to_mail'} = $varPOST{'mailpc'};
				} else {
					$mail{'to_mail'} = $varPOST{'mailcell'};
				}
				$mail{'message'} = $replyMail;
				$mail{'subject'}	= '【大同キャスティングス】エントリーを受け付けました';
				$rets = &sendMail(%mail);
			}
			print "Content-Type: text/html; charset=UTF-8\n\n";
			print "{\"result\":".$ret{'result'}."}";
			exit(0);
		} else {
			$varPOST{'mode'} = "conf";
		}
	}	case 'conf' {
		if( $chk == 1 ){
			$btnimg = "b_send.jpg";
			$btnimgh = "b_send_ov.jpg";
			$varPOST{'mode'} = "regist";
		} else {
			$btnimg = "b_check.jpg";
			$btnimgh = "b_check_ov.jpg";
			$varPOST{'mode'} = "conf";
		}
	}	case 'revision' {
		$chk = 0;
		$btnimg = "b_check.jpg";
		$btnimgh = "b_check_ov.jpg";
		$varPOST{'mode'} = "conf";
		if( $varGET{'exp'} eq '1' ){
			$varPOST{'exp'} = 1;
		} elsif( $varGET{'exp'} eq '2' ){
			$varPOST{'exp'} = 2;
		} else  {
			$varPOST{'exp'} = 0;
		}
	}	else {
		$btnimg = "b_check.jpg";
		$btnimgh = "b_check_ov.jpg";
		$varPOST{'mode'} = "conf";
		if( $varGET{'exp'} eq '1' ){
			$varPOST{'exp'} = 1;
		} elsif( $varGET{'exp'} eq '2' ){
			$varPOST{'exp'} = 2;
		} else  {
			$varPOST{'exp'} = 0;
		}
	}
}

#これ以降の処理は全てページ表示される場合になります。(メール送信やチェック処理ではここに到達以前に終了する仕様)
#設定による入力可否
switch( $settings{'ctrl'} ){
	case 2 {
		if( $varPOST{'exp'} ne '0' ){
			print "Location: ".$homepage."\n\n";
			exit(0);
		}
	} case 1 {
		if( $varPOST{'exp'} ne '1' ){
			print "Location: ".$homepage."\n\n";
			exit(0);
		}
	} case 7 {
		if( $varPOST{'exp'} ne '2' ){
			print "Location: ".$homepage."\n\n";
			exit(0);
		}
	} case 3 {
		if( $varPOST{'exp'} ne '0' && $varPOST{'exp'} ne '1' ){
			print "Location: ".$homepage."\n\n";
			exit(0);
		}
	} case 4 {
		if( $varPOST{'exp'} ne '0' && $varPOST{'exp'} ne '2' ){
			print "Location: ".$homepage."\n\n";
			exit(0);
		}
	} case 6 {
		if( $varPOST{'exp'} ne '1' && $varPOST{'exp'} ne '2' ){
			print "Location: ".$homepage."\n\n";
			exit(0);
		}
	} case 5 {
		if( $varPOST{'exp'} ne '0' && $varPOST{'exp'} ne '1' && $varPOST{'exp'} ne '2' ){
			print "Location: ".$homepage."\n\n";
			exit(0);
		}
	} case 0 {
		print "Location: ".$homepage."\n\n";
		exit(0);
	} else {
		print "Location: ".$homepage."\n\n";
		exit(0);
	}
}

#select等の初期値を設定
$defBirthyear = $ret{'defBirthyear'};
$defBirthmon = $ret{'defBirthmon'};
$defBirthday = $ret{'defBirthday'};
$defGraduateyear = $ret{'defGraduateyear'};
$defGraduatemon = $ret{'defGraduatemon'};
#textareaに対応した改行処理
$dispLicense = $sntPOST{'license'};
$dispLicense =~ s/\n/<br>/g;
$dispIntro = $sntPOST{'intro'};
$dispIntro =~ s/\n/<br>/g;
$dispEtc = $sntPOST{'etc'};
$dispEtc =~ s/\n/<br>/g;
#Radio,Checkbox初期値処理
if( $varPOST{'emgclass'} eq "1" ){
	$dispEmgclass = "現住所と同じ";
	$jsDef = $jsDef . '$("#emgclass").attr("checked",true);'."\n";
} else {
	$dispEmgclass = "";
	$jsDef = $jsDef . '$("#emgclass").attr("checked",false);'."\n";
}
$jsDef =  $jsDef . "\$(\"input[name='schoolgrade']\").val(['" . $varPOST{'schoolgrade'} . "']);\n";
$jsDef =  $jsDef . "\$(\"input[name='schoolkind']\").val(['" . $varPOST{'schoolkind'} . "']);\n";

#入力欄他表示
if( $chk == 1 ){
$jsDisp = << 'EOF';
	$(".txt-confirm").css('display','inline');
	$(".inputDiv").css('display','none');
	$(".input").css('display','none');
	$(".cap").css('display','none');
	$(".caps").css('display','none');
	$("#btnRevision").css('display','inline');

EOF
} else {
$jsDisp = << 'EOF';
	$(".txt-confirm").css('display','none');
	$(".inputDiv").css('display','block');
	$(".input").css('display','inline');

EOF
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

<link rel="stylesheet" href="css/html5-doctor-reset-stylesheet.css" />
<link rel="stylesheet" href="css/style.css" />

<!-- jQuery,jQueryUI -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js" integrity="sha256-VazP97ZCwtekAsvgPBSUwPFKdrwD3unUfSGVYrahUqU=" crossorigin="anonymous"></script>
<link type="text/css" rel="stylesheet" href="https://code.jquery.com/ui/1.11.4/themes/excite-bike/jquery-ui.css" />
<!--
<script type="text/javascript" src="jquery/jquery-1.8.3.js"></script>
<script type="text/javascript" src="jquery/ui/jquery-ui.min.js"></script>
<link type="text/css" rel="stylesheet" href="jquery/themes/excite-bike/jquery-ui.css" />
-->

<!-- ZIPCloudAPI 郵便番号⇒住所 jQueryPlugin-->
<script type="text/javascript" src="jquery/plugin/zipcloud/jquery.zipcloud.js"></script>
<link rel="stylesheet" href="jquery/plugin/zipcloud/jquery.zipcloud.css" />

<script language=javascript>
<!--
\$(function(){

	preload([
		'images/b_send_gray.jpg',
		'images/b_send_ov.jpg',
		'images/b_send.jpg',
		'images/b_revision_ov.jpg',
		'images/b_revision.jpg',
		'images/b_check_ov.jpg',
		'images/b_check.jpg'
	]);

	\$("#btnSubmit").hover(function(){
			this.src = 'images/$btnimgh';
	},function(){
			this.src = 'images/$btnimg';
	});

	\$("#btnRevision").hover(function(){
			this.src = 'images/b_revision_ov.jpg';
	},function(){
			this.src = 'images/b_revision.jpg';
	});

	\$("#btnSubmit").on('click', function(){
		if( \$("#mode").val() == 'regist' ){
			\$(this).unbind("hover");
			this.src = 'images/b_send_gray.jpg';
			var postdata = \$("#frmEntry").serialize();
			\$.ajax({
				async: false,
				type: "POST",
				url: 'entryform.cgi',
				data: postdata,
				dataType: 'json',
				success: function(msg){
					if (msg.result == 1) {
						location.href = "result.html";
					} else {
						\$("#btnSubmit").attr("disabled", "disabled");
						\$(".txt-confirm").css('display','none');
						\$(".inputDiv").css('display','none');
						\$(".input").attr('type','hidden');
					}
				},
				error: function(a,b,c){
				}
			});
		} else {
			\$("#frmEntry").submit();
		}
	});

	\$("#btnRevision").on('click', function(){
		\$("#mode").val('revision');
		\$("#frmEntry").submit();
	});

	\$("#zip").zipcloud({
		zip:'#zip',
		addtype:'1',
		add1:"#add",
		type:'hover',
		disp:'#add'
	});
	\$("#emgzip").zipcloud({
		zip:'#emgzip',
		addtype:'1',
		add1:"#emgadd",
		type:'hover',
		disp:'#emgadd'
	});

	\$(".async_chk").on("blur",function(){
		var checkurl = \$(this).attr('checkurl');
		var msglocate = \$(this).attr('msg');
		var checkmode = \$(this).attr('checkmode');
		var postdata = \$(this).attr('name') + "=" + encodeURIComponent(\$(this).val()) + "&mode=" + checkmode;
		\$.ajax({
			type: "POST",
			url: checkurl,
			cache: false,
			data: postdata,
			dataType: 'json',
			success: function(msg){
				if( msg[checkmode] == 1){
					\$('#' + msglocate ).css('display','none');
				} else {
					\$('#' + msglocate ).css('display','inline');
				}
			}
		})
	});
	\$(".async_chkc").on("change",function(){
		var checkurl = \$(this).attr('checkurl');
		var msglocate = \$(this).attr('msg');
		var checkmode = \$(this).attr('checkmode');
		var postdata = \$(this).attr('name') + "=" + encodeURIComponent(\$(this).val()) + "&mode=" + checkmode;
		\$.ajax({
			type: "POST",
			url: checkurl,
			data: postdata,
			dataType: 'json',
			success: function(msg){
				if( msg[checkmode] == 1){
					\$('#' + msglocate ).css('display','none');
				} else {
					\$('#' + msglocate ).css('display','inline');
				}
			}
		})
	});
	\$(".clear_chk").on("focus",function(){
		var msglocate = \$(this).attr('msg');
		\$("#" + msglocate).css('display','none');
	});

$jsDef
$jsDisp
});

function preload(arrayOfImages) {
	\$(arrayOfImages).each(function(){
		\$('<img/>')[0].src = this;
	});
}

//-->
</script>

<style type="text/css">
<!--
.msgErr {
	display:none;
	color:crimson;
	font-size:12px;
}
#btnRevision {
	display:none;
}
-->
</style>

</head>
<body>

<div id="header">
	<div id="header1">
		<a href="http://www.d-cast.jp"><img src="images/logo.jpg" alt="大同キャスティングス" width="248" height="46"></a>
	</div>
</div>

<div id="wp">
	<img src="images/tag_entry.png" alt="エントリー" width="960" height="31">
	<div id="main">
		<div id="entry">
			<form method="post" action="entryform.cgi" id="frmEntry">
			<input type="hidden" id="mode" name="mode" value="$varPOST{'mode'}" />
			<input type="hidden" name="exp" value="$varPOST{'exp'}" />
			<table class="tblEntryForm">
				<tr>
					<th class="first"><ul><li>氏名&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td class="first">
						<span class="caps">姓&nbsp;&nbsp;</span>
						<span class="txt-confirm">$sntPOST{'namefamily'}</span>
						<input type="text" style="width:130px;" name="namefamily" value="$escPOST{'namefamily'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="namefamily" msg="namefamilyErr" />&nbsp;&nbsp;&nbsp;&nbsp;
						<span class="caps">名&nbsp;&nbsp;</span>
						<span class="txt-confirm">$sntPOST{'namefirst'}</span>
						<input class="input async_chk clear_chk" type="text" style="width:130px;" name="namefirst" value="$escPOST{'namefirst'}" checkurl="entryform.cgi" checkmode="namefirst" msg="namefirstErr" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap"><br>※旧字は使用はお控え下さい。(JIS第1・2水準漢字をご使用下さい)</span><br>
						<span id="namefamilyErr" class="msgErr">※姓が未入力もしくは入力内容に誤りがあります。<br></span>
						<span id="namefirstErr" class="msgErr">※名が未入力もしくは入力内容に誤りがあります。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th><ul><li>ふりがな&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td>
						<span class="caps">せい&nbsp;&nbsp;</span>
						<span class="txt-confirm">$sntPOST{'rubyfamily'}</span>
						<input type="text" style="width:130px;" name="rubyfamily" value="$escPOST{'rubyfamily'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="rubyfamily" msg="rubyfamilyErr" />&nbsp;&nbsp;&nbsp;&nbsp;
						<span class="caps">めい&nbsp;&nbsp;</span>
						<span class="txt-confirm">$sntPOST{'rubyfirst'}</span>
						<input type="text" style="width:130px;" name="rubyfirst" value="$escPOST{'rubyfirst'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="rubyfirst" msg="rubyfirstErr" /><br>
						<span id="rubyfamilyErr" class="msgErr">※せいが未入力もしくは入力内容に誤りがあります。<br></span>
						<span id="rubyfirstErr" class="msgErr">※めいが未入力もしくは入力内容に誤りがあります。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th><ul><li>生年月日&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td>
						<span class="txt-confirm">$sntPOST{'birthyear'}</span>
						<select name="birthyear" id="birthyear" class="input async_chkc" checkurl="entryform.cgi" checkmode="birthyear" msg="birthdayErr">
							$defBirthyear
							<option value="2000">2000</option><option value="1999">1999</option>
							<option value="1998">1998</option><option value="1997">1997</option>
							<option value="1996">1996</option><option value="1995">1995</option>
							<option value="1994">1994</option><option value="1993">1993</option>
							<option value="1992">1992</option><option value="1991">1991</option>
							<option value="1990">1990</option><option value="1989">1989</option>
							<option value="1988">1988</option><option value="1987">1987</option>
							<option value="1986">1986</option><option value="1985">1985</option>
							<option value="1984">1984</option><option value="1983">1983</option>
							<option value="1982">1982</option><option value="1981">1981</option>
							<option value="1980">1980</option><option value="1979">1979</option>
							<option value="1978">1978</option><option value="1977">1977</option>
							<option value="1976">1976</option><option value="1975">1975</option>
							<option value="1974">1974</option><option value="1973">1973</option>
							<option value="1972">1972</option><option value="1971">1971</option>
							<option value="1970">1970</option><option value="1969">1969</option>
							<option value="1968">1968</option><option value="1967">1967</option>
							<option value="1966">1966</option><option value="1965">1965</option>
							<option value="1964">1964</option><option value="1963">1963</option>
							<option value="1962">1962</option><option value="1961">1961</option>
							<option value="1960">1960</option>
						</select>
						&nbsp;年&nbsp;&nbsp;
						<span class="txt-confirm">$sntPOST{'birthmon'}</span>
						<select name="birthmon" id="brithmon" class="input async_chkc" checkurl="entryform.cgi" checkmode="birthmon" msg="birthdayErr">
							$defBirthmon
							<option value="1">1</option><option value="2">2</option><option value="3">3</option>
							<option value="4">4</option><option value="5">5</option><option value="6">6</option>
							<option value="7">7</option><option value="8">8</option><option value="9">9</option>
							<option value="10">10</option><option value="11">11</option><option value="12">12</option>
						</select>&nbsp;月&nbsp;&nbsp;
						<span class="txt-confirm">$sntPOST{'birthday'}</span>
						<select name="birthday" id="brithday" class="input async_chkc" checkurl="entryform.cgi" checkmode="birthday" msg="birthdayErr">
							$defBirthday
							<option value="1">1</option><option value="2">2</option><option value="3">3</option>
							<option value="4">4</option><option value="5">5</option><option value="6">6</option>
							<option value="7">7</option><option value="8">8</option><option value="9">9</option>
							<option value="10">10</option><option value="11">11</option><option value="12">12</option>
							<option value="13">13</option><option value="14">14</option><option value="15">15</option>
							<option value="16">16</option><option value="17">17</option><option value="18">18</option>
							<option value="19">19</option><option value="20">20</option><option value="21">21</option>
							<option value="22">22</option><option value="23">23</option><option value="24">24</option>
							<option value="25">25</option><option value="26">26</option><option value="27">27</option>
							<option value="28">28</option><option value="29" class="monfeb">29</option><option value="30" class="monfebleap">30</option>
							<option value="31" class="monshort">31</option>
						</select>&nbsp;日<br>
						<span id="birthdayErr" class="msgErr">※生年月日を正しく選択して下さい。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="2"><ul><li>メールアドレス&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">PC</th>
					<td>
						<span class="txt-confirm">$sntPOST{'mailpc'}<br></span>
						<input type="text" style="width:150px;" name="mailpc" value="$escPOST{'mailpc'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="mailpc" msg="mailErr"/>
					</td>
				</tr>
				<tr>
				<th  class="cl2">携帯・スマホ</th>
					<td>
						<span class="txt-confirm">$sntPOST{'mailcell'}<br></span>
						<input type="text" style="width:150px;" name="mailcell" value="$escPOST{'mailcell'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="mailcell" msg="mailErr" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※どちらかは必ず入力してください。</span><br>
						<span id="mailErr" class="msgErr">※メールアドレスを正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="4"><ul><li>現住所&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">郵便番号</th>
					<td>
						<span class="txt-confirm">$sntPOST{'zip'}<br></span>
						<input id="zip" type="text" name="zip" value="$escPOST{'zip'}" class="input clear_chk" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※郵便番号は(-)をいれずに入力して下さい。(例:4550022)</span><br>
						<span id="zipErr" class="msgErr">※郵便番号が未入力もしくは入力内容に誤りがあります。<br></span>
					</td>
				</tr>
				<tr>
				<th  class="cl2">住所</th>
					<td>
						<span class="txt-confirm">$sntPOST{'add'}<br></span>
						<input id="add" type="text" name="add" value="$escPOST{'add'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="add" msg="addErr" /><br>
						<span id="addErr" class="msgErr">※住所を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">携帯電話番号</th>
					<td>
						<span class="txt-confirm">$sntPOST{'phonecell'}<br></span>
						<input id="phonecell" type="text" name="phonecell" value="$escPOST{'phonecell'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="phonecell" msg="phonecellErr" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※携帯,電話番号は(-)をいれて入力して下さい。(例:052-691-5191)</span><br>
						<span id="phonecellErr" class="msgErr">※携帯電話番号を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">自宅電話番号</th>
					<td>
						<span class="txt-confirm">$sntPOST{'phone'}<br></span>
						<input id="phone" type="text" name="phone" value="$escPOST{'phone'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="phone" msg="phoneErr" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※電話番号のどちらかは必ず入力してください。</span><br>
						<span id="phoneErr" class="msgErr">※電話番号を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="4"><ul><li>休暇中の連絡先&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td>
						<span class="txt-confirm"></span>
						$dispEmgclass<input class="input" type="checkbox" name="emgclass" id="emgclass" value="1"><span class="caps">&nbsp;現住所と同じ</span>
						<span id="emgclassErr" class="msgErr">※休暇中の連絡先を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">郵便番号</th>
					<td>
						<span class="txt-confirm">$sntPOST{'emgzip'}<br></span>
						<input id="emgzip" type="text" name="emgzip" value="$escPOST{'emgzip'}" class="input clear_chk" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※郵便番号は(-)をいれずに入力して下さい。(例:4550022)</span><br>
						<span id="emgzipErr" class="msgErr">※郵便番号が未入力もしくは入力内容に誤りがあります。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">住所</th>
					<td>
						<span class="txt-confirm">$sntPOST{'emgadd'}<br></span>
						<input id="emgadd" type="text" name="emgadd" value="$escPOST{'emgadd'}" class="input" /><br>
						<span id="emgaddErr" class="msgErr">※住所を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">電話番号</th>
					<td>
						<span class="txt-confirm">$sntPOST{'emgphone'}<br></span>
						<input type="text" name="emgphone" value="$escPOST{'emgphone'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="emgphone" msg="emgphoneErr" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※電話番号は(-)をいれて入力して下さい。(例:052-691-5191)</span><br>
						<span id="emgphoneErr" class="msgErr">※電話番号を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="5"><ul><li>学校情報&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">学校種別</th>
					<td>
						<span class="txt-confirm">$sntPOST{'schoolgrade'}<br></span>
						<div class="inputDiv">
							<input type="radio" name="schoolgrade" class="schoolgrade" value="大学">&nbsp;大学&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" value="大学院（修士）">&nbsp;大学院（修士）&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" value="短大">&nbsp;短大&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" value="専門学校">&nbsp;専門学校&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" value="高専">&nbsp;高専&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" value="高校">&nbsp;高校&nbsp;<br>
							<span id="schoolgradeErr" class="msgErr">※学校種別を正しく選択して下さい。<br></span>
						</div>
					</td>
				</tr>
				<tr>
					<th  class="cl2">学校名</th>
					<td>
						<span class="txt-confirm">$sntPOST{'schoolname'}<br></span>
						<input type="text" name="schoolname" value="$escPOST{'schoolname'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="schoolname" msg="schoolnameErr" /><br>
						<span id="schoolnameErr" class="msgErr">※学校名を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">学部・学科名</th>
					<td>
						<span class="txt-confirm">$sntPOST{'schoolfaculty'}<br></span>
						<input type="text" name="schoolfaculty" value="$escPOST{'schoolfaculty'}" class="input async_chk clear_chk" checkurl="entryform.cgi" checkmode="schoolfaculty" msg="schoolfacultyErr" /><br>
						<span id="schoolfacultyErr" class="msgErr">※学部・学科名を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">文理区分</th>
					<td>
						<span class="txt-confirm">$sntPOST{'schoolkind'}<br></span>
						<div class="inputDiv">
							<input type="radio" name="schoolkind" class="schoolkind" value="文系">&nbsp;文系&nbsp;
							<input type="radio" name="schoolkind" class="schoolkind" value="理系">&nbsp;理系&nbsp;<br>
							<span id="schoolkindErr" class="msgErr">※理系・文系を正しく選択して下さい。<br></span>
						</div>
					</td>
				</tr>
				<tr>
					<th  class="cl2">卒業予定年月</th>
					<td>
						<span class="txt-confirm">$sntPOST{'graduateyear'}</span>
						<select name="graduateyear" id="graduateyear" class="input async_chkc" checkurl="entryform.cgi" checkmode="graduateyear" msg="graduateyearErr">
							$defGraduateyear
							<option value="2013">2013</option><option value="2014">2014</option><option value="2015">2015</option>
							<option value="2016">2016</option><option value="2017">2017</option><option value="2018">2018</option>
							<option value="2019">2019</option><option value="2020">2020</option><option value="2021">2021</option>
							<option value="2022">2022</option><option value="2023">2023</option>
						</select>
						&nbsp;年&nbsp;&nbsp;
						<span class="txt-confirm">$sntPOST{'graduatemon'}</span>
						<select name="graduatemon" id="graduatemon" class="input async_chkc" checkurl="entryform.cgi" checkmode="graduatemon" msg="graduateyearErr">
							$defGraduatemon
							<option value="1">1</option><option value="2">2</option><option value="3">3</option>
							<option value="4">4</option><option value="5">5</option><option value="6">6</option>
							<option value="7">7</option><option value="8">8</option><option value="9">9</option>
							<option value="10">10</option><option value="11">11</option><option value="12">12</option>
						</select>&nbsp;月&nbsp;&nbsp;<br>
						<span id="graduateyearErr" class="msgErr">※卒業予定年月を正しく選択して下さい。<br></span>
					</td>
				</tr>
$preDisp
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th>資格・経験</th>
					<th class="cl2"></th>
					<td>
						<span class="txt-confirm">$dispLicense</span>
						<div class="inputDiv">
							<textarea style="width:550px;" name="license" rows="8">$sntPOST{'license'}</textarea>&nbsp;&nbsp;&nbsp;&nbsp;<br><span class="cap">※TOEIC等資格、留学やサークル活動など</span>
						</div>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th>自己紹介</th>
					<th  class="cl2"></th>
					<td>
						<span class="txt-confirm">$dispIntro</span>
						<div class="inputDiv">
							<textarea class="input" style="width:550px;" name="intro" rows="8">$sntPOST{'intro'}</textarea>&nbsp;&nbsp;&nbsp;&nbsp;<br><span class="cap">※趣味・特技、誰にも負けないこと、アルバイト経験など</span>
						</div>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th class="last">その他</th>
					<th  class="cl2 last"></th>
					<td class="last">
						<span class="txt-confirm">$dispEtc</span>
						<div class="inputDiv">
							<textarea class="input" style="width:550px;" name="etc" rows="8">$sntPOST{'etc'}</textarea>&nbsp;&nbsp;&nbsp;&nbsp;<br>
						</div>
					</td>
				</tr>
			</table></form>
		</div>

		<div id="button" class="entry">
			<input class="ibutton" id="btnRevision" type="image" src="images/b_revision.jpg" style="cursor:pointer;" value="内容を修正する">
			<input class="ibutton" id="btnSubmit" type="image" src="images/$btnimg" style="cursor:pointer;" value="送信する">
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

#UTF8 全角チルダ,全角ハイフン問題対応
sub exchangech {
	my $chg = $_[0];
	$chg =~ s/\xef\xbc\x8d/\xe2\x88\x92/g;	#全角ハイフン
	$chg =~ s/\xef\xbd\x9e/\xe3\x80\x9c/g;	#全角チルダ
	return $chg;
}

#subroutine 入力項目チェック
sub chk_namefamily {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	my @jpchar;
	my ($char,$cchar);
	$ret{'namefamily'} = 0;
	if( defined($inp) ){
		$chk =~ s/[a-zA-Z0-9ぁ-ゖむゝ-ヾ々一-龠]{1,30}/x/; #漢字等全部の設定。ExcelCSV(shiftJIS)への対応を考えると不適切
		if( $chk eq "x" ) {
			$ret{'namefamily'} = 1;
		}
	}
	return %ret;
}
sub chk_namefirst {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'namefirst'} = 0;
	if( defined($inp) ){
		$chk =~ s/[a-zA-Z0-9ぁ-ゖむゝ-ヾ々一-龠]{1,30}/x/;
		if( $chk eq "x" ) {
			$ret{'namefirst'} = 1;
		}
	}
	return %ret;
}
sub chk_rubyfamily {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'rubyfamily'} = 0;
	if( defined($inp) ){
		$chk =~ s/[a-zA-Z0-9ぁ-ゖむゝ-ヾ]{1,30}/x/;
		if( $chk eq "x" ) {
			$ret{'rubyfamily'} = 1;
		}
	}
	return %ret;
}
sub chk_rubyfirst {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'rubyfirst'} = 0;
	if( defined($inp) ){
		$chk =~ s/[a-zA-Z0-9ぁ-ゖむゝ-ヾ]{1,30}/x/;
		if( $chk eq "x" ) {
			$ret{'rubyfirst'} = 1;
		}
	}
	return %ret;
}

sub chk_birthyear {
	my %ret;
	my $wkBuf;
	my $inp = $_[0];
	$ret{'birthyear'} = 0;
	$ret{'defBirthyear'} = '<option value="西暦">西暦</option>';
	if( defined($inp) ){
		if( $inp =~ /^[0-9]+$/ ){
			$wkBuf = $inp + 0;
			if( $wkBuf >= 1960 && $wkBuf <= 2000 ){
				$ret{'birthyear'} = 1;
				$ret{'defBirthyear'} = '<option value="'.$inp.'">'.$inp.'</option>';
			}
		}
	}
	return %ret;
}
sub chk_birthmon {
	my %ret;
	my $wkBuf;
	my $inp = $_[0];
	$ret{'birthmon'} = 0;
	$ret{'defBirthmon'} = '<option value=""></option>';
	if( defined($inp) ){
		if( $inp =~ /^[0-9]+$/ ){
			$wkBuf = $inp + 0;
			if( $wkBuf >= 1 && $wkBuf <= 12 ){
				$ret{'birthmon'} = 1;
				$ret{'defBirthmon'} = '<option value="'.$inp.'">'.$inp.'</option>';
			}
		}
	}
	return %ret;
}
sub chk_birthday {
	my %ret;
	my $wkBuf;
	my $inp = $_[0];
	$ret{'birthday'} = 0;
	$ret{'defBirthday'} = '<option value=""></option>';
	if( defined($inp) ){
		if( $inp =~ /^[0-9]+$/ ){
			$wkBuf = $inp + 0;
			if( $wkBuf >= 1 && $wkBuf <= 31 ){
				$ret{'birthday'} = 1;
				$ret{'defBirthday'} = '<option value="'.$inp.'">'.$inp.'</option>';
			}
		}
	}
	return %ret;
}

sub chk_schoolname {
	my %ret;
	my $inp = $_[0];
	$ret{'schoolname'} = 0;
	if( defined($inp) && $inp ne "" ){
		$ret{'schoolname'} = 1;
	}
	return %ret;
}
sub chk_schoolfaculty {
	my %ret;
	my $inp = $_[0];
	$ret{'schoolfaculty'} = 0;
	if( defined($inp) && $inp ne "" ){
		$ret{'schoolfaculty'} = 1;
	}
	$ret{'schoolfaculty'} = 1; #入力必須から除外
	return %ret;
}
sub chk_schoolgrade {
	my %ret;
	my $inp = $_[0];
	$ret{'schoolgrade'} = 0;
	if( $inp eq "大学" || $inp eq "大学院（修士）" || $inp eq "大学院（博士）" || $inp eq "高専" || $inp eq "高校" || $inp eq "短大" || $inp eq "専門学校" ){
		$ret{'schoolgrade'} = 1;
	}
	return %ret;
}
sub chk_schoolkind {
	my %ret;
	my $inp = $_[0];
	$ret{'schoolkind'} = 0;
	if( $inp eq "理系" || $inp eq "文系" ){
		$ret{'schoolkind'} = 1;
	}
	return %ret;
}

sub chk_graduateyear {
	my %ret;
	my $wkBuf;
	my $inp = $_[0];
	$ret{'graduateyear'} = 0;
	$ret{'defGraduateyear'} = '<option value="西暦">西暦</option>';
	if( defined($inp) ){
		if( $inp =~ /^[0-9]+$/ ){
			$wkBuf = $inp + 0;
			if( $wkBuf >= 2013 && $wkBuf <= 2023 ){
				$ret{'graduateyear'} = 1;
				$ret{'defGraduateyear'} = '<option value="'.$inp.'">'.$inp.'</option>';
			}
		}
	}
	return %ret;
}
sub chk_graduatemon {
	my %ret;
	my $wkBuf;
	my $inp = $_[0];
	$ret{'graduatemon'} = 0;
	$ret{'defGraduatemon'} = '<option value=""></option>';
	if( defined($inp) ){
		if( $inp =~ /^[0-9]+$/ ){
			$wkBuf = $inp + 0;
			if( $wkBuf >= 1 && $wkBuf <= 12 ){
				$ret{'graduatemon'} = 1;
				$ret{'defGraduatemon'} = '<option value="'.$inp.'">'.$inp.'</option>';
			}
		}
	}
	return %ret;
}

sub chk_add {
	my %ret;
	my $inp = $_[0];
	$ret{'add'} = 0;
	if( defined($inp) && $inp ne "" ){
		$ret{'add'} = 1;
	}
	return %ret;
}

sub chk_zip {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'zip'} = 0;
	if( defined($inp) ){
		$chk =~ s/[0-9]{7}/x/;
		if( $chk eq "x" || $inp eq "" ) {
			$ret{'zip'} = 1;
		}
	} else {
		$ret{'zip'} = 1;
	}
	return %ret;
}
sub chk_emgzip {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'emgzip'} = 0;
	if( defined($inp) ){
		$chk =~ s/[0-9]{7}/x/;
		if( $chk eq "x" || $inp eq "" ) {
			$ret{'emgzip'} = 1;
		}
	} else {
		$ret{'emgzip'} = 1;
	}
	return %ret;
}

sub chk_phone {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'phone'} = 0;
	if( defined($inp) ){
		$chk =~ s/0[0-9]{1,4}-[0-9]{1,4}-[0-9]{4,5}/x/;
		if( $chk eq "x" || $inp eq "" ) {
			$ret{'phone'} = 1;
		}
	} else {
		$ret{'phone'} = 1;
	}
	return %ret;
}
sub chk_phonecell {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'phonecell'} = 0;
	if( defined($inp) ){
		$chk =~ s/0[0-9]{1,4}-[0-9]{1,4}-[0-9]{4,5}/x/;
		if( $chk eq "x" || $inp eq "" ) {
			$ret{'phonecell'} = 1;
		}
	} else {
		$ret{'phonecell'} = 1;
	}
	return %ret;
}
sub chk_emgphone {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'emgphone'} = 0;
	if( defined($inp) ){
		$chk =~ s/0[0-9]{1,4}-[0-9]{1,4}-[0-9]{4,5}/x/;
		if( $chk eq "x" || $inp eq "" ) {
			$ret{'emgphone'} = 1;
		}
	} else {
		$ret{'emgphone'} = 1;
	}
	return %ret;
}

sub chk_nphone {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'phone'} = 0;
	if( defined($inp) ){
		$chk =~ s/0[0-9]{8,11}/x/;
		if( $chk eq "x" || $inp eq "" ) {
			$ret{'phone'} = 1;
		}
	} else {
		$ret{'phone'} = 1;
	}
	return %ret;
}
sub chk_nphonecell {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'phonecell'} = 0;
	if( defined($inp) ){
		$chk =~ s/0[0-9]{8,11}/x/;
		if( $chk eq "x" || $inp eq "" ) {
			$ret{'phonecell'} = 1;
		}
	} else {
		$ret{'phonecell'} = 1;
	}
	return %ret;
}
sub chk_nemgphone {
	my %ret;
	my $inp = $_[0];
	my $chk = $_[0];
	$ret{'emgphone'} = 0;
	if( defined($inp) ){
		$chk =~ s/0[0-9]{8,11}/x/;
		if( $chk eq "x" || $inp eq "" ) {
			$ret{'emgphone'} = 1;
		}
	} else {
		$ret{'emgphone'} = 1;
	}
	return %ret;
}

sub chk_mailpc {
	my %ret;
	my $inp = $_[0];
	$ret{'mailpc'} = 0;
	if( $inp eq "" ){
		$ret{'mailpc'} = 1;
	} elsif( defined($inp) ){
		$ret{'mailpc'} = &mailaddress_chk($inp);
	} else {
		$ret{'mailpc'} = 1;
	}
	return %ret;
}
sub chk_mailcell {
	my %ret;
	my $inp = $_[0];
	$ret{'mailcell'} = 0;
	if( $inp eq "" ){
		$ret{'mailcell'} = 1;
	} elsif( defined($inp) ){
		$ret{'mailcell'} = &mailaddress_chk($inp);
	} else {
		$ret{'mailcell'} = 1;
	}
	return %ret;
}

#正しいメールアドレスか判定する
sub mailaddress_chk {
	my $email = $_[0];
	my $esc         = '\\\\';
	my $Period      = '\.';
	my $space       = '\040';
	my $tab         = '\t';
	my $OpenBR      = '\[';
	my $CloseBR     = '\]';
	my $OpenParen   = '\(';
	my $CloseParen  = '\)';
	my $NonASCII    = '\x80-\xff';
	my $ctrl        = '\000-\037';
	my $CRlist      = '\n\015';
	my $qtext       = qq/[^$esc$NonASCII$CRlist\"]/;
	my $dtext       = qq/[^$esc$NonASCII$CRlist$OpenBR$CloseBR]/;
	my $quoted_pair = qq<${esc}[^$NonASCII]>;
	my $ctext       = qq<[^$esc$NonASCII$CRlist()]>;
	my $Cnested     = qq<$OpenParen$ctext*(?:$quoted_pair$ctext*)*$CloseParen>;
	my $comment     = qq<$OpenParen$ctext*(?:(?:$quoted_pair|$Cnested)$ctext*)*$CloseParen>;
	my $X           = qq<[$space$tab]*(?:${comment}[$space$tab]*)*>;
	my $atom_char   = qq/[^($space)<>\@,;:\".$esc$OpenBR$CloseBR$ctrl$NonASCII]/;
	my $atom        = qq<$atom_char+(?!$atom_char)>;
	my $quoted_str  = qq<\"$qtext*(?:$quoted_pair$qtext*)*\">;
	my $word        = qq<(?:$atom|$quoted_str)>;
	my $domain_ref  = $atom;
	my $domain_lit  = qq<$OpenBR(?:$dtext|$quoted_pair)*$CloseBR>;
	my $sub_domain  = qq<(?:$domain_ref|$domain_lit)$X>;
	my $domain      = qq<$sub_domain(?:$Period$X$sub_domain)*>;
	my $route       = qq<\@$X$domain(?:,$X\@$X$domain)*:$X>;
	my $local_part  = qq<$word$X(?:$Period$X$word$X)*>;
	my $addr_spec   = qq<$local_part\@$X$domain>;
	my $route_addr  = qq[<$X(?:$route)?$addr_spec>];
	my $phrase_ctrl = '\000-\010\012-\037';
	my $phrase_char = qq/[^()<>\@,;:\".$esc$OpenBR$CloseBR$NonASCII$phrase_ctrl]/;
	my $phrase      = qq<$word$phrase_char*(?:(?:$comment|$quoted_str)$phrase_char*)*>;
	my $mailbox     = qq<$X(?:$addr_spec|$phrase$route_addr)>;
	if( $email =~ /^$mailbox$/o ){
		return 1;
	} else {
		return 0;
	}
}

sub sendMail {
	my $SENDMAIL = '/usr/lib/sendmail';
	my %arg = @_;	#引数のハッシュの受渡し
	my $to_name = $arg{'to_name'};
	my $to_mail = $arg{'to_mail'};
	my $from_name = $arg{'from_name'};
	my $from_mail = $arg{'from_mail'};
	my $subject = $arg{'subject'};
	my $msg = $arg{'message'};

	#if( ! $from_name or ! $from_mail or ! $subject or ! $msg ){
	if( ! $from_mail or ! $subject or ! $msg ){
		return 0;
  } else {
		#Encode(v5.8upper環境)
		#$from_name = decode('utf-8', $from_name);
		#$to_name = decode('utf-8', $to_name);
		#$msg = decode('utf-8', $msg);
    #$to_name = encode('MIME-Header-ISO_2022_JP', $to_name);
    #$from_name = encode('MIME-Header-ISO_2022_JP', $from_name);
    #$subject = encode('MIME-Header-ISO_2022_JP', $subject);
		#$msg = encode('jis', $msg);
		#Jcode.pm仕様
		$to_name = Jcode::convert( $to_name , "jis", "utf8" );
		$to_name = Jcode->new( $to_name, "jis")->mime_encode;
		$from_name = Jcode::convert( $from_name , "jis", "utf8" );
		$from_name = Jcode->new( $from_name, "jis")->mime_encode;
		$subject = Jcode::convert( $subject , "jis", "utf8" );
		$subject = Jcode->new( $subject, "jis")->mime_encode;
		$msg = Jcode::convert( $msg , "jis", "utf8" );
    open(SENDMAIL, "| $SENDMAIL -t") or 0;
    print SENDMAIL "To: $to_name <$to_mail>\n";
    print SENDMAIL "From: $from_name <$from_mail>\n";
    print SENDMAIL "Subject: $subject\n";
    print SENDMAIL "Mime-Version: 1.0\n";
    print SENDMAIL "Content-Type: text/plain; charset=ISO-2022-JP\n\n";
    print SENDMAIL $msg;
    close SENDMAIL;
  }
  return 1;
}

#指定文字数で分割する
sub strJfold{
	my $str = shift; #指定文字列
	my $byte = shift; #指定文字数
	my $j = new Jcode($str);
	my @result = ();
	foreach my $buff ( $j->jfold($byte) ){
		push(@result, $buff);
	}
	return(@result);
}

exit(0);
