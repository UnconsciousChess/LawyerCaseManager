

// 定义一个异步函数，用于将输入传递给后端
async function sendInputToBackEnd(){
    // 从id为test-user-input的元素中获取输入，保存在input中
    const userInput = document.getElementById('save-dir').value;
    // 调用后端的sendInput函数，并传递input参数，结果保存在response中
    const response = await window.pywebview.api.generateArchiveDirectoryDocument(userInput);
    // 将后端返回的结果response显示在页面上，即id为response的元素
    document.getElementById('response').innerText = response;
}



// 定义一个异步函数，用于将输入案件原告等传递给后端
async function sendCaseToBackEnd(){
    // 读取一系列
    const userInput1 = document.getElementById('plaintiff-txt-dir').value;
    const userInput2 = document.getElementById('defendant-txt-dir').value;
    const userInput3 = document.getElementById('casefolder-save-dir').value;
    window.pywebview.api.generateCaseFolder(userInput1, userInput2, userInput3);
}