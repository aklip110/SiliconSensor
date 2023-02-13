from socketserver import ForkingUDPServer
import ROOT as root
import numpy as np
import matplotlib.pyplot as plt
import sys

# open .root file
try:
    f = root.TFile.Open(sys.argv[1])
except:
    print("Error opening file")
    sys.exit(1)

if f:
    print("File opened successfully")
    # open raw data tree
    try:
        tree = f.Get("raw_events")
        if tree:
            print("Tree opened successfully")
            # get number of entries
            nentries = tree.GetEntries()
            print("Number of entries: ", nentries)

            # get data from tree
            branch = tree.GetBranch('RAW Event')
            vector = root.vector('unsigned short')()
            tree.SetBranchAddress("RAW Event", vector)

            figure = plt.figure()
            ax = figure.add_subplot(111)

            # loop over all entries and plot
            for i in range(nentries):
                if i % 100 == 0:
                    print("Entry: ", i)
                    
                tree.GetEntry(i)
                array = np.asarray(vector)
                print(array.shape)

                ax.set_title("AMS Raw Data Event: " + str(i))
                ax.set_xlabel("Channel")
                ax.set_ylabel("ADC")
                ax.set_xlim(0, 1024)
                ax.xaxis.set_major_locator(plt.MultipleLocator(64))
                ax.grid(True)
                ax.plot(array)
                plt.pause(0.0001)
                ax.clear()

        else:
            print("Error opening tree")
            sys.exit(1)
    except:
        print("Error opening tree")
        sys.exit(1)
else:
    print("Error opening file")
    sys.exit(1)
