#Definition of classes

class ThermalCoupleCh:
    def __init__(self,) -> None:
        self.NumOfCh = None
        self.Value = []
        self.Name = None
        self.Time = []
        self.ColoumInCSV = None
    
class CurrentCh:
    def __init__(self) -> None:
        self.NumOfCh = None
        self.Value = []
        self.Name = None
        self.Time = []
        self.ColoumInCSV = None

class VoltageCh:
    def __init__(self) -> None:
        self.NumOfCh = None
        self.Value = []
        self.Name = None
        self.Time = []
        self.ColoumInCSV = None

class MetaData:
    def __init__(self) -> None:
        self.Date = None
        self.NumOfChannels = None
        self.NumOfThermoCoup = None
        self.NumOfVoltageCh = None
        self.NumOfCurrentCh = None
    def Display(self)->None:
         print(f"Date: {self.Date}, \n Number of thermo couples: {self.NumOfThermoCoup},\n Number of Voltage Ch: {self.NumOfVoltageCh},\n Number of Current Ch: {self.NumOfCurrentCh}")

        

    