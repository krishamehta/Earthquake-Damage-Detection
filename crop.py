import PIL
from PIL import Image, ImageTk # for windows is this option , ImageGrab
import tkFileDialog
import os

# open a file chooser dialog and allow the user to select an input
opts = {}
opts['filetypes'] =[('Supported types',('.jpeg','.jpg','.JPG','.JPEG')),
                             ('EEG files','.eeg'),('all files','.*')]
        
path1 = tkFileDialog.askdirectory(title = "Select Input Folder")
#if path1 == '': return
print path1    

path2 = tkFileDialog.askdirectory(title = "Select Output Folder")
#if path2 == '': return
print path2  

basewidth= int(input("Please enter reduction factor for your image (100-half size, 200-quarter size, 300...): "))

listing = os.listdir(path1)  
print listing  
for file in listing:
    img = Image.open(path1 +'/' +file) 
    #basewidth=100  
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save(path2 +'/crop'+ file)

#basewidth = 300
#img = Image.open('SLOLogo.jpeg')
#wpercent = (basewidth/float(img.size[0]))
#hsize = int((float(img.size[1])*float(wpercent)))
#img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
#img.save('sompic.jpg') 




#from multiprocessing import Pool
#import os

#path1 = "some/path"
#path2 = "some/other/path"

#listing = os.listdir(path1)    

#p = Pool(5) # process 5 images simultaneously

#def process_fpath(path):
#    im = Image.open(path1 + path)    
#    im.resize((50,50))                # need to do some more processing here             
#    im.save(os.path.join(path2,path), "JPEG")

#p.map(process_fpath, listing)

