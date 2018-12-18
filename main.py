# import the necessary packages
import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import os

def image_concrete():
	os.system('python ImageTagGUI.py')
def images_own():
	os.system('python ImageTagOwn.py')
def review_image():
	os.system('python ReviewTag.py')
def review_own():
	os.system('python ReviewTagOwn.py')
def stats():
	os.system('python histConcLabels.py')
def select_crop_image():
	os.system('python crop.py')


#Main Window Code   
root = tk.Tk()
root.title("C.I.T.T. Civil Infrastructure Tagging Tool");

#verlogo=ImageTk.PhotoImage(file= "logo.png")
calpolylogo=ImageTk.PhotoImage(file= "SLOLogo.png")

cv=tk.Canvas(width=360, height=400)
#cv.create_image(50,10,image=verlogo, anchor='nw')
cv.create_image(30,50,image=calpolylogo, anchor='nw')
cv.pack(pady=12, side='left', fill='both', expand='yes')


imgicon = ImageTk.PhotoImage(file=os.path.join(os.getcwd(),'logo.ico'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)  

#instructions

label=tk.Label(root, width=50, text="C.I.T.T.:",font=("Italic",10, "bold"))
label1=tk.Label(root, text="The Civil Infrastructure Tagging Tool (CITT) was developed by:")
label2=tk.Label(root, text="Drs. Maria Pantoja and Anahid A. Behrouzi") 
label3=tk.Label(root, text="California Polytechnic State University San Luis Obispo, 2017.") 
label4=tk.Label(root, text="CITT is a program to assist engineers in manually tagging post-hazard or inspection") 
label5=tk.Label(root, text="of photos of civil infrastructure.") 
label6=tk.Label(root, text="Refer to help menu for additional documentation.") 


label.pack(pady=8, anchor='w')
label1.pack( padx=8,anchor='w')
label2.pack( padx=8,anchor='w')
label3.pack( padx=8,anchor='w')
label4.pack( padx=8,anchor='w')
label5.pack( padx=8,anchor='w')
label6.pack( padx=8,anchor='w')


button = tk.Button(root, text="Tag Reinforced Concrete Building Images", command=image_concrete)
button.pack(pady=8,padx=8,fill="both", expand="no")

button = tk.Button(root, text="Tag Images with User-Generated Labels ", command=images_own)
button.pack(pady=8,padx=8,fill="both", expand="no")

button = tk.Button(root, text="Review/Edit Previously Tagged Concrete Building Images", command=review_image)
button.pack(pady=8,padx=8,fill="both", expand="no")

button = tk.Button(root, text="Review/Edit Previously Tagged (Own Labels) Images", command=review_own)
button.pack(pady=8,padx=8,fill="both", expand="no")

button = tk.Button(root, text="Create Statistics from Image Batch", command=stats)
button.pack(pady=8,padx=8,fill="both", expand="no")

button = tk.Button(root, text="Reduce Dimensions of Image Batch", command=select_crop_image)
button.pack(pady=8,padx=8,fill="both", expand="no")

# kick off the GUI
root.mainloop()
