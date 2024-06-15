import numpy as np
import csv
import math

# Mean Square Error
def MSE(y, t):
    return np.sum((y - t)**2) / 36.0

# Mean Absolute Error 
def MAE(y, t):
    return np.sum(abs(y-t)) / 36.0

# Root Mean Square Error
def RMSE(y, t):
    return math.sqrt(np.sum((y - t)**2)) / 36.0

with open('compare.csv') as f:
    f_csv = csv.reader(f)

    headers = next(f_csv)

    ori_arr = np.array([])
    test1_arr = np.array([])
    test2_arr = np.array([])

    for row in f_csv:
        ori = row[8]
        test1 = row[2]
        test2 = row[4]
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
    mse_yolo = MSE(ori_arr, test1_arr)
    mse_centernet = MSE(ori_arr, test2_arr)
    mae_yolo = MAE(ori_arr, test1_arr)
    mae_centernet = MAE(ori_arr, test2_arr)
    rmse_yolo = RMSE(ori_arr, test1_arr)
    rmse_centernet = RMSE(ori_arr, test2_arr)
    print("MSE of Yolo: " + str(mse_yolo))
    print("MSE of CenterNet: " + str(mse_centernet))
    print("MAE of Yolo: " + str(mae_yolo))
    print("MAE of CenterNet: " + str(mae_centernet))
    print("RMSE of Yolo: " + str(rmse_yolo))
    print("RMSE of CenterNet: " + str(rmse_centernet))