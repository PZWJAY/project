import xgboost as xgb
import pandas as pd
import numpy as np

if __name__=='__main__':
    test_xy = pd.read_csv('fileTest.csv')
    test_xy = test_xy.fillna(0)
    test_y = test_xy.label
    test_x = test_xy.drop(['label'],axis=1)
    test_x_Matrix = xgb.DMatrix(test_x,label=test_y)

    model = xgb.Booster(model_file='xgb2.model')
    #model.load_model('xgb2.model')

    preds = model.predict(test_x_Matrix)
    np.savetxt('xgb_submission.csv', np.c_[range(1, len(test_xy) + 1), preds], delimiter=',', header='fildId,Label',
               comments='', fmt='%d')