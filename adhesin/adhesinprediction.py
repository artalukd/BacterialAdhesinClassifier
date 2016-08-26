#!/usr/bin/python
from myproject.settings import MEDIA_ROOT
# import numpy as np
# import sys
# from scipy import interp
# import pylab as pl
import pandas as pd
import datetime
from sklearn.externals import joblib
from pydpi.pypro import PyPro  # from Prediction_protocol.py
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold
from django.http import Http404
'''
!!----------DO NOT DELETE-----------!!
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

!!----------DO NOT DELETE-----------!!
'''
from sklearn.metrics import *
# import matplotlib.image as mpimg
# from tempfile import mkstemp #new
import os
from sklearn.ensemble import RandomForestClassifier

Selected_Descriptor = ['611', 'M', '_NormalizedVDWVD2025', '_SecondaryStrD1075', '_PolarizabilityD1001',
                       '_SolventAccessibilityD3001', '332', '653', 'S', 'APAAC13', '266']

class DC_CLASS(object):

    def Decriptor_generator(self, ps):
        protein = PyPro()
        protein.ReadProteinSequence(ps)
        DS_1 = protein.GetAAComp()
        # print len(DS_1)
        #DS_2 = protein.GetDPComp()

        # print len(DS_2)
        #DS_3 = protein.GetTPComp() # takes time
        # print len(DS_3)
        DS_4 = protein.GetTriad()

        DS_5 = protein.GetPAAC(lamda=5,weight=0.5) # takes time

        DS_6 = protein.GetAPAAC(lamda=5,weight=0.5) # takes time

        DS_7 = protein.GetCTD()

        DS_8 = protein.GetGearyAuto()

        DS_9 = protein.GetMoranAuto()

        DS_10 = protein.GetMoreauBrotoAuto()

        DS_11 = protein.GetQSO()
        
        DS_12 = protein.GetSOCN()

        DS_ALL = {}
        
        for DS in (DS_1,DS_4,DS_5,DS_6,DS_7,DS_8,DS_9,DS_10,DS_11,DS_12):
            DS_ALL.update(DS)
        # print len(DS_ALL)
        return DS_ALL

    def Return_DF(self,FASTA_list):
        values = []
        for f in FASTA_list:
            value = DC_CLASS().Decriptor_generator(f.sequence)
            values.append(value)
        df1 = pd.DataFrame(values) #pd ?

        return df1
        
    def main_p(self,FASTA_list):
        df1 =  DC_CLASS().Return_DF(FASTA_list)
        new_df = df1[Selected_Descriptor]
        return new_df

class PRED_CLASS(object):

    def data_gen(self, csv_path):
        df = pd.read_csv(csv_path)
        clm_list = []
        clm_list = list(df.columns)
        # print df #contains reduced_Data file
        X_data = df[clm_list[0:len(clm_list)-1]].values
        # print X_data
        y_data = df[clm_list[len(clm_list)-1]].values
        # print y_data #contains 0 and 1
        return X_data, y_data, clm_list   # train_x, train_y,train_l
    
    def Prediction(self,xtest, alg):
        #alg.fit(xdata,ydata)  # train_x, train_y
        b = alg.predict(xtest) # test_x
        pb = alg.predict_proba(xtest)
        pb2 = []
        for i  in pb:
            pb2.append(round(i[1],3))
        return b, pb2
    
    def main_process(self, FASTA_list,algo):
        add = os.path.join(MEDIA_ROOT, "algo/")
        add2 = os.path.join(MEDIA_ROOT, "reduced_Data.csv")
        xdata, ydata ,train_l = PRED_CLASS().data_gen(add2)
        ''' To generate the files in a new system for future use.

        RF = RandomForestClassifier(n_estimators=10)
        RF.fit(xdata,ydata)
        joblib.dump(RF, os.path.join(add, str("R"+".pkl")))
        LR = LogisticRegression()
        LR.fit(xdata,ydata)
        joblib.dump(LR, os.path.join(add, str("L"+".pkl")))
        GNB = GaussianNB()
        GNB.fit(xdata,ydata)
        joblib.dump(GNB, os.path.join(add, str("G"+".pkl")))
        KNB = KNeighborsClassifier()
        KNB.fit(xdata,ydata)
        joblib.dump(KNB, os.path.join(add, str("K"+".pkl")))
        DT = DecisionTreeClassifier()
        DT.fit(xdata,ydata)
        joblib.dump(DT, os.path.join(add, str("D"+".pkl")))
        SV = SVC(probability=True)
        SV.fit(xdata,ydata)
        joblib.dump(SV, os.path.join(add, str("S"+".pkl")))
       
        !!----------DO NOT DELETE-----------!!
        '''
        lst = ['R','L','G','K','D','S']
        if algo in lst:  
            al = joblib.load(os.path.join(add, str(algo+".pkl"))) 
        else:
             raise Http404("Error: Unexpected Request")
        test_x = DC_CLASS().main_p(FASTA_list)
        return PRED_CLASS().Prediction(test_x,al)
