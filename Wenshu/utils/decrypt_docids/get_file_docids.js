var obj = require('./docid.js');

function (runeval, cids){
    var js = obj.GetJs(runeval)
    var js_objs = js.split(';;');
    var js1 = js_objs[0] + ';';
    var js2 = /_\[_\]\[_\]\((.*?)\)\(\);/.exec(js_objs[1])[1];
    var key = /\"([0-9a-z]{32})\"/.exec(obj.EvalKey(js1,js2))[1];

    for( var index = 0; index < cids.length; index++) {
        var docid = obj.DecryptDocID(key, cids[index]);
    }

}
