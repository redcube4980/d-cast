<?php

//処理文字コードの指定
mb_language("Japanese");
mb_internal_encoding("UTF-8");
mb_regex_encoding("UTF-8");

//時刻取得
$dateSerial = time();
$dateString = date('Y/m/d H:i:s', $dateSerial);
$dateStr = date('YmdHis', $dateSerial);
$dateArray = getdate($dateSerial);

//Include,Require
include_once("../manage/subroutine.php");

//サニタイジング
$varCOOKIE = sanitize($_COOKIE, 'aKV');
$varSESSION = sanitize($_SESSION, 'aKV');
$varGET = sanitize($_GET, 'aKV');

?>
<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8" />
<meta name="description" content="大同キャスティングス" />
<meta name="keywords" content="大同キャスティングス" />

<title>エントリーフォーム｜大同キャスティングス</title>

<link rel="stylesheet" href="css/html5-doctor-reset-stylesheet.css" />
<link rel="stylesheet" href="css/style.css?<? echo $dateStr; ?>" />

<!-- jQueryUI -->
<script type="text/javascript" src="/jquery3/jquery.js"></script>
<script type="text/javascript" src="/jquery3/ui/jquery-ui.min.js"></script>
<link type="text/css" rel="stylesheet" href="/jquery3/themes/vader/jquery-ui.min.css" />
<link type="text/css" rel="stylesheet" href="/jquery3/themes/vader/theme.css" />
<!--
<link type="text/css" rel="stylesheet" href="/jquery3/themes/blitzer/jquery-ui.min.css" />
<link type="text/css" rel="stylesheet" href="/jquery3/themes/blitzer/theme.css" />
-->
<!-- i18n JapaneseDatepicker -->
<script type="text/javascript" src="/jquery3/ui/i18n/datepicker-ja.js"></script>

<!-- jQuery,jQueryUI
<script type="text/javascript" src="jquery/jquery-1.8.3.js"></script>
<script type="text/javascript" src="jquery/ui/jquery-ui.min.js"></script>
<link type="text/css" rel="stylesheet" href="jquery/themes/excite-bike/jquery-ui.css" />
-->

<!-- YM Picker.js -->
<script type="text/javascript" src="/jquery3/plugin/jquery-ui.ympicker.js"></script>

<!-- ZIPCloudAPI 郵便番号⇒住所 jQueryPlugin-->
<script type="text/javascript" src="/jquery3/plugin/zipcloud/jquery.zipcloud.js"></script>
<link rel="stylesheet" href="/jquery3/plugin/zipcloud/jquery.zipcloud.css" />

<script language=javascript>
<!--
$(function(){

	preload([
		'images/b_send_gray.jpg',
		'images/b_send_ov.jpg',
		'images/b_send.jpg',
		'images/b_revision_ov.jpg',
		'images/b_revision.jpg',
		'images/b_check_ov.jpg',
		'images/b_check.jpg'
	]);

	$("#btnConfirm").hover(function(){
			this.src = 'images/b_check_ov.jpg';
	},function(){
			this.src = 'images/b_check.jpg';
	});
	$("#btnSubmit").hover(function(){
			this.src = 'images/b_send_ov.jpg';
	},function(){
			this.src = 'images/b_send.jpg';
	});
	$("#btnRevision").hover(function(){
			this.src = 'images/b_revision_ov.jpg';
	},function(){
			this.src = 'images/b_revision.jpg';
	});

	$("#btnSubmit").click(function(){
		if( $("#mode").val() == 'regist' ){
			$(this).unbind("hover");
			this.src = 'images/b_send_gray.jpg';
			var postdata = $("#frmEntry").serialize();
			$.ajax({
				async: false,
				type: "POST",
				url: 'entryforchk.php',
				data: postdata,
				dataType: 'json',
				success: function(msg){
					if (msg.result == 1) {
						location.href = "result.html";
					} else {
						$("#btnSubmit").attr("disabled", "disabled");
						$(".txt-confirm").css('display','none');
						$(".inputDiv").css('display','none');
						$(".input").attr('type','hidden');
					}
				},
				error: function(a,b,c){
				}
			});
		} else {
			$("#frmEntry").submit();
		}
	});

	$("#btnRevision").click(function(){
		$("#mode").val('revision');
		$("#frmEntry").submit();
	});
/*
	$("#zip").zipcloud({
		zip:'#zip',
		addtype:'1',
		add1:"#add",
		type:'hover',
		disp:'#add'
	});
	$("#emgzip").zipcloud({
		zip:'#emgzip',
		addtype:'1',
		add1:"#emgadd",
		type:'hover',
		disp:'#emgadd'
	});
*/
	$(document).on("blur", ".async_chk", function(){
		var checkurl = $(this).attr('checkurl');
		var msglocate = $(this).attr('msg');
		var checkmode = $(this).attr('checkmode');
		var postdata = $(this).attr('name') + "=" + encodeURIComponent($(this).val()) + "&mode=" + checkmode;
		$.ajax({
			type: "POST",
			url: checkurl,
			cache: false,
			data: postdata,
			dataType: 'json',
			success: function(msg){
				if( msg[checkmode] == 1){
					$('#' + msglocate ).css('display','none');
				} else {
					$('#' + msglocate ).css('display','inline');
				}
			}
		})
	});
	$(document).on("change", ".async_chkc", function(){
		var checkurl = $(this).attr('checkurl');
		var msglocate = $(this).attr('msg');
		var checkmode = $(this).attr('checkmode');
		var postdata = $(this).attr('name') + "=" + encodeURIComponent($(this).val()) + "&mode=" + checkmode;
		$.ajax({
			type: "POST",
			url: checkurl,
			data: postdata,
			dataType: 'json',
			success: function(msg){
				if( msg[checkmode] == 1){
					$('#' + msglocate ).css('display','none');
				} else {
					$('#' + msglocate ).css('display','inline');
				}
			}
		})
	});
	$(document).on("focus", ".clear_chk", function(){
		var msglocate = $(this).attr('msg');
		$("#" + msglocate).css('display','none');
	});
	$(document).on("blur", ".copy_chk", function(){
		var dsplocate = $(this).attr('copy');
		$('#' + dsplocate ).html( $(this).val().replace("\n", "<br>\n") );
	});

});

function preload(arrayOfImages) {
	$(arrayOfImages).each(function(){
		$('<img/>')[0].src = this;
	});
}

//-->
</script>

<style type="text/css">
<!--
#btnRevision {
	display:none;
}
-->
</style>

</head>
<body>

<div id="header">
	<div id="header1">
		<a href="http://www.d-cast.jp/"><img src="images/logo.jpg" alt="大同キャスティングス" width="248" height="46"></a>
	</div>
</div>

<div id="wp">
	<img src="images/tag_entry.png" alt="エントリー" width="960" height="31">
	<div id="main">
		<div id="entry">
			<form id="frmEntry" name="frmEntry">
			<input type="hidden" id="mode" name="mode" value="$varPOST{'mode'}" />
			<input type="hidden" name="exp" value="$varGET{'exp'}" />
			<table class="tblEntryForm">
				<tr>
					<th class="first"><ul><li>氏名&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td class="first">
						<span class="caps">姓&nbsp;&nbsp;</span>
						<input type="text" name="namefamily" class="input async_chk clear_chk w130" checkmode="namefamily" msg="namefamilyErr" copy="namefamilyDsp" />&nbsp;&nbsp;&nbsp;&nbsp;
						<span class="caps">名&nbsp;&nbsp;</span>
						<input type="text" name="namefirst" class="input async_chk clear_chk w130" checkmode="namefirst" msg="namefirstErr" copy="namefirstDsp" /><br>
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
						<input type="text" name="rubyfamily" class="input async_chk clear_chk w130" checkmode="rubyfamily" msg="rubyfamilyErr" copy="rubyfamilyDsp" />&nbsp;&nbsp;&nbsp;&nbsp;
						<span class="caps">めい&nbsp;&nbsp;</span>
						<input type="text" name="rubyfirst" class="input async_chk clear_chk w130" checkmode="rubyfirst" msg="rubyfirstErr" copy="rubyfirstDsp" /><br>
						<span id="rubyfamilyErr" class="msgErr">※せいが未入力もしくは入力内容に誤りがあります。<br></span>
						<span id="rubyfirstErr" class="msgErr">※めいが未入力もしくは入力内容に誤りがあります。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th><ul><li>生年月日&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td>
						<input type="text" name="brithday" id="brithday" class="datepicker w150" />
<?php
$presentYear = $dateArray['year'];
$minDate = ($presentYear - 50);
$maxDate = ($presentYear - 16);
$defDate = ($presentYear - 21);
?>
<script>
$(function(){
	$('.datepicker').datepicker({
		dateFormat: "yy/mm/dd",
		changeYear: true,
		changeMonth: true,
		minDate: new Date(<?php echo $minDate; ?>, 4 - 1, 2),
		maxDate: new Date(<?php echo $maxDate; ?>, 4 - 1, 1),
		defaultDate: new Date(<?php echo $defDate; ?>, 4 - 1, 1),
		yearRange: "<?php echo $minDate; ?>:<?php echo $maxDate; ?>",
		onSelect: function(dateText, inst){
			$('#birthdayDsp').html(dateText);
		}
	});
});
</script>
						<span id="birthdayErr" class="msgErr">※生年月日を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="2"><ul><li>メールアドレス&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">PC</th>
					<td>
						<input type="text" name="mailpc" class="input async_chk clear_chk w150" checkmode="mailpc" msg="mailErr" copy="mailpcDsp" />
					</td>
				</tr>
				<tr>
				<th  class="cl2">携帯・スマホ</th>
					<td>
						<input type="text" name="mailcell" class="input async_chk clear_chk w150" checkmode="mailcell" msg="mailErr" copy="mailcellDsp" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※どちらかは必ず入力してください。</span><br>
						<span id="mailErr" class="msgErr">※メールアドレスを正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="4"><ul><li>現住所&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">郵便番号</th>
					<td>
						<input id="zip" type="text" name="zip" copy="zipDsp" class="input clear_chk" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※郵便番号は(-)をいれずに入力して下さい。(例:4550022)</span><br>
						<span id="zipErr" class="msgErr">※郵便番号が未入力もしくは入力内容に誤りがあります。<br></span>
					</td>
				</tr>
				<tr>
				<th  class="cl2">住所</th>
					<td>
						<input id="add" type="text" name="add" copy="addDsp" class="input async_chk clear_chk" checkmode="add" msg="addErr" /><br>
						<span id="addErr" class="msgErr">※住所を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">携帯電話番号</th>
					<td>
						<input id="phonecell" type="text" name="phonecell" class="input async_chk clear_chk" checkmode="phonecell" msg="phonecellErr" copy="phonecellDsp" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※携帯,電話番号は(-)をいれて入力して下さい。(例:052-691-5191)</span><br>
						<span id="phonecellErr" class="msgErr">※携帯電話番号を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">自宅電話番号</th>
					<td>
						<input id="phone" type="text" name="phone" class="input async_chk clear_chk" checkmode="phone" msg="phoneErr" copy="phoneDsp" />
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
						<input class="input" type="checkbox" name="emgclass" id="emgclass" value="1"><span class="caps">&nbsp;現住所と同じ</span>
						<span id="emgclassErr" class="msgErr">※休暇中の連絡先を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">郵便番号</th>
					<td>
						<input id="emgzip" type="text" name="emgzip" copy="emgzipDsp" class="input clear_chk" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※郵便番号は(-)をいれずに入力して下さい。(例:4550022)</span><br>
						<span id="emgzipErr" class="msgErr">※郵便番号が未入力もしくは入力内容に誤りがあります。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">住所</th>
					<td>
						<input id="emgadd" type="text" name="emgadd" copy="emgaddDsp" class="input" /><br>
						<span id="emgaddErr" class="msgErr">※住所を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">電話番号</th>
					<td>
						<input type="text" name="emgphone" class="input async_chk clear_chk" checkmode="emgphone" msg="emgphoneErr" copy="emgphoneDsp" />
						&nbsp;&nbsp;&nbsp;&nbsp;<span class="cap">※電話番号は(-)をいれて入力して下さい。(例:052-691-5191)</span><br>
						<span id="emgphoneErr" class="msgErr">※電話番号を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="5"><ul><li>学校情報&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">学校種別</th>
					<td>
						<div class="inputDiv">
							<input type="radio" name="schoolgrade" class="schoolgrade" copy="schoolgradeDsp" value="大学">&nbsp;大学&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" copy="schoolgradeDsp" value="大学院（修士）">&nbsp;大学院（修士）&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" copy="schoolgradeDsp" value="短大">&nbsp;短大&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" copy="schoolgradeDsp" value="専門学校">&nbsp;専門学校&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" copy="schoolgradeDsp" value="高専">&nbsp;高専&nbsp;
							<input type="radio" name="schoolgrade" class="schoolgrade" copy="schoolgradeDsp" value="高校">&nbsp;高校&nbsp;<br>
							<span id="schoolgradeErr" class="msgErr">※学校種別を正しく選択して下さい。<br></span>
						</div>
					</td>
				</tr>
				<tr>
					<th  class="cl2">学校名</th>
					<td>
						<input type="text" name="schoolname" class="input async_chk clear_chk" checkmode="schoolname" msg="schoolnameErr" copy="schoolnameDsp" /><br>
						<span id="schoolnameErr" class="msgErr">※学校名を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">学部・学科名</th>
					<td>
						<input type="text" name="schoolfaculty" class="input async_chk clear_chk" checkmode="schoolfaculty" msg="schoolfacultyErr" copy="schoolfacultyDsp" /><br>
						<span id="schoolfacultyErr" class="msgErr">※学部・学科名を正しく入力して下さい。<br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">文理区分</th>
					<td>
						<div class="inputDiv">
							<input type="radio" name="schoolkind" class="schoolkind" copy="schoolkindDsp" value="文系">&nbsp;文系&nbsp;
							<input type="radio" name="schoolkind" class="schoolkind" copy="schoolkindDsp" value="理系">&nbsp;理系&nbsp;<br>
							<span id="schoolkindErr" class="msgErr">※理系・文系を正しく選択して下さい。<br></span>
						</div>
					</td>
				</tr>
				<tr>
					<th  class="cl2">卒業予定年月</th>
					<td>
						<input type="month" name="graduatedate" id="graduatedate" />
<script>
$(function(){
	$('input#graduatedate').click(function(e){
		monthPickerShow(e, this);
	});
});
</script>
						<span id="graduateyearErr" class="msgErr">※卒業予定年月を正しく入力して下さい。<br></span>
					</td>
				</tr>
<?php
if( $varGET['exp'] == '2' ){
echo <<< EOF
				<tr>
					<th colspan="2" class="line2"><hr></th>
					<td class="line3"><hr>
						<span class="cap2">※以下の項目の記載は自由です。<br>※3月1日以降、正式エントリーに移行致します。</span><br>
					</td>
				</tr>

EOF;
}
?>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th>資格・経験</th>
					<th class="cl2"></th>
					<td>
						<div class="inputDiv">
							<textarea name="license" id="license" copy="licenseDsp" rows="8"></textarea>&nbsp;&nbsp;&nbsp;&nbsp;<br><span class="cap">※TOEIC等資格、留学やサークル活動など</span>
						</div>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th>自己紹介</th>
					<th  class="cl2"></th>
					<td>
						<div class="inputDiv">
							<textarea class="input" name="intro" id="intro" copy="introDsp" rows="8"></textarea>&nbsp;&nbsp;&nbsp;&nbsp;<br><span class="cap">※趣味・特技、誰にも負けないこと、アルバイト経験など</span>
						</div>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th class="last">その他</th>
					<th  class="cl2 last"></th>
					<td class="last">
						<div class="inputDiv">
							<textarea class="input" name="etc" id="etc" copy="etcDsp" rows="8"></textarea><br><br>
						</div>
					</td>
				</tr>
			</table></form>
<script>
$(function(){
	$(document).on('change', 'input, select, textarea', function(){
		var copy = $(this).attr('copy');
		if( typeof copy === "undefined" ){
		} else {
			switch( $(this).prop("tagName").toLowerCase() ){
				case 'input':
					if( $(this).attr('type') == 'radio' ){
						var radioName = $(this).attr('name');
			    	var radioVal = $("input[name='" + radioName + "']:checked").val();
						$('#' + copy).html( radioVal );
					} else {
						$('#' + copy).html( $(this).val() );
					}
					break;
				case 'textarea':
					$('#' + copy).html( $(this).val().replace(/\n/g,"<br>\n") );
					break;
				case 'select':
					break;
				default:
					break;
			}
		}
	});
});
</script>
		</div>
		<div id="confirm">
			<table class="tblEntryForm">
				<tr>
					<th class="first"><ul><li>氏名&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td class="first">
						<span class="caps">姓&nbsp;&nbsp;</span><span class="txt-confirm" id="namefamilyDsp"></span>
						<span class="caps">名&nbsp;&nbsp;</span><span class="txt-confirm" id="namefirstDsp"></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th><ul><li>ふりがな&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td>
						<span class="caps">せい&nbsp;&nbsp;</span><span class="txt-confirm" id="rubyfamilyDsp"></span>
						<span class="caps">めい&nbsp;&nbsp;</span><span class="txt-confirm" id="rubyfirstDsp"></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th><ul><li>生年月日&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td>
						<span class="txt-confirm" id="birthdayDsp"></span><br>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="2"><ul><li>メールアドレス&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">PC</th>
					<td>
						<span class="txt-confirm" id="mailpcDsp"><br></span>
					</td>
				</tr>
				<tr>
				<th  class="cl2">携帯・スマホ</th>
					<td>
						<span class="txt-confirm" id="mailcellDsp"><br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="4"><ul><li>現住所&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">郵便番号</th>
					<td>
						<span class="txt-confirm" id="zipDsp"><br></span>
					</td>
				</tr>
				<tr>
				<th  class="cl2">住所</th>
					<td>
						<span class="txt-confirm" id="addDsp"><br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">携帯電話番号</th>
					<td>
						<span class="txt-confirm" id="phonecellDsp"><br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">自宅電話番号</th>
					<td>
						<span class="txt-confirm" id="phoneDsp"><br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="4"><ul><li>休暇中の連絡先&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2"></th>
					<td>
						<span class="txt-confirm"></span>
						$dispEmgclass
					</td>
				</tr>
				<tr>
					<th  class="cl2">郵便番号</th>
					<td>
						<span class="txt-confirm" id="emgzipDsp"><br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">住所</th>
					<td>
						<span class="txt-confirm" id="emgaddDsp"><br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">電話番号</th>
					<td>
						<span class="txt-confirm" id="emgphoneDsp"><br></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th rowspan="5"><ul><li>学校情報&nbsp;</li><li><div class="m_must"></div></li></ul></th>
					<th  class="cl2">学校種別</th>
					<td>
						<span class="txt-confirm" id="schoolgradeDsp"><br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">学校名</th>
					<td>
						<span class="txt-confirm" id="schoolnameDsp"><br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">学部・学科名</th>
					<td>
						<span class="txt-confirm" id="schoolfacultyDsp"><br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">文理区分</th>
					<td>
						<span class="txt-confirm" id="schoolkindDsp"><br></span>
					</td>
				</tr>
				<tr>
					<th  class="cl2">卒業予定年月</th>
					<td>
						<span class="txt-confirm" id="graduatedateDsp"></span>&nbsp;年&nbsp;&nbsp;<span class="txt-confirm" id="graduatemonDsp"></span>&nbsp;月&nbsp;&nbsp;<br>
					</td>
				</tr>
<?php
if( $varGET['exp'] == '2' ){
echo <<< EOF
				<tr>
					<th colspan="2" class="line2"><hr></th>
					<td class="line3"><hr>
						<span class="cap2">※以下の項目の記載は自由です。<br>※3月1日以降、正式エントリーに移行致します。</span><br>
					</td>
				</tr>

EOF;
}
?>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th>資格・経験</th>
					<th class="cl2"></th>
					<td>
						<span class="txt-confirm" id="licenseDsp"></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th>自己紹介</th>
					<th  class="cl2"></th>
					<td>
						<span class="txt-confirm" id="introDsp"></span>
					</td>
				</tr>
				<tr><th colspan="2" class="line2"><hr></th><td class="line3"><hr></td></tr>
				<tr>
					<th class="last">その他</th>
					<th  class="cl2 last"></th>
					<td class="last">
						<span class="txt-confirm" id="etcDsp"></span>
					</td>
				</tr>
			</table>
		</div>

		<div id="button" class="entryButtons">
			<input class="ibutton" id="btnRevision" type="image" src="images/images/b_revision.jpg" style="cursor:pointer;" value="内容を修正する">
			<input class="ibutton" id="btnConfirm" type="image" src="images/b_check.jpg" style="cursor:pointer;" value="内容を確認する">
			<input class="ibutton" id="btnSubmit" type="image" src="images/b_send.jpg" style="cursor:pointer;" value="送信する">
		</div>

	</div>
</div>
<footer id="global_footer">
	<div id="global_footer_area">
		<p class="rc"><a href="http://www.daido.co.jp/">大同特殊鋼株式会社</a></p>
		<p id="copyright" class="lc"><small>Copyright © 大同キャスティングス All rights reserved.</small></p>
	</div>
</footer>
<?php
$presentYear = $dateArray['year'];
$minDate = ($presentYear - 50);
$maxDate = ($presentYear - 16);
$defDate = ($presentYear - 21);

include('./monthpicker.php');
MonthPicker::write(1999,2017,2005);
?>
</body>
</html>
