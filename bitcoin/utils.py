import pickle
import time
import numpy as np

error_dict=pickle.load(open('error.pkl','rb'))

def translate_error(error_json):
    return error_dict[error_json['error_code']]

def timestamp_to_time(stamp):
    timeArray = time.localtime(stamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime

def minimum_mean(minimum_list):
    return np.mean(minimum_list)