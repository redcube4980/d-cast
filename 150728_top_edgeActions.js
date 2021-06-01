/***********************
* Adobe Edge Animate コンポジションアクション
*
* このファイルを編集する際には注意が必要です。必ず関数シグニチャと
* 「Edge」で始まるコメントを保持して、 Adobe Edge 内からこれらのアクションを
* 操作可能な状態にしておいてください。 
*
***********************/
(function($, Edge, compId){
var Composition = Edge.Composition, Symbol = Edge.Symbol; // よく使用する Edge クラスのエイリアス

   //Edge symbol: 'stage'
   (function(symbolName) {
      
      
      Symbol.bindElementAction(compId, symbolName, "${linkbotton}", "click", function(sym, e) {
         // マウスクリックのコードをここに挿入します
         // 現在のウィンドウで新しい URL に移動します
         // (「_self」を適切なターゲット属性に置き換えます)
         window.open("./inspection/", "_self");
         

      });
      //Edge binding end

      Symbol.bindElementAction(compId, symbolName, "${naibu_01}", "click", function(sym, e) {
         // マウスクリックのコードをここに挿入します
         
      });
      //Edge binding end

      Symbol.bindTriggerAction(compId, symbolName, "Default Timeline", 2398, function(sym, e) {
         // コードをここに挿入
      });
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
         /*
         sym.getSymbolElement().hide();
         $(".movieWrapper").hide();
         */
         location.href = '/inspection/';
         
         // コンポジションですべてのオーディオトラックをミュートします。オフに切り替えるには、ミュートを false に設定します。
         $("audio").prop("muted", true);
         

      });
      //Edge binding end

   })("stage");
   //Edge symbol end:'stage'

   //=========================================================
   
   //Edge symbol: 'linkbotton'
   (function(symbolName) {   
         

      

      Symbol.bindTimelineAction(compId, symbolName, "Default Timeline", "complete", function(sym, e) {
         // タイムラインの最後で実行されるコードをここに挿入
         sym.play();

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