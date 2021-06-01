$(function(){

	yesterday = Date.parse(Date()) - 86400000;
	//月は0～11 now = new Date(); y = now.getFullYear(); m = now.getMonth(); d = now.getDate(); var maxD = new Date(y,m,d);
	var minD = new Date(2013,9,10);
	var maxD = new Date(yesterday);
	var orgValue;
	var arrayDate = new Array();
	$('.dtpicker').scroller({
		preset: 'date',
		theme: 'default',
		display: 'bubble',
		mode: 'scroller',
		width:40,
		setText:'OK',
		cancelText:'Cancel',
		dateFormat:'yyyy/mm/dd',
		dateOrder:'yyyymmdd',
		monthNames :[1,2,3,4,5,6,7,8,9,10,11,12],
		monthNamesShort :[1,2,3,4,5,6,7,8,9,10,11,12],
		yearText : '年',
		monthText : '月',
		dayText : '日',
		minDate:minD,
		onShow:function(html,valueText,inst){
			orgValue = $("#" + this.id).val();
		},
		onSelect:function(valueText,inst){
			if( orgValue != valueText.val ){
				wkDate = new Date();
				switch(this.id){
					case "date_s":
						date_s = Date.parse($("#date_s").val());
						if( $("#date_e").val() == "" ||$("#date_e").val() == null || $("#date_e").val() == undefined ){
							wkDate.setTime(date_s);
							arrayDate[0] = wkDate.getFullYear();
							arrayDate[1] = wkDate.getMonth();
							arrayDate[2] = wkDate.getDate();
							arrayDate[3] = wkDate.getHours();
							arrayDate[4] = wkDate.getMinutes();
							$("#date_e").mobiscroll('setValue',arrayDate,true,0);
						} else if( $("#date_s").val() > $("#date_e").val()){
							wkDate.setTime(date_s);
							arrayDate[0] = wkDate.getFullYear();
							arrayDate[1] = wkDate.getMonth();
							arrayDate[2] = wkDate.getDate();
							arrayDate[3] = wkDate.getHours();
							arrayDate[4] = wkDate.getMinutes();
							$("#date_e").mobiscroll('setValue',arrayDate,true,0);
						}
					case "date_e":
						date_e = Date.parse($("#date_e").val());
						if( $("#date_s").val() == "" || $("#date_s").val() == null || $("#date_s").val() == undefined ){
							wkDate.setTime(date_e);
							arrayDate[0] = wkDate.getFullYear();
							arrayDate[1] = wkDate.getMonth();
							arrayDate[2] = wkDate.getDate();
							arrayDate[3] = wkDate.getHours();
							arrayDate[4] = wkDate.getMinutes();
							$("#date_s").mobiscroll('setValue',arrayDate,true,0);
						} else if( $("#date_s").val() > $("#date_e").val()){
							wkDate.setTime(date_e);
							arrayDate[0] = wkDate.getFullYear();
							arrayDate[1] = wkDate.getMonth();
							arrayDate[2] = wkDate.getDate();
							arrayDate[3] = wkDate.getHours();
							arrayDate[4] = wkDate.getMinutes();
							$("#date_s").mobiscroll('setValue',arrayDate,true,0);
						}
					default:
						break;
				}
			}
		}
	});
	//inputがGrayOutするのを防ぐ
	$('.dtpicker').removeAttr('readOnly');

	$("#btnClose").on('click', function(){
		window.open("about:blank","_self").close();
	});

	$("#btnDownload").on('click', function(){
		var dlFile = $("#dlFile").val();
		location.href = dlFile;
	});

	$("#btnMake").on('click', function(){
		$("#dispMessage").html('');
		$("#btnMake").attr("disabled","disabled");
		var postdata = $("#frmCSV").serialize();
		$.ajax({
			async: true,
			type: "POST",
			url: 'mgetcsv.cgi?proc=make',
			data: postdata,
			dataType: 'json',
			success: function(msg){
				if( msg.result == 1 ){
					$("#dlFile").val(msg.target);
					$("#dlButton").animate({ opacity: 'hide', height: 'hide' }, 500, 'swing', function(){ });
					$("#dlLink").animate({ opacity: 'show', height: 'show' }, { duration: 500 }, { easing: 'swing' }); 
				} else {
					$("#btnMake").removeAttr("disabled");
				}
				$("#dispMessage").html(msg.message);
			},
			error: function(a,b,c){
				$("#btnMake").removeAttr("disabled");
			}
		});
	});

	$("#btnDelete").on('click', function(){
		$("#btnDelete").attr("disabled","disabled");
		var postdata = 'target=' + $("#dlFile").val();
		$.ajax({
			async: true,
			type: "POST",
			url: 'mgetcsv.cgi?proc=del',
			data: postdata,
			dataType: 'json',
			success: function(msg){
				if( msg.result == 1 ){
					$("#dlLink").animate({ opacity: 'hide', height: 'hide' }, 500, 'swing', function(){ });
					$("#dlClose").animate({ opacity: 'show', height: 'show' }, { duration: 500 }, { easing: 'swing' }); 
				} else {
					$("#btnDelete").removeAttr("disabled");
				}
			},
			error: function(a,b,c){
				$("#btnDelete").removeAttr("disabled");
			}
		});
	});

	$("#btnPublic").on('click', function(){
		var postdata = $("#frmPublic").serialize();
		$.ajax({
			async: true,
			type: "POST",
			url: 'mgetcsv.cgi?proc=pub',
			data: postdata,
			dataType: 'json',
			success: function(msg){
				$("#publicForm").html(msg.public);
			},
			error: function(a,b,c){
			}
		});
	});

	$("#btnDDel").on('click', function(){
		var postdata = "";
		$.ajax({
			async: true,
			type: "POST",
			url: 'mgetcsv.cgi?proc=ddel',
			data: postdata,
			dataType: 'json',
			success: function(msg){
				$("#msgDDel").css('display','block');
				$("#btnDDel").css('display','none');
			},
			error: function(a,b,c){
			}
		});
	});

	$("#ddel").on('change', function(){
		if( $("#ddelText").val() == '削除' && $("#ddel").prop('checked') ){
			$("#btnDDel").removeAttr("disabled");
		} else {
			$("#btnDDel").attr('disabled','disabled');
		}
	});
	$("#ddelText").on('blur', function(){
		if( $("#ddelText").val() == '削除' && $("#ddel").prop('checked') ){
			$("#btnDDel").removeAttr("disabled");
		} else {
			$("#btnDDel").attr('disabled','disabled');
		}
	});

});
