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
my $indexType1 = "html/index1.html"; #既卒採用のみのHOME画面
my $indexType2 = "html/index2.html"; #新卒採用のみのHOME画面
my $indexType3 = "html/index3.html"; #新卒・既卒採用時のHOME画面
my $indexType4 = "html/index4.html"; #新卒・プレエントリー採用時のHOME画面
my $indexType5 = "html/index5.html"; #新卒・プレエントリー・既卒採用時のHOME画面
my $indexType6 = "html/index6.html"; #プレエントリー・既卒採用時のHOME画面
my $indexType7 = "html/index7.html"; #プレエントリーのみのHOME画面
my $homepage = 'closing.html'; #公開期間外の場合に表示する頁のURL

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
		#open (FILE, $indexType7) or print "Location: ".$homepage."\n\n";
		open (FILE, $indexType7) or $flg = 0;
		if( $flg == 0 ){
			print "Location: ".$homepage."\n\n"
		} else {
			print "Content-Type: text/html; charset=UTF-8\n\n";
			while (<FILE>) {
				print $_;
			}
		}
	} case 6 {
		#open (FILE, $indexType6) or print "Location: ".$homepage."\n\n";
		open (FILE, $indexType6) or $flg = 0;
		if( $flg == 0 ){
			print "Location: ".$homepage."\n\n"
		} else {
			print "Content-Type: text/html; charset=UTF-8\n\n";
			while (<FILE>) {
				print $_;
			}
		}
	} case 5 {
		#open (FILE, $indexType5) or print "Location: ".$homepage."\n\n";
		open (FILE, $indexType5) or $flg = 0;
		if( $flg == 0 ){
			print "Location: ".$homepage."\n\n"
		} else {
			print "Content-Type: text/html; charset=UTF-8\n\n";
			while (<FILE>) {
				print $_;
			}
		}
	} case 4 {
		#open (FILE, $indexType4) or print "Location: ".$homepage."\n\n";
		open (FILE, $indexType4) or $flg = 0;
		if( $flg == 0 ){
			print "Location: ".$homepage."\n\n"
		} else {
			print "Content-Type: text/html; charset=UTF-8\n\n";
			while (<FILE>) {
				print $_;
			}
		}
	} case 3 {
		#open (FILE, $indexType3) or print "Location: ".$homepage."\n\n";
		open (FILE, $indexType3) or $flg = 0;
		if( $flg == 0 ){
			print "Location: ".$homepage."\n\n"
		} else {
			print "Content-Type: text/html; charset=UTF-8\n\n";
			while (<FILE>) {
				print $_;
			}
		}
	} case 2 {
		open (FILE, $indexType2) or $flg = 0;
		if( $flg == 0 ){
			print "Location: ".$homepage."\n\n"
		} else {
			print "Content-Type: text/html; charset=UTF-8\n\n";
			while (<FILE>) {
				print $_;
			}
		}
	} case 1 {
		open (FILE, $indexType1) or $flg = 0;
		if( $flg == 0 ){
			print "Location: ".$homepage."\n\n"
		} else {
			print "Content-Type: text/html; charset=UTF-8\n\n";
			while (<FILE>) {
				print $_;
			}
		}
	} case 0 {
		print "Location: ".$homepage."\n\n";
	} else {
		print "Location: ".$homepage."\n\n";
	}
}

exit(0);
