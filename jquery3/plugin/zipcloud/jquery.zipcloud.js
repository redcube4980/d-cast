(function($){
	//jQuery Plugin 郵便番号 to 住所
	$.fn.zipcloud=function(options){
		var opts = $.extend({}, $.fn.zipcloud.defaults, options);
		return this.each(function(i){
			var add1 = "",add2 = "",add3 = "";
			var addtype = opts.addtype;
			var pos1 = opts.add1;
			var pos2 = opts.add2;
			var pos3 = opts.add3;
			$(opts.disp).wrap("<div style='position:relative; margin:0px; padding:0px; border:0px; display:inline-block;'></div>");
			var vpos = $(opts.disp).height() + parseInt($(opts.disp).css('margin-top')) + parseInt($(opts.disp).css('border-top-width')) + parseInt($(opts.disp).css('padding-top')) + parseInt($(opts.disp).css('border-bottom-width')) + parseInt($(opts.disp).css('padding-bottom'));
			var hpos = $(opts.disp).css('margin-left');
			if( opts.type == 'click' ) {
				$(opts.disp).after("<div class='zipcloud_selection_div' style='top:" + vpos + "px; left:" + hpos +"; cursor:pointer;'>");
				$(this).click(function(){
					var ret_str = "";
					var postdata = "zipcode=" + $(opts.zip).val();
					if( $(opts.zip).val() != '' ){
						$("body").css('cursor','wait');
						$.ajax({
							async: false,
							url: "http://zipcloud.ibsnet.co.jp/api/search",
							data: postdata,
							dataType: 'jsonp',
							success: function(msg){
								if(msg.results != null && msg.status == "200"){
									for(var j = 0;j < msg.results.length; j++){
										switch ( addtype ){
										case "1":
											add1 = msg.results[j].address1 + msg.results[j].address2 + msg.results[j].address3;
											ret_str = ret_str + "<div class='zipcloud_address_div' onClick='$(" + '"' + pos1 + '"' + ").val(" + '"' + add1 + '"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").css(" + '"display","none"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").html(" + '""' + ");'>" + add1 + "</div>";
											break;
										case "2":
											add1 = msg.results[j].address1 + msg.results[j].address2;
											add2 = msg.results[j].address3;
											ret_str = ret_str + "<div class='zipcloud_address_div' onClick='$(" + '"' + pos1 + '"' + ").val(" + '"' + add1 + '"' + "); $(" + '"' + pos2 + '"' + ").val(" + '"' + add2 + '"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").css(" + '"display","none"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").html(" + '""' + ");'>" + add1 + add2 + "</div>";
											break;
										case "3":
											add1 = msg.results[j].address1;
											add2 = msg.results[j].address2 + msg.results[j].address3;
											ret_str = ret_str + "<div class='zipcloud_address_div' onClick='$(" + '"' + pos1 + '"' + ").val(" + '"' + add1 + '"' + "); $(" + '"' + pos2 + '"' + ").val(" + '"' + add2 + '"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").css(" + '"display","none"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").html(" + '""' + ");'>" + add1 + add2 + "</div>";
											break;
										case "4":
											add1 = msg.results[j].address1;
											add2 = msg.results[j].address2;
											add3 = msg.results[j].address3;
											ret_str = ret_str + "<div class='zipcloud_address_div' onClick='$(" + '"' + pos1 + '"' + ").val(" + '"' + add1 + '"' + "); $(" + '"' + pos2 + '"' + ").val(" + '"' + add2 + '"' + "); $(" + '"' + pos3 + '"' + ").val(" + '"' + add3 + '"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").css(" + '"display","none"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").html(" + '""' + ");'>" + add1 + add2 + add3 + "</div>";
											break;
										default:
										}
									}
									if(msg.results.length == 1){
										switch ( addtype ){
										case "1":
											$(pos1).val(add1);
											break;
										case "2":
										case "3":
											$(pos1).val(add1);
											$(pos2).val(add2);
											break;
										case "4":
											$(pos1).val(add1);
											$(pos2).val(add2);
											$(pos3).val(add3);
											break;
										default:
										}
									} else {
										$(opts.disp).parent().children(".zipcloud_selection_div").append(ret_str);
										$(opts.disp).parent().children(".zipcloud_selection_div").css('display','block');
									}
								}
								$("body").css('cursor','default');
							},
							error: function(a,b,c){
								$("body").css('cursor','default');
							}
						});
						$("body").css('cursor','default');
					}
				});
			} else {
				$(opts.disp).after("<div class='zipcloud_selection_div' style='top:" + vpos + "px; left:" + hpos +"; cursor:pointer;'>");
				$(this).blur(function(){
					var ret_str = "";
					var postdata = "zipcode=" + $(opts.zip).val();
					if( $(opts.zip).val() != '' ){
						$("body").css('cursor','wait');
						$.ajax({
							async: false,
							url: "http://zipcloud.ibsnet.co.jp/api/search",
							data: postdata,
							dataType: 'jsonp',
							success: function(msg){
								if(msg.results != null && msg.status == "200"){
									for(var j = 0;j < msg.results.length; j++){
										switch ( addtype ){
										case "1":
											add1 = msg.results[j].address1 + msg.results[j].address2 + msg.results[j].address3;
											ret_str = ret_str + "<div class='zipcloud_address_div' onClick='$(" + '"' + pos1 + '"' + ").val(" + '"' + add1 + '"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").css(" + '"display","none"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").html(" + '""' + ");'>" + add1 + "</div>";
											break;
										case "2":
											add1 = msg.results[j].address1 + msg.results[j].address2;
											add2 = msg.results[j].address3;
											ret_str = ret_str + "<div class='zipcloud_address_div' onClick='$(" + '"' + pos1 + '"' + ").val(" + '"' + add1 + '"' + "); $(" + '"' + pos2 + '"' + ").val(" + '"' + add2 + '"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").css(" + '"display","none"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").html(" + '""' + ");'>" + add1 + add2 + "</div>";
											break;
										case "3":
											add1 = msg.results[j].address1;
											add2 = msg.results[j].address2 + msg.results[j].address3;
											ret_str = ret_str + "<div class='zipcloud_address_div' onClick='$(" + '"' + pos1 + '"' + ").val(" + '"' + add1 + '"' + "); $(" + '"' + pos2 + '"' + ").val(" + '"' + add2 + '"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").css(" + '"display","none"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").html(" + '""' + ");'>" + add1 + add2 + "</div>";
											break;
										case "4":
											add1 = msg.results[j].address1;
											add2 = msg.results[j].address2;
											add3 = msg.results[j].address3;
											ret_str = ret_str + "<div class='zipcloud_address_div' onClick='$(" + '"' + pos1 + '"' + ").val(" + '"' + add1 + '"' + "); $(" + '"' + pos2 + '"' + ").val(" + '"' + add2 + '"' + "); $(" + '"' + pos3 + '"' + ").val(" + '"' + add3 + '"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").css(" + '"display","none"' + "); $(\"" + opts.disp + "\").parent().children(" + '".zipcloud_selection_div"' + ").html(" + '""' + ");'>" + add1 + add2 + add3 + "</div>";
											break;
										default:
										}
									}
									if(msg.results.length == 1){
										switch ( addtype ){
										case "1":
											$(pos1).val(add1);
											break;
										case "2":
										case "3":
											$(pos1).val(add1);
											$(pos2).val(add2);
											break;
										case "4":
											$(pos1).val(add1);
											$(pos2).val(add2);
											$(pos3).val(add3);
											break;
										default:
										}
									} else {
										$(opts.disp).parent().children(".zipcloud_selection_div").append(ret_str);
										$(opts.disp).parent().children(".zipcloud_selection_div").css('display','block');
									}
								}
								$("body").css('cursor','default');
							},
							error: function(a,b,c){
								$("body").css('cursor','default');
							}
						});
						$("body").css('cursor','default');
					}
				});
			}

		});
	};
	$.fn.zipcloud.defaults = {
		//type => hover,click
		//addtypeは、1 => 住所一括,2 => 都道府県 市区町村以下,3=> 都道府県市区町村 町村字以下,4 => 都道府県,市区町村,町村字
		//addtype 1 => add1のみ,2 => add2まで,3 => add3まで指定必須
		//dispは、複数アドレスの際の選択ボックス表示位置
		type: 'click',
		zip: '#zip',
		addtype: '1',
		add1: '#address1',
		disp: '#zip',
	};
})(jQuery);
