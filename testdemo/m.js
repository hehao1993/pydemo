function kuadu(num) {
	num = num + ""
	var s = num.split("").sort(),
		max = Math.max.apply(null, s),
		min = Math.min.apply(null, s),
		r = max - min
	return r
}

function hewei(num) {
	num = num + ""
	var s = num.split("")
	var h = 0
	for (var i in s) {
		h = h + parseInt(s[i])
	}
	h = h.toString()
	return h.substr(h.length - 1, 1)
}

function housan(num) {
	var leixing_a = num.substr(-1, 1);
	var leixing_b = num.substr(-2, 1);
	var leixing_c = num.substr(-3, 1);
	var leixing_d = 0;
	if (leixing_a == leixing_b)
		leixing_d++;
	if (leixing_b == leixing_c)
		leixing_d++;
	if (leixing_c == leixing_a)
		leixing_d++;
	switch (leixing_d) {
		case 0:
			return "组六";
		case 1:
			return "组三";
		case 3:
			return "豹子";
	}
}

function vues(num) {
    var ret = "";
    if (String(num).length == 5) {
        var k = "跨度" + kuadu(num);
        var h = "合尾" + hewei(num);
        var s = housan(num);
        ret = [k, h, s].join(" ")
    }
    return ret
}