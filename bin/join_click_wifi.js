/**
Author: Konrad Markus <konker@gmail.com>

*/

var INIT_URL = 'http://ipv4.0-9.fi/';

//console.log('Loading init url');
//00:26:b0:f9:40:6b

var JAVSCRIPT_RE = /^javascript:/;

var page = require('webpage').create();
page.onLoadFinished = function(status) {
    console.log('onLoadFinished: ' + status);
}
page.onError = function(msg, trace) {
    var msgStack = ['ERROR: ' + msg];
    /*
    if (trace) {
        msgStack.push('TRACE: ');
    }
    */
    console.error('onError: ' + msgStack.join("\n"));
}
page.open(INIT_URL, function(status) {
    //console.log('open: ' + status);
    if (status !== 'success') {
        console.log('Unable to load: ' + INIT_URL);
        return -1;
    }

    //page.injectJs('meerkat/http/static/js/jquery.js');
    var h = page.evaluate(function() {
        var JAVSCRIPT_RE = /^javascript:/;
        var ARG_RE = /open\('([^']*)'\)/;

        var d = document.getElementById('display');
        var as = d.getElementsByTagName('a');
        var a = as[0];
        var h = a.href;
        h = h.replace(JAVSCRIPT_RE, '');
        h = h.replace(ARG_RE, '$1');

        function kopen(e) {
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

        return kopen(h);
        //open(h);
        //eval(h);
        //return h;
        //var h =  $('#display a').attr('href');
        //return h;
        //$('#display a').click();
        //return document.body.innerHTML;
        //return  $('#display a').attr('href');
        //return document.getElementById('display').innerHTML;
        //return document.getElementById('display').innerText;
    });
    console.log(h);

    /*
    var foo = page.evaluate(function() {
        window.location = 'http://www.google.co.uk/';
        return document.body.innerHTML;
    });
    console.log(foo);
    */
    /*
    page.open(h, function(status) {
        if (status !== 'success') {
            console.log('Unable to load: ' + INIT_URL);
            return -1;
        }
        console.log(page.content);
    }); 
    */
    //console.log(page.content);
    //console.log('Clicked');
    /*
    page.open(INIT_URL, function(status) {
        if (status !== 'success') {
            console.log('Unable to load: ' + INIT_URL);
            return -1;
        }
        console.log(page.content);
    }); 
    */

    phantom.exit();
});

