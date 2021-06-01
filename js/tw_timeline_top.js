/*===========================================================
copyright: (c)visual and echo japan
created: 2013.08.20
===========================================================*/

var _twTimerURA;
var _twTimerAUTOcl;

//初期設定
function twOCsetting(){
	
	if(twOC == "open"){
		$("#tr_list"+twINDEX).css("zIndex",100);
		$("#tr_timeline a").css("background-position","top left");
		_twTimerURA=setTimeout(function(){twSlideHideURA()},2000);
	}
	else{
		$("#tr_timeline a").css("background-position","bottom left");
		//_twTimerAUTOcl=setTimeout(function(){twSlideHideAUTOcl()},3500);
	}
	
}

//ボタン設定
function twBtnSetting(){
	
	$("#tr_timeline").click(function(){
		
		clearTimeout(_twTimerURA);
		clearTimeout(_twTimerAUTOcl);
		
		if(twOC == "open"){
			twOC = "close";
			$("#tr_list"+twINDEX).css("zIndex",100);
			$("#tr_list"+twINDEX).stop(true,true).slideDown('fast');
			$("#tr_timeline a").css("background-position","bottom left");
		}
		else{
			twOC = "open";
			$("#tr_list"+twINDEX).stop(true,true).slideUp('fast');
			$("#tr_timeline a").css("background-position","top left");
		}
	});
	
	/*$("#tr_timeline").hover(
		function(){
			$(this).css("cursor","pointer");
			$(this).stop().animate({opacity:"0.4"},{duration:50});
			$(this).delay('50').animate({opacity:"1"},{duration:150});
		},
		function(){
			$(this).css("cursor","default");
			$(this).stop().animate({opacity:'1'},{duration:100});			
		}
	);*/
	
	$("#tr_list"+twINDEX).hover(
		function(){
			clearTimeout(_twTimerAUTOcl);
		},
		function(){
			
		}
	);
	
}

//初回クローズ時 裏に潜り込ませる処理
/*function twSlideHideURA(){
	
	clearTimeout(_twTimerURA);	
	$("#tr_list"+twINDEX).stop(true,true).slideUp('fast');
	
}

//初回オープン時 自動的に隠す処理
function twSlideHideAUTOcl(){
	
	clearTimeout(_twTimerAUTOcl);
	twOC = "close";
	$("#tr_list"+twINDEX).stop(true,true).slideUp('fast');
	$("#tr_timeline a").css("background-position","top left");
	
}*/

$(document).ready(function(){
	
	twOCsetting();
	twBtnSetting();
	
});