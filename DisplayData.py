#import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.widgets import Slider, Button
import csv
from datetime import datetime
import time
import Class
import Function
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

PlotStyleOptionName=["Show data points with: o-",
                     "Show data points with: .-",
                     "Display 1 min vertical lines",
                     "Display 5 min vertical lines",
                     "Display 10 min vertical lines",
                     "Display 20 min vertical lines",]





def ProcessCSV(file_path):
    #Name of data to be read
    CSVName = file_path

    #funkcija prebere 3. vrstico CSV file, v tej vrstici je zapisan delimator
    
    with open('{}'.format(CSVName),mode='r',encoding='utf-8') as csv_file:
        csv_reader = list(csv.reader(csv_file))
        DelimiterData=csv_reader[2][0].split(":",1)
        Delimiter_=DelimiterData[1].replace(" ","")
        
        
    


    #funkcija prebere CSV file in ga zapiše v data_list
    data_list=[]
    with open('{}'.format(CSVName),mode='r',encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=Delimiter_)
        for row in csv_reader:
            if not (row):    
                continue
            data_list.append(row)
            
    #MetaData object
    MeasurementData = Class.MetaData()
    ###Add Meta data to MeasurementData
    #Number of measured channes is copied to MeasurementData
    #Date is copied to MeasurementData
    MeasurementData.Date = data_list[3][1]
    #Number of channels is copied to MeasurementData and converted from str to int
    MeasurementData.NumOfChannels = int(data_list[6][1])
    #Determinate number of specific channels and write them to MeasurementData
    MeasurementData.NumOfThermoCoup, MeasurementData.NumOfCurrentCh, MeasurementData.NumOfVoltageCh  = Function.DeterminateThermalOrCurrentOrVoltageChannel(data_list,MeasurementData.NumOfChannels)
    '''
    Meta Data is filled
    '''

    #create list for voltage ch objects, for current ch objects and for thermal channel objects
    VoltageChannels = []
    CurrentChannels = []
    ThermalCoupleChannels = []
    ListOfChannels = [ThermalCoupleChannels, CurrentChannels,VoltageChannels] 
    #create instances of voltage, current, thermal classes
    for i in range(MeasurementData.NumOfVoltageCh):
        VoltageChannels.append(Class.VoltageCh())
    for i in range(MeasurementData.NumOfCurrentCh):
        CurrentChannels.append(Class.CurrentCh())
    for i in range(MeasurementData.NumOfThermoCoup):
        ThermalCoupleChannels.append(Class.ThermalCoupleCh())

    #Add data to Channels
    Function.AddNameAndNumOfChToObject(ListOfChannels, data_list,MeasurementData.NumOfChannels)
    Function.AddTimeAndValueOfChToObject(ListOfChannels, data_list,MeasurementData.NumOfChannels)
    Function.AddValueAndTimeToObject(ListOfChannels, data_list,MeasurementData.NumOfChannels )
    '''
    Channel Data is filled
    '''
    #Test
    #plt.plot(ListOfChannels[0][1].Time,ListOfChannels[0][1].Value,"x")
    #plt.show()
    return ListOfChannels, MeasurementData

#Create the main application window
root = tk.Tk()
#set the window title
root.title("Plot CSV Data")
#set the window size
root.geometry("500x1100")

# Function to open file dialog and allow only CSV files to be selected

def select_csv_file():
    # Open a file dialog where only .csv files can be selected
    file_path = filedialog.askopenfilename(title="Select a CSV File",filetypes=[("CSV Files", "*.csv")] ) # Filter for .csv files only

    if file_path:  # If a file was selected
        label.config(text=f"Selected File: {file_path}")  # Update the label with the file path
        ListOfChannels, MeasurementData =ProcessCSV(file_path)

        # Create a label to display the selected folder
        label1 = tk.Label(root, text="Channels found in CSV:", font=("Arial", 12,"bold"))
        label1.pack(pady=0.1)

        #Create check boxes, checked boxes will be displayed
        # Create variables to track the state of each checkbox, number of variables is equal to number of channels
        CheckBoxesState=[]
        for i in range(MeasurementData.NumOfChannels):
            CheckBoxesState.append (tk.IntVar())
        # Create checkboxes and link them to the CheckBoxesState variable
        CheckBox=[]
        j=0
        #sprehod čez vse vrste kanalov
        for Chnannels in ListOfChannels:
        #sprehod čez vse kanale enega tipa
            for Channel in Chnannels:
                CheckBox.append( tk.Checkbutton(root, text=Channel.Name, variable=CheckBoxesState[j]))
                j +=1
        #Add checkboxes to the window
        for ChBox in CheckBox:
            ChBox.pack(pady=0.1)

        # Create a label to display the Syle options
        label1 = tk.Label(root, text="Plot style options:", font=("Arial", 12,"bold"))
        label1.pack(pady=0.1)

        #Create check boxes for style
        # Create variables to track the state of each checkbox
        CheckBoxesStateStyle=[]
        for i in range(6):
            CheckBoxesStateStyle.append (tk.IntVar())
        # Create checkboxes and link them to the CheckBoxesStateStyle variable
        CheckBoxStyle=[]
        for i in range(6):
            CheckBoxStyle.append( tk.Checkbutton(root, text=PlotStyleOptionName[i], variable=CheckBoxesStateStyle[i]))
            
        #Add checkboxes to the window
        for ChBox in CheckBoxStyle:
            ChBox.pack(pady=0.1)
        
        # Create a label for Title of plot
        label5 = tk.Label(root, text="Enter title of plot:")
        label5.pack(pady=0.1)

        # Create a scrolled text area for title of plot
        text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=0.5)
        text_area.pack(padx=10, pady=0.1)
        # Create a label for Title of plot
        label6 = tk.Label(root, text="Enter X axis name:")
        label6.pack(pady=0.1)
        # Create a scrolled text area for x axis name
        text_area1 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=0.5)
        text_area1.pack(padx=10, pady=0.1)
        
        label6 = tk.Label(root, text="Enter Y axis name:")
        label6.pack(pady=0.1)
        # Create a scrolled text area for y axis name
        text_area2 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=0.5)
        text_area2.pack(padx=10, pady=0.1)

        def PlotChannels():
            TitleOfPlot=text_area.get("1.0",tk.END)
            XaxisName=text_area1.get("1.0",tk.END)
            YaxisName=text_area2.get("1.0",tk.END)
            Ploty=[]
            PlotLabel=[]
            PlotStyle=[]
            Plotx=ListOfChannels[0][0].Time
            
            
            #print(CheckBoxesState)
            j=0
            #sprehod čez vse vrste kanalov
            for Chnannels in ListOfChannels:
            #sprehod čez vse kanale enega tipa
                for Channel in Chnannels:
                    if(CheckBoxesState[j].get()==1):
                        print("sdfsdf")
                        Ploty.append( Channel.Value)
                        PlotLabel.append(Channel.Name)
                    j +=1
            
            if(CheckBoxesStateStyle[0].get()==1):
                for y, Name in zip(Ploty,PlotLabel):
                    plt.plot(Plotx,y,label=Name,linestyle="--")
            
            
            elif(CheckBoxesStateStyle[1].get()==1):
                for y, Name in zip(Ploty,PlotLabel):
                    plt.plot(Plotx,y,label=Name,linestyle="dashdot")
            else:
                for y, Name in zip(Ploty,PlotLabel):
                    plt.plot(Plotx,y,label=Name)
            
            if(CheckBoxesStateStyle[2].get()==1):
                for i in range(0,int(Plotx[len(Plotx)-1]),60):
                    plt.axvline(i, color='red',linestyle="--")
            if(CheckBoxesStateStyle[3].get()==1):
                for i in range(0,int(Plotx[len(Plotx)-1]),300):
                    plt.axvline(i, color='blue')
            if(CheckBoxesStateStyle[4].get()==1):
                for i in range(0,int(Plotx[len(Plotx)-1]),600):
                    plt.axvline(i, color='black',linestyle="--")
            if(CheckBoxesStateStyle[5].get()==1):
                for i in range(0,int(Plotx[len(Plotx)-1]),1200):
                    plt.axvline(i, color='green')

            plt.title(TitleOfPlot)
            plt.xlabel(XaxisName)
            plt.ylabel(YaxisName)
            plt.legend()
            plt.show()
        
        
        # Create a button to Plot selected channels with style
        Plot_button = tk.Button(root, text="Plot",command=PlotChannels)
        Plot_button.pack(pady=5)



         
        

# Create a button that triggers the folder selection dialog
button = tk.Button(root, text="Select Folder", command=select_csv_file)
button.pack(pady=20)  # Add some padding around the button

# Create a label to display the selected folder
label = tk.Label(root, text="No folder selected", font=("Arial", 12))
label.pack(pady=10)

#start the Tkinter event loop
root.mainloop()


#TEST- after finisfed delete
'''
#print(ListOfChannels[2][1].Time)
plt.plot(ListOfChannels[0][1].Time,ListOfChannels[0][1].Value,"x")
plt.show()

j=8+MeasurementData.NumOfChannels+15
print(data_list[j][1])
print(data_list[j])

for i in range(len(ListOfChannels[2])):
    print(ListOfChannels[2][i].ColoumInCSV)
    print(ListOfChannels[2][i].Name)
    print("__________")

MeasurementData.Display()

'''


