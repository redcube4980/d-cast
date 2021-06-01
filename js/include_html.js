//Javascript Document
function glovalHeader() {
	//ヒアドキュメント
	var include_html = (function () {/*
	<div id=header>
		<H1><IMG border=0 alt=誕生、時代を先駆ける総合鋳造メーカー src="http://www.d-cast.jp/images/header1.gif" width=780 height=59 useMap=#Map></H1>
		<div id=topmenu>
			<UL id=button>
				<LI class=button><A href="/index.html">HOME</A></LI>
				<LI class=button><A href="/about/index.html">会社概要</A></LI>
				<LI class=button><A href="/product/index.html">製品案内</A></LI>
				<LI class=button><A href="/inspection/index.html">放射線検査</A></LI>
				<LI class=button><A href="/equipment/index.html">生産設備</A></LI>
				<LI class=button><A href="/service/index.html">サービス体制</A></LI>
				<LI class=button><A href="/recruit/index.html">採用情報</A></LI>
			</UL>
		</div>
	</div>
	<!--
	<map name="Map" id="Map2">
		<area shape="rect" coords="49,17,302,47" href="/index.html" />
		<area shape="rect" coords="670,41,763,57" href="mailto:IMANISHI@d-cast.jp" />
	</map>
	-->
	*/}).toString().replace(/(\n)/g, '').split('*')[1];
	document.write(include_html);
}

function glovalFooter() {
	//ヒアドキュメント
	var include_html = (function () {/*
	<div id="footer">
		<img src="/images/footer_spring.gif" width="780" height="24" /><img src="/images/footer.gif" width="780" height="31" border="0" usemap="#Map2" />
		<map name="Map2" id="Map2"><area shape="rect" coords="26,2,131,20" href="/privacy/index.html" /></map>
	</div>
	*/}).toString().replace(/(\n)/g, '').split('*')[1];
	document.write(include_html);
}
