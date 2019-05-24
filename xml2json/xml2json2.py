#!/usr/bin/python
# -*- coding: utf-8 -*-
#Function:Xml_To_Json
#version 1.1
#Author: Herman
#Date: 2018-06-01
#Usage: python Xml_To_Json.py xmlfile_dir >> tar_dir

import xmltodict;
import json;
import sys;

def pythonXmlToJson():
    with  open(sys.argv[1], 'r') as f:
        xmlStr = f.read()

    convertedDict = xmltodict.parse(xmlStr);
    jsonStr = json.dumps(convertedDict, indent=1);
    print(jsonStr)

if __name__=="__main__":
    pythonXmlToJson();