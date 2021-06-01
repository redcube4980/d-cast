/*jslint */
/*global AdobeEdge: false, window: false, document: false, console:false, alert: false */
(function (compId) {

    "use strict";
    var im='images/',
        aud='media/',
        vid='media/',
        js='js/',
        fonts = {
        },
        opts = {
            'gAudioPreloadPreference': 'auto',
            'gVideoPreloadPreference': 'auto'
        },
        resources = [
        ],
        scripts = [
        ],
        symbols = {
            "stage": {
                version: "6.0.0",
                minimumCompatibleVersion: "5.0.0",
                build: "6.0.0.400",
                scaleToFit: "none",
                centerStage: "none",
                resizeInstances: false,
                content: {
                    dom: [
                        {
                            id: 'houshasen_01',
                            type: 'image',
                            rect: ['81px', '41px', '509px', '206px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted.svg",'0px','0px']
                        },
                        {
                            id: 'Xsen_01',
                            type: 'image',
                            rect: ['612px', '45px', '84px', '204px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted2.svg",'0px','0px']
                        },
                        {
                            id: 'guma_01',
                            type: 'image',
                            rect: ['801px', '35px', '74px', '339px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted3.svg",'0px','0px']
                        },
                        {
                            id: 'naibu_01',
                            type: 'image',
                            rect: ['406px', '315px', '469px', '53px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted4.svg",'0px','0px']
                        },
                        {
                            id: 'pic1_02',
                            type: 'image',
                            rect: ['42px', '-133px', '586px', '808px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted5.svg",'0px','0px']
                        },
                        {
                            id: 'saisentan2',
                            type: 'image',
                            rect: ['80px', '34px', '71px', '272px', 'auto', 'auto'],
                            fill: ["rgba(0,0,0,0)",im+"saisentan2.svg",'0px','0px']
                        },
                        {
                            id: 'xsen2',
                            type: 'image',
                            rect: ['322px', '324px', '275px', '51px', 'auto', 'auto'],
                            fill: ["rgba(0,0,0,0)",im+"xsen2.svg",'0px','0px']
                        },
                        {
                            id: 'oto0729',
                            display: 'none',
                            type: 'audio',
                            tag: 'audio',
                            rect: ['1067', '306', '320px', '45px', 'auto', 'auto'],
                            source: [aud+"150730_music/oto0729.mp3"],
                            preload: 'auto'
                        },
                        {
                            id: 'pi2_02',
                            type: 'image',
                            rect: ['690px', '-20px', '193px', '276px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted7.svg",'0px','0px']
                        },
                        {
                            id: 'rekishi_02',
                            type: 'image',
                            rect: ['643px', '36px', '67px', '168px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted9.svg",'0px','0px']
                        },
                        {
                            id: 'jisseki_02',
                            type: 'image',
                            rect: ['638px', '228px', '238px', '146px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted10.svg",'0px','0px']
                        },
                        {
                            id: 'black_03',
                            type: 'image',
                            rect: ['-375px', '0px', '1700px', '400px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted11.svg",'0px','0px']
                        },
                        {
                            id: 'red_03',
                            type: 'image',
                            rect: ['-375px', '0px', '1700px', '400px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted12.svg",'0px','0px']
                        },
                        {
                            id: 'kensyutu_04',
                            type: 'image',
                            rect: ['59px', '37px', '391px', '244px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted13.svg",'0px','0px']
                        },
                        {
                            id: 'pic1_04',
                            type: 'image',
                            rect: ['483px', '110px', '457px', '305px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted14.svg",'0px','0px'],
                            transform: [[],[],[],['3','3']]
                        },
                        {
                            id: 'browhall_04',
                            type: 'image',
                            rect: ['61px', '285px', '399px', '87px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted15.svg",'0px','0px']
                        },
                        {
                            id: 'kuroi_04',
                            type: 'image',
                            rect: ['822px', '34px', '66px', '337px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted16.svg",'0px','0px']
                        },
                        {
                            id: '_350_04',
                            type: 'image',
                            rect: ['471px', '39px', '334px', '119px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted17.svg",'0px','0px']
                        },
                        {
                            id: 'kizu_04',
                            type: 'image',
                            rect: ['554px', '179px', '51px', '183px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted18.svg",'0px','0px']
                        },
                        {
                            id: 'morosa_04',
                            type: 'image',
                            rect: ['468px', '173px', '79px', '194px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted19.svg",'0px','0px']
                        },
                        {
                            id: 'maininjapan_05',
                            type: 'image',
                            rect: ['55px', '50px', '849px', '310px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted20.svg",'0px','0px']
                        },
                        {
                            id: 'lineer_06',
                            type: 'image',
                            rect: ['261px', '38px', '463px', '143px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted21.svg",'0px','0px']
                        },
                        {
                            id: 'tyokusen_06',
                            type: 'image',
                            rect: ['70px', '41px', '172px', '325px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted22.svg",'0px','0px']
                        },
                        {
                            id: 'speed_06',
                            type: 'image',
                            rect: ['261px', '196px', '477px', '170px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted23.svg",'0px','0px']
                        },
                        {
                            id: 'toujou_06',
                            type: 'image',
                            rect: ['755px', '36px', '134px', '333px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted24.svg",'0px','0px']
                        },
                        {
                            id: 'copyright_07',
                            display: 'none',
                            type: 'image',
                            rect: ['186px', '339px', '593px', '28px', 'auto', 'auto'],
                            opacity: '1',
                            fill: ["rgba(0,0,0,0)",im+"Pasted26.svg",'0px','0px']
                        },
                        {
                            id: 'ryaon_black_07',
                            type: 'image',
                            rect: ['324px', '182px', '309px', '98px', 'auto', 'auto'],
                            opacity: '1',
                            fill: ["rgba(0,0,0,0)",im+"Pasted27.svg",'0px','0px']
                        },
                        {
                            id: 'linkbotton',
                            symbolName: 'linkbotton',
                            display: 'none',
                            type: 'rect',
                            rect: ['324', '182', '309', '98', 'auto', 'auto'],
                            opacity: '1'
                        },
                        {
                            id: 'madeinjapan',
                            type: 'image',
                            rect: ['49px', '34px', '683px', '123px', 'auto', 'auto'],
                            fill: ["rgba(0,0,0,0)",im+"madeinjapan.svg",'0px','0px']
                        },
                        {
                            id: 'no',
                            type: 'image',
                            rect: ['757px', '37px', '142px', '146px', 'auto', 'auto'],
                            fill: ["rgba(0,0,0,0)",im+"mo.svg",'0px','0px']
                        },
                        {
                            id: 'hinshitu_05',
                            type: 'image',
                            rect: ['64px', '205px', '393px', '164px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted30.svg",'0px','0px']
                        },
                        {
                            id: 'otosanai_05',
                            type: 'image',
                            rect: ['472px', '285px', '341px', '81px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"Pasted31.svg",'0px','0px']
                        },
                        {
                            id: 'tenishitanowa',
                            type: 'image',
                            rect: ['269px', '38px', '416px', '51px', 'auto', 'auto'],
                            opacity: '0',
                            fill: ["rgba(0,0,0,0)",im+"tenishitanowa.svg",'0px','0px']
                        },
                        {
                            id: 'hoshasensousa',
                            type: 'image',
                            rect: ['176px', '93px', '603px', '54px', 'auto', 'auto'],
                            fill: ["rgba(0,0,0,0)",im+"hoshasensousa.svg",'0px','0px']
                        },
                        {
                            id: 'mutebutton2',
                            type: 'image',
                            rect: ['800px', '380px', '67px', '15px', 'auto', 'auto'],
                            fill: ["rgba(0,0,0,0)",im+"mutebutton.svg",'0px','0px']
                        },
                        {
                            id: 'Skipbutton',
                            type: 'image',
                            rect: ['877px', '380px', '67px', '15px', 'auto', 'auto'],
                            fill: ["rgba(0,0,0,0)",im+"Skipbutton.svg",'0px','0px']
                        }
                    ],
                    style: {
                        '${Stage}': {
                            isStage: true,
                            rect: ['null', 'null', '960px', '400px', 'auto', 'auto'],
                            overflow: 'hidden',
                            fill: ["rgba(255,255,255,0.00)"]
                        }
                    }
                },
                timeline: {
                    duration: 43235.922549997,
                    autoPlay: true,
                    labels: {
                        "シーン02": 10035
                    },
                    data: [
                        [
                            "eid55",
                            "opacity",
                            1285,
                            0,
                            "linear",
                            "${pic1_02}",
                            '0',
                            '0'
                        ],
                        [
                            "eid67",
                            "opacity",
                            5961,
                            824,
                            "linear",
                            "${pic1_02}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid91",
                            "opacity",
                            10609,
                            552,
                            "linear",
                            "${pic1_02}",
                            '1',
                            '0'
                        ],
                        [
                            "eid142",
                            "opacity",
                            20765,
                            200,
                            "linear",
                            "${morosa_04}",
                            '0',
                            '1'
                        ],
                        [
                            "eid171",
                            "opacity",
                            23249,
                            746,
                            "linear",
                            "${morosa_04}",
                            '1',
                            '0'
                        ],
                        [
                            "eid145",
                            "opacity",
                            18054,
                            531,
                            "linear",
                            "${pic1_04}",
                            '0',
                            '0.2'
                        ],
                        [
                            "eid358",
                            "opacity",
                            18586,
                            300,
                            "linear",
                            "${pic1_04}",
                            '0.2',
                            '1'
                        ],
                        [
                            "eid166",
                            "opacity",
                            23249,
                            746,
                            "linear",
                            "${pic1_04}",
                            '1',
                            '0'
                        ],
                        [
                            "eid148",
                            "opacity",
                            18916,
                            523,
                            "easeInQuad",
                            "${kensyutu_04}",
                            '0',
                            '1'
                        ],
                        [
                            "eid165",
                            "opacity",
                            23249,
                            746,
                            "linear",
                            "${kensyutu_04}",
                            '1',
                            '0'
                        ],
                        [
                            "eid7",
                            "opacity",
                            3717,
                            155,
                            "linear",
                            "${guma_01}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid47",
                            "opacity",
                            5317,
                            326,
                            "linear",
                            "${guma_01}",
                            '1',
                            '0'
                        ],
                        [
                            "eid194",
                            "opacity",
                            29052,
                            251,
                            "linear",
                            "${lineer_06}",
                            '0',
                            '1'
                        ],
                        [
                            "eid206",
                            "opacity",
                            32250,
                            304,
                            "linear",
                            "${lineer_06}",
                            '1',
                            '0'
                        ],
                        [
                            "eid196",
                            "opacity",
                            30069,
                            41,
                            "easeInQuad",
                            "${speed_06}",
                            '0',
                            '1'
                        ],
                        [
                            "eid208",
                            "opacity",
                            32250,
                            304,
                            "linear",
                            "${speed_06}",
                            '1',
                            '0'
                        ],
                        [
                            "eid368",
                            "opacity",
                            24945,
                            204,
                            "easeInQuad",
                            "${no}",
                            '0',
                            '1'
                        ],
                        [
                            "eid372",
                            "opacity",
                            28000,
                            162,
                            "linear",
                            "${no}",
                            '1',
                            '0'
                        ],
                        [
                            "eid430",
                            "scaleX",
                            24945,
                            0,
                            "linear",
                            "${no}",
                            '1',
                            '1'
                        ],
                        [
                            "eid431",
                            "scaleX",
                            25149,
                            0,
                            "linear",
                            "${no}",
                            '1',
                            '1'
                        ],
                        [
                            "eid139",
                            "opacity",
                            20184,
                            200,
                            "linear",
                            "${kuroi_04}",
                            '0',
                            '1'
                        ],
                        [
                            "eid168",
                            "opacity",
                            23249,
                            746,
                            "linear",
                            "${kuroi_04}",
                            '1',
                            '0'
                        ],
                        [
                            "eid378",
                            "left",
                            7411,
                            396,
                            "easeOutQuart",
                            "${xsen2}",
                            '322px',
                            '76px'
                        ],
                        [
                            "eid442",
                            "display",
                            38868,
                            0,
                            "linear",
                            "${linkbotton}",
                            'none',
                            'block'
                        ],
                        [
                            "eid284",
                            "opacity",
                            26070,
                            819,
                            "easeInQuad",
                            "${otosanai_05}",
                            '0',
                            '1'
                        ],
                        [
                            "eid293",
                            "opacity",
                            28000,
                            162,
                            "linear",
                            "${otosanai_05}",
                            '1',
                            '0'
                        ],
                        [
                            "eid75",
                            "opacity",
                            9144,
                            779,
                            "easeInQuad",
                            "${jisseki_02}",
                            '0',
                            '1'
                        ],
                        [
                            "eid88",
                            "opacity",
                            10609,
                            552,
                            "linear",
                            "${jisseki_02}",
                            '1',
                            '0'
                        ],
                        [
                            "eid217",
                            "opacity",
                            1285,
                            0,
                            "linear",
                            "${copyright_07}",
                            '1',
                            '0'
                        ],
                        [
                            "eid225",
                            "opacity",
                            39995,
                            634,
                            "easeInQuad",
                            "${copyright_07}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid440",
                            "volume",
                            500,
                            2165,
                            "easeInQuad",
                            "${oto0729}",
                            '0',
                            '1'
                        ],
                        [
                            "eid281",
                            "opacity",
                            25500,
                            423,
                            "linear",
                            "${hinshitu_05}",
                            '0',
                            '1'
                        ],
                        [
                            "eid292",
                            "opacity",
                            28000,
                            162,
                            "linear",
                            "${hinshitu_05}",
                            '1',
                            '0'
                        ],
                        [
                            "eid309",
                            "top",
                            5317,
                            0,
                            "easeOutCubic",
                            "${naibu_01}",
                            '315px',
                            '315px'
                        ],
                        [
                            "eid371",
                            "opacity",
                            35249,
                            1001,
                            "easeInQuad",
                            "${hoshasensousa}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid5",
                            "opacity",
                            4075,
                            827,
                            "easeOutCubic",
                            "${naibu_01}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid46",
                            "opacity",
                            5317,
                            326,
                            "easeOutCubic",
                            "${naibu_01}",
                            '1',
                            '0'
                        ],
                        [
                            "eid357",
                            "scaleY",
                            17643,
                            1242,
                            "linear",
                            "${pic1_04}",
                            '3',
                            '1'
                        ],
                        [
                            "eid377",
                            "opacity",
                            6785,
                            683,
                            "linear",
                            "${saisentan2}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid383",
                            "opacity",
                            10609,
                            552,
                            "easeOutQuart",
                            "${saisentan2}",
                            '1',
                            '0'
                        ],
                        [
                            "eid36",
                            "left",
                            3872,
                            1029,
                            "easeOutCubic",
                            "${naibu_01}",
                            '406px',
                            '91px'
                        ],
                        [
                            "eid437",
                            "display",
                            39995,
                            0,
                            "easeInQuad",
                            "${copyright_07}",
                            'none',
                            'block'
                        ],
                        [
                            "eid197",
                            "opacity",
                            31250,
                            628,
                            "easeInQuad",
                            "${toujou_06}",
                            '0',
                            '1'
                        ],
                        [
                            "eid209",
                            "opacity",
                            32250,
                            304,
                            "linear",
                            "${toujou_06}",
                            '1',
                            '0'
                        ],
                        [
                            "eid141",
                            "opacity",
                            21000,
                            1250,
                            "easeInQuad",
                            "${kizu_04}",
                            '0',
                            '1'
                        ],
                        [
                            "eid170",
                            "opacity",
                            23249,
                            746,
                            "linear",
                            "${kizu_04}",
                            '1',
                            '0'
                        ],
                        [
                            "eid370",
                            "opacity",
                            33000,
                            1709,
                            "easeInQuart",
                            "${tenishitanowa}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid6",
                            "opacity",
                            1500,
                            1795,
                            "easeInQuad",
                            "${houshasen_01}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid49",
                            "opacity",
                            5317,
                            326,
                            "linear",
                            "${houshasen_01}",
                            '1',
                            '0'
                        ],
                        [
                            "eid323",
                            "opacity",
                            37250,
                            1618,
                            "linear",
                            "${ryaon_black_07}",
                            '0',
                            '1'
                        ],
                        [
                            "eid379",
                            "opacity",
                            7411,
                            396,
                            "easeOutQuart",
                            "${xsen2}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid382",
                            "opacity",
                            10609,
                            552,
                            "easeOutQuart",
                            "${xsen2}",
                            '1',
                            '0'
                        ],
                        [
                            "eid68",
                            "opacity",
                            7785,
                            872,
                            "linear",
                            "${pi2_02}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid86",
                            "opacity",
                            10609,
                            552,
                            "linear",
                            "${pi2_02}",
                            '1',
                            '0'
                        ],
                        [
                            "eid230",
                            "background-color",
                            1285,
                            0,
                            "linear",
                            "${Stage}",
                            'rgba(255,255,255,0.00)',
                            'rgba(255,255,255,0.00)'
                        ],
                        [
                            "eid347",
                            "top",
                            13135,
                            0,
                            "linear",
                            "${black_03}",
                            '0px',
                            '0px'
                        ],
                        [
                            "eid346",
                            "top",
                            13683,
                            0,
                            "linear",
                            "${black_03}",
                            '0px',
                            '0px'
                        ],
                        [
                            "eid361",
                            "top",
                            17525,
                            0,
                            "linear",
                            "${black_03}",
                            '0px',
                            '0px'
                        ],
                        [
                            "eid294",
                            "opacity",
                            1893,
                            9552,
                            "linear",
                            "${black_03}",
                            '0',
                            '0.000000'
                        ],
                        [
                            "eid108",
                            "opacity",
                            11445,
                            561,
                            "linear",
                            "${black_03}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid343",
                            "opacity",
                            16896,
                            747,
                            "linear",
                            "${black_03}",
                            '1',
                            '0'
                        ],
                        [
                            "eid32",
                            "left",
                            1540,
                            0,
                            "linear",
                            "${houshasen_01}",
                            '81px',
                            '81px'
                        ],
                        [
                            "eid8",
                            "opacity",
                            3545,
                            129,
                            "linear",
                            "${Xsen_01}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid48",
                            "opacity",
                            5317,
                            326,
                            "linear",
                            "${Xsen_01}",
                            '1',
                            '0'
                        ],
                        [
                            "eid140",
                            "opacity",
                            20384,
                            200,
                            "linear",
                            "${_350_04}",
                            '0',
                            '1'
                        ],
                        [
                            "eid169",
                            "opacity",
                            23249,
                            746,
                            "linear",
                            "${_350_04}",
                            '1',
                            '0'
                        ],
                        [
                            "eid34",
                            "left",
                            3729,
                            0,
                            "linear",
                            "${guma_01}",
                            '801px',
                            '801px'
                        ],
                        [
                            "eid138",
                            "opacity",
                            19439,
                            200,
                            "linear",
                            "${browhall_04}",
                            '0',
                            '1'
                        ],
                        [
                            "eid167",
                            "opacity",
                            23249,
                            746,
                            "linear",
                            "${browhall_04}",
                            '1',
                            '0'
                        ],
                        [
                            "eid106",
                            "opacity",
                            11285,
                            0,
                            "linear",
                            "${red_03}",
                            '0',
                            '0'
                        ],
                        [
                            "eid111",
                            "opacity",
                            12006,
                            554,
                            "linear",
                            "${red_03}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid113",
                            "opacity",
                            12560,
                            525,
                            "linear",
                            "${red_03}",
                            '1',
                            '0'
                        ],
                        [
                            "eid117",
                            "opacity",
                            13792,
                            525,
                            "linear",
                            "${red_03}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid118",
                            "opacity",
                            14317,
                            535,
                            "linear",
                            "${red_03}",
                            '1',
                            '0'
                        ],
                        [
                            "eid122",
                            "opacity",
                            15643,
                            500,
                            "linear",
                            "${red_03}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid123",
                            "opacity",
                            16143,
                            500,
                            "linear",
                            "${red_03}",
                            '1',
                            '0'
                        ],
                        [
                            "eid195",
                            "opacity",
                            29830,
                            48,
                            "linear",
                            "${tyokusen_06}",
                            '0',
                            '1'
                        ],
                        [
                            "eid207",
                            "opacity",
                            32250,
                            304,
                            "linear",
                            "${tyokusen_06}",
                            '1',
                            '0'
                        ],
                        [
                            "eid356",
                            "scaleX",
                            17643,
                            1242,
                            "linear",
                            "${pic1_04}",
                            '3',
                            '1'
                        ],
                        [
                            "eid355",
                            "display",
                            37250,
                            0,
                            "linear",
                            "${ryaon_black_07}",
                            'none',
                            'block'
                        ],
                        [
                            "eid33",
                            "left",
                            3549,
                            0,
                            "linear",
                            "${Xsen_01}",
                            '612px',
                            '612px'
                        ],
                        [
                            "eid432",
                            "scaleY",
                            24945,
                            0,
                            "linear",
                            "${no}",
                            '1',
                            '1'
                        ],
                        [
                            "eid433",
                            "scaleY",
                            25149,
                            0,
                            "linear",
                            "${no}",
                            '1',
                            '1'
                        ],
                        [
                            "eid76",
                            "opacity",
                            8657,
                            165,
                            "linear",
                            "${rekishi_02}",
                            '0',
                            '1'
                        ],
                        [
                            "eid87",
                            "opacity",
                            10609,
                            552,
                            "linear",
                            "${rekishi_02}",
                            '1',
                            '0'
                        ],
                        [
                            "eid367",
                            "opacity",
                            24250,
                            482,
                            "linear",
                            "${madeinjapan}",
                            '0',
                            '1'
                        ],
                        [
                            "eid369",
                            "opacity",
                            28000,
                            162,
                            "linear",
                            "${madeinjapan}",
                            '1',
                            '0'
                        ],
                            [ "eid441", "trigger", 500, function executeMediaFunction(e, data) { this._executeMediaAction(e, data); }, ['play', '${oto0729}', [] ] ],
                            [ "eid330", "trigger", 38867.922549997, function executeSymbolFunction(e, data) { this._executeSymbolAction(e, data); }, ['play', '${linkbotton}', [] ] ]
                    ]
                }
            },
            "linkbotton": {
                version: "6.0.0",
                minimumCompatibleVersion: "5.0.0",
                build: "6.0.0.400",
                scaleToFit: "none",
                centerStage: "none",
                resizeInstances: false,
                content: {
                    dom: [
                        {
                            rect: ['0px', '0px', '309px', '98px', 'auto', 'auto'],
                            id: 'ryaon_black_07',
                            opacity: '0',
                            type: 'image',
                            fill: ['rgba(0,0,0,0)', 'images/Pasted27.svg', '0px', '0px']
                        },
                        {
                            rect: ['0px', '0px', '309px', '98px', 'auto', 'auto'],
                            id: 'rayon_red_07',
                            opacity: '0',
                            type: 'image',
                            fill: ['rgba(0,0,0,0)', 'images/Pasted28.svg', '0px', '0px']
                        }
                    ],
                    style: {
                        '${symbolSelector}': {
                            rect: [null, null, '309px', '98px']
                        }
                    }
                },
                timeline: {
                    duration: 4368,
                    autoPlay: true,
                    data: [
                        [
                            "eid237",
                            "opacity",
                            4368,
                            0,
                            "linear",
                            "${ryaon_black_07}",
                            '1',
                            '1'
                        ],
                        [
                            "eid234",
                            "opacity",
                            0,
                            203,
                            "linear",
                            "${rayon_red_07}",
                            '0',
                            '1'
                        ],
                        [
                            "eid239",
                            "opacity",
                            203,
                            208,
                            "linear",
                            "${rayon_red_07}",
                            '1',
                            '0'
                        ],
                        [
                            "eid248",
                            "opacity",
                            911,
                            187,
                            "linear",
                            "${rayon_red_07}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid249",
                            "opacity",
                            1098,
                            187,
                            "linear",
                            "${rayon_red_07}",
                            '1',
                            '0'
                        ],
                        [
                            "eid253",
                            "opacity",
                            1766,
                            168,
                            "linear",
                            "${rayon_red_07}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid254",
                            "opacity",
                            1934,
                            172,
                            "linear",
                            "${rayon_red_07}",
                            '1',
                            '0'
                        ],
                        [
                            "eid258",
                            "opacity",
                            2606,
                            191,
                            "linear",
                            "${rayon_red_07}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid259",
                            "opacity",
                            2797,
                            162,
                            "linear",
                            "${rayon_red_07}",
                            '1',
                            '0'
                        ],
                        [
                            "eid263",
                            "opacity",
                            3459,
                            210,
                            "linear",
                            "${rayon_red_07}",
                            '0.000000',
                            '1'
                        ],
                        [
                            "eid264",
                            "opacity",
                            3669,
                            199,
                            "linear",
                            "${rayon_red_07}",
                            '1',
                            '0'
                        ],
                        [
                            "eid373",
                            "opacity",
                            4368,
                            0,
                            "linear",
                            "${rayon_red_07}",
                            '0',
                            '0'
                        ]
                    ]
                }
            },
            "Symbol_1": {
                version: "6.0.0",
                minimumCompatibleVersion: "5.0.0",
                build: "6.0.0.400",
                scaleToFit: "none",
                centerStage: "none",
                resizeInstances: false,
                content: {
                    dom: [
                        {
                            font: ['\'ヒラギノ角ゴ Pro W3\', \'Hiragino Kaku Gothic Pro\', \'メイリオ\', Meiryo, \'ＭＳＰゴシック\', MS PGothic, sans-serif', [24, ''], 'rgba(0,0,0,1)', 'normal', 'none', '', 'break-word', 'nowrap'],
                            id: 'Text',
                            text: '<p style=\"margin: 0px;\">​SKIP</p>',
                            type: 'text',
                            rect: ['0px', '0px', 'auto', 'auto', 'auto', 'auto']
                        }
                    ],
                    style: {
                        '${symbolSelector}': {
                            rect: [null, null, '55px', '30px']
                        }
                    }
                },
                timeline: {
                    duration: 0,
                    autoPlay: true,
                    data: [

                    ]
                }
            },
            "MuteButton": {
                version: "6.0.0",
                minimumCompatibleVersion: "5.0.0",
                build: "6.0.0.400",
                scaleToFit: "none",
                centerStage: "none",
                resizeInstances: false,
                content: {
                    dom: [
                        {
                            type: 'text',
                            id: 'Text',
                            text: '<p style=\"margin: 0px;\">​Mute</p>',
                            rect: ['0px', '0px', 'auto', 'auto', 'auto', 'auto'],
                            font: ['\'ヒラギノ明朝 Pro W3\', \'Hiragino Mincho Pro\', \'ＭＳＰ明朝\', MS PMincho, serif', [15, 'px'], 'rgba(0,0,0,1)', 'normal', 'none', '', 'break-word', 'nowrap']
                        }
                    ],
                    style: {
                        '${symbolSelector}': {
                            rect: [null, null, '61px', '30px']
                        }
                    }
                },
                timeline: {
                    duration: 0,
                    autoPlay: true,
                    data: [

                    ]
                }
            }
        };

    AdobeEdge.registerCompositionDefn(compId, symbols, fonts, scripts, resources, opts);

    if (!window.edge_authoring_mode) AdobeEdge.getComposition(compId).load("150728_top_edgeActions.js");
})("EDGE-445985688");
