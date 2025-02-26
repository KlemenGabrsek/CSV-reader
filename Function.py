from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def DeterminateThermalOrCurrentOrVoltageChannel(data_list,NumOfCh)->tuple:
  #channel data:
  # ['1008', 'LED 1 Master', 'Temp (Type K)', 'None', 'C', 'Temp (Type K)#0,2#0,016#Auto#0,001#C#External#0#true#10 M', 'False', '1', '0', 'C', ' ', '']
  # ['1038', 'V4', 'DC Voltage', 'Auto', '5,5', 'DC Voltage#10M#1#0,016#Auto#0,001', 'False', '1', '0', 'VDC', ' ', '']
  #check if channel is for temperature or current
  NumOfCurrentCh = 0
  NumOfThermalCh = 0
  NumOfVoltageCh = 0
 
  for i in range(7,(NumOfCh+8)):
    if(data_list[i][2].split()[0] == "Temp" ):
      NumOfThermalCh = NumOfThermalCh +1
    if(data_list[i][2] == "DC Voltage" ):
       NumOfVoltageCh = NumOfVoltageCh+1
    if(data_list[i][9] == "ADC" ):
       NumOfCurrentCh = NumOfCurrentCh+1
  
  return NumOfThermalCh,NumOfCurrentCh,NumOfVoltageCh

def AddNameAndNumOfChToObject(ListOfChannels, data_list,NumOfCh ) -> bool:
  #list of channels vrstnired:
  #ListOfChannels = [ThermalCoupleChannels, CurrentChannels,VoltageChannels]
  ZapStThermalKanala=0
  ZapStCurrentKanala=0
  ZapStVoltageKanala=0
  ZapStKanala = [ZapStThermalKanala,ZapStCurrentKanala,ZapStVoltageKanala]
  for Row in range(8,(NumOfCh+8)):
    if(data_list[Row][2].split()[0] == "Temp" ):
      TypeOfCh = 0
      
    if(data_list[Row][9] == "ADC" ):
      TypeOfCh = 1
      
    if(data_list[Row][2] == "DC Voltage" ):
      TypeOfCh = 2
      
    ListOfChannels[TypeOfCh][ZapStKanala[TypeOfCh]].Name= data_list[Row][1]
    ListOfChannels[TypeOfCh][ZapStKanala[TypeOfCh]].NumOfCh= int(data_list[Row][0])
    if (TypeOfCh == 0):
      ZapStKanala[0] += 1
    if (TypeOfCh == 1):
      ZapStKanala[1] += 1
    if (TypeOfCh == 2):
      ZapStKanala[2] += 1
  
  return True

def AddTimeAndValueOfChToObject(ListOfChannels, data_list,NumOfCh ) -> bool:
  #line number of header with data
  StartOfData = 8+NumOfCh+15
  #Data of header (InforLIne)
  InfoLine = data_list[StartOfData]
  
  #sprehod čez vse vrste kanalov
  for Chnannels in ListOfChannels:
    #print(Chnannels)
    #sprehod čez vse kanale enega tipa
    for Channel in Chnannels:
      #print(Channel)
      #sorehod čez vse stolpce v InfoLine, prva 2 stolpca nista relevantana
      for coloum in range(2,len(InfoLine)):
        #če je 1.beseda stolpca "Limit" naj ta stolpec preskoči
        if (InfoLine[coloum].split()[0] !="Limit"):
        #primerjava številke kanala (iz objekta) in iz Infoline
          if (Channel.NumOfCh == int(InfoLine[coloum].split()[0])) :
              # stopec s podatki za določen objekt se zapiše v ta objekt
              Channel.ColoumInCSV = coloum 
              #ko se stolpec za določen objekt najde, se for loop s coloum lahko zaključi
              break
  return True

def AddValueAndTimeToObject(ListOfChannels, data_list,NumOfCh ) -> bool:
  #line number where Values start
  StartOfData = 8+NumOfCh+16
  NotRelavant,StartTime = data_list[StartOfData][1].split()
  TimeFormat = "%H:%M:%S:%f"
  StartTimeObject=datetime.strptime(StartTime, TimeFormat)
  #sprehod čez vse vrstice, ki imajo podatke
  for row in range(StartOfData,len(data_list)):
    #sprehod čez vse vrste kanalov
    for Chnannels in ListOfChannels:
      #sprehod čez vse kanale enega tipa
      for Channel in Chnannels:
        #zapis vrednosti iz ene vrstice v pripadajoč objekt
        Channel.Value.append( float((data_list[row][Channel.ColoumInCSV]).replace(",",".")))
        DatePart, TimePart = data_list[row][1].split()
        TimePartObject=datetime.strptime(TimePart, TimeFormat)
        DifferenceBetweenStartAndTimePart = TimePartObject-StartTimeObject
        MInutes = DifferenceBetweenStartAndTimePart.total_seconds() 
        Channel.Time.append( MInutes)
  return True

