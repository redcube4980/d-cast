/***********************
* Adobe Edge Animate コンポジションアクション
*
* このファイルを編集する際には注意が必要です。必ず関数シグニチャと
* 「Edge」で始まるコメントを保持して、 Adobe Edge 内からこれらのアクションを
* 操作可能な状態にしておいてください。 
*
***********************/
(function($, Edge, compId, event){
var Composition = Edge.Composition, Symbol = Edge.Symbol; // よく使用する Edge クラスのエイリアス

   //Edge symbol: 'stage'
   (function(symbolName) {
      Symbol.bindElementAction(compId, symbolName, "${linkbotton}", "click", function(sym, e) {
         // マウスクリックのコードをここに挿入します
         // 現在のウィンドウで新しい URL に移動します
         // (「_self」を適切なターゲット属性に置き換えます)
         //window.open("./inspection/", "_self");
         sym.getSymbolElement().hide();
		     $(".movieWrapper").hide();
         

      });
      //Edge binding end

      Symbol.bindElementAction(compId, symbolName, "${naibu_01}", "click", function(sym, e) {
         // マウスクリックのコードをここに挿入します
         
      });
      //Edge binding end

     //Edge binding end
      Symbol.bindTriggerAction(compId, symbolName, "Default Timeline", 0, function(sym, e) {
        //任意の秒(ミリ秒)をトリガ
        console.log('X');
        $(".movieWrapper").hide();
        $("audio").prop("muted", true);
        //任意の秒(ミリ秒)をトリガ
        $(document).on('click', '#inspeciton_movie img:not(.grayscale)', function(){
          $(".movieWrapper").fadeIn(750).children('div').fadeIn(750);
          console.log('$');
          sym.play(1);
          $("audio").prop("muted", false);
					$(this).addClass("grayscale");
					setTimeout(restore_button, 40500);
        });
      });
		 function restore_button(){
			 $("#inspeciton_movie img.grayscale").removeClass("grayscale");
		 }
      //Edge binding end

     Symbol.bindElementAction(compId, symbolName, "${mutebutton2}", "click", function(sym, e) {
         // マウスクリックのコードをここに挿入します
         
         // コンポジションですべてのオーディオトラックをミュートします。オフに切り替えるには、ミュートを false に設定します。
         $("audio").prop("muted", true);

      });
      //Edge binding end

      Symbol.bindElementAction(compId, symbolName, "${Skipbutton}", "click", function(sym, e) {
        // マウスクリックのコードをここに挿入します
        // エレメントを非表示にします
        sym.getSymbolElement().hide();
        $(".movieWrapper").hide();
        // コンポジションですべてのオーディオトラックをミュートします。オフに切り替えるには、ミュートを false に設定します。
        $("audio").prop("muted", true);
      });
      //Edge binding end

      Symbol.bindElementAction(compId, symbolName, "${Skipbutton}", "creationComplete", function(sym, e) {
        console.log('/');
      });
      //Edge binding end

   })("stage");
   //Edge symbol end:'stage'

   //=========================================================
   
   //Edge symbol: 'stage'
   (function(symbolName) {
         
     Symbol.bindTimelineAction(compId, symbolName, "Default Timeline", "complete", function(sym, e) {
        // タイムラインの最後で実行されるコードをここに挿入
        $(".movieWrapper").fadeOut(1500, 'linear');
      });
      //Edge binding end

   })("stage");
   //Edge symbol end:'stage'

  //Edge symbol: 'linkbotton'
   (function(symbolName) {   

      
      Symbol.bindTimelineAction(compId, symbolName, "Default Timeline", "complete", function(sym, e) {
        //sym.play(); //点滅を無限ループ
      });
      //Edge binding end

   })("linkbotton");
   //Edge symbol end:'linkbotton'

   //=========================================================
   
   //Edge symbol: 'Symbol_1'
   (function(symbolName) {   
   
      Symbol.bindElementAction(compId, symbolName, "${Text}", "click", function(sym, e) {
         // マウスクリックのコードをここに挿入します
         

      });
      //Edge binding end

   })("Symbol_1");
   //Edge symbol end:'Symbol_1'

   //=========================================================
   
   //Edge symbol: 'MuteButton'
   (function(symbolName) {   
   
   })("MuteButton");
   //Edge symbol end:'MuteButton'

})(window.jQuery || AdobeEdge.$, AdobeEdge, "EDGE-445985688");