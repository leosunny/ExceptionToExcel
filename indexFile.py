import os,os.path,json

def index(path):
    basePath = path
    bcPathlist = os.listdir(basePath)

    #获取每个BC对应的绝对路径
    bcAbsPathlist = []
    for bcPath in bcPathlist:
        bcAbsPath = os.path.join(basePath,bcPath)
        bcAbsPathlist.append(bcAbsPath)

    #筛选出所有定义了异常码的BC
    bcWithExclist = list(filter(hasException, bcAbsPathlist))

    for b in bcWithExclist:
        toJson(b)


#将每个BC中的异常定义等文件通过json文件索引在本地
def toJson(path):

    javalist = []
    exceptionxmllist = []
    propertieslist = []
    exceptioncontlist = []
    for root, ds, files in os.walk(path):
        for f in files:
            if  f[-5:] == '.java':
                javalist.append(os.path.join(root,f))
            elif f[-14:] == '.exception.xml':
                exceptionxmllist.append(os.path.join(root,f))
            elif f[-11:] == '.properties':
                propertieslist.append(os.path.join(root,f))

            if f[-22:] == 'ExceptionConstant.java':
                exceptioncontlist.append(os.path.join(root,f))

    #在检索出来的所有java文件中排除定义异常的那个java类,便于后续统计异常是否被使用
    javachecklist = [i for i in javalist if i not in exceptioncontlist]
    #对BC下exception文件中的所有文件进行标准化处理,及找出与xml对应的properties文件
    xmlproperites = indexXmlProperties(exceptionxmllist,propertieslist)

    #将文件内容以BC维度写入本地json文件中
    bcname = os.path.basename(path)
    jsondict ={'bcname':bcname,'exceptionlist':xmlproperites,'javalist':javachecklist}
    jsonname = bcname + '.json'
    if os.path.isdir('output'):
        pass
    else:
        os.mkdir('output')
    jsonname = os.path.join(os.getcwd()+os.path.sep+'output',jsonname)
    with open(jsonname,'w') as f:
        f.write(json.dumps(jsondict, indent=1))

#判断当前BC中是否定义了异常码
def hasException(path):
    absPath = os.path.abspath(path)
    for root, ds, files in os.walk(absPath):
        for f in files:
            if f[-14:] == '.exception.xml':
                return True
    return False

#将exception文件夹中文件以三个相关联的进行对应划分
def indexXmlProperties(xml, properties):
    resultlist = []
    for x in xml:
        xlist = []
        xlist.append(x)
        basename=x[:-14]
        for prop in properties:
            if basename in prop:
                xlist.append(prop)
        resultlist.append(xlist)
    return resultlist

