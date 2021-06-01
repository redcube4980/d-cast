var sidebar_html = (function () {/*
<ul>
<li id="b_top"><a href="/index.html"></a></li>
<li id="b_rtop"><a href="/recruit/index.html"></a></li>
<!--
	<li id="b_mes"><a href="#"></a></li>
	<li id="b_boss"><a href="/recruit/message/pre.html"></a></li>
-->
<li id="b_apply"><a href="/recruit/guideline/guideline.html"></a></li>
<!--
<li id="b_new"><a href="#"></a></li>
<li id="b_new0"><a href="/recruit/new/sennpainokoe-top.html"></a></li>
-->
<li class="b_new1"><a href="/recruit/new/personal.html"></a></li>
<!-- <li class="b_new4"><a href="/recruit/guideline/operator.html"></a></li> -->
<!-- <li class="b_new3"><a href="/recruit/new/info.html"></a></li> -->
</ul>
*/}).toString().replace(/(\n)/g, '').split('*')[1];
	document.write(sidebar_html);
