import os 
import regrid
import shutil
import sys
import regrid

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n") 

print('This will add/remove opacity files to your folder and regrid the opacity files according to your start/end wavelengths.')

#Changes directory to be the place where you want opacity files to end up
os.chdir("../Spectra/DATA/")

#CHANGE THIS PATH
path = ('/home/ajwingat/EmissionforUndergrads/Spectra/')


#Lists current opacity files
print('Current opacity files are: \n'+str(os.listdir()))

#now it asks if you need to add any opacity files to the folder
add = query_yes_no('First, do you need to add any opacity files to the list?')

if add == True:
    #Here it asks for names of elements to be added. Please respond with "O2" rather than "opacO2.dat" or "O2_hires". Other 
                        #parameters later specify the rest
    files_add = input("Enter names of elements of opacity files needed to be added, seperated by commas (NO SPACES!!) \n also please enter 'O2' rather than 'opacO2.dat' ")
    highres = query_yes_no('Is this High res? Yes or no')
    
    #splits the names of opacity files into a iterable list
    opac_add_list  = files_add.split(",")
    
    #different source folders depending on temperature range
    temp = input('Is this 100-3000 K or 500-5000 K? Answer "1" if 100-3000 K, "2" if 500-5000 K')
    if temp == '1':
        source = '/nfs/turbo/lsa-erausche/Opacity_Files/opac_100-3000/'
    elif temp == '2':
        source = '/nfs/turbo/lsa-erausche/Opacity_Files/opac_500-5000/'
    else:
        raise Exception('Temperature input must be a 1 or a 2!')
    
    #pulls different files depending if they are hires or not
    
    if highres == True: 
        for name in opac_add_list:
            #this physically moves the files over
            namenew = 'opac'+name+'_hires.dat'
            shutil.copyfile(source+namenew, namenew)
        #prints current directory so you can double check the opacity files
        
    else:
        for name in opac_add_list:
            namenew = 'opac'+name+'.dat'
            shutil.copyfile(source+namenew, namenew)

print('Current opacity files are: \n'+str(os.listdir()))     
remove = query_yes_no('Do you need to remove any opacity files from the list?')

if remove == True:
    files_rm = input("Enter opacity files needed to be removed, seperated by commas (NO SPACES!!)")
    opac_rm_list  = files_rm.split(",")
    for names in opac_rm_list:
        os.remove('opac'+names+'.dat')
    print('Current opacity files are: \n'+str(os.listdir()))

#regridding part
regrid_question = query_yes_no('\n Second, do you need to regrid the opacity files for a different wavelength? ')

if regrid_question == True:
    start_wavelength = input('Enter starting wavelength (in microns): ')
    end_wavelength = input('Enter ending wavelength (in microns): ')
    
    if add == True: #this is because temp is only called if add == true
        for x in os.listdir():
            #calls the regrid code  
            regrid.regrid(start_wavelength,end_wavelength,name, temp, path)

    else:
        temp = input('Is this 100-3000 K or 500-5000 K? Answer 1 if 100-3000 K, 2 if 500-5000 K')
        if int(temp) != 1 and int(temp) !=2:
            raise Exception('Temperature input must be a 1 or a 2!')
        for x in os.listdir():
            regrid.regrid(start_wavelength,end_wavelength,name, temp, path)

elif regrid_question == False:
    print('Current opacity files are: \n'+str(os.listdir()))
    print("Exit, you chose not to regrid any opacity files. Please rerun this script if opacity files are incorrect.")
