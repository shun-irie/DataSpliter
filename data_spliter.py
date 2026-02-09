#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 11:20:19 2026

@author: irieshun
"""
import os
import tkinter.filedialog as tf
import pandas as pd
import numpy as np
#%%
def uiimport(num=41):
    fn = tf.askopenfilename()
    df = pd.read_csv(fn,header=num,encoding="cp932")
    return df,fn

path = os.getcwd()
with open(os.path.join(path,"BRANL.csv"),"r", encoding="cp932") as r:
    template = r.read()
newline_positions = [i for i, c in enumerate(template) if c == "\n"] #25から書き換え
df,fn = uiimport()
#%%
print("Which mode?? 1: single participant 2: two participants")
a = input("")
#%%
if a== "1":
    print("OK. divided to multiple files")
    chNum = int(len([c for c in df.columns if "Ch" in c])/3)
    print(f"Ch number is {chNum}")
    lastChNum = chNum%16
    if lastChNum==0:
        filesNum = int(chNum/16)
    else:
        filesNum = int(chNum/16)+1
    print(f"Split into {filesNum} files")
    dataList = []
    for i in range(filesNum):
        ChList = []
        for count in range(16):
            if i*16+count+1<= chNum:
                ChList.extend([f"Ch{i*16+count+1}(O)",f"Ch{i*16+count+1}(D)",f"Ch{i*16+count+1}(O+D)"])
        temp_array = np.array(df[ChList])
        evt = np.asarray(df["evt"]).reshape(-1, 1)   # (N,) -> (N,1)

        if temp_array.shape[1] != 48:
            pad = max(0, 48 - temp_array.shape[1])  # 念のため
            temp_array = np.hstack((
                evt,
                temp_array,
                np.zeros((temp_array.shape[0], pad))
            ))
        else:
            temp_array = np.hstack((evt, temp_array))

        dataList.append("\n".join(",".join(map(str, row)) for row in temp_array))
    for i,d in enumerate(dataList):
        outPath = f"{fn[0:-4]}_{i+1}.csv"
        with open(outPath,"w",encoding="cp932") as w:
            w.write(template[0:newline_positions[25]+1]+d)
        
    

    
