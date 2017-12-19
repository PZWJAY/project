import pandas as pd
from stmp import *
import xgboost as xgb
from sklearn.cross_validation import train_test_split
import numpy as np
from xgboost.sklearn import XGBClassifier
from sklearn.grid_search import GridSearchCV

def createDataFrame(filename,type,df): #filename:文件名，type:文件类型（0表示正文本，1表示负文本），df为DataFrame)
    cnt = 0
    file = open(filename,'r',encoding='UTF-8')
    for line in file.readlines():
        line = line.strip()
        line = list(line.split(' '))
        tmp = dict()
        for i in range(0,len(line),2):
            tmp[line[i]] = float(line[i+1])
        tmp['label'] = type
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
    #df = pd.read_csv('filedf.csv')
    df = df.fillna(0.0)
    df_test = pd.DataFrame(columns=chac)
    df_test = createDataFrame('posFileTest.txt',0,df_test)
    df_test = createDataFrame('negFileTest.txt',1,df_test)
    df_test.to_csv('fileTest.csv',index=None)
    df_test.fillna(0.0)

    train_xy,val = train_test_split(df,test_size=0.3,random_state=1)
    train_y = train_xy.label
    train_x = train_xy.drop(['label'],axis=1)
    val_y = val.label
    val_x = val.drop(['label'],axis=1)

    xgb_val = xgb.DMatrix(val_x,label=val_y)
    xgb_train = xgb.DMatrix(train_x,label=train_y)
    xgb_test = xgb.DMatrix(df_test)

    params={
        'booster':'gbtree',
        'silent':0,
        'eta':0.07,
        'min_child_weight':1,
        'max_depth':12,
        #'max_leaf_nodes':
        'gamma':0.3,
        'subsample':0.8,
        'colsample_bytree':0.5,
        'lambda':4,
        'objective':'binary:logistic',
        'eval_metric':'error',
    }
    '''
    param_test1 = {
        'lambda':[i for i in range(0,5)]
    }
    gsearch1 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1,n_estimators=140,max_depth=12,
                                                    min_child_weight=1,gamma=0,subsample=0.7,objective='binary:logistic',
                                                    seed=27),param_grid=param_test1,scoring='roc_auc',
                            n_jobs=4,iid=False,cv=5)
    gsearch1.fit(train_x,train_y)
    print(gsearch1.grid_scores_)
    print(gsearch1.best_params_)
    print(gsearch1.best_score_)
    sendMail()
    '''
    plst = list(params.items())
    num_rounds = 5000 #迭代次数
    watchlist = [(xgb_train,'train'),(xgb_val,'val')]
    model = xgb.train(plst,xgb_train,num_rounds,watchlist,early_stopping_rounds=200)
    model.save_model('xgb2.model')
    print("best best_ntree_limit", model.best_ntree_limit)
    preds = model.predict(xgb_test,ntree_limit=model.best_ntree_limit)
    np.savetxt('xgb_submission.csv',np.c_[range(1,len(df_test)+1),preds],delimiter=',',header='fildId,Label',comments='',fmt='%d')
    sendMail()
