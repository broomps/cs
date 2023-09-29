# Skeleton Program for the AQA A1 Summer 2017 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA AS1 Programmer Team
# developed in a Python 3 environment

from random import *

SOIL = '.'
SEED = 'S'
PLANT = 'P'
ROCKS = 'X'

FIELDLENGTH = 20 
FIELDWIDTH = 35 

#If you put stepping mode it will show you each year but if you enter a year it will just show you the end
def GetHowLongToRun():
  print('Welcome to the Plant Growing Simulation')
  print()
  print('You can step through the simulation a year at a time')
  print('or run the simulation for 0 to 5 years')
  print('How many years do you want the simulation to run?')
  Years = int(input('Enter a number between 0 and 5, or -1 for stepping mode: '))
  return Years

def CreateNewField(): 
  #Field is a 2d array with number of lists equal to the length of the field and list length width of field
  Field = [[SOIL for Column in range(FIELDWIDTH)] for Row in range(FIELDLENGTH)]
  Row = FIELDLENGTH // 2
  Column = FIELDWIDTH // 2
  #Plants a seed in the centre of the soil
  Field[Row][Column] = SEED
  return Field

def ReadFile():   
  FileName = input('Enter file name: ')
  Field = [[SOIL for Column in range(FIELDWIDTH)] for Row in range(FIELDLENGTH)]
  #It tries to open the file and sees if it can read the field that is in the file
  #TestCase.txt is the default field but a user can create a custom field
  try:
    FileHandle = open(FileName, 'r')
    for Row in range(FIELDLENGTH):
      FieldRow = FileHandle.readline()
      for Column in range(FIELDWIDTH):
        Field[Row][Column] = FieldRow[Column]
    FileHandle.close()
  except:
    #If the field cannot be read then the default field is used
    Field = CreateNewField()
  return Field

#It asks the user if they want to use a custom field - if not it will use the default field
def InitialiseField(): 
  Response = input('Do you want to load a file with seed positions? (Y/N): ')
  if Response == 'Y':
    Field = ReadFile()
  else:
    Field = CreateNewField()
  return Field

def Display(Field, Season, Year):
  print('Season: ', Season, '  Year number: ', Year)
  for Row in range(FIELDLENGTH):
    for Column in range(FIELDWIDTH):
      print(Field[Row][Column], end='') #Prints each list on the same line
    print('|{0:>3}'.format(Row)) #Right aligns 3 spaces the line and a new line
  print() #New line after the whole has been printed

#It just iterates through the whole field and counts how many plants there
def CountPlants(Field):
  NumberOfPlants = 0
  for Row in range(FIELDLENGTH):
    for Column in range(FIELDWIDTH):
      if Field[Row][Column] == PLANT:
        NumberOfPlants += 1
  if NumberOfPlants == 1:
    print('There is 1 plant growing')
  else:  
    print('There are', NumberOfPlants, 'plants growing')

def SimulateSpring(Field):
  #Changes seeds to plants
  for Row in range(FIELDLENGTH):
    for Column in range(FIELDWIDTH):
      if Field[Row][Column] == SEED:  
        Field[Row][Column] = PLANT
  CountPlants(Field) #Counts number of plants
  #50/50 chance of frost occuring
  if randint(0, 1) == 1:
    Frost = True
  else:
    Frost = False
  #Simulates frost
  if Frost:    
    PlantCount = 0
    #1 in 3 plants found turns back to soil
    for Row in range(FIELDLENGTH):
      for Column in range(FIELDWIDTH):
        if Field[Row][Column] == PLANT:
          PlantCount += 1
          if PlantCount % 3 == 0:
            Field[Row][Column] = SOIL
    print('There has been a frost')
    CountPlants(Field) #Recounts the number of plants in the field
  return Field

#Summer simulation
def SimulateSummer(Field):
  #1/3 chance of getting a drought 
  RainFall = randint(0, 2)
  if RainFall == 0:
    PlantCount = 0
    #Iterates through the field
    for Row in range(FIELDLENGTH):
      for Column in range(FIELDWIDTH):
        if Field[Row][Column] == PLANT:
          PlantCount += 1
          #1 in every 2 plants becomes soil
          if PlantCount % 2 == 0:
            Field[Row][Column] = SOIL
    print('There has been a severe drought')
    CountPlants(Field)
  return Field

#Makes sure that the seed can be placed within the field
def SeedLands(Field, Row, Column): 
  if Row >= 0 and Row < FIELDLENGTH and Column >= 0 and Column < FIELDWIDTH: 
    if Field[Row][Column] == SOIL:
      #If the seed can be put within the field then the seed is planted
      Field[Row][Column] = SEED
  return Field

#Autumn is simulated
def SimulateAutumn(Field): 
  for Row in range(FIELDLENGTH):
    for Column in range(FIELDWIDTH):
      if Field[Row][Column] == PLANT:
        #The 8 available spaces around the plant get seeds
        Field = SeedLands(Field, Row - 1, Column - 1)
        Field = SeedLands(Field, Row - 1, Column)
        Field = SeedLands(Field, Row - 1, Column + 1)
        Field = SeedLands(Field, Row, Column - 1)
        Field = SeedLands(Field, Row, Column + 1)
        Field = SeedLands(Field, Row + 1, Column - 1)
        Field = SeedLands(Field, Row + 1, Column)
        Field = SeedLands(Field, Row + 1, Column + 1)
  return Field

#Winter is simulated - all plants turn to soil
def SimulateWinter(Field):
  for Row in range(FIELDLENGTH):
    for Column in range(FIELDWIDTH):
      if Field[Row][Column] == PLANT:
        Field[Row][Column] = SOIL
  return Field

#It simulates every season in a year and displays the season and the field
def SimulateOneYear(Field, Year):
  Field = SimulateSpring(Field)
  Display(Field, 'spring', Year)
  Field = SimulateSummer(Field)
  Display(Field, 'summer', Year)
  Field = SimulateAutumn(Field)
  Display(Field, 'autumn', Year)
  Field = SimulateWinter(Field)
  Display(Field, 'winter', Year)

#It is basically main
def Simulation():
  #Gets number of years
  YearsToRun = GetHowLongToRun()
  if YearsToRun != 0: #Validates to make sure number of years is more than 0
    Field = InitialiseField() #Gets the initial blank field - from template or custom
    if YearsToRun >= 1: 
      #If not stepping mode then it just runs the simulation for the number of years
      for Year in range(1, YearsToRun + 1):
        SimulateOneYear(Field, Year)
    else: #Starts stepping mode
      Continuing = True                     
      Year = 0
      while Continuing: #While user wants to keep running
        Year += 1
        SimulateOneYear(Field, Year) #Simulates a year
        #Asks if the user wants to end - if not it runs again
        Response = input('Press Enter to run simulation for another Year, Input X to stop: ')
        if Response == 'x' or Response == 'X': #If user wants to stop then it ends
          Continuing = False
    print('End of Simulation')
  input()
   
if __name__ == "__main__":
  Simulation()      

