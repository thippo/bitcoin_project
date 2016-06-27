import pickle

error_dict={}

with open('a.th') as A:
    for i in A.readlines():
        lin=i.strip().split()
        error_dict[int(lin[0])]=lin[1]

B=open('error.pkl','wb')
pickle.dump(error_dict,B)
B.close()