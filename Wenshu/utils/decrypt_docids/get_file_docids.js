var obj = require('./docid.js');

function get_line_ids(runeval, cids){
    var js = obj.GetJs(runeval);
    var js_objs = js.split(';;');
    var js1 = js_objs[0] + ';';
    var js2 = /_\[_\]\[_\]\((.*?)\)\(\);/.exec(js_objs[1])[1];
    var key = /\"([0-9a-z]{32})\"/.exec(obj.EvalKey(js1, js2))[1];

    var lineids = new Array();
    for(var i = 0; i < cids.length; i++) {
        var docid = obj.DecryptDocID(key, cids[i]);

        lineids.push(docid);
    }
    return lineids;
}

function get_file_ids(text) {
    lines = text.split('\n');

    ids_array = new Array();
    for(var index = 0; index < lines.length - 1; index++) {
        allobj = lines[index].split(',');

        lineids = get_line_ids(allobj[0], allobj.slice(1));
        for(var i = 0; i < lineids.length; i++) {
            ids_array.push(lineids[i]);
        }
    }
    return ids_array;
}


//
//var fs = require('fs');
//var data = fs.readFileSync('./2001-01-01.txt');
//
//var data_str = data.toString();
//
//var iwant = get_file_ids(data_str);


