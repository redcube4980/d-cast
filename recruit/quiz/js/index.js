/*===========================================================
copyright: (c)visual and echo japan
created: 2013.08.20
===========================================================*/

/*__ DEFAULT _______________________*/

var firstFlag;

$(document).ready(function(){
	
	
	firstFlag=location.search.substr(1);
	
	clearChara01_01 = $.cookie('d_cast_chara01_01');
	clearChara01_02 = $.cookie('d_cast_chara01_02');
	clearChara01_03 = $.cookie('d_cast_chara01_03');
	
	clearChara02_01 = $.cookie('d_cast_chara02_01');
	clearChara02_02 = $.cookie('d_cast_chara02_02');
	clearChara02_03 = $.cookie('d_cast_chara02_03');
	
	clearChara03_01 = $.cookie('d_cast_chara03_01');
	clearChara03_02 = $.cookie('d_cast_chara03_02');
	clearChara03_03 = $.cookie('d_cast_chara03_03');
	
	clearChara04_01 = $.cookie('d_cast_chara04_01');
	clearChara04_02 = $.cookie('d_cast_chara04_02');
	clearChara04_03 = $.cookie('d_cast_chara04_03');	
	
	if(clearChara01_03 == 'clear'){charaAnimation03("quiz_top1_");}
	else if(clearChara01_02 == 'clear'){charaAnimation02("quiz_top1_");}
	else if(clearChara01_01 == 'clear'){charaAnimation01("quiz_top1_");}
	else if(firstFlag=="g1"){charaAnimation01("quiz_top1_");}
	else{charaAnimation00("quiz_top1_");}
	
	if(clearChara02_03 == 'clear'){charaAnimation03("quiz_top2_");}
	else if(clearChara02_02 == 'clear'){charaAnimation02("quiz_top2_");}
	else if(clearChara02_01 == 'clear'){charaAnimation01("quiz_top2_");}
	else if(firstFlag=="g2"){charaAnimation01("quiz_top2_");}
	else{charaAnimation00("quiz_top2_");}
	
	if(clearChara03_03 == 'clear'){charaAnimation03("quiz_top3_");}
	else if(clearChara03_02 == 'clear'){charaAnimation02("quiz_top3_");}
	else if(clearChara03_01 == 'clear'){charaAnimation01("quiz_top3_");}
	else if(firstFlag=="g3"){charaAnimation01("quiz_top3_");}
	else{charaAnimation00("quiz_top3_");}
	
	if(clearChara04_03 == 'clear'){charaAnimation03("quiz_top4_");}
	else if(clearChara04_02 == 'clear'){charaAnimation02("quiz_top4_");}
	else if(clearChara04_01 == 'clear'){charaAnimation01("quiz_top4_");}
	else if(firstFlag=="g4"){charaAnimation01("quiz_top4_");}
	else{charaAnimation00("quiz_top4_");}
	
});

/*__ ANIMATION _______________________*/

function charaAnimation00(obj){
	for (i=0;i<=3;i++){
		$("#"+obj+i).hide();
	}
	$("#"+obj+"0").show();
}

function charaAnimation01(obj){
	for (i=0;i<=3;i++){
		$("#"+obj+i).hide();
	}
	$("#"+obj+"1").show();
}

function charaAnimation02(obj){
	for (i=0;i<=3;i++){
		$("#"+obj+i).hide();
	}
	$("#"+obj+"1").show();
	$("#"+obj+"1").css({opacity:1});
	$("#"+obj+"2").show();
	$("#"+obj+"2").css({opacity:0});
	
	charaAnimation02_ST(obj);
}
function charaAnimation02_ST(obj){
	$("#"+obj+"2").delay(3000).animate({opacity:1},{duration:2000,
		complete:function(){
			$("#"+obj+"1").css({opacity:0});
			$("#"+obj+"1").css({zIndex:11});
			$("#"+obj+"2").css({opacity:1});
			$("#"+obj+"2").css({zIndex:10});
		}
	});
	$("#"+obj+"1").delay(8000).animate({opacity:1},{duration:2000,
		complete:function(){
			$("#"+obj+"1").css({opacity:1});
			$("#"+obj+"1").css({zIndex:10});
			$("#"+obj+"2").css({opacity:0});
			$("#"+obj+"2").css({zIndex:11});
			charaAnimation02_ST(obj);
		}
	});
}

function charaAnimation03(obj){
	for (i=0;i<=3;i++){
		$("#"+obj+i).hide();
	}
	$("#"+obj+"1").show();
	$("#"+obj+"1").css({opacity:1});
	$("#"+obj+"2").show();
	$("#"+obj+"2").css({opacity:0});
	$("#"+obj+"3").show();
	$("#"+obj+"3").css({opacity:0});
	
	charaAnimation03_ST(obj);
}
function charaAnimation03_ST(obj){
	$("#"+obj+"2").delay(3000).animate({opacity:1},{duration:2000,
		complete:function(){
			$("#"+obj+"1").css({opacity:0});
			$("#"+obj+"1").css({zIndex:11});
			$("#"+obj+"2").css({opacity:1});
			$("#"+obj+"2").css({zIndex:10});
			$("#"+obj+"3").css({opacity:0});
			$("#"+obj+"3").css({zIndex:11});
		}
	});
	$("#"+obj+"3").delay(8000).animate({opacity:1},{duration:2000,
		complete:function(){
			$("#"+obj+"1").css({opacity:0});
			$("#"+obj+"1").css({zIndex:11});
			$("#"+obj+"2").css({opacity:0});
			$("#"+obj+"2").css({zIndex:11});
			$("#"+obj+"3").css({opacity:1});
			$("#"+obj+"3").css({zIndex:10});
		}
	});
	$("#"+obj+"1").delay(13000).animate({opacity:1},{duration:2000,
		complete:function(){
			$("#"+obj+"1").css({opacity:1});
			$("#"+obj+"1").css({zIndex:10});
			$("#"+obj+"2").css({opacity:0});
			$("#"+obj+"2").css({zIndex:11});
			$("#"+obj+"3").css({opacity:0});
			$("#"+obj+"3").css({zIndex:11});
			charaAnimation03_ST(obj);
		}
	});
}