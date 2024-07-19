import time
import os,sys
import shutil


# 不要生成字节码
sys.dont_write_bytecode = True


# 对于传入的MergeList中的各文件名，将其转换为pdf文件，并将其合并为一个pdf文件
def MergeFiles( MergeList: list, MergeOutputName: str, FolderPath:str) -> str:
    # 导入第三方库-docx2pdf
    from docx2pdf import convert    
    # 文件计数器初始化
    MergeFileCount = 0

    for MergeFileDir in MergeList:            
        # 获取合并文件之前的时间
        beforeconverttime = time.time()
        # 如果是docx文件，则将其转换为pdf文件
        if MergeFileDir.split('.')[-1] == 'docx':
            # 定义输出文件的名称，为序号.pdf
            OutputFileName = str(MergeFileCount) + '.pdf'
            OutputPath = FolderPath + "\\" + OutputFileName
            # 目前使用的是docx2pdf库，但是感觉效率非常的低，后期需要修改
            convert(input_path=MergeFileDir,
                    output_path=OutputPath)

            print('第%d个文件转换完成，文件名：%s，耗时：%s秒' % 
                    (MergeFileCount+1,MergeFileDir.split("\\")[-1].split('.')[0],
                    str(round(time.time() - beforeconverttime ,2)))
                )
            # 合并完成后，文件计数器加1
            MergeFileCount += 1

        # 如果是pdf文件，则直接复制一份到输出文件夹
        elif MergeFileDir.split('.')[-1] == 'pdf':
            # 定义输出文件的名称，为序号.pdf
            OutputFileName = str(MergeFileCount) + '.pdf'
            OutputPath = FolderPath + "\\" + OutputFileName
            # 直接复制文件
            shutil.copy(MergeFileDir,OutputPath)
            # 合并完成后，文件计数器加1
            MergeFileCount += 1


    MergeBegin = time.time()
    # 导入第三方库-pypdf
    from pypdf import PdfWriter    #导入这个库需要5秒钟，不知道为什么
    # 合并部分将所有pdf文件合并为一个pdf文件
    merger = PdfWriter()   
    for i in range(MergeFileCount):
        merger.append(FolderPath + "\\" + str(i)+ '.pdf')
    # 写合并文件
    merger.write(FolderPath + "\\" + MergeOutputName + '.pdf')
    # 关闭合并的文件
    merger.close()

    print('合并文件耗时：%s秒' % str(round(time.time() - MergeBegin,2))
        )
    # 随后删除所有此前作为中间变量pdf文件
    for i in range(MergeFileCount):
        os.remove(FolderPath + "\\" + str(i)+ '.pdf')

    return "Success"

