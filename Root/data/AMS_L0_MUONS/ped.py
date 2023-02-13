#given the name of a pedestal file, open file, average over all events for each channel, return vector of averages
#start by taking input args but eventually use as a function
#use readAMS as guide

from socketserver import ForkingUDPServer
import ROOT as root
import numpy as np
import matplotlib.pyplot as plt
import sys

#pedFile = sys.argv[1]

def computePed(pedFile):
    #open pedestal file
    '''
    INPUT: string name of a pedestal file
    OUTPUT: np array 1xn where n is number of channels, each element is average value for channel
    GOAL: computes that channel average for a pedestal run--therefore gets the average "offset" value for each channel
    '''
    try:
        f = root.TFile.Open(pedFile)
    except:
        print("Error opening pedestal file")
        sys.exit(1)
        
    if f:
        print("Pedestal file opened successfully")
        #open tree
        try:
            tree = f.Get("raw_events")  #Tree name is "raw_events"
            if tree:
                #get entries
                print("raw_events tree opened successfully")
                nentries = tree.GetEntries()
                print("Number of entries: ", nentries)
                #get branch
                branch = tree.GetBranch('RAW Event')
                vector = root.vector('unsigned short')()
                tree.SetBranchAddress("RAW Event", vector)
                #check size of branch
                tree.GetEntry(0)
                #convert to numpy array
                array = np.asarray(vector)
                print("Entry 0 shape: ", array.shape)
                size = array.shape[0]   #number of channels
                print("Size: ", size)
                #array to store averages
                avgs = np.zeros(size)
                
                #now loop over each entry and add values to avgs element-wise
                #then divide by nentries
                for i in range(nentries):
                    #get the entry
                    #print("Entry #: ", i)
                    tree.GetEntry(i)
                    #convert to numpy array
                    arr = np.asarray(vector)
                    #divide by nentries first
                    arr = arr / nentries
                    #add to averages (pre-divided! bc maybe will save space)
                    avgs = np.add(avgs, arr)
                #now the avgs array will have the pedestral averages for all [size] channels
            else:
                print("Error opening tree")
                sys.exit(1)
        except:
            print("Get failed")
            sys.exit(1)
    else:
        print("Error opening file")
        sys.exit(1)
    return avgs
            
            
#run function
a = computePed("001_conv.root")
print(a)
print(len(a))

#good

#to do: make an option to plot the pedestal vs channel number
