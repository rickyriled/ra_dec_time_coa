import argparse
import os
import numpy as np
from configparser import ConfigParser
import json
import sys


def ra_dec_builder(ra_n, dec_n, N):
    

    print("make ra_dec folder...")   #### 
    
    #create data folder, link/import important files
    os.chdir("dirs_folder")
    name=str(ra_n)+"_"+str(dec_n)
    os.mkdir(name)
    os.chdir(name)
    os.system("ln -s  ../../data_and_methods/get_injection_times.py")
    os.system("ln -s  ../../data_and_methods/create_datafile.py")
    os.system("cp ../../data_and_methods/aligo_O4high_extrapolated.txt .")
    os.system("cp ../../data_and_methods/avirgo_O4high_NEW.txt .")
    os.system("cp ../../data_and_methods/inj_config.ini .")
    
    print("parser config...")
    #edit the inj_config file
    parser = ConfigParser()
    parser.read('inj_config.ini')
    RA=str(2*np.pi*(ra_n/N))
    DEC=str(np.pi*(dec_n/N))
    parser.set('extrinsic', 'ra', RA)
    parser.set('extrinsic', 'dec', DEC)
    with open('inj_config.ini', 'w') as config_file:
        parser.write(config_file)
    
    print("creating waveforms...")
    #create the waveform data for L1/H1/V1
    os.system("python create_datafile.py -c  inj_config.ini -o injection.hdf5")
    
    print("getting coa times...")
    #find the max times and send it to the output folder
    
    #import get_injection_times
    import get_injection_times as gert
    DETS=["L","V","H"]

    for DET in DETS: 
        print("measuring {}1...".format(DET))  
        frame_file="{}-{}1_STRAIN-1264068796-870.gwf".format(DET,DET)
        channel="{}1:SIM-STRAIN".format(DET)
        coa_time=gert.get_trigger_time("inj_config.ini", frame_file, channel)
    
        print("dumping {}1...".format(DET))
        key_ra_dec=str(ra_n)+"_"+str(dec_n)
        COA_DIC={key_ra_dec : coa_time }
        with open("../../indiv_timekey_folder/{}1_keys/{}1_{}_{}.json".format(DET,DET,str(ra_n),str(dec_n)), "w") as f:
            json.dump(COA_DIC, f, indent=2, sort_keys=True)

    os.chdir("../../")
    print("done!")

if __name__=="__main__":

    #sys.stdout = open(os.devnull, 'w')
    print("entering parser...")
    parser = argparse.ArgumentParser()
    parser.add_argument('--ra_n', type=int)
    parser.add_argument('--dec_n', type=int)
    parser.add_argument('--N', type=int)

    args = parser.parse_args()

    print("entering ra_dec_builder")
    ra_dec_builder(args.ra_n, args.dec_n, args.N)    #write strings input with quotes
    
    #enables print
    #sys.stdout = sys.__stdout__
    print("done!")
    
