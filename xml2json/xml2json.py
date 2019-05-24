#!/usr/bin/python
# -*- coding: utf-8 -*-
#Function:Xml_To_Json
#version 1.0
#Author: Herman

#需要用到的两个模块
import xmltodict;
import json;

#定义函数
def pythonXmlToJson():
    with  open('/users/gaohanghang/manner.xml', 'r') as f:
        xmlStr = f.read()

    convertedDict = xmltodict.parse(xmlStr);
    jsonStr = json.dumps(convertedDict, indent=1);

    with open('/users/gaohanghang/manner.json', 'w') as f:
        f.write(jsonStr)

    # print(jsonStr)


#执行函数
if __name__=="__main__":
    pythonXmlToJson();
