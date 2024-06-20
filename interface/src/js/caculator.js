/* 下面函数用于计算财产案件的案件受理费
	【法律依据】
	《诉讼费用交纳办法》（中华人民共和国国务院令第481号，以下略）第十三条
	案件受理费分别按照下列标准交纳：
	（一）财产案件根据诉讼请求的金额或者价额，按照下列比例分段累计交纳：
　　1.不超过1万元的，每件交纳50元；
　　2.超过1万元至10万元的部分，按照2.5％交纳；
　　3.超过10万元至20万元的部分，按照2％交纳；
　　4.超过20万元至50万元的部分，按照1.5％交纳；
　　5.超过50万元至100万元的部分，按照1％交纳；
　　6.超过100万元至200万元的部分，按照0.9％交纳；
　　7.超过200万元至500万元的部分，按照0.8％交纳；
　　8.超过500万元至1000万元的部分，按照0.7％交纳；
　　9.超过1000万元至2000万元的部分，按照0.6％交纳；
　　10.超过2000万元的部分，按照0.5％交纳。 
*/
function litigationFeeCaculator(litigantAmount) {
	var result = 0;
	if (litigantAmount < 0) {
		return "error";
	} else if (litigantAmount == 0) {
		result = 0;
	} else if (litigantAmount > 0 && litigantAmount <= 10000) {
		result = 50;
	} else if (litigantAmount > 10000 && litigantAmount <= 100000) {
		result = litigantAmount * 0.025 - 200;
	} else if (litigantAmount > 100000 && litigantAmount <= 200000) {
		result = litigantAmount * 0.02 + 300;
	} else if (litigantAmount > 200000 && litigantAmount <= 500000) {
		result = litigantAmount * 0.015 + 1300;
	} else if (litigantAmount > 500000 && litigantAmount <= 1000000) {
		result = litigantAmount * 0.01 + 3800;
	} else if (litigantAmount > 1000000 && litigantAmount <= 2000000) {
		result = litigantAmount * 0.009 + 4800;
	} else if (litigantAmount > 2000000 && litigantAmount <= 5000000) {
		result = litigantAmount * 0.008 + 6800;
	} else if (litigantAmount > 5000000 && litigantAmount <= 10000000) {
		result = litigantAmount * 0.007 + 11800;
	} else if (litigantAmount > 10000000 && litigantAmount <= 20000000) {
		result = litigantAmount * 0.006 + 21800;
	} else if (litigantAmount > 20000000) {
		result = litigantAmount * 0.005 + 41800;
	}
	// 取两位小数
	result = result.toFixed(2);

	return result;
}


/* 
下面函数用于计算执行费
	【法律依据】
 	《诉讼费用交纳办法》第十四条（一）
		依法向人民法院申请执行人民法院发生法律效力的判决、裁定、调解书，仲裁机构依法作出的裁决和调解书，公证机关依法赋予强制执行效力的债权文书，申请承认和执行外国法院判决、裁定以及国外仲裁机构裁决的，按照下列标准交纳：
　			1.没有执行金额或者价额的，每件交纳50元至500元。
 　			2.执行金额或者价额不超过1万元的，每件交纳50元；
 				超过1万元至50万元的部分，按照1.5％交纳；
				超过50万元至500万元的部分，按照1％交纳；
				超过500万元至1000万元的部分，按照0.5％交纳；
				超过1000万元的部分,按照0.1％交纳。 
			3.符合民事诉讼法第五十五条第四款规定，未参加登记的权利人向人民法院提起诉讼的，按照本项规定的标准交纳申请费，不再交纳案件受理费。
*/
function executionFeeCaculator(executionAmount) {
	var result = 0;
	if (executionAmount < 0) {
		return "error";
	}
	if ((executionAmount > 0) && (executionAmount < 10000)) {
		result = 50
	}
	else if ((executionAmount >= 10000) && (executionAmount <= 500000)) {
		result = executionAmount * 0.015 - 100
	}
	else if ((executionAmount >= 500000) && (executionAmount <= 5000000)) {
		result = executionAmount * 0.01 + 2400
	}
	else if ((executionAmount >= 5000000) && (executionAmount <= 10000000)) {
		result = executionAmount * 0.005 + 24700
	}
	else if (executionAmount > 10000000) {
		result = executionAmount * 0.001 + 77400
	}
	// 取两位小数
	result = result.toFixed(2);
	return result;
}

/*
下面函数用于计算保全申请费
	【法律依据】
	《诉讼费用交纳办法》第十四条（二）
	申请保全措施的，根据实际保全的财产数额按照下列标准交纳：
　　	财产数额不超过1000元或者不涉及财产数额的，每件交纳30元；
		超过1000元至10万元的部分，按照1%交纳；
		超过10万元的部分，按照0.5％交纳。
		但是，当事人申请保全措施交纳的费用最多不超过5000元。
*/
function preservationFeeCaculator(preservationAmount) {
	var result = 0;
	if (preservationAmount < 0) {
		// 如果输入值小于0，返回错误
		return "error";
	}
	// 财产数额不超过1000元或者不涉及财产数额的，每件交纳30元；
	if ((preservationAmount > 0) && (preservationAmount <= 1000)) {
		result = 30
	}
	// 超过1000元至10万元的部分，按照1%交纳；
	// 下面的公式相当于在1000以下的部分少算了（30-1000*1%）=20元，所以在这里加上20元
	else if ((preservationAmount > 1000) && (preservationAmount <= 100000)) {
		result = preservationAmount * 0.01 + 20
	}
	// 超过10万元的部分，按照0.5％交纳； 
	// 下面的公式用总数直接乘0.5%，相当于在1000-10万之间的部分少算了99000x(1%-0.5%)=495元，在1000以下的部分少算了（30-1000*0.5%）=25元
	// 所以总共少算了520元，故在这里加上520元
	else if (preservationAmount > 100000) {
		result = preservationAmount * 0.005 + 520
	}
	// 但是，当事人申请保全措施交纳的费用最多不超过5000元。
	if ((result >= 5000)) {
		result = 5000
	}
	// 取两位小数
	result = result.toFixed(2);

	return result;
}

// 导出
export {
	litigationFeeCaculator,
	executionFeeCaculator,
	preservationFeeCaculator,
};
