import numpy as np
import csv
import math

# Mean Square Error
def MSE(y, t):
    return np.sum((y - t)**2) / 30.0

# Mean Absolute Error 
def MAE(y, t):
    return np.sum(abs(y-t)) / 30.0

# Root Mean Square Error
def RMSE(y, t):
    return math.sqrt(np.sum((y - t)**2)) / 30.0

with open('compare_model.csv') as f:
    f_csv = csv.reader(f)

    headers = next(f_csv)

    ori_arr = np.array([])
    test1_arr = np.array([])
    test2_arr = np.array([])

    for row in f_csv:
        ori = row[1]
        test1 = row[2]
        test2 = row[7]
        if(ori == '' or ori == 'null'):
            ori = '0'
        if(test1 == '' or test1 == 'null'):
            test1 = '0'
        if(test2 == '' or test2 == 'null'):
            test2 = '0'
        ori_arr = np.append(ori_arr, float(ori))
        test1_arr = np.append(test1_arr, float(test1))
        test2_arr = np.append(test2_arr, float(test2))
    print(ori_arr)
    print(test1_arr)
    print(test2_arr)
    mse_new = MSE(ori_arr, test1_arr)
    mse_old = MSE(ori_arr, test2_arr)
    mae_new = MAE(ori_arr, test1_arr)
    mae_old = MAE(ori_arr, test2_arr)
    rmse_new = RMSE(ori_arr, test1_arr)
    rmse_old = RMSE(ori_arr, test2_arr)
    print("MSE of new model: " + str(mse_new))
    print("MSE of old model: " + str(mse_old))
    print("MAE of new model: " + str(mae_new))
    print("MAE of old model: " + str(mae_old))
    print("RMSE of new model: " + str(rmse_new))
    print("RMSE of old model: " + str(rmse_old))