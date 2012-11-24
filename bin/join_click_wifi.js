/**
Author: Konrad Markus <konker@gmail.com>

*/

var INIT_URL = 'http://ipv4.0-9.fi/';

var page = require('webpage').create();
page.open(INIT_URL, function(status) {
    if (status !== 'success') {
        console.log('Unable to load: ' + INIT_URL);
        return -1;
    }

    var h = page.evaluate(function() {
        var JAVSCRIPT_RE = /^javascript:/;
        var ARG_RE = /open\('([^']*)'\)/;

        var d = document.getElementById('display');
        var as = d.getElementsByTagName('a');
        var a = as[0];
        var h = a.href;
        h = h.replace(JAVSCRIPT_RE, '');
        h = h.replace(ARG_RE, '$1');

        function myOpen(e) {
            e = "http://nextmesh.net/extranet/r/" + billing + "?nasid=" + nasid + "&url=" + encodeURIComponent(e) + "&" + (new Date).getTime();
            var t = document.getElementById("container");
            var n = document.getElementById("loading");
            t.style.display = "none";
            n.style.display = "block";
            var r = "https://internetnetservices.com/adsplashmulti-nu/";
            var i = hex_md5("bdea4dd3c3e42cf655a33d32af353950" + e);
            var s = encodeURIComponent(e);
            var o = r + "?res=notyet&rxurl=" + s + "&rsec=" + i;
            var u = document.location.search;
            u = u.substring(1);
            var a = u.split("&");
            var f = "";
            var l = false;
            for (var c = 0; c < a.length; c++) {
                var h = a[c].split("=");
                var p = h[0];
                if (p == "nas" || p == "nasid") {
                    l = true;
                    p = "nasid"
                }
                var d = h[1];
                f += p + "=" + d + "&"
            }
            o += "&" + f + "id=1";
            if (!l) {
                o = e
            } else {
                o = "http://nextmesh.net/extranet/prer/" + billing + "?nasid=" + nasid + "&url=" + encodeURIComponent(o) + "&" + (new Date).getTime()
            }
            //urltimer = setTimeout("window.location.href = '" + o + "';", 1)
            return o;
        }

        return myOpen(h);
    });
    console.log(h);

    phantom.exit();
});

