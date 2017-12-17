import pandas as pd
from stmp import *

def createDataFrame(filename,type,df): #filename:文件名，type:文件类型（0表示正文本，1表示负文本），df为DataFrame)
    cnt = 0
    file = open(filename,'r',encoding='UTF-8')
    for line in file.readlines():
        line = line.strip()
        line = list(line.split(' '))
        tmp = dict()
        for i in range(0,len(line),2):
            tmp[line[i]] = float(line[i+1])
        tmp['class'] = type
        df = df.append(tmp,ignore_index=True)
        print(cnt)
        cnt += 1
    file.close()
    return df

if __name__=='__main__':
    chacFile = open('chacSet.txt','r',encoding='UTF-8')
    chac = chacFile.read()
    chacFile.close()
    chac = list(chac.split(' '))
    chac.append('class')
    df = pd.DataFrame(columns=chac)
    df = createDataFrame('posFile.txt',0,df)
    df = createDataFrame('negFile.txt',1,df)
    df.to_csv('filedf.csv',index=None)
    sendMail()