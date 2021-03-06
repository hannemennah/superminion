from backtester import *
from includes import *
import sys, getopt

variablesArr = []
settingsArr = []
btcDateArr = []
btcPriceArr = []
btcVolumeArr = []


def getData(whichExchange, tBegin, tEnd):
    global btcDateArr
    global btcPriceArr
    global btcVolumeArr
    if(whichExchange == 'Bitfinex' or whichExchange == 'data/bitfinex.csv'):
        bitcoinDateArr, btcPA, btcVA = buildArrays(ifile="data/bitfinex.csv", beginTime=int(tBegin), endTime=int(tEnd))
    else:
        bitcoinDateArr, btcPA, btcVA = buildArrays(ifile="data/bitstamp.csv", beginTime=int(tBegin), endTime=int(tEnd))



def minitialize(minitfile):
    global variablesArr
    variablesArr = []
    try:
        rawData = open(minitfile, 'r').read()
        try:
            rawDataLines = rawData.split('\n'); del rawDataLines[-1]

            singleLine = rawDataLines[-1]

            values = singleLine.split(' ')
            valIdx = 0
            for topLevelVal in range(0,32):
                if(topLevelVal < 24):
                    variablesArr.append([])
                    for bottomLevelVal in range(0,3):
                        if(topLevelVal in [0, 3, 4, 7, 8, 11, 12, 15, 18, 19, 21, 23]):
                            variablesArr[topLevelVal].append(int(values[valIdx]))
                        else:
                            variablesArr[topLevelVal].append(float(values[valIdx]))
                        valIdx += 1
                else:
                    if(topLevelVal == 24):
                        variablesArr.append(str(values[valIdx])) #dataFile
                    if(topLevelVal == 25):
                        variablesArr.append(str2bool(values[valIdx])) #doWeReactBySelling
                    if(topLevelVal == 26):
                        variablesArr.append(str2bool(values[valIdx])) #doWeReactByBuying
                    if(topLevelVal == 27):
                        variablesArr.append(str2bool(values[valIdx])) #doWeCheatBTSR
                    if(topLevelVal == 28):
                        variablesArr.append(str2bool(values[valIdx])) #doWeCheatSTBR
                    if(topLevelVal == 29):
                        variablesArr.append(str2bool(values[valIdx])) #doWeCheatVioBuys
                    if(topLevelVal == 30):
                        variablesArr.append(str2bool(values[valIdx])) #doWeCheatVioSells
                    if(topLevelVal == 31):
                        variablesArr.append(str2bool(values[valIdx])) #doWeShort
                    valIdx += 1



            if(len(variablesArr) > 0):
                nonEmptiness = True
            else:
                print("Empty minitialize array - no data in array")
                sys.exit()


        except Exception as e:
            print('failed raw minit', str(e))
            sys.exit()
            

    except Exception as e:
        print('failed to even open the minit file...', str(e))
        sys.exit()



def pinitialize(pinitfile):
    global settingsArr
    settingsArr = []
    try:
        rawData = open(pinitfile, 'r').read()
        try:
            rawDataLines = rawData.split('\n')
            #print('rawD =', rawDataLines)
            del rawDataLines[-1]

            singleLine = rawDataLines[-1]
            singleLine = singleLine.replace(',', '')
            singleLine = singleLine.replace('[', '')
            singleLine = singleLine.replace(']', '')

            values = singleLine.split(' ')
            valIdx = 0
            for value in values:
                settingsArr.append(value)

            if(len(settingsArr) > 0):
                nonEmptiness = True
            else:
                print("Empty pinitialize array - no data in array")
                sys.exit()


        except Exception as e:
            print('failed raw pinit', str(e))
            sys.exit()
            

    except Exception as e:
        print('failed to even open the pinit file...', str(e))
        sys.exit()


def buildArrays(ifile="data/bitfinex.csv", howFarBack=0, beginTime=1392786050, endTime=1393414657):# beginTime=None, endTime=None):
    global btcDateArr
    global btcPriceArr
    global btcVolumeArr

    try:
        howFarBack = int(howFarBack)
        if(beginTime):
            beginTime = int(beginTime)
        if(endTime):
            endTime = int(endTime)
    except Exception as e:
        print('non-integer passed as an argument to integer flag...', str(e))
        sys.exit(2)

    try:
        rawData = open(ifile, 'r').read()
        try:
            rawDataLines = rawData.split('\n'); del rawDataLines[-1]

            for singleLine in rawDataLines[-howFarBack:]:
                if(beginTime):
                    if(int(singleLine[:10]) < int(beginTime)):
                        continue

                if(endTime):
                    if(int(singleLine[:10]) > int(endTime)):
                        break
 
                splitLine = singleLine.split(',')
                btcDate = splitLine[0]

                btcPrice = splitLine[1]
                btcVolume = splitLine[2]
                        
                btcDateArr.append(int(btcDate))
                btcPriceArr.append(float(btcPrice))
                btcVolumeArr.append(float(btcVolume))
            
            if(len(btcDateArr) > 0):
                nonEmptiness = True
                return (btcDateArr, btcPriceArr, btcVolumeArr) 
            else:
                print("Empty array - no data in array")
                sys.exit()

        except Exception as e:
            print('failed raw data', str(e))
            sys.exit()
            

    except Exception as e:
        print('failed to even open the file...', str(e))
        sys.exit()




def main(argv):
    global variablesArr
    global settingsArr
    global btcDateArr
    global btcPriceArr
    global btcVolumeArr

    inputfile = ''
    outputfile = ''
    lastntrades = 0
    beginT = ''
    endT = ''
    usageString = 'justplot.py -i <inputfile> -o <outputfile> -l <lastntrades> -b <begintime> -e <endtime>'
    try:
        opts, args = getopt.getopt(argv, 'hi:o:l:b:e:',['ifile=','ofile=','lastntrades=','begintime=','endtime='])
    except getopt.GetoptError:
        print(usageString)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usageString)
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
        elif opt in ('-l', '--lastntrades'):
            lastntrades = arg
        elif opt in ('-b', '--begintime'):
            beginT = arg
        elif opt in ('-e', '--endtime'):
            endT = arg

    minitialize('plotminitialization.txt')
    pinitialize('plotsettings.txt')


    #myPlot = Plotter()
    if(inputfile):
        getData(str(inputfile), tBegin=beginT, tEnd=endT)
    else:
        getData(str(variablesArr[24]), tBegin=beginT, tEnd=endT)


    plotTester = Backtester(btcDA=btcDateArr, btcPA=btcPriceArr, btcVA=btcVolumeArr, whichVar=0, BTSRint=int(variablesArr[0][0]), BTSRcut=float(variablesArr[1][0]), BTSRret=float(variablesArr[2][0]), BTSRmoas=int(variablesArr[3][0]), STBRint=int(variablesArr[4][0]), STBRcut=float(variablesArr[5][0]), STBRret=float(variablesArr[6][0]), STBRmoas=int(variablesArr[7][0]), volInt=int(variablesArr[8][0]), volCut=float(variablesArr[9][0]), volRet=float(variablesArr[10][0]), volMOAS=int(variablesArr[11][0]), vioBuyInt=int(variablesArr[12][0]), vioBuyCut=float(variablesArr[13][0]), vioBuyRet=float(variablesArr[14][0]), vioSellInt=int(variablesArr[15][0]), vioSellCut=float(variablesArr[16][0]), vioSellRet=float(variablesArr[17][0]), BTSRwindowLenForward=int(variablesArr[18][0]), BTSRwindowLenBack=int(variablesArr[19][0]), reactToVioBuy=variablesArr[25], reactToVioSell=variablesArr[26], reactToVioBuyCut=float(variablesArr[20][0]), reactToVioSellCut=float(variablesArr[22][0]), reactToVioBuyForward=int(variablesArr[21][0]), reactToVioSellForward=int(variablesArr[23][0]), whichExchange=str(variablesArr[24]), cheatBTSR=variablesArr[27], cheatSTBR=variablesArr[28], cheatVioBuys=variablesArr[29], cheatVioSells=variablesArr[30], doWeShort=variablesArr[31])

    multiString = ''
    usingMultiString = False
    multiPass = []

    
    if(len(multiString) > 0):
        multiString = multiString[0:-2]
    if(usingMultiString):
        multiPass.append('l')
        multiPass.append(multiString)
    plotTester.multiPlot(multiPass)


if __name__ == '__main__':
    main(sys.argv[1:])
