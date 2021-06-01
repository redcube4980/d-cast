/*===========================================================
copyright: (c)visual and echo japan
created: 2013.08.20
===========================================================*/

/*__ DEFAULT _______________________*/

$(document).ready(function(){	
	
	$("#steam_01").css({opacity:0});
	$("#steam_02").css({opacity:0});
	$("#steam_03").css({opacity:0});
	
	$("#train_steam_01").css({opacity:0,marginTop:"12px"});
	$("#train_steam_02").css({opacity:0,marginTop:"12px"});
	
	btnSeting();
	
	trainMove01();
	trainStream01();
	
	boatMove01();
	
	spaceshipMove01();
	
	neonMove01();
	
	signboardMove01();
	
	steamLoop01();	
});


/*__ BTN _______________________*/

function btnSeting(){
	
	$("#train_area").hover(
		function(){
			$(this).css("cursor","pointer");
			$("#train").stop();
			$("#train_steam_01").stop();
			$("#train_steam_02").stop();
			$("li#product a").css("color","#FFFF00");
		},
		function(){
			$(this).css("cursor","default");
			trainMove01();
			trainStream01();
			$("li#product a").css("color","#999999");
		}
	);
	
	$("#boat_area").hover(
		function(){
			$(this).css("cursor","pointer");
			$("#boat").stop();
			$("li#service a").css("color","#FFFF00");
		},
		function(){
			$(this).css("cursor","default");
			boatMove01();
			$("li#service a").css("color","#999999");
		}
	);
	
	$("#spaceship_area").hover(
		function(){
			$(this).css("cursor","pointer");
			$("#spaceship").stop();
			$("li#equipment a").css("color","#FFFF00");
		},
		function(){
			$(this).css("cursor","default");
			spaceshipMove01();
			$("li#equipment a").css("color","#999999");
		}
	);
	
	$("#neon_area").hover(
		function(){
			$(this).css("cursor","pointer");
			$("#neon_off").stop();
			$("li#about a").css("color","#FFFF00");
		},
		function(){
			$(this).css("cursor","default");
			neonMove01();
			$("li#about a").css("color","#999999");
		}
	);
	
	$("li#product a,li#service a,li#equipment a,li#about a").hover(
		function(){
			$(this).css("cursor","pointer");
			$(this).css("color","#FFFF00");
		},
		function(){
			$(this).css("cursor","default");
			$(this).css("color","#999999");
		}
	);
	
}


/*__ 列車 _______________________*/

function trainMove01(){
	$("#train").stop().animate({marginTop:"-1px"},{duration:300,complete:function(){trainMove02();}});
}
function trainMove02(){
	$("#train").stop().animate({marginTop:0},{duration:300,complete:function(){trainMove03();}});
}
function trainMove03(){
	$("#train").stop().animate({marginTop:"-1px"},{duration:300,complete:function(){trainMove04();}});
}
function trainMove04(){
	$("#train").stop().animate({marginTop:0},{duration:300,complete:function(){trainMove05();}});
}
function trainMove05(){
	$("#train").stop().animate({marginTop:"-1px"},{duration:300,complete:function(){trainMove06();}});
}
function trainMove06(){
	$("#train").stop().animate({marginTop:0},{duration:300,complete:function(){trainMove07();}});
}
function trainMove07(){
	$("#train").stop().animate({marginTop:0},{duration:4000,complete:function(){trainMove01();}});
}
function trainStream01(){
	$("#train_steam_01").css({opacity:0,marginTop:"12px"});
	$("#train_steam_02").css({opacity:0,marginTop:"12px"});
	if(!jQuery.support.opacity){
		$("#train_steam_01").css({opacity:1});
		$("#train_steam_02").css({opacity:1});
		$("#train_steam_01").stop().animate({marginTop:0},{duration:2000});
		$("#train_steam_02").stop().animate({marginTop:0},{duration:3000,complete:function(){trainStream02();}});
	}
	else{
		$("#train_steam_01").stop().animate({opacity:1,marginTop:0},{duration:2000});
		$("#train_steam_02").stop().animate({opacity:1,marginTop:0},{duration:3000,complete:function(){trainStream02();}});
	}
}
function trainStream02(){
	if(!jQuery.support.opacity){
		$("#train_steam_01").stop().animate({marginTop:"-6px"},{duration:2000});
		$("#train_steam_02").stop().animate({marginTop:"-6px"},{duration:2000,complete:function(){trainStream01();}});
	}
	else{
		$("#train_steam_01").stop().animate({opacity:0,marginTop:"-6px"},{duration:2000});
		$("#train_steam_02").stop().animate({opacity:0,marginTop:"-6px"},{duration:2000,complete:function(){trainStream01();}});
	}
}


/*__ 屋形船 _______________________*/

function boatMove01(){
	$("#boat").stop().animate({marginTop:"-2px"},{duration:1200,complete:function(){boatMove02();}});
}
function boatMove02(){
	$("#boat").stop().animate({marginTop:0},{duration:1200,complete:function(){boatMove01();}});
}


/*__ 宇宙船 _______________________*/

function spaceshipMove01(){
	$("#spaceship").stop().animate({marginTop:"15px"},{duration:9000,complete:function(){spaceshipMove02();}});
}
function spaceshipMove02(){
	$("#spaceship").stop().animate({marginTop:0},{duration:9000,complete:function(){spaceshipMove01();}});
}


/*__ センターネオン _______________________*/

function neonMove01(){
	if(!jQuery.support.opacity){
		$("#neon_on").css({opacity:0});
		$("#neon_on").stop().animate({opacity:0},{duration:600,complete:function(){neonMove02();}});
	}
	else{
		$("#neon_on").stop().animate({opacity:0},{duration:600,complete:function(){neonMove02();}});
	}
}
function neonMove02(){
	if(!jQuery.support.opacity){
		$("#neon_on").css({opacity:1});
		$("#neon_on").stop().animate({opacity:1},{duration:600,complete:function(){neonMove03();}});
	}
	else{
		$("#neon_on").stop().animate({opacity:1},{duration:600,complete:function(){neonMove03();}});
	}
}
function neonMove03(){
	if(!jQuery.support.opacity){
		$("#neon_on").css({opacity:0});
		$("#neon_on").stop().animate({opacity:0},{duration:1000,complete:function(){neonMove04();}});
	}
	else{
		$("#neon_on").stop().animate({opacity:0},{duration:1000,complete:function(){neonMove04();}});
	}
}
function neonMove04(){
	if(!jQuery.support.opacity){
		$("#neon_on").css({opacity:0});
		$("#neon_on").stop().animate({opacity:0},{duration:1600,complete:function(){neonMove05();}});
	}
	else{
		$("#neon_on").stop().animate({opacity:0},{duration:1600,complete:function(){neonMove05();}});
	}
}
function neonMove05(){
	if(!jQuery.support.opacity){
		$("#neon_on").css({opacity:1});
		$("#neon_on").stop().animate({opacity:1},{duration:600,complete:function(){neonMove01();}});
	}
	else{
		$("#neon_on").stop().animate({opacity:1},{duration:600,complete:function(){neonMove01();}});
	}
}


/*__ 時代を先駆けるネオン _______________________*/

function signboardMove01(){
	$("#signboard").stop().animate({opacity:0},{duration:1200,complete:function(){signboardMove02();}});
}
function signboardMove02(){
	$("#signboard").stop().animate({opacity:1},{duration:1600,complete:function(){signboardMove01();}});
}


/*__ 蒸気 _______________________*/

function steamLoop01(){
	if(!jQuery.support.opacity){
		$("#steam_01").css({opacity:0});
		$("#steam_02").css({opacity:0});
		$("#steam_03").css({opacity:0});
	}
	else{
		$("#steam_01").stop().animate({opacity:1},{duration:3000});
		$("#steam_02").stop().animate({opacity:1},{duration:5000});
		$("#steam_03").stop().animate({opacity:1},{duration:7000,complete:function(){steamLoop02();}});
	}
}
function steamLoop02(){
	if(!jQuery.support.opacity){}
	else{
		$("#steam_01").stop().animate({opacity:0},{duration:3000});
		$("#steam_02").stop().animate({opacity:0},{duration:3000});
		$("#steam_03").stop().animate({opacity:0},{duration:3000,complete:function(){steamLoop01();}});
	}	
}