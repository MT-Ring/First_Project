#!/usr/bin/env python
# coding: utf-8
import pandas as pd, matplotlib.pyplot as plt, numpy as np, tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

## File open
def get_filename():

    root = Tk()
    root.geometry('200x100+2500+500')# winodw size plus position
    options = {'parent':root, 'title':'Select file to process','filetypes':[('CSV Files','*.csv')]}
    filename = askopenfilename(**options)

    if filename == "":
        return False
    root.destroy()
    return filename 

fileName = get_filename()

# read data in to dataframe
df = pd.read_csv(fileName, index_col = False) 
dfr = df[['Time','End Entity','Az(T)','Rng','Alt']] # extract the columns needed for polar plot
dfr.columns = dfr.columns.str.strip() #strip out white space
dfr.columns = dfr.columns.str.replace(' ', '')#strip out white space
dfr = dfr.dropna() # drop all NaN entries

entities = dfr.EndEntity.unique() # get list of unique values in this column
entities = entities.tolist() # convert to list for use in selection form

Plots=[] #list that will hold items to plot

#Function to select items to plot
def SelectPlots():
    root = tk.Tk()
    root.title("Targets to Plot")
    root.geometry('300x200+2500+500') #window size and position for dual screeen

    listbox = Listbox(root, selectmode=MULTIPLE,width=20) #populate listbox from entities....
    for x,y in enumerate(entities):
        listbox.insert(x+1,y)
    listbox.pack(anchor = tk.CENTER)

    def select():
        selection = listbox.curselection()
        for i in selection:
            entry = listbox.get(i)
            Plots.append(entry) # and add to Plots[] list
        root.destroy()
        
    btn = Button(root, text="Select", command=select)
    btn.pack()

    root.mainloop()


SelectPlots() # call select plots function

pColor = {'Red':'r', 'Blue':'b', 'Green':'g', 'Black':'k', 'Cyan':'c', 'Magenta':'m',"Yellow":'y','White':'w'} #dictionary to hold plot colours
lStyle = {'Solid':'-','Dashed':'--', 'Dash-Dot':'-.','Dotted':':'}

plotColor=[] # empty list for plot colours
LineStyle = [] #empty list for Line sytles

#function to select colour for plot of each item
def selectColor():
    
    root = tk.Tk()
    root.title("Choose Plot Color for plot " + str(index+1))
    root.geometry('300x200+2500+500')
    
    def select():
        for key in listbox1.selection_get().split():
            plotColor.append(pColor[key]) #add selected from list to plotColor[] list
            root.destroy()
        
    listbox1 = Listbox(root, width=20,)
    for key in pColor: # populate list from pColor dictionary and....
        listbox1.insert('end', key)
    listbox1.grid(row=0, column =0)
    listbox1.pack(anchor = tk.CENTER)
    btn = Button(root, text="Select", command=select)
    btn.pack()
    

    root.mainloop()

def selectStyle():
    
    root = tk.Tk()
    root.title("Choose Style for plot " + value)
    root.geometry('300x200+2500+500')

    
    def select():
        for key in listbox1.selection_get().split():
            LineStyle.append(lStyle[key]) #add selected from list to plotColor[] list
            root.destroy()    
    
    
    listbox1 = Listbox(root, width=20,)
    for key in lStyle: # populate list from pColor dictionary and....
        listbox1.insert('end', key)
    listbox1.grid(row=0, column =0)
    listbox1.pack(anchor = tk.CENTER)
    btn = Button(root, text="Select", command=select)
    btn.pack()
  

    root.mainloop()  
    
    
#plot the targets
fig = plt.figure(figsize=(10,10))
ax = plt.subplot(111, projection = 'polar') #matplot lib polar plot
ax.set_theta_zero_location ('N')
ax.set_theta_direction(-1)
ax.grid(True)
ax.tick_params(axis = 'y', colors='r')

for index,value in enumerate(Plots):
    
    df1 = dfr.loc[dfr['EndEntity'] == value] # plot where 'EndEntity is in Plots[] list
    theta = np.deg2rad(df1['Az(T)']) # degrees to radians of bearing
    rng = df1['Rng'] #range
    selectColor() # call setcolor to change clour for each item
    selectStyle()
    ax.plot(theta, rng, c = plotColor[index], linestyle=LineStyle[index],label = value)

ax.legend()    
plt.savefig('Polar.png')    # save plot to graphic
plt.show() #show plot

plotColor = [] # empty lists
LineStyle = [] # empty lists


