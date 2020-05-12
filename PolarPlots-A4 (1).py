#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd, matplotlib.pyplot as plt, numpy as np, tkinter as tk


# In[2]:


from tkinter import *


# In[3]:


from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


# In[4]:


## File open


# In[5]:


root = Tk()
root.title("Open File")
root.geometry('200x100+2500+500')# winodw size plus position

def openFile():
    global fileName
    fileName = askopenfilename()
    root.destroy()
    
btn = Button(root,text='Open File', command = openFile)
btn.pack()
root.mainloop()


# In[6]:


# read data in to dataframe


# In[7]:


df = pd.read_csv(fileName, index_col = False) 


# In[8]:


dfr = df[['Time','End Entity','Az(T)','Rng','Alt']] # extract the columns needed for polar plot


# In[9]:


dfr.columns = dfr.columns.str.strip() #strip out white space


# In[10]:


dfr.columns = dfr.columns.str.replace(' ', '')#strip out white space


# In[11]:


dfr = dfr.dropna() # drop all NaN entries


# In[12]:


entities = dfr.EndEntity.unique() # get list of unique values in this column


# In[13]:


entities = entities.tolist() # convert to list for use in selection form


# In[14]:


Plots=[] #list that will hold items to plot


# In[15]:


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


# In[16]:


SelectPlots() # call select plots function


# In[17]:


pColor = {'Red':'r', 'Blue':'b', 'Green':'g', 'Black':'k', 'Cyan':'c', 'Magenta':'m',"Yellow":'y','White':'w'} #dictionary to hold plot colours


# In[18]:


plotColor=[] # empty list for plot colours


# In[19]:


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


# In[20]:


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


# In[21]:


plotColor=[] #reset colors


# In[ ]:





# In[ ]:




