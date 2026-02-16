#coding=utf-8

def GetItemId(item):
    idx = item.find("-")
    return item[idx + 1 : ]