#to be changed: string appended to pedVals line 16, number of padded zeros line 38, file name line 38, ranges in lines 54, 69

from socketserver import ForkingUDPServer
import ROOT as root
import numpy as np
import matplotlib.pyplot as plt
import sys
from ped import computePed

def detNrPed(pedNs, num):
    if num > pedNs[-1]:
        p = len(pedNs) - 1
    else:
        for i in range(len(pedNs) - 1):
            if (num > pedNs[i]) and (num < pedNs[i+1]):
                threshold = np.floor((pedNs[i+1] - pedNs[i]) / 2)
                if num < threshold:
                    p = i
                elif num >= threshold:
                    p = i + 1
    # want to return the index of the pedestal, not its file number
    return int(p)

pedVals = ["001", "088", "140", "206", "321", "405"]  #already strings
rangeVal = 1  #optional param (number of nearby files to use)
filNum = 407    #total number of files
chanNum = 1024   #total number of channels (1024)


#initialize an array to save pedestal values
pedAvgs = np.zeros((len(pedVals), chanNum))

print("pedestal files: ", pedVals)
for j in range(len(pedVals)):
    print("Pedestal file ", j+1, " of "+str(len(pedVals)))
    filName = pedVals[j] + "_conv.root"
    #call function from ped.py and save to row in array
    pedAvgs[j, :] = computePed(filName)
    
#pedAvgs stores the 1024 channel averages for all pedestal files--each row is a different file

#get floats
pedNums = np.zeros(len(pedVals))
for i in range(len(pedVals)):
    pedNums[i] = str.lstrip(pedVals[i])
    
#test detNrPed function
print(detNrPed(pedNums, 50))
print(detNrPed(pedNums, 40))
print(detNrPed(pedNums, 100))
 

#iterate through all files, pick which pedestal is closest,
for k in range(2,3):
    #skip pedestal values
    if not (k in pedNums):
        print("file: ", k)
        #determine nearest pedestal
        p = detNrPed(pedNums, k)
        print("pedestal index: ", p)
        #get filename
        fil = str(k).zfill(3) + "_conv.root"
        #open file
        f = root.TFile.Open(fil)
        tree = f.Get("raw_events")
        nentries = tree.GetEntries()
        branch = tree.GetBranch('RAW Event')
        vector = root.vector('unsigned short')()
        tree.SetBranchAddress("RAW Event", vector)
        #iterate through entries
        for l in range(2,10):
            tree.GetEntry(l)
            arr = np.asarray(vector)
            newArr = np.subtract(arr, pedAvgs[p, :])
            
            plt.plot(newArr)
            plt.title("Pedestal Subtracted")
            plt.xlabel("Channel Number")
            plt.ylabel("ADC Signal")
            plt.show()
            
            plt.plot(arr)
            plt.title("Raw Data")
            plt.xlabel("Channel Number")
            plt.ylabel("ADC Signal")
            plt.show()
            
        #for now lets stick to plotting arr and newArr

#question is where to save new info--ideally, will end up with final file for each raw data file

