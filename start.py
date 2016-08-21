import os

from indexFile import *
from toExcel import *

codePath = r"/Users/hhxi/GitProjects/ExceptionToExcel/TestData/Foundation"

#将指定代码根路径下的所有java文件、异常定义文件及语言文件进行索引
index(codePath)
print("已完成文件索引")


#将本地索引中的文件中的异常信息输出到excel表中
toExcel()
print("已完成将异常码定义及语言信息输出到Excel表中")

