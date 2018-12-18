import Tkinter as tk
from Tkinter import *
from PIL import Image, ImageTk # for windows is this option , ImageGrab
# for windows is this option
from PIL import ImageGrab
#for linux
#import pyscreenshot as ImageGrab
from math import sqrt,ceil
import tkFileDialog
import os
import tkMessageBox

class Gui():
    def __init__(self, root):
        self.root=root
 	
	frameCanvas=Frame(self.root)
	frameCanvas.grid(row=0,column=0,pady=20,sticky="n")
        self.canvas=tk.Canvas(frameCanvas,  width=450, height=550,borderwidth=2, relief="groove",cursor="cross")
        self.canvas.grid(row=0,column=0, pady=0, padx=10)
	buttonNext = tk.Button(frameCanvas, text="Next", command=self.ImageNext).grid(row=1,column=0,pady=5,sticky="n")


	self.x = self.y = 0
	
	#variables to be able to erase elements on the canvas
	self.rec_id=list()
	self.text_id_DM=list()
	self.text_id_ST=list()
	self.erase=0
	self.recErase="a"

	#Image Canvas
     	self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
	
	#variables necesary to draw rectangles on the canvas
        self.rect = None
        self.start_x = None
        self.start_y = None

	# add a File Save menu
	menu=Menu(root)
	root.config(menu=menu)
	filemenu = Menu(menu)
	menu.add_cascade(label="File", menu=filemenu)
	filemenu.add_command(label="Open...", command=self.open_file)
	#filemenu.add_command(label="Open All files in folder...", command=self.open_folder)
	filemenu.add_command(label="Select Output folder...", command=self.out_folder)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)

	helpmenu = Menu(menu)
	menu.add_cascade(label="Help", menu=helpmenu)
	helpmenu.add_command(label="Instructions...", command=self.help)
	helpmenu.add_command(label="About C.I.T.T...",command=self.about)
	self.path_out="Out/"
	self.path="a"

	#list for names of images ina a folder
	self.ImageList=[]
	self.ImageListIndex=1
	self.ImageLoaded=0

	
	frameD=Frame(self.root)
	frameD.grid(row=0,column=1,pady=20,sticky="n")
	#Damages
	DAMAGES = [
		("Shear cracking", "Scrack"),
        	("Flexural cracking", "Fcrack"),
        	("Concrete spalling", "spal"),
        	("Concrete core crushing", "contcrush"),
		("Longitudinal bar buckling", "LbarB"),
		("Longitudinal bar fracture", "LbarF"),
		("Failure of confining hoops/ties", "FailHopp"),
		("Anchorage/connection failure", "AnchFail"),
		("Lap splice failure", "LapSFail"),
		("Distributed plastic hinging", "DistPlas"),
		("Concentrated flexural cracking", "ConcFlex"),
		("Global buckling/instability", "GlobalBuck"),
		("Shear/diagonal failure", "ShearFail"),
		("Shear/compression failure", "ShearCompFail"),
		("Interface sliding", "IntSlid"),
		("Interaction b/w infill and frame", "Interac"),
		("Slab fracture", "SlabFrac"),
		("Punching shear failure", "PunchShearFrac"),
		("Unseating/collapse of stairs", "Unseating"),
		("Pounding", "Pounding"),
		("Differential settlement", "DiffSett"),
		("Residual displacement", "ResidualDisp"),
		("Soft story failure", "SoftStoryFail"),
		("Partial/full collapse", "Collapse"),
    	]
	#VARIABLE FOR DAMAGE SELECTION
	self.DamageStr=tk.StringVar()
	self.DamageStr.set("Damage Label") # initialize
	l = tk.Label(frameD,borderwidth=2, relief="groove", text="Type of Damage").grid(row=0,column=1,sticky="nw")
	r=1
    	for text, mode in DAMAGES:
        	self.panelB = tk.Radiobutton(frameD, text=text, variable=self.DamageStr, value=text,command=self.DamageSel)
		self.panelB.grid(row=r,column=1,pady=2,sticky="w")
		r=r+1
        

	
	frameS=Frame(root)
	frameS.grid(row=0,column=2,pady=20, padx=10,sticky="n")
	#Structures
	STRUCTURES = [
        	("Short/captive column", "Scrack"),
        	("Slender column", "Fcrack"),
        	("Structural wall", "spal"),
        	("Infill wall", "contcrush"),
		("Tilt-up precast panel", "LbarB"),
		("Joint-column connection", "LbarF"),
		("Beam", "FailHopp"),
		("Coupling beam", "AnchFail"),
		("Foundation beam", "LapSFail"),
		("Floor diaphragm/slab", "DistPlas"),
		("Frame", "ConcFlex"),
		("Scissor stairs", "GlobalBuck"),
		("Corbel/support", "ShearFail"),
		("Cantilevered balcony", "ShearCompFail"),
		("Construction joint", "IntSlid"),
		("Full story", "Interac"),
		("Partial/full building", "SlabFrac"),
		("Unknown", "PunchShearFrac"),
	]    		
	#VARIABLE FOR STRUCTURES
	self.StructureStr=tk.StringVar()
	self.StructureStr.set("Structure Label") # initialize
	l1 = tk.Label(frameS,borderwidth=2, relief="groove", text="Type of Structure").grid(row=0,column=2,sticky="nw")
        r=1
    	for text, mode in STRUCTURES:
        	self.panelC = tk.Radiobutton(frameS, text=text, variable=self.StructureStr, value=text,command=self.StructureSel)
		self.panelC.grid(row=r,column=2,pady=4,sticky="w")
		r=r+1

	#Add the delete New Label and Delete Label to screen
	frameM=Frame(root)
	frameM.grid(row=0,column=3,pady=20, padx=10,sticky="n")
	l2 = tk.Label(frameM,borderwidth=2, relief="groove", text="Create a New Label").grid(row=1,column=3,sticky="n")
	self.newST=tk.StringVar(frameM, value=self.StructureStr.get())
	self.newDM=tk.StringVar(frameM, value=self.DamageStr.get())
	self.textST=tk.Entry(frameM, width=25, textvariable=self.newST).grid(row=3,column=3,sticky="n")
	self.textDM=tk.Entry(frameM, width=25, textvariable=self.newDM).grid(row=2,column=3,sticky="n")

	#label History
	self.labelHist=tk.Listbox(frameM, width=50, height=5)
	self.labelHist.grid(row=4,column=3,pady=5,sticky="ns")
	self.scrollbar=Scrollbar(frameM,orient=VERTICAL)
	self.scrollbar.grid(row=4, column=4,sticky=N+S)
	self.labelHist.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.labelHist.yview)

	self.labelHist.insert(10,"New Label History list:")
	#read This from a file
	fileHistLabel=open("histlabel.txt","r")
	for item in fileHistLabel:
		item=item[:-1] #erases the stupid /0 end of string char
		self.labelHist.insert(20,item)
	fileHistLabel.close()
	#button that creates label once you are done entering values Necesary???
	doneButton=tk.Button(frameM,text="Done Creating Label", command= self.create_new_label)
	doneButton.grid(row=5,column=3,pady=10,sticky="n")


	#delete labels two buttons
	l4=tk.Label(frameM,borderwidth=2, relief="groove",text="Delete Options").grid(row=8,column=3,pady=10,sticky="n")
	buttonDeleteStart=tk.Button(frameM, width=25,text="Start Deleting", command=self.deleteStart).grid(row=9,column=3,sticky="n")
	buttonDeleteStop=tk.Button(frameM, width=25,text="Stop Deleting", command=self.deleteStop).grid(row=10,column=3,sticky="n")

	buttonDeleteAll=tk.Button(frameM, width=25,text="Delete ALL Labels", command=self.delete_all).grid(row=11,column=3,sticky="n")
	#add the save Image/ Exit
	button = tk.Button(frameM, text="Save", command=self.save).grid(row=20,column=3,pady=20,sticky="n")
	button1 = tk.Button(frameM, text="Cancel (DO NOT SAVE)", command=root.quit).grid(row=21,column=3,pady=5,sticky="n")


	#console
	self.consoleLabel=tk.Label(frameM,width=25,borderwidth=2, relief="groove", text="Progress")
	self.consoleLabel.grid(row=14,column=3,pady=15,sticky="n")
	#Console History
	self.consoleHist=tk.Listbox(frameM,background="light gray", width=50, height=15)
	self.consoleHist.grid(row=15,column=3,padx=10,sticky="n")
	self.scrollbar2=tk.Scrollbar(frameM,orient=VERTICAL)
	self.scrollbar2.grid(row=15,column=4,sticky=N+S)
	self.consoleHist.config(yscrollcommand=self.scrollbar2.set)
        self.scrollbar2.config(command=self.consoleHist.yview)


    def _draw_image(self,path):
	 #write to console hist name of file
	 self.consoleHist.insert(20,os.path.basename(path)+"\n")
         self.im = Image.open(path)
         self.tk_im = ImageTk.PhotoImage(self.im)
         self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)
         self.ImageSize=self.im.size  
	 #make size of canvas same as image
	 self.canvas.config(width=self.ImageSize[0], height=self.ImageSize[1])
	 self.ImageLoaded=1

    
    def ImageNext(self):
	#save stuff from Image first, than load the new Image
        self.save()
        self.consoleHist.delete(0,END)
        if self.ImageListIndex <len(self.ImageList):
            #erase stuff on the console
            pathNext= self.ImageList[self.ImageListIndex]
            dirpath=os.path.dirname(self.path)
            self._draw_image(dirpath+'/'+pathNext)
            self.ImageListIndex=self.ImageListIndex+1
            #make the new picture the path
            self.path=dirpath+'/'+pathNext
        else:
            root.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

       	# create rectangle, initial dot if not erasing it but only if there is an image already loaded
	if self.ImageLoaded==1:
		if self.erase == 0:
        		self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline="red")
			self.testDM=self.canvas.create_text(self.start_x,self.start_y-10,fill="red", font="Times 10", text=self.DamageStr.get())
			self.testST=self.canvas.create_text(self.start_x,self.start_y,fill="red", font="Times 10", text=self.StructureStr.get())
			#add recId to a list so then it can be erased
			self.rec_id.append(self.rect)
			self.text_id_DM.append(self.testDM)
			self.text_id_ST.append(self.testST)
		else:
			#if delete rec pressed than check if there is a rectangle to be erased
			self.collision(self.start_x,self.start_y)

    def on_move_press(self, event):
	if self.ImageLoaded==1:
	        curX, curY = (event.x, event.y)
	        # expand rectangle as you drag the mouse if not erasing
        	if self.erase == 0:
			self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
	#show rec coord and labels on console self.consoleHist.insert(20,self.DamageStr.get())
	#save rect to out
	if self.ImageLoaded==1:
 		if self.erase==0:
			#erase label if less than 3 pixel width or height
			if abs(self.start_x - event.x) <=3 or abs(self.start_y - event.y) <=3 :
				last=len(self.rec_id) -1
				#delete rectangle and labels
				self.canvas.delete(self.rec_id[last])
				del self.rec_id[last]
				self.canvas.delete(self.text_id_DM[last])
				del self.text_id_DM[last]
				self.canvas.delete(self.text_id_ST[last])
				del self.text_id_ST[last]
			else:	 
				text="rect:" + str(self.start_x)+" "+str(self.start_y)+" "+str(event.x)+" "+str(event.y)+" "+ self.DamageStr.get()+ " "+ self.StructureStr.get()+"\n"
				#write to console history
				self.consoleHist.insert(20,text)

 
    def collision(self,x,y):
        print len(self.rec_id)
        
        for rec in range(len(self.rec_id)):
            #print rec
	    pt=self.canvas.coords(self.rec_id[rec])
	    distance= sqrt((pt[0]-x)**2+(pt[1]-y)**2)
            if distance< 5:
		#create a text to search on the 
		self.recErase="rect:" + str(int(ceil(pt[0])))+" "+str(int(ceil(pt[1])))+" "+str(int(ceil(pt[2])))+" "+str(int(ceil(pt[3])))+" "+ "\n"
		#self.recErase="rect:" + str(pt[0])+" "+str(pt[1])+" "+str(pt[2])+" "+str(pt[3])+" "+ "\n" 
		#delete rectangle and labels
		self.canvas.delete(self.rec_id[rec])
		del self.rec_id[rec]
		self.canvas.delete(self.text_id_DM[rec])
		del self.text_id_DM[rec]
		self.canvas.delete(self.text_id_ST[rec])
		del self.text_id_ST[rec]
		
		#erase from list
		# get a list of listbox lines
		i=0
    		temp_list = list(self.consoleHist.get(0, tk.END))
   		for item in temp_list:
                        #print item[0:20]
                        #print self.recErase[0:20]
			if item[0:20] == self.recErase[0:20]:
				del temp_list[i]
			i=i+1
		#write the temp list back to consoleHist
		self.consoleHist.delete(0,END)
		for item in temp_list:
			self.consoleHist.insert(20,item)
		
			
    #selects the Damage Label
    def DamageSel(self):
	self.newDM.set(self.DamageStr.get())
		
   
    #select the structure label
    def StructureSel(self):
	self.newST.set(self.StructureStr.get())

    #delete last label/rectangle entered
    def deleteStart(self):
	self.erase=1

    def deleteStop(self):
	self.erase=0

	
    #delete all the labels and rectangles from the image
    def delete_all(self):
	self._draw_image(self.path)
	#clear all elements on list
	self.consoleHist.delete(1,END)
	
    #Create the new Structure+Damage Label
    #allows to select name from the radio button just in case one one of the entries needs to change
    def create_new_label(self):
	#set label to the new one created
	self.DamageStr.set(self.newDM.get())
	self.StructureStr.set(self.newST.get())
	with open("histlabel.txt", "a+") as text_file:
    		text_file.write(self.newDM.get()+"\n")
           	text_file.write(self.newST.get()+"\n")

	#add to history
	self.labelHist.insert(20, self.StructureStr.get()+" "+self.DamageStr.get())

    #function to save the annotations for the PASCAL VOC FORM so the tags can be used in Tensorflow 
    def create_xml(self):
	# get a list of listbox lines from the console
    	temp_list = list(self.consoleHist.get(0, tk.END))
    
	#save label Annotations
	dirpath=os.path.dirname(self.path)
	Imagefolder=os.path.basename(dirpath)
	Imagefilename=os.path.basename(self.path)
	#change filename to xml
	index=Imagefilename.index('.')
	xmlfilename=Imagefilename[0:index]+".xml"
	p="annotations/"+xmlfilename
	with open(p, "w") as text_file:
		text_file.write("<annotation verified=\"yes\">\n")
		
		text_file.write("\t<folder>")
		text_file.write(Imagefolder) #filename no path
		text_file.write("</folder>\n")
		
		text_file.write("\t<filename>")
		text_file.write(Imagefilename) #filename no path
		text_file.write("</filename>\n")
		
		text_file.write("\t<size>\n")
		text_file.write("\t\t<width>")
		text_file.write(str(self.ImageSize[0])) 
		text_file.write("</width>\n")
		
		text_file.write("\t\t<height>")
		text_file.write(str(self.ImageSize[1])) 
		text_file.write("</height>\n")

		text_file.write("\t\t<depth>")
		text_file.write("3") 
		text_file.write("</depth>\n")
		text_file.write("\t</size>\n")
		text_file.write("\t<segmented>")
		text_file.write("0") 
		text_file.write("</segmented>\n")
		
			
		for line in temp_list:
			#if line statrt with rec than is a rectangles and create an obj
			#create the xml bound box
			if 'rect'==line[0:4]:
				#ERASE THE WORD RECT: FIRST from line	
				words=line[5:].split()
			
				#numElem=(len(words)-4)/2
				#strDM=' '.join(words[4:(4+numElem)])
				#strST=' '.join(words[4+numElem:])
				
				text_file.write("\t<object>\n")
				text_file.write("\t\t<name>")
				text_file.write(' '.join(words[4:]))
				text_file.write("</name>\n")
				text_file.write("\t\t<bndbox>\n")
				text_file.write("\t\t\t<xmin>")
				text_file.write(str(words[0]))
				text_file.write("</xmin>\n")
				text_file.write("\t\t\t<ymin>")
				text_file.write(str(words[1]))
				text_file.write("</ymin>\n")
				text_file.write("\t\t\t<xmax>")
				text_file.write(str(words[2]))
				text_file.write("</xmax>\n")
				text_file.write("\t\t\t<ymax>")
				text_file.write(str(words[3]))
				text_file.write("</ymax>\n")
				text_file.write("\t\t</bndbox>\n")
    				text_file.write("\t</object>\n")


		text_file.write("</annotation>\n")
   
	
    #save image and exit progrma
    def save(self):
	# get a list of listbox lines
    	temp_list = list(self.consoleHist.get(0, tk.END))
    	# add a trailing newline char to each line, no need
    	#temp_list = [chem + '\n' for chem in temp_list]
    	# save to file use path_out
	index=self.path.index('.')
	outfilename=self.path[0:index]+"-out.jpeg"

	if self.path_out=="a":
		p="Output.txt"
		p1=outfilename
	else:
		p=os.path.join(os.getcwd(),self.path_out, "Output.txt")
		#print p
		filename=os.path.basename(self.path)
		index2=filename.index('.')
		filename=filename[0:index2]+"-out.jpeg"
		p1=os.path.join(self.path_out,filename)
		#print p1
	temp_list = list(self.consoleHist.get(0, tk.END))
	with open(p, "a+") as text_file:
    		text_file.writelines(temp_list)
   	#for WINDOWS ImageGrab(0,0,self.width,self.height).save("out.jpeg")
	widget=self.canvas 
	x=root.winfo_rootx()+widget.winfo_x()
    	y=root.winfo_rooty()+widget.winfo_y()
    	x1=x+widget.winfo_width()
    	y1=y+widget.winfo_height() 
    	ImageGrab.grab(bbox=(x,y,x1,y1)).save(p1)
	self.create_xml()
	
    def open_file(self):
	# open a file chooser dialog and allow the user to select an input
	opts = {}
        opts['filetypes'] = [('Supported types',('.jpeg','.jpg','.JPG','.JPEG')),
                             ('EEG files','.eeg'),('all files','.*')]
        
        self.path = tkFileDialog.askopenfilename(title='Enter Input File',**opts)
        if self.path == '': return
        	
	#create a list qith all images names on the directory the file is selected 
	dirpath=os.path.dirname(self.path)
   	listin=os.listdir(dirpath)
	for file in listin:
		#enter the name of the file into a list
		#the next element of the list will be loaded when Next button is clicked  
		self.ImageList.append(file)   
	self._draw_image(self.path)
    def out_folder(self):
	#output folder by default is same as the input images folder
	#out.txt file contains all labels and by default will be on the same folder as the 
	self.path_out = tkFileDialog.askdirectory(title='Enter Output Directory')

    def help(self):
	tkMessageBox.showinfo("Help","For Instructions of how to use CITT:\nhttps://github.com/mpantoja314/Image")
    def about(self):
	tkMessageBox.showinfo("Information","C.I.T.T Civil Infrastructure Tagging Tool: \nVersion 1.0. \nUpdated  October 2017. \nDeveloped by:\nMaria Pantoja and Anahid Behrouzi \nCalPoly SLO")

if __name__== '__main__':
    root=tk.Tk()
    gui=Gui(root)
    root.title("C.I.T.T. Civil Infrastructure Tagging Tool");
    #root.geometry("1000x1500+0+0")
    imgicon = ImageTk.PhotoImage(file=os.path.join(os.getcwd(),'logo.ico'))
    root.tk.call('wm', 'iconphoto', root._w, imgicon)

    root.mainloop()
