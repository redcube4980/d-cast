/*===========================================================
copyright: (c)visual and echo japan
created: 2013.08.20
===========================================================*/

/*__ DEFAULT _______________________*/

//シーン番号
var sceneNum = 1;

//QA番号
var QAnum = 1;

//各シーンのコメント合計数
var txtC1t = 5;
var txtC2t = 4;
var txtC3t = 5;
var txtC4t = 4;
var txtC5t = 6;
var txtC6t = 4;
var txtC7t = 3;
var txtC8t = 2;
var txtC9t = 5;
var txtC10t = 7;
var txtC11t = 3;
var txtC12t = 3;

//各シーンのコメント現在番号
var txtC1n = 0;
var txtC2n = 0;
var txtC3n = 0;
var txtC4n = 0;
var txtC5n = 0;
var txtC6n = 0;
var txtC7n = 0;
var txtC8n = 0;
var txtC9n = 0;
var txtC10n = 0;
var txtC11n = 0;
var txtC12n = 0;

//プロフィールが完了したか
var profileFIX = 0;

//QA
var QATimer;

//次のコメント
var NextCommentTimer;

//AUTO
var autoOnOff = "ON";
var autoTimer;
var autoSpeed = 3000;

//早送り／戻し
var fastOnOff = "OFF";
var fastTimer;
var fastSpeed = 400;

//Comment Open Close
var commentOC = "open";
var commentOCTimer;

//不正解時コメント遅れ処理用
var ngCommentTimer;

//INDEXに戻るまでの時間
var indexTimer;

$(document).ready(function(){
	
	//背景キャラ
	$("#girlL2_01").hide();
	$("#girl2_01").hide();
	$("#girlL2_02").hide();
	$("#girl2_02").hide();
	$("#girlL3_01").hide();
	$("#girl3_01").hide();
	
	//QA
	closeQA();
	
	//プロフィール	
	$("#profile").hide();
	
	//コメント
	commentNext();
	
	//コメントエリアCLOSE
	$("#speech_close").hide();
	
	//オート設定
	$("#contentsArea #speech #speech_menu .menu01").addClass('autoON');
	autoCommentStart();
	
	//不正解時暗転
	$("#incorrect").hide();
	$("#incorrectBTN").hide();
	
	//ボタン設定
	btnSetting();
	
});

/*__ BTN SETTING _______________________*/
function btnSetting(){
	
	//コメントエリア オープンクローズ
	$("#contentsArea #speech #speech_menu .menu05").click(function(){commentOpenClose();});
	$("#contentsArea #speech_close").click(function(){commentOpenClose();});
	
	//オートボタン
	$("#contentsArea #speech #speech_menu .menu01").click(function(){
	  if(autoOnOff == "ON"){
		  autoOnOff = "OFF";
		  autoCommentStop();
		  $("#contentsArea #speech #speech_menu .menu01").removeClass('autoON');
	  }
	  else{
		  autoOnOff = "ON";
		  autoCommentStart();
		  $("#contentsArea #speech #speech_menu .menu01").addClass('autoON');
	  }
	});
	
	//早送りボタン
	$("#contentsArea #speech #speech_menu .menu02").mouseup(function(){
		fastOnOff="OFF";
		clearTimeout(fastTimer);
		if(autoOnOff=="ON"){autoCommentStart();}
		else{}
	}).mousedown(function(){
		fastOnOff="PREV";
		clearTimeout(fastTimer);
		clearTimeout(autoTimer);
		fastCommentPrev();
	});	
	$("#contentsArea #speech #speech_menu .menu03").mouseup(function(){
		fastOnOff="OFF";
		clearTimeout(fastTimer);
		if(autoOnOff=="ON"){autoCommentStart();}
		else{}
	}).mousedown(function(){
		fastOnOff="NEXT";
		clearTimeout(fastTimer);
		clearTimeout(autoTimer);
		fastCommentNext();
	});
	
	//スキップボタン
	$("#contentsArea #speech #speech_menu .menu04").click(function(){skipScene();});
	
	//コマ送りボタン
	$("#speech_L").click(function(){
		fastOnOff="OFF";	
		commentPrev();
	});
	$("#speech_R").click(function(){
		fastOnOff="OFF";
		if(sceneNum == 3 && txtC3n == txtC3t){//次の問題へ
			if(profileFIX==1){
				clearTimeout(autoTimer);
				clearTimeout(fastTimer);
				sceneNum = 5;
				txtC5n = 0;
				charaAnimation01Back();
				NextCommentTimer =setTimeout(function(){commentNext();},1000);
				profileFIX=0;
			}
			else{}
		}
		else if(sceneNum == 8 && txtC8n == txtC8t){//次の問題へ
			clearTimeout(autoTimer);
			clearTimeout(fastTimer);
			sceneNum = 9;
			txtC8n = 0;
			charaAnimation02B_Start();
			NextCommentTimer =setTimeout(function(){commentNext();},1600);
		}
		else if(sceneNum == 12 && txtC12n == txtC12t){//INDEXに戻る処理
			location.href="index.html";
			commentNext();
		}
		else{commentNext();}
	});
	
	//アンサーボタン
	$("#answer1_1").click(function(){ngStart();});
	$("#answer1_2").click(function(){seikaiStart();});
	$("#answer1_3").click(function(){ngStart();});
	$("#answer2_1").click(function(){ngStart();});
	$("#answer2_2").click(function(){ngStart();});
	$("#answer2_3").click(function(){seikaiStart();});
	$("#answer3_1").click(function(){ngStart();});
	$("#answer3_2").click(function(){ngStart();});
	$("#answer3_3").click(function(){seikaiStart();});
	
}

/*__ SKIP SCENE _______________________*/
function skipScene(){
	
	skipChara01 = $.cookie('d_cast_chara02_01');
	skipChara02 = $.cookie('d_cast_chara02_02');
	skipChara03 = $.cookie('d_cast_chara02_03');
	
	//背景キャラ
	if(skipChara01 == "clear"){
		$("#girlL1_01").hide();
		$("#girl1_01").hide();
		$("#girlL2_01").hide();
		$("#girl2_01").hide();
		$("#girlL2_02").hide();
		$("#girl2_02").hide();
		$("#girlL3_01").hide();
		$("#girl3_01").hide();
		$("#profile").hide();
		closeQA();
	}
	else{}
	
	if(skipChara03 == 'clear'){
		sceneNum = 12;
		txtC12n = 0;
		commentNext();
		$("#girlL3_01").show();
		$("#girl3_01").show();
	}
	else if(skipChara02 == 'clear'){
		sceneNum = 9;
		txtC9n = 0;
		commentNext();
		$("#girlL2_02").show();
		$("#girl2_02").show();
	}
	else if(skipChara01 == 'clear'){
		sceneNum = 5;
		txtC5n = 0;
		commentNext();
		$("#girlL1_01").show();
		$("#girl1_01").show();
	}
	else{}
	
}

/*__ QA AREA _______________________*/
function startQA(){
	
	clearTimeout(QATimer);
	
	$("#answer"+QAnum+"_1").show();
	$("#answer"+QAnum+"_2").show();
	$("#answer"+QAnum+"_3").show();
	$("#answer"+QAnum+"_1").css({marginLeft:50+"px"});
	$("#answer"+QAnum+"_2").css({marginLeft:-50+"px"});
	$("#answer"+QAnum+"_3").css({marginLeft:50+"px"});
	
	if(!jQuery.support.opacity){
		$("#answer"+QAnum+"_1").stop().animate({marginLeft:0},{duration:400});
		$("#answer"+QAnum+"_2").stop().animate({marginLeft:0},{duration:400});
		$("#answer"+QAnum+"_3").stop().animate({marginLeft:0},{duration:400});
	}
	else{
		$("#answer"+QAnum+"_1").css({opacity:0});
		$("#answer"+QAnum+"_2").css({opacity:0});
		$("#answer"+QAnum+"_3").css({opacity:0});
		$("#answer"+QAnum+"_1").stop().animate({marginLeft:0,opacity:1},{duration:400});
		$("#answer"+QAnum+"_2").stop().animate({marginLeft:0,opacity:1},{duration:400});
		$("#answer"+QAnum+"_3").stop().animate({marginLeft:0,opacity:1},{duration:400});
	}
	
}
function closeQA(){	
	for (i=1;i<=3;i++){
		$("#answer1_"+i).hide();
		$("#answer2_"+i).hide();
		$("#answer3_"+i).hide();
	}	
}

/*__ 不正解時暗転 _______________________*/
function NG_Animation(){
	
	clearTimeout(autoTimer);
	clearTimeout(fastTimer);
		
	$("#incorrect").hide();
	$("#incorrectBTN").show();
	
	$("#incorrect").stop().animate({height:'show'},{duration:800});
	$("#incorrect").delay(1000).animate({height:'hide'},{duration:600,complete:function(){$("#incorrectBTN").hide();}});
	
}

/*__ 1問目：アニメーション _______________________*/

function charaAnimation01Start(){
	
	profileFIX=0;
	
	$("#girl1_01").css({marginLeft:0});
	$("#girl1_01").stop().delay(600).animate({marginLeft:-80+"px"},{duration:1000});
	
	$("#profile").show();
	$("#profile").css({marginTop:60+"px"});
	if(!jQuery.support.opacity){
		$("#profile").stop().animate({marginTop:0},{duration:1000});
	}
	else{
		$("#profile").css({opacity:0});
		$("#profile").stop().delay(1500).animate({marginTop:0,opacity:1},{duration:1000});
	}
	
	$("#speech_name").stop().animate({opacity:1},{duration:2500,complete:function(){profileFIX=1;}});
	
}
function charaAnimation01Back(){	
	$("#girl1_01").stop().animate({marginLeft:0},{duration:800});
	$("#profile").hide();
}

/*__ 2問目：アニメーション _______________________*/

function charaAnimation02A_Start(){
	
	commentOC="open";
	commentOpenClose();
	
	commentOCTimer =setTimeout(function(){commentOC="close";commentOpenClose();},3000);
	
	clearTimeout(autoTimer);
	clearTimeout(fastTimer);
	
	$("#girl2_01").show();
	$("#girlL2_01").show();
	$("#girl2_01").css({marginLeft:80+"px"});
	
	if(!jQuery.support.opacity){
		$("#girl1_01").hide();
		$("#girlL1_01").hide();
		$("#girl2_01").stop().animate({marginLeft:0},{duration:1000});		
	}
	else{
		$('#girl1_01').stop().animate({marginLeft:-80+"px",opacity:0},{'duration':1000,'complete':function(){$("#girl1_01").hide();}});
		$('#girlL1_01').stop().animate({marginLeft:0,opacity:0},{'duration':1000,'complete':function(){$("#girlL1_01").hide();}});
		$("#girl2_01").css({opacity:0});
		$("#girlL2_01").css({opacity:0});
		$("#girl2_01").stop().animate({marginLeft:0,opacity:1},{duration:1600});
		$("#girlL2_01").stop().animate({marginLeft:0,opacity:1},{duration:1600});
	}	
	
}
function charaAnimation02A_Back(){
	commentOC="close";
	commentOpenClose();
		
	$("#girl1_01").show();
	$("#girlL1_01").show();
	$("#girl1_01").css({opacity:1});
	$("#girlL1_01").css({opacity:1});
	$("#girl1_01").css({marginLeft:0});
	$("#girl2_01").hide();
	$("#girlL2_01").hide();
}

function charaAnimation02B_Start(){	
	
	$("#girl2_02").show();
	$("#girlL2_02").show();
	$("#girl2_02").css({marginLeft:-80+"px"});
	
	if(!jQuery.support.opacity){
		$("#girl2_01").hide();
		$("#girlL2_01").hide();
		$("#girl2_02").stop().animate({marginLeft:0},{duration:1000});		
	}
	else{
		$('#girl2_01').stop().animate({marginLeft:80+"px",opacity:0},{'duration':1000,'complete':function(){$("#girl1_01").hide();}});
		$('#girlL2_01').stop().animate({marginLeft:0,opacity:0},{'duration':1000,'complete':function(){$("#girlL1_01").hide();}});
		$("#girl2_02").css({opacity:0});
		$("#girlL2_02").css({opacity:0});
		$("#girl2_02").stop().animate({marginLeft:0,opacity:1},{duration:1600});
		$("#girlL2_02").stop().animate({marginLeft:0,opacity:1},{duration:1600});
	}
	
}
function charaAnimation02B_Back(){
	commentOC="open";
	commentOpenClose();
	
	$("#girl2_01").show();
	$("#girlL2_01").show();
	$("#girl2_01").css({opacity:1});
	$("#girlL2_01").css({opacity:1});
	$("#girl2_01").css({marginLeft:0});
	$("#girl2_02").hide();
	$("#girlL2_02").hide();
}

/*__ 3問目：アニメーション _______________________*/

function charaAnimation03_Start(){
	
	commentOC="open";
	commentOpenClose();
	
	commentOCTimer =setTimeout(function(){commentOC="close";commentOpenClose();},3000);
	
	clearTimeout(autoTimer);
	clearTimeout(fastTimer);
	
	$("#girl3_01").show();
	$("#girlL3_01").show();
	$("#girl3_01").css({marginLeft:80+"px"});
	
	if(!jQuery.support.opacity){
		$("#girl2_02").hide();
		$("#girlL2_02").hide();
		$("#girl3_01").stop().animate({marginLeft:0},{duration:1000});		
	}
	else{
		$('#girl2_02').stop().animate({marginLeft:-80+"px",opacity:0},{'duration':1000,'complete':function(){$("#girl1_01").hide();}});
		$('#girlL2_02').stop().animate({marginLeft:0,opacity:0},{'duration':1000,'complete':function(){$("#girlL1_01").hide();}});
		$("#girl3_01").css({opacity:0});
		$("#girlL3_01").css({opacity:0});
		$("#girl3_01").stop().animate({marginLeft:0,opacity:1},{duration:1600});
		$("#girlL3_01").stop().animate({marginLeft:0,opacity:1},{duration:1600});
	}	
	
}
function charaAnimation03_Back(){
	commentOC="close";
	commentOpenClose();
		
	$("#girl2_02").show();
	$("#girlL2_02").show();
	$("#girl2_02").css({opacity:1});
	$("#girlL2_02").css({opacity:1});
	$("#girl2_02").css({marginLeft:0});
	$("#girl3_01").hide();
	$("#girlL3_01").hide();
}

/*__ 正解不正解 _______________________*/

function seikaiStart(){
	
	closeQA();
	
	//1問目
	if(sceneNum == 2){
		sceneNum = 3;
		txtC3n = 0;
		commentNext();		
	}
	
	//2問目
	if(sceneNum == 5){
		sceneNum = 6;
		txtC6n = 0;
		commentNext();		
	}
	
	//3問目
	if(sceneNum == 9){		
		sceneNum = 10;
		txtC10n = 0;
		commentNext();	
	}
	
}

function ngStart(){
	
	closeQA();
	
	//1問目
	if(sceneNum == 2){
		sceneNum = 4;
		txtC3n = 0;
		commentNext();		
	}
	
	//2問目
	if(sceneNum == 5){
		sceneNum = 7;
		txtC6n = 0;
		commentNext();		
	}
	
	//3問目
	if(sceneNum == 9){		
		sceneNum = 11;
		txtC10n = 0;
		commentNext();	
	}
	
}


/*__ COMMENT AREA _______________________*/

//オート処理
function autoCommentStart(){
	clearTimeout(autoTimer);
	if(sceneNum == 12 && txtC12n == 1){
		if(commentOC == "open"){autoTimer=setTimeout(function(){commentNext();autoCommentStart();},autoSpeed);}
		else{}
	}
	else{
		autoTimer=setTimeout(function(){commentNext();autoCommentStart();},autoSpeed);
	}
}
function autoCommentStop(){
	clearTimeout(autoTimer);
}

//早送り処理
function fastCommentPrev(){
	clearTimeout(fastTimer);
	clearTimeout(autoTimer);
	if(sceneNum == 12 && txtC12n == 1){
		if(commentOC == "open"){fastTimer=setTimeout(function(){commentPrev();fastCommentPrev();},fastSpeed);}
		else{fastOnOff="OFF";}
	}
	else{
		fastTimer=setTimeout(function(){commentPrev();fastCommentPrev();},fastSpeed);
	}
}
function fastCommentNext(){
	clearTimeout(fastTimer);
	clearTimeout(autoTimer);
	if(sceneNum == 12 && txtC12n == 1){
		if(commentOC == "open"){fastTimer=setTimeout(function(){commentNext();fastCommentNext();},fastSpeed);}
		else{fastOnOff="OFF";}
	}
	else{
		fastTimer=setTimeout(function(){commentNext();fastCommentNext();},fastSpeed);
	}
}

//<<PREV
function commentPrev(){
	
	closeQA();
	
	if(this["txtC"+sceneNum+"n"] == 1){
		for (i=1;i<=12;i++){
			this["txtC"+i+"n"] = 0;
			this["txtC"+sceneNum+"n"] = 1;
		}
	}
	
	if(sceneNum == 3 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){
		charaAnimation01Back();
	}
	
	if(sceneNum == 6 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){
		charaAnimation02A_Back();
	}
	
	if(sceneNum == 9 && this["txtC"+sceneNum+"n"] == 1){
		charaAnimation02B_Back();
	}
	
	if(sceneNum == 12 && this["txtC"+sceneNum+"n"] == 1){
		charaAnimation03_Back();
	}
	
	if(this["txtC"+sceneNum+"n"] == 1){
		if(sceneNum == 4){//不正解
			sceneNum = 2;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = this["txtC"+sceneNum+"t"];
			}
			commentAnimation();
			QAnum=1;
			startQA();
		}
		else if(sceneNum == 7){//不正解
			sceneNum = 5;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = this["txtC"+sceneNum+"t"];
			}
			commentAnimation();
			QAnum=2;
			startQA();
		}
		else if(sceneNum == 11){//不正解
			sceneNum = 9;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = this["txtC"+sceneNum+"t"];
			}
			commentAnimation();
			QAnum=3;
			startQA();
		}
		else if(sceneNum == 12){//最後
			sceneNum = 10;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = this["txtC"+sceneNum+"t"];
			}
			commentAnimation();
		}
		else if(sceneNum == 5){//プロフィールへ戻る
			sceneNum = 3;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = this["txtC"+sceneNum+"t"];
			}
			commentAnimation();
			charaAnimation01Start();
		}
		else if(sceneNum == 8){//2問目正解へ戻る
			charaAnimation02A_Back();
			sceneNum = 6;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = this["txtC"+sceneNum+"t"];
			}
			commentAnimation();
		}
		else if(sceneNum == 1){//最初			
		}
		else{//単純な送り
			sceneNum -= 1;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = this["txtC"+sceneNum+"t"];
			}
			commentAnimation();
			
			if(sceneNum == 2 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){//問題
				QAnum=1;
				startQA();
			}
			else if(sceneNum == 5 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){//問題
				QAnum=2;
				startQA();
			}
			else if(sceneNum == 9 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){//問題
				QAnum=3;
				startQA();
			}
			else{}			
		}
	}
	else{
		this["txtC"+sceneNum+"n"] -= 1;
		commentAnimation();
	}
	
}

//NEXT>>
function commentNext(){
	
	clearTimeout(NextCommentTimer);
	
	//Cookieの設定	
	if(sceneNum == 10){
		$.cookie('d_cast_chara02_01','clear',{expires:30});
		$.cookie('d_cast_chara02_02','clear',{expires:30});
		$.cookie('d_cast_chara02_03','clear',{expires:30});
	}
	else if(sceneNum == 6){
		$.cookie('d_cast_chara02_01','clear',{expires:30});
		$.cookie('d_cast_chara02_02','clear',{expires:30});
	}
	else if(sceneNum == 3){
		$.cookie('d_cast_chara02_01','clear',{expires:30});
	}
	else{}
	
	if(this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){
		for (i=1;i<=12;i++){
			this["txtC"+i+"n"] = 0;
			this["txtC"+sceneNum+"n"] = this["txtC"+sceneNum+"t"];
		}
	}
	
	/*if(sceneNum == 5 && this["txtC"+sceneNum+"n"] == 0){
		charaAnimation01Back();
	}*/
	
	if(this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){
		if(sceneNum == 2){//問題
		}
		else if(sceneNum == 5){//問題
		}
		else if(sceneNum == 9){//問題
		}
		else if(sceneNum == 3){//正解
		}
		else if(sceneNum == 6){//正解
			clearTimeout(autoTimer);
			clearTimeout(fastTimer);
			charaAnimation02A_Start();
			sceneNum = 8;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = 1;
			}
			commentAnimation();
		}
		else if(sceneNum == 10){//正解
			clearTimeout(autoTimer);
			clearTimeout(fastTimer);
			charaAnimation03_Start();
			sceneNum = 12;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = 1;
			}
			commentAnimation();
		}
		else if(sceneNum == 8){//私服公開時
		}
		else if(sceneNum == 4){//不正解
			NG_Animation();
			sceneNum = 1;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = 1;
			}
			ngCommentTimer =setTimeout(function(){commentAnimation();},1200);
		}
		else if(sceneNum == 7){//不正解
			NG_Animation();
			sceneNum = 5;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = 1;
			}
			ngCommentTimer =setTimeout(function(){commentAnimation();},1200);
		}
		else if(sceneNum == 11){//不正解
			NG_Animation();
			sceneNum = 9;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = 1;
			}
			ngCommentTimer =setTimeout(function(){commentAnimation();},1200);
		}
		else if(sceneNum == 12){//INDEXに戻る処理			
			indexTimer =setTimeout(function(){location.href="index.html";},3000);					
		}				
		else{//単純な送り
			sceneNum += 1;
			for (i=1;i<=12;i++){
				this["txtC"+i+"n"] = 0;
				this["txtC"+sceneNum+"n"] = 1;
			}
			commentAnimation();			
		}
	}
	else{
		this["txtC"+sceneNum+"n"] += 1;
		commentAnimation();
		
		if(sceneNum == 2 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){//問題
			QAnum=1;
			QATimer =setTimeout(function(){startQA();},800);
		}
		else if(sceneNum == 5 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){//問題
			QAnum=2;
			QATimer =setTimeout(function(){startQA();},800);
		}
		else if(sceneNum == 9 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){//問題
			QAnum=3;
			QATimer =setTimeout(function(){startQA();},800);
		}
		else{}
		
		if(sceneNum == 3 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){//正解
			charaAnimation01Start();
		}
		else if(sceneNum == 10 && this["txtC"+sceneNum+"n"] == this["txtC"+sceneNum+"t"]){//正解
			//charaAnimation03_Start();
		}
		else{}
	}
}

//コメントアニメーション
function commentAnimation(){
	clearTimeout(ngCommentTimer);
	
	$("#contentsArea #speech #txt_area ul li").hide();
	$("#contentsArea #speech #txt_area ul li").removeClass('txt');
	$("#contentsArea #speech #txt_area").find('ul').eq(sceneNum-1).find('li').eq(this["txtC"+sceneNum+"n"]-1).addClass('txt');
	$("#contentsArea #speech #txt_area").find('ul').eq(sceneNum-1).find('li').eq(this["txtC"+sceneNum+"n"]-1).stop().animate({height:'show'},{duration:300});
	
	if(fastOnOff=="PREV"){
		fastCommentPrev();
	}
	else if(fastOnOff=="NEXT"){
		fastCommentNext();
	}
	else{
		if(autoOnOff=="ON"){
			if(commentOC == "open"){autoCommentStart();}
			else{}
		}
		else{}
	}
}

//オープンクローズアニメーション
function commentOpenClose(){
	
	if(commentOC == "open"){
		commentOC="close";
		clearTimeout(fastTimer);
		clearTimeout(autoTimer);
		$("#speech").hide();
		$("#speech_close").show();
	}
	else{
		clearTimeout(commentOCTimer);
		commentOC="open";
		if(autoOnOff=="ON"){autoCommentStart();}
		else{}
		$("#speech").show();
		$("#speech_close").hide();
	}
	
}