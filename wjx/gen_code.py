import js2py
import requests
import re

curID = 39164517
submittype = 1
data = requests.get('https://www.wjx.cn/jq/%s.aspx?from=timeline' % curID)
hlv = 1
data = data.text
jqnonce = re.search('jqnonce="(.*?)"', data).group(1)
rndnum = re.search('rndnum="(.*?)"', data).group(1)
starttime = re.search('starttime="(.*?)"', data).group(1)
t = 1
js_res = js2py.eval_js('''
function gen(jqnonce, ktimes) {
    jqnonce = encodeURIComponent(jqnonce);
    var c, d, e, b = ktimes % 10;
    var a = jqnonce;
    for (0 == b && (b = 1), c = [], d = 0; d < a.length; d++) e = a.charCodeAt(d) ^ b,
        c.push(String.fromCharCode(e));
    var jqsign = encodeURIComponent(c.join(""));
    return jqsign;
}
''')
ktimes = 50
print(js_res(jqnonce, ktimes))
