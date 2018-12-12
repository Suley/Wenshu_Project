var obj = require('./docid.js');

var js = obj.GetJs('w61aS8KOwoMwDD0LwqjCi0TCjMOmAsKowqseYcKWVsKEKsO6YzFlwpQywqvCqncfwqDCiMOySQMdAk3DqcKTwpArEsObw49+ThwidXHCiDbDm1MowqPCn2TDucKVw4jDqMK4w7/DnMOJw7h7dVjDi1XCvMOZMsOPw7FIQFgtPkACw4R7wqzCkDkkw7Imw5sVXQnCtcKFAMOvYBYCw5UDYyguEgYnYAd0IHXDpA8Sw4AEwohBw5bDoAnDiSElVAACC8OBQsOBfT9YwrphfDwlw7I3TGLDqcO6AQUifRjDs8OOwpdMwq18w44XTldLSsKFEB5zw7IJTnXCn8OZRMO3TMO+wrrCuMO9O8KBWDbCnGrCkMKTw43CkMKgw7TCpwFYV3cKwoPDu2DCjcK4wpXCusOawpjCqsOew5TDoyVUHnXCm8KiVgjDihw0wr7DiyDDuzFaecOtDMK7wqfDhiNqD8Orw77Dj2DCgMOVUFMjw7bCncO7w4TCgHvDg8KeXsOAXcK5F8KLwo5FeQcZFW1cw4cTeMKfCmLCshXCrwXCp1rCp8Kkw47Crm8ew5lswrLDtw/CnnkXFMOew63DgTEHw7bChMOWwq3CjWXDnMKdNcOOw6Fnw4F3wo1hw5gnw4U0PcK2wqE9NCsnL1M8TRTDjcODwr/Dl33Dk0rCvhTDl8OLVnJUw6vDoMOqw5HCqkMacEHCtsKIPMOEU8KBw6XCjMO7fw==')
var js_objs = js.split(';;');
var js1 = js_objs[0] + ';';
var js2 = /_\[_\]\[_\]\((.*?)\)\(\);/.exec(js_objs[1])[1];
var key = /\"([0-9a-z]{32})\"/.exec(obj.EvalKey(js1,js2))[1];


var docid = obj.DecryptDocID(key, 'HcKOw4cRBDEMw4NaUsKyLD5lwoXDvkvCusKde8KDQ8KgQsKoUMOhw6RPT8OhbcOoE8KwYcOFET3ClBvDuXJrwoYkOcKPfhNqaj/DmsKSaioXw4PCsVbDpm5qVxbCt2EMPQ7CjcKhfh9MwrIgwqbCkMKBHHZRAsOvDcOMPFzDr8K4wpnDj8OvZcKbw5vDkcONw6nDi0HCsxbDhcK6ecKOOcKJw5XDmcKZw5LDr8O+w4vDngnDvcK4T3cZw7DDr8KFw5V8UsOkJlvDs8O7AQ==')
console.log(docid)

function decrypt_line()










