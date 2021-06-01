<?php
class MonthPicker {
	static function write( $from = 0, $to = 0, $def = 0 ){
		if( $from == 0 ){ $from = 1901; }
		if( $to == 0 ){ $to = 2100; }
		if( $def == 0 ){ $def = date('Y', time()); }
		if( $from > $to ){
			$temp = $from;
			$from = $to;
			$to = $temp;
		}
		$select = "";
		for( $i = $from; $i <= $to; $i++ ){
			if( $i == $def ){
				$select .= "<option value=\"$i\" selected=\"selected\">$i</option>\n";
			} else {
				$select .= "<option value=\"$i\">$i</option>\n";
			}
		};
echo <<< EOF
<div id="ui-monthpicker-div" class="ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all">
	<div class="ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-all">
		<a class="ui-datepicker-prev ui-corner-all" data-handler="prev" data-event="click" title="<前">
			<span class="ui-icon ui-icon-circle-triangle-w">&lt;前</span>
		</a>
		<a class="ui-datepicker-next ui-corner-all" data-handler="next" data-event="click" title="次>">
			<span class="ui-icon ui-icon-circle-triangle-e">次&gt;</span>
		</a>
		<div class="ui-datepicker-title">
			<select class="ui-datepicker-year" data-handler="selectYear" data-event="change">
{$select}
			</select>年
		</div>
	</div>
	<table class="ui-datepicker-calendar">
		<tbody>
			<tr>
				<td class=" " data-handler="selectDay" data-event="click" data-month="01" data-year="{$def}"><a class="ui-state-default" href="#">1月</a></td>
				<td class=" " data-handler="selectDay" data-event="click" data-month="02" data-year="{$def}"><a class="ui-state-default" href="#">2月</a></td>
				<td class=" " data-handler="selectDay" data-event="click" data-month="03" data-year="{$def}"><a class="ui-state-default" href="#">3月</a></td>
			</tr>
			<tr>
				<td class=" " data-handler="selectDay" data-event="click" data-month="04" data-year="{$def}"><a class="ui-state-default" href="#">4月</a></td>
				<td class=" " data-handler="selectDay" data-event="click" data-month="05" data-year="{$def}"><a class="ui-state-default" href="#">5月</a></td>
				<td class=" " data-handler="selectDay" data-event="click" data-month="06" data-year="{$def}"><a class="ui-state-default" href="#">6月</a></td>
			</tr>
			<tr>
				<td class=" " data-handler="selectDay" data-event="click" data-month="07" data-year="{$def}"><a class="ui-state-default" href="#">7月</a></td>
				<td class=" " data-handler="selectDay" data-event="click" data-month="08" data-year="{$def}"><a class="ui-state-default" href="#">8月</a></td>
				<td class=" " data-handler="selectDay" data-event="click" data-month="09" data-year="{$def}"><a class="ui-state-default" href="#">9月</a></td>
			</tr>
			<tr>
				<td class=" " data-handler="selectDay" data-event="click" data-month="10" data-year="{$def}"><a class="ui-state-default" href="#">10月</a></td>
				<td class=" " data-handler="selectDay" data-event="click" data-month="11" data-year="{$def}"><a class="ui-state-default" href="#">11月</a></td>
				<td class=" " data-handler="selectDay" data-event="click" data-month="12" data-year="{$def}"><a class="ui-state-default" href="#">12月</a></td>
			</tr>
		</tbody>
	</table>
</div>
<style type="text/css">
<!--
div#ui-monthpicker-div {
	display: none;
	position: absolute;
	top: 0px;
	left: 0px;
	z-index: 1;
}
div#ui-monthpicker-div.ui-datepicker {
	width: 12em;	
}
div#ui-monthpicker-div .ui-datepicker-year {
	width: 70%;
}
-->
</style>
<script language=javascript>
<!--
var monthPicker;
var prevTarget;

$(function(){
	$('div#ui-monthpicker-div select.ui-datepicker-year').change(function(){
		$('div#ui-monthpicker-div table.ui-datepicker-calendar td[data-year]').attr('data-year', $(this).val());
	});
	$('a[data-handler="prev"]').click(function(){
		var dataYear;
		dataYear = $('div#ui-monthpicker-div table.ui-datepicker-calendar td').attr('data-year');
		if( dataYear > {$from} ){
			 var dataYearP = parseInt(dataYear) - 1;
			$('div#ui-monthpicker-div table.ui-datepicker-calendar td[data-year]').attr('data-year', dataYearP);
			$('div#ui-monthpicker-div select.ui-datepicker-year option[value="' + dataYearP + '"]').prop('selected', true);
		}
	});
	$('a[data-handler="next"]').click(function(){
		var dataYear;
		dataYear = $('div#ui-monthpicker-div table.ui-datepicker-calendar td').attr('data-year');
		if( dataYear < {$to} ){
			 var dataYearN = parseInt(dataYear) + 1;
			$('div#ui-monthpicker-div table.ui-datepicker-calendar td[data-year]').attr('data-year', dataYearN);
			$('div#ui-monthpicker-div select.ui-datepicker-year option[value="' + dataYearN + '"]').prop('selected', true);
		}
	});
	$('div#ui-monthpicker-div table.ui-datepicker-calendar td').click(function(){
		monthPicker.val( $(this).attr('data-year') + '/' + $(this).attr('data-month') );
		$('div#ui-monthpicker-div').hide();
	});
	$('a.ui-datepicker-prev').hover(function(){
		$(this).addClass('ui-state-hover').addClass('ui-datepicker-prev-hover');
	},function(){
		$(this).removeClass('ui-state-hover').removeClass('ui-datepicker-prev-hover');
	});
	$('a.ui-datepicker-next').hover(function(){
		$(this).addClass('ui-state-hover').addClass('ui-datepicker-next-hover');
	},function(){
		$(this).removeClass('ui-state-hover').removeClass('ui-datepicker-next-hover');
	});
	$('div#ui-monthpicker-div td a').hover(function(){
		$(this).addClass('ui-state-hover');
	},function(){
		$(this).removeClass('ui-state-hover');
	});
	$(document).focusin(function(event){
		var target = $(event.target);
		if( prevTarget.closest('div#ui-monthpicker-div').length != 0 ){
			var target = $(event.target);
			if( target.closest('div#ui-monthpicker-div').length == 0 ){
				$('div#ui-monthpicker-div').hide();
			}
		}
	}).focusout(function(event){
		prevTarget = $(event.target);
	});
});
function monthPickerShow(e, _this){
	var posX = $(_this).offset().left;	var posY = $(_this).offset().top + $(_this).outerHeight();
	$('div#ui-monthpicker-div').css('display', 'block').offset({top: posY,left: posX});
	$('select.ui-datepicker-year').focus();
	monthPicker = $(_this);
};
//-->
</script>

EOF;
	}
}
?>
