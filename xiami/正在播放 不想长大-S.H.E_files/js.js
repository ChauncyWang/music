function s(a) {
    if (-1 !== a.indexOf("http://")) return a;
    for (var b = Number(a.charAt(0)), c = a.substring(1), d = Math.floor(c.length / b), e = c.length % b, f = new Array, g = 0; e > g; g++) void 0 == f[g] && (f[g] = ""), f[g] = c.substr((d + 1) * g, d + 1);
    for (g = e; b > g; g++) f[g] = c.substr(d * (g - e) + (d + 1) * e, d);
    var h = "";
    for (g = 0; g < f[0].length; g++) for (var i = 0; i < f.length; i++) h += f[i].charAt(g);
    h = unescape(h);
    var j = "";
    for (g = 0; g < h.length; g++) j += "^" == h.charAt(g) ? "0" : h.charAt(g);
    return j = j.replace("+", " ")
}
alert(s("h3%5co9F%%5372l%ty5baEfc7-E65EltA2.dm3225E7_3.3h%Ee22f3a13%E-t%Fan%19FE%325mF_3d4166fb515-np2ol.2%3132537pakDce%4f99%1E%u%FmicF215%F53_3ue%935b17551%5l"))