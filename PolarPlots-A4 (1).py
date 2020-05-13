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

plotColor=[] # empty list for plot colours

#function to select colour for plot of each item
def selectColor():
    
    root = tk.Tk()
    root.title("Choose Plot Color for plot " + str(i+1))
    root.geometry('300x200+2500+500')

    listbox1 = Listbox(root, width=20,)
    for x,y in enumerate(pColor): # populate list from pColor dictionary and....
        listbox1.insert(x+1,y)
    listbox1.pack(anchor = tk.CENTER)
    
    
    def select():
        entry1.delete(0, 'end')
        selection = listbox1.get(ANCHOR)
        entry1.insert(0,pColor[selection])
        plotColor.append(selection) #add selected from list to plotColor[] list
        root.destroy()
        
    btn = Button(root, text="Select", command=select)
    btn.pack()
    
    entry1 = Entry(root, width=20)

    root.mainloop()

# plot out the items to MatPlotLib
ax = plt.subplot(111, projection = 'polar') #matplot lib polar plot
ax.set_theta_zero_location ('N')
ax.set_theta_direction(-1)
ax.grid(True)
ax.tick_params(axis = 'y', colors='r')
i=0 # set loop to go through each item selected for plotting

for item in Plots:
    
    df1 = dfr.loc[dfr['EndEntity'] == item] # plot where 'EndEntity is in Plots[] list
    theta = np.deg2rad(df1['Az(T)']) # degrees to radians of bearing
    rng = df1['Rng'] #range
    selectColor() # call setcolor to change clour for each item
    
    ax.plot(theta, rng, c = plotColor[i])
    i+=1 # incremetn loop
    
    
    
plt.savefig('Polar.png')    # save plot to graphic
plt.show() #show plot

