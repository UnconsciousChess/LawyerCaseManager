// 导入区域代码（用json）
import areaCodeArray from "../../../data/public/CitizenIdentificationAreaCode.json" assert {type: "json"};

// 该函数用来检验身份证中的出生日期是否合法
const checkBirthdayValid = (birthday) => {
    // 格式化传入的日期格式为 yyyy-mm-dd
    const serializedBirthday = `${birthday.slice(0, 4)}-${birthday.slice(4,6)}-${birthday.slice(6)}`;
    // 将日期字符串转换为日期对象
    const birthdayDate = new Date(serializedBirthday).getTime();
    // 如果日期格式不正确，则返回false
    if (isNaN(birthdayDate)) {
        return false;
    }
    // 获取当前时间
    const currentTime = new Date().getTime();
    // 如果出生日期大于当前时间，则返回false
    if (birthdayDate > currentTime) {
        return false;
    }
    // 如果通过了上面的检验，则返回true
    return true;
};

// 以下是用来检验身份证号码的函数
function checkIdNumberValid(idNumber) {
	// 默认不通过
	let passOrNot = false;

	// 检验长度是否为18位，不是则直接返回false
	if (idNumber.length != 18) {
        console.log("长度不为18位");
        return passOrNot;
    }

    // 18位身份证号码正则
    let personIdNumberReg =
        /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dxX]$/;
    // 如果通过了正则表达式的检验，则进行校验位的检测，否则直接返回false
    if (!personIdNumberReg.test(idNumber)) {
        console.log("正则表达式不通过");
        return passOrNot;
    }

    // 将身份证前6位的地区代码提取出来
    let areaCode = Number(idNumber.slice(0, 6));
    // 判断地区代码是否合法,如果合法进入下一步
    if (areaCodeArray.indexOf(areaCode) == -1) {
        console.log("地区代码不合法");
        return passOrNot;
    }

    // 将身份证中间8位的生日部分提取出来，放入函数中checkBirthdayValid检验
    let birthday = idNumber.slice(6, 14);
    // 如果生日合法，则进入下一步校验码计算
    if (checkBirthdayValid(birthday) == false) {
        console.log("生日不合法");
        return passOrNot;
    }

    // 下面是校验码的计算

    // 在输入的身份证号码中得到校验码
    let idCheckNum = idNumber[17];
    // 设定加权因子
    let factors = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
    // 设定校验码换算关系
    let charSet = "10X98765432";

    let ci;
    let wi;
    let sum = 0;

    // 根据校验码式（1）算出总和
    for (let i = 0; i < 17; i++) {
        ci = parseInt(idNumber[i]);
        wi = factors[i];
        sum += ci * wi;
    }

    let caculatedCheckNum;
    // 得到经过计算的出来的校验码
    caculatedCheckNum = sum % 11;

    // 如果输入的校验码与以计算出来的校验码为index，在字符集中对应的value相等，则通过
    if (idCheckNum == charSet[caculatedCheckNum]) {
        passOrNot = true;
        console.log("校验码通过，全部通过");
        return passOrNot;
    }
    // 否则，如果校验码为X，且计算出来的校验码为10，则通过
    else{
        if (idCheckNum == "X" && caculatedCheckNum == 10) {
            passOrNot = true;
            console.log("校验码通过，全部通过");
            return passOrNot;
        }
        // 否则，返回false
        console.log("校验码不通过");
        return passOrNot;
    }

}


// 法律依据：GB 32100-2015《法人和其他组织统一社会信用代码编码规则》
function checkEnterpriseIdNumberValid(enterpriseIdNumber) {
	// 默认值为不通过检验
	let passOrNot = false;

	// 当长度18位时
	if (enterpriseIdNumber.length == 18) {
		// 18位统一社会信用代码正则
		let enterpriseIdNumberReg =
			/^[1-9A-HJ-NPQRTUWXY]{2}\d{6}[1-9A-HJ-NPQRTUWXY]{10}$/;
        // 如果通过了正则表达式的检验，则进行校验位的检测，否则直接返回false 
		if (enterpriseIdNumberReg.test(enterpriseIdNumber)) {
			// 4.1　结构
			// 设定字符集，不含I、O、S、V、Z
			// 统一代码由十八位的阿拉伯数字或大写英文字母（不使用I、O、Z、S、V）组成，
			// 包括第1位登记管理部门代码、第2位机构类别代码、第3位～第8位登记管理机关行政区划码、
			// 第9位～第17位主体标识码（组织机构代码）、第18位校验码五个部分。

            // 设定字符集，该字符集对应的序号即为附录A中的代码字符数值
			let charSet = "0123456789ABCDEFGHJKLMNPQRTUWXY";
			// 设定加权因子
			let factors = [
				1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28,
			];

			// 4.2.5　第18位：校验码 校验码使用阿拉伯数字或大写英文字母表示。
			// 校验码计算方法参照GB/T 17710。校验码按式（1）计算：
			let ci;
			let wi;
			let sum = 0;
			let checkNum = charSet.indexOf(enterpriseIdNumber[17]); // 从输入的字符串中获得校验码

			// 根据校验码式（1）算出总和
			for (let i = 0; i < 17; i++) {
				ci = charSet.indexOf(enterpriseIdNumber[i]);
				wi = factors[i];
				sum += ci * wi;
			}

			// 得到经过计算的出来的校验码
			caculatedCheckNum = 31 - (sum % 31);

			// 如果校验码相等，则通过
			if (checkNum == caculatedCheckNum) {
				passOrNot = true;
			}
			// 当 MOD 函数值为1，校验码应用符号Y表示；
			else if (caculatedCheckNum == 30 && checkNum == "Y") {
				passOrNot = true;
			}
			// 当 MOD 函数值为0，校验码用0表示。校验位代码字符集参见附录A。
			else if (caculatedCheckNum == 31 && checkNum == 0) {
				passOrNot = true;
			}
		}
	}
    // 最终返回结果
    return passOrNot;
}



// 导出上面的函数
export {checkIdNumberValid, checkEnterpriseIdNumberValid};


