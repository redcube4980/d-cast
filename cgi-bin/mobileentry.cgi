#!/usr/bin/perl
use strict;
use warnings;
#use Encode;
use Jcode;
use Time::HiRes qw/ gettimeofday /;
use Switch;
#文字コード設定,環境に依存
#use utf8;
#binmode(STDOUT, ":utf8");

#設定項目
my $inifile = "edata/ini.csv"; #iniファイル(csv形式)の指定
my $indexType1 = "html/mindex1.html"; #既卒採用のみのHOME画面
my $indexType2 = "html/mindex2.html"; #新卒採用のみのHOME画面
my $indexType3 = "html/mindex3.html"; #新卒・既卒採用時のHOME画面
my $indexType4 = "html/mindex4.html"; #新卒・プレエントリー採用時のHOME画面
my $indexType5 = "html/mindex5.html"; #新卒・プレエントリー・既卒採用時のHOME画面
my $indexType6 = "html/mindex6.html"; #プレエントリー・既卒採用時のHOME画面
my $indexType7 = "html/mindex7.html"; #プレエントリーのみのHOME画面
my $indexType0 = "html/closing.html"; #採用期間外画面

my $error = "<h3 class='notify'>※エラーが発生しました。お手数をお掛けしますが暫くしてから再度お試し下さい。</h3>\n"; #エラー

#変数定義 スコープ付き(my使用,環境依存)
my ($string,$value,$name,$pair);
my @pairs;
#GET値の初期化
my %varGET = ('exp' => '', 'mode' => '');
#GET値の受け渡し
$string = $ENV{'QUERY_STRING'};
@pairs = split(/&/,$string);
foreach $pair (@pairs){
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$varGET{$name} = $value;
}

my (@wkBuf,@wkItems);
my ($i,$wkKey,$wkValue,$fileHandle);
my $debug = 0;
my $wkRecBuf = "";

#設定値の初期化
my %settings = (
	'ctrl' => '0'
);

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

$flg = 1;
#公開中の画面を選択して表示
switch( $settings{'ctrl'} ){
	case 7 {
		if( $varGET{'mode'} eq 'jump' ){
			if( $varGET{'exp'} ne '2' ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"0"}';
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"1"}';
			}
			exit(0);
		} else {
			#open (FILE, $indexType7) or print "Location: ".$homepage."\n\n";
			open (FILE, $indexType7) or $flg = 0;
			if( $flg == 0 ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print $error;
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				while (<FILE>) {
					print $_;
				}
			}
		}
	} case 6 {
		if( $varGET{'mode'} eq 'jump' ){
			if( $varGET{'exp'} ne '1' && $varGET{'exp'} ne '2' ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"0"}';
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"1"}';
			}
			exit(0);
		} else {
			#open (FILE, $indexType6) or print "Location: ".$homepage."\n\n";
			open (FILE, $indexType6) or $flg = 0;
			if( $flg == 0 ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print $error;
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				while (<FILE>) {
					print $_;
				}
			}
		}
	} case 5 {
		if( $varGET{'mode'} eq 'jump' ){
			if( $varGET{'exp'} ne '0' && $varGET{'exp'} ne '1' && $varGET{'exp'} ne '2' ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"0"}';
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"1"}';
			}
			exit(0);
		} else {
			#open (FILE, $indexType5) or print "Location: ".$homepage."\n\n";
			open (FILE, $indexType5) or $flg = 0;
			if( $flg == 0 ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print $error;
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				while (<FILE>) {
					print $_;
				}
			}
		}
	} case 4 {
		if( $varGET{'mode'} eq 'jump' ){
			if( $varGET{'exp'} ne '0' && $varGET{'exp'} ne '2' ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"0"}';
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"1"}';
			}
			exit(0);
		} else {
			#open (FILE, $indexType4) or print "Location: ".$homepage."\n\n";
			open (FILE, $indexType4) or $flg = 0;
			if( $flg == 0 ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print $error;
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				while (<FILE>) {
					print $_;
				}
			}
		}
	} case 3 {
		if( $varGET{'mode'} eq 'jump' ){
			if( $varGET{'exp'} ne '0' && $varGET{'exp'} ne '1' ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"0"}';
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"1"}';
			}
			exit(0);
		} else {
			#open (FILE, $indexType3) or print "Location: ".$homepage."\n\n";
			open (FILE, $indexType3) or $flg = 0;
			if( $flg == 0 ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print $error;
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				while (<FILE>) {
					print $_;
				}
			}
		}
	} case 2 {
		if( $varGET{'mode'} eq 'jump' ){
			if( $varGET{'exp'} ne '0' ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"0"}';
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"1"}';
			}
			exit(0);
		} else {
			open (FILE, $indexType2) or $flg = 0;
			if( $flg == 0 ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print $error;
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				while (<FILE>) {
					print $_;
				}
			}
		}
	} case 1 {
		if( $varGET{'mode'} eq 'jump' ){
			if( $varGET{'exp'} ne '1' ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"0"}';
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"1"}';
			}
			exit(0);
		} else {
			open (FILE, $indexType1) or $flg = 0;
			if( $flg == 0 ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print $error;
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				while (<FILE>) {
					print $_;
				}
			}
		}
	} case 0 {
		if( $varGET{'mode'} eq 'jump' ){
			if( $varGET{'exp'} ne '1' ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print '{"result":"0"}';
			}
		} else {
			open (FILE, $indexType0) or $flg = 0;
			if( $flg == 0 ){
				print "Content-Type: text/html; charset=UTF-8\n\n";
				print $error;
			} else {
				print "Content-Type: text/html; charset=UTF-8\n\n";
				while (<FILE>) {
					print $_;
				}
			}
		}
		exit(0);
	} else {
		print "Content-Type: text/html; charset=UTF-8\n\n";
		print $error;
		exit(0);
	}
}

exit(0);
