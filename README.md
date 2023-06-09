# Choose_opacity and Regrid


*************************************************
************       GENERAL       ****************
*************************************************

This is a guide for how to use the scripts 'choose_opacity.py' and 'regrid.py'

'choose_opacity.py' is the file that moves opacity files from the repository on great lakes, located at '/nfs/turbo/lsa-erausche/Opacity-Files' .

There are 3 subfolders here, currently titled opac_100-3000 , opac_500-5000, and opac_weird_format. The names correspond to the temperature ranges and whether Alex could understand how the files were formatted. These will be adjusted in the future. 

In each folder there are high_res versions. Again, these will be renamed soon for clarity. 

The two scripts 'choose_opacity.py' and 'regrid.py' work in tandem but can be used separately. It is best explained flowing from choose_opacity to regrid. 


*************************************************
************       HOW TO RUN       *************
*************************************************

You can run each script the way you would normally run a python script from command line — by typing 'python3 *script.py*'

**Note — this file requires pandas and several other python scripts, so you may need to type 'module load python3.9-anaconda' first**

*************************************************
********       choose_opacity.py	 ********
*************************************************

choose_opacity is essentially a user input file that grabs the opacity files the user requests. There are several parameters needed that require user input, such as temperature range, if high res, etc. 

There are 3 main functions you can choose to do with this script. You can add opacity files to your main folder, remove opacity files currently in the folder, or regrid opacity files that are currently in your folder for a specific wavelength range. 

The script prints the current opacity files in your folder, then asks if you need to add any. 

If you need to add elements, respond with the names of elements needed, seperated by commas and with no spaces. Also respond with "O2" rather than "opacO2.dat" or "O2_hires", it will mess up the naming convention in the code. 

After specifying the temperature range (again, here respond with a '1' if temperature range is 100-3000K, '2' if temperature range is 500-5000K), it will move the files from the repository to your working folder. 

It then asks you if you want to remove any opacity files from the list. This works great as long as your opacity files are not high res. If they are not high res, follow the naming convention for adding. If they are, currently you have to delete the high res files yourself. Sorry. 

Finally, it asks if you would like to regrid your files. Important to note that this will loop over all your opacity files, so be careful. Input your wavelengths (in microns, so say '3' instead of 3e-6), and wait for it to regrid your files. 

*************************************************
***********       regrid.py	    *************
*************************************************

Although this file is called by choose_opacity.py, it can be run on its own. You just need to specify the parameters called in the regrid function. 

If you import regrid.py as regrid, then the function itself is regrid.regrid —— sorry. 

There are 4 parameters needed — starting wavelength, ending wavelength, name of file, and path. All are commented in the regrid.py file, but it is important to note that the conventions are the same as for the choose_opacity.py file. 



In progress updates (not yet implemented) are variable temperature ranges, ability to regrid CIA files. 
