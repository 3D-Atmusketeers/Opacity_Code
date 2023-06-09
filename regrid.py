import numpy as np
import pandas as pd
from scipy import interpolate
import math

def find_nearest(array,value): #used to find the nearest wavelength 
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def regrid(start,end,name, path): 
    """
    Regrids an opacity file to specified wavelengths. 
    Arguments
    ---------
    start = Starting wavelength in microns. For example, if you want your file to be from 3 to 4 microns, 
                                                                you would set start = 3
    end = Ending wavelength in microns
    name = The name of the file you want regridded. Need to include the '.dat', for example: 'opacH2O.dat'
    temptype = Either '1' if temperature range is 100-3000K, '2' if temp range is 500-5000K
    path = Location of file(s)
    ---------
    Returns —— Regridded file. 
    """
    if end < start:           
        raise Exception("Your ending wl is shorter than your starting one, switch them!")
    
    header = pd.read_csv(name, delim_whitespace = True, header = 0, nrows=0).columns.tolist() #reads in header to determine temperature range
    
    if header == ['500.000', '600.000', '700.000', '800.000', '900.000', '1000.000', '1100.000', '1200.000', '1300.000', '1400.000', '1500.000', '1600.000', '1700.000', '1800.000', '1900.000', '2000.000', '2100.000', '2200.000', '2300.000', '2400.000', '2500.000', '2600.000', '2700.000', '2800.000', '2900.000', '3000.000', '3100.000', '3200.000', '3300.000', '3400.000', '3500.000', '3600.000', '3700.000', '3800.000', '3900.000', '4000.000', '4100.000', '4200.000', '4300.000', '4400.000', '4500.000', '4600.000', '4700.000', '4800.000', '4900.000', '5000.000']: 
        #this looks terrible but is the best way to do this
        codf =  pd.read_csv(name, delim_whitespace= True, header=0,dtype=np.float64, names=['P','500.000', '600.000', '700.000', '800.000', '900.000', '1000.000', '1100.000', '1200.000', '1300.000', '1400.000', '1500.000', '1600.000', '1700.000', '1800.000', '1900.000', '2000.000', '2100.000', '2200.000', '2300.000', '2400.000','2500.000', '2600.000', '2700.000', '2800.000', '2900.000', '3000.000', '3100.000', '3200.000', '3300.000', '3400.000', '3500.000', '3600.000', '3700.000', '3800.000', '3900.000', '4000.000', '4100.000', '4200.000', '4300.000', '4400.000', '4500.000', '4600.000', '4700.000', '4800.000', '4900.000', '5000.000'], skiprows=2)
        
        codf = pd.DataFrame(codf)
        
        offset = 28      #found from the lines above the first wavelength
        interval = 29    #found from the amount of numbers in between each wavelength value
        
    if header == ['100.000', '200.000', '300.000', '400.000', '500.000', '600.000', '700.000', '800.000', '900.000', '1000.000', '1100.000', '1200.000', '1300.000', '1400.000', '1500.000', '1600.000', '1700.000', '1800.000', '1900.000', '2000.000','2100.000', '2200.000', '2300.000', '2400.000', '2500.000', '2600.000', '2700.000', '2800.000', '2900.000', '3000.000']: 
        codf = pd.read_csv(name, delim_whitespace= True, header=0,dtype=np.float64, names=['P','100.000', '200.000', '300.000', '400.000', '500.000', '600.000', '700.000', '800.000', '900.000', '1000.000', '1100.000', '1200.000', '1300.000', '1400.000', '1500.000', '1600.000', '1700.000', '1800.000', '1900.000', '2000.000','2100.000', '2200.000', '2300.000', '2400.000', '2500.000', '2600.000', '2700.000', '2800.000', '2900.000', '3000.000'], skiprows=2)
        
        codf = pd.DataFrame(codf)
        
        offset = 13      #found from the lines above the first wavelength
        interval = 14    #found from the amount of numbers in between each wavelength value
    
    totallambda= int((len(codf) - offset)/interval) #calculates the total number of wavelength values are in 
                                                            #the originall data file
    
    wlvalstot=[]    #set up empty list

    for i in range(totallambda):
        x = codf.iloc[offset+interval*i,0]     #grabs each wavelength value
        wlvalstot.append(x)                   #appends the wavelength value to the list wlvalstot

    startindex = find_nearest(wlvalstot, start*1e-6)    #finds the index of the closest wavelength value to the lower limit 
                                                            #you are looking for 
        
    endindex = find_nearest(wlvalstot, end*1e-6)        #finds the index of the closest wavelength value to the upper limit
                                                            #you are looking for
    
    wlvalssm=wlvalstot[startindex:endindex]       #cuts your wavelength array down to just the indexes you want
    
    chunk= codf.loc[startindex*interval+offset:endindex*interval+offset,:] #creates a chunk which is just the wavelength range
                                                                                  #you wanted
        
    chunk.to_csv(path+name,index=False, sep=' ', float_format='%5.8E')  #rewrites the file to new subset 
    
    print(name, 'opacity file regridded')
    return 


