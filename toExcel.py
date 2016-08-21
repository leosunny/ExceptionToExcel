import os,os.path,json,xml.dom.minidom,xlrd,xlwt

#将异常吗定义及语言信息输出到excel表中
def toExcel():
    jsonpath = os.getcwd() + os.sep + 'output'
    jsonlist = os.listdir(jsonpath)

    #从json文件中获取已有的信息,主要是各文件的路径列表
    for bcjson in jsonlist:
        bcjsonpath = os.path.join(jsonpath,bcjson)
        with open(bcjsonpath) as f:
            exceptiondict = json.load(f)
        bcname = exceptiondict['bcname']
        exceptionlist = exceptiondict['exceptionlist']
        javalist = exceptiondict['javalist']

        expInJavalist = findExceptioninJavafiles(javalist)
        bcexceptionlist = readExceptioninXmlfiles(exceptionlist)
        saveExcel(bcname,bcexceptionlist)


def saveExcel(bcname,bcexceptionlist):
    excelname = 'common.xls'
    if os.path.isdir('output'):
        pass
    else:
        os.mkdir('output')
    excelname = os.path.join(os.getcwd() + os.path.sep + 'output', excelname)

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(bcname)

    #生成表头
    worksheet.write(0, 0, 'ID')
    worksheet.write(0, 1, 'Type')
    worksheet.write(0, 2, 'Name')
    worksheet.write(0, 3, 'Level')

    worksheet.write(0, 4, 'Title_zh')
    worksheet.write(0, 5, 'Title_en')
    worksheet.write(0, 6, 'Desc_zh')
    worksheet.write(0, 7, 'Desc_en')
    worksheet.write(0, 8, 'Help_zh')
    worksheet.write(0, 9, 'Help_en')

    for i in range(1,len(bcexceptionlist)+1):
        bcexception = bcexceptionlist[i-1]
        worksheet.write(i,0,bcexception['id'])
        worksheet.write(i,1,bcexception['type'])
        worksheet.write(i,2,bcexception['name'])
        worksheet.write(i,3,bcexception['level'])

        worksheet.write(i,4,bcexception['titleZH'])
        worksheet.write(i,5,bcexception['titleEN'])
        worksheet.write(i,6,bcexception['descZH'])
        worksheet.write(i,7,bcexception['descEN'])
        worksheet.write(i,8,bcexception['helpZH'])
        worksheet.write(i,9,bcexception['helpEN'])

    workbook.save(excelname)

#从java文件中获取所有的异常码,方便后续对比是否新增、删除异常码
def findExceptioninJavafiles(javalist):
    pass

#从xml及properties文件中读取异常码定义及语言信息,方便后续写入excel表中
def readExceptioninXmlfiles(exceptionlist):
    #记录同一个组件下不同xml文件中所有异常信息
    bcexceptionlist = []
    for filelist in exceptionlist:
        for f in filelist:
            if 'exception.xml' in f:
                xmlfile = f
            elif 'zh_CN.exception' in f:
                zhpropfile = f
            elif 'en_US.exception' in f:
                enpropfile = f
        zhpropdict = readProperties(zhpropfile,'zh_CN')
        enpropdict = readProperties(enpropfile)

        dom = xml.dom.minidom.parse(xmlfile)
        exceptioncol = dom.getElementsByTagName('Exception')
        bcexceptionlist.extend(getExcetpion(exceptioncol,enpropdict,zhpropdict))
    return bcexceptionlist

#整合异常码信息
def getExcetpion(exceptioncol,enpropdict,zhpropdict):
    # 解析单个异常xml中的异常
    exceptionlist = []
    for excep in exceptioncol:
        exceptiondict = {}

        exceptiondict['name'] = get_attrvalue(excep, "Name")
        exceptiondict['id'] = get_attrvalue(excep, 'Id')
        exceptiondict['level'] = get_attrvalue(excep, 'Level')
        exceptiondict['type'] = get_attrvalue(excep, 'Type')

        # 同时记录异常key及对应的中英文异常信息
        titlenode = get_xmlnode(excep, 'Title')
        exceptiondict['title'] = get_nodevalue(titlenode[0])
        exceptiondict['titleEN'] = enpropdict[exceptiondict['title']]
        exceptiondict['titleZH'] = zhpropdict[exceptiondict['title']]
        descnode = get_xmlnode(excep, "Description")
        exceptiondict['desc'] = get_nodevalue(descnode[0])
        exceptiondict['descEN'] = enpropdict[exceptiondict['desc']]
        exceptiondict['descZH'] = zhpropdict[exceptiondict['desc']]
        helpnode = get_xmlnode(excep, "HelpTips")
        exceptiondict['help'] = get_nodevalue(helpnode[0])
        exceptiondict['helpEN'] = enpropdict[exceptiondict['help']]
        exceptiondict['helpZH'] = zhpropdict[exceptiondict['help']]
        exceptionlist.append(exceptiondict)

    return exceptionlist


#读取properties文件中有效数据,过滤注释
def readProperties(propfile, lang = 'en_US'):
    with open(propfile,'r') as f:
        propcont = f.readlines()
    propcont = list(filter(washcont,propcont))

    propdict = {}
    for cont in propcont:
        contlist = str(cont).split('=')
        if lang == 'zh_CN':
            propdict[contlist[0]] = (contlist[1].strip('\n'))
        else:
            propdict[contlist[0]] = contlist[1].strip('\n')
    return propdict

#清洗xml中的数据,去除注释行、空行等
def washcont(cont):
    if str(cont).startswith('#') or cont == '\n':
        return False
    else:
        return True

#xml操作
def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index=0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node, name):
    return node.getElementsByTagName(name) if node else []

