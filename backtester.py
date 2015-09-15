from includes import *
import matplotlib
from matplotlib.widgets import MultiCursor
import matplotlib.pyplot as plt
import collections


o
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

#Backtester
class Backtester:
    def __init__(self, btcDA, btcPA, btcVA, whichVar, BTSRint, BTSRcut, BTSRret, BTSRmoas, STBRint, STBRcut, STBRret, STBRmoas, volInt, volCut, volRet, volMOAS, vioBuyInt, vioBuyCut, vioBuyRet, vioSellInt, vioSellCut, vioSellRet, BTSRwindowLenForward, BTSRwindowLenBack, reactToVioBuy, reactToVioSell, reactToVioBuyCut, reactToVioSellCut, reactToVioBuyForward, reactToVioSellForward, whichExchange, cheatBTSR=True, cheatSTBR=True, cheatVioBuys=True, cheatVioSells=True, doWeShort=True):

        self.btcDateArr = btcDA
        self.startSec = self.btcDateArr[0]
        self.endSec = self.btcDateArr[-1]
        self.btcPriceArr = btcPA
        self.btcVolumeArr = btcVA
        self.whichVar = whichVar
        self.BTSRinterval = BTSRint
        self.BTSRcutoff = BTSRcut
        self.BTSRreturn = BTSRret
        self.BTSRMOAS = BTSRmoas
        self.STBRinterval = STBRint
        self.STBRcutoff = STBRcut
        self.STBRreturn = STBRret
        self.STBRMOAS = STBRmoas
        self.VolumeInterval = volInt
        self.VolumeCutoff = volCut
        self.VolumeReturn = volRet
        self.VolumeMOAS = volMOAS
        self.ViolenceBuyInterval = vioBuyInt
        self.ViolenceBuyThreshold = vioBuyCut
        self.ViolenceBuyReturn = vioBuyRet
        self.ViolenceSellInterval = vioSellInt
        self.ViolenceSellThreshold = vioSellCut
        self.ViolenceSellReturn = vioSellRet
        self.BTSRwindowForwardLen = BTSRwindowLenForward
        self.BTSRwindowBackLen = BTSRwindowLenBack
        self.doWeReactBySelling = reactToVioBuy
        self.doWeReactByBuying = reactToVioSell
        self.reactSellCut = reactToVioBuyCut
        self.reactBuyCut = reactToVioSellCut
        self.reactBuyWindowLenForward = reactToVioSellForward
        self.reactSellWindowLenForward = reactToVioBuyForward
        self.cheatBTSR = cheatBTSR
        self.cheatSTBR = cheatSTBR
        self.cheatVioBuys = cheatVioBuys
        self.cheatVioSells = cheatVioSells
        self.doWeShort = doWeShort
        self.whichExchange = whichExchange

        self.firstRun()
        self.myIntegral = 1.0
        self.myReturn = 1.0

        self.textDropper = 0 
        self.isMPressed = False #mark
        self.isYPressed = False #y data (journal)
        self.isDPressed = False #date
        self.isBPressed = False #begin (console)
        self.isEPressed = False #end (console)

    def firstRun(self):
        print('BEGIN BACKTEST: ', str(prettifyDate(self.startSec)), 'to', str(prettifyDate(self.endSec)), '(', str(self.startSec), '-', str(self.endSec), ')')
        self.fullPrice = self.stretchData(self.btcPriceArr)
        self.fullVolumeArr = self.preciseVolArr()
        self.volAvg = precisePeriodSum(self.fullVolumeArr, self.VolumeInterval)
        #SECTION #1 - BTSR setup
        if(self.cheatBTSR):
            if(self.whichExchange == 'Bitstamp'):
                self.BTSRbuys = [1357544570, 1358185204, 1358740345, 1359321154, 1360211325, 1361981621, 1362371780, 1363632224, 1364813826, 1365786804, 1366118625, 1366317526, 1366717253, 1367099161, 1367586334, 1367643672, 1367586334, 1367643672, 1367956935, 1368170677, 1368593229, 1368706677, 1369310910, 1369841155, 1370891781, 1371519032, 1373205130, 1373473952, 1373593155, 1375018651, 1376883964, 1377092774, 1377567117, 1378725249, 1381675664, 1382078675, 1382327979, 1382884696, 1383492024, 1385156824, 1385297805, 1385487587, 1385552655, 1385624695, 1386060031, 1386144465, 1386412764, 1386466551, 1386538367, 1386621357, 1386698835, 1387255334, 1387373040, 1387384662, 1387418931, 1387442472, 1387501028, 1387686378, 1387955740, 1388345966, 1388531781, 1388679901, 1388734106, 1388920675, 1388972359, 1389167122, 1389198637, 1389241497, 1389277424, 1389295072, 1389339548, 1389363891, 1389389756, 1389401472, 1389425815, 1389435400, 1389483935, 1389535513, 1389624214, 1389645971, 1389757495, 1390140476, 1390664645, 1390741697, 1390871691, 1390902093, 1390924108, 1391097084, 1391260886, 1391944209, 1392067857, 1392372018, 1392614025, 1392828260, 1392958521, 1393010757, 1393082169, 1393363849, 1393801577, 1393918613, 1394364276, 1394485940, 1394568593, 1395380572, 1395658284, 1396329423, 1396516548, 1397184381, 1397213475, 1397447547, 1397538134, 1397592354, 1397678974, 1397886597, 1398041323, 1398334905, 1398516079, 1398673449, 1398847847, 1398956441, 1399147392, 1399355836, 1399448396, 1399642992, 1399755230, 1400550375, 1400592647, 1400736954, 1400969448, 1401202671, 1401439539, 1401583845, 1401731796, 1401965019, 1402629705, 1402854911, 1403031286, 1403397884, 1403813313, 1404102655, 1405074175, 1405593097, 1406566803, 1406773060, 1408185518, 1408419470, 1408535352, 1408714643, 1409834114, 1410180304, 1410303475, 1411489595, 1412042098, 1412573753, 1412748886, 1413117917, 1413620383, 1415517660, 1415738662, 1416078504, 1416756103] 
            else:
                #assume Bitfinex
                self.BTSRbuys = [1377859580, 1381649614, 1382073981, 1382875888, 1383478781, 1384319496, 1384981139, 1385485084, 1386528874, 1387426401, 1387958269, 1388649456, 1389344860, 1393051364, 1389330952, 1394337861, 1395645221, 1396319762, 1397432409, 1398857333, 1399441224, 1400523559, 1400960290, 1402849629, 1404060135, 1405061769, 1408527139, 1409808851, 1411470726, 1413108896, 1415121077, 1415554930, 1416759247, 1421554072]
        else:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")


        #SECTION #2 - STBR setup
        if(self.cheatSTBR):
            if(self.whichExchange == 'Bitstamp'):
                self.STBRsells = [1358082772, 1359768064, 1365873973, 1366037717, 1366553028, 1366909892, 1367328695, 1367423494, 1367488477, 1367866144, 1368556235, 1369677560, 1369938161, 1370156836, 1370593364, 1370750382, 1371154026, 1371756615, 1372371535, 1372854099, 1373004541, 1374117645, 1375276786, 1377188136, 1378301619, 1380719684, 1381930591, 1384035174, 1384850849, 1385089432, 1385242807, 1385382239, 1385604555, 1385655680, 1385847785, 1386228124, 1386326501, 1386424236, 1386499479, 1386597816, 1386645793, 1386753964, 1387212721, 1387264870, 1387310462, 1387343390, 1387389132, 1387455882, 1387525314, 1387559881, 1387723925, 1388107137, 1388452273, 1388621283, 1388710785, 1388763100, 1388954711, 1389004505, 1389089595, 1389114807, 1389182879, 1389262297, 1389289400, 1389310200, 1389347916, 1389382910, 1389406797, 1389459592,1389486065,1389519081,1389616607, 1389679900, 1389688420, 1389871301, 1390218840, 1390388670, 1390527051, 1390690853, 1390839455, 1390881388, 1390919915, 1391060130, 1391163915, 1391706831, 1392026200, 1392131334, 1392309864, 1392422932, 1392526083, 1392548564, 1392845452, 1392872562, 1392990259, 1393028610, 1393175401, 1393556264, 1393901421, 1393945062, 1394178473, 1394442300, 1394541483, 1395113438, 1395438098, 1395877809, 1396123122, 1396439847, 1396236191, 1397097100, 1396877575, 1397200250, 1397386714, 1397560615, 1397714019, 1397809896, 1397991070, 1398069094, 1398394414, 1398540544, 1398612617, 1398722380, 1398797098, 1398920729, 1399002357, 1399178003, 1399430904, 1399499414, 1399559906, 1399789485, 1399812078, 1399976063, 1400858667, 1400883447, 1401168417, 1401265350, 1401838933, 1402076529, 1402288617, 1402454059, 1402580145, 1402669791, 1402749961, 1402922692, 1403210577, 1403487529, 1403642768, 1404243318, 1404452490, 1404725069, 1406192189, 1406512142, 1406709653, 1406913723, 1407019402, 1407771547, 1407902006, 1408257671, 1408504013, 1408668727, 1408814491, 1409460228, 1410131473, 1410379273, 1410926666, 1411522953, 1411587586, 1411898239, 1412331902, 1412878151, 1414033197, 1415642756, 1416226533, 1416466299, 1416916642, 1418019565, 1418661720, 1420246259, 1421101077]
            else:
                #assume Bitfinex
                self.STBRsells = [1378297117, 1380707227, 1381923258, 1382578831, 1384016739, 1385844094, 1386220391, 1386721676, 1387168445, 1387552720, 1389059745, 1389504803, 1389852505, 1390193253, 1390513139, 1390513139, 1391618831, 1392105614, 1392300327, 1392522857, 1392856651, 1389497849, 1394164010, 1395200162, 1395860796, 1396437981, 1397084707, 1397703616, 1398385112, 1398600687, 1398985504, 1399778267, 1402564804, 1403200913, 1403480991, 1403632897, 1404700991, 1406182081, 1407762859, 1409452820, 1410122159, 1410819946, 1412315992, 1414006523, 1416452557, 1417993484, 1418659224, 1420230072, 1421090298]
        else:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        #SECTION #3 - volume setup
        if not (self.cheatBTSR and self.cheatSTBR): 
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")
 
        #SECTION #4 - vioBuys setup
        if not (self.cheatVioBuys and self.cheatVioSells):
            #at least one of these isn't cheating, so we need fullPrice
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if(self.cheatVioBuys):
            if(self.whichExchange == 'Bitstamp'):
                self.vioBuys = [1367331941, 1367334930, 1367380214, 1367401370, 1367433565, 1367435664, 1367490820, 1367504603, 1367507569, 1367511320, 1367547958, 1367595412, 1367660750, 1367679069, 1367692241, 1367736730, 1367738475, 1367871286, 1367875514, 1367927047, 1368562833, 1368572107, 1368577369, 1368603460, 1369684623, 1369943364, 1370163875, 1370187674, 1370605341, 1370611984, 1370760470, 1370766112, 1370831765, 1370835612, 1371163106, 1371778407, 1372386551, 1372691608, 1372891238, 1372910042, 1373045386, 1373244179, 1373292416, 1373358135, 1373486197, 1373490609, 1373497226, 1373620356, 1374131015, 1375286598, 1375478552, 1380736715, 1382592840, 1383681966, 1383814150, 1383969105, 1384045471, 1384057690, 1384099345, 1384762484, 1384765261, 1384805549, 1384806751, 1384810633, 1384823667, 1384825053, 1384827087, 1384829583, 1384849457, 1384851120, 1384859255, 1384861570, 1384863977, 1384864852, 1384865290, 1384889578, 1384905990, 1384909454, 1384921781, 1384923933, 1384925209, 1384944465, 1384949096, 1384975209, 1385076192, 1385137242, 1385215906, 1385216636, 1385258393, 1385263681, 1385267985, 1385469038, 1385576977, 1385577463, 1385646882, 1385705240, 1385785558, 1385877235, 1385879816, 1385899280, 1385925195, 1385926332, 1385927579, 1385928913, 1385930575, 1385932893, 1385939128, 1385990962, 1385990912, 1386190665, 1386232342, 1386233035, 1386233840, 1386237133, 1386248776, 1386292148, 1386345368, 1386347563, 1386369194, 1386382155, 1386386300, 1386387483, 1386397044, 1386402716, 1386418470, 1386418590, 1386420387, 1386425580, 1386432730, 1386433631, 1386505281, 1386756486, 1386758059, 1386764549, 1386775169, 1386790410, 1386819319, 1387200529, 1387217720, 1387223072, 1387235991, 1387245307, 1387346944, 1387347670, 1387351560, 1387356280, 1387363335, 1387364994, 1387366239, 1387367899, 1387371115, 1387439019, 1387447157, 1387452487, 1387563602, 1387570593, 1387610529, 1387700642, 1387855881, 1387856058, 1387856142, 1387904489, 1388024069, 1388092029, 1388254391, 1388464087, 1388777608, 1388937196, 1388943793, 1388960443, 1389002882, 1389008111, 1389010281, 1389012371, 1389013771, 1389023977, 1389074719, 1389100606, 1389122293, 1389132317, 1389135327, 1389139612, 1389190338, 1389194450, 1389195398, 1389266397, 1389275847, 1389291737, 1389293874, 1389316828, 1389526825, 1389530824, 1389572683, 1389619697, 1389704946, 1389791518, 1389986570, 1389957205, 1390222701, 1390390281, 1390533038, 1390541296, 1390543524, 1390548298, 1390552118, 1390552118, 1390564722, 1390694837, 1390751041, 1390840958, 1390844470, 1390863821, 1390865255, 1390883459, 1390887797, 1390920995, 1391642169, 1391671939, 1391738261, 1391742123, 1391751755, 1391756343, 1391806796, 1391818566, 1391899308, 1392027920, 1392030076, 1392034079, 1392142831, 1392154161, 1392154197, 1392190843, 1392191008, 1392320893, 1392326720, 1392341795, 1392347923, 1392370376, 1392372592, 1392395812, 1392399332, 1392578687, 1392630760, 1392634790, 1392880069, 1392881073, 1392891867, 1392942960, 1392944423, 
1392946319]
            else:
                #assume Bitfinex
                self.vioBuys = [1367331941, 1367334930, 1367380214]
        else:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        #SECTION #5 - vioSells setup
        if(self.cheatVioSells):
            self.vioSells = [1378297117, 1380707227, 1381923258, 1382578831, 1384016739, 1385844094, 1386220391, 1386721676, 1387168445, 1387552720, 1389059745, 1389504803, 1389852505, 1390193253, 1390513139, 1390513139, 1391618831, 1392105614, 1392300327, 1392522857, 1392856651, 1389497849, 1394164010, 1395200162, 1395860796, 1396437981, 1397084707, 1397703616, 1398385112, 1398600687, 1398985504, 1399778267, 1402564804, 1403200913, 1403480991, 1403632897, 1404700991, 1406182081, 1407762859, 1409452820, 1410122159, 1410819946, 1412315992, 1414006523, 1416452557, 1417993484, 1418659224, 1420230072, 1421090298]
        else:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")


        #SECTION #6 - reactSells setup
        if(self.doWeReactBySelling):
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        #SECTION #7 - reactBuys setup
        if(self.doWeReactByBuying):
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        #SECTION #8 - associate BTSR/STBR with volume (window)
        if not self.cheatBTSR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")
        if not self.cheatSTBR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.printVariables()
        self.recombineBuysAndSells()
        self.checkProfits()

    def recombineBuysAndSells(self):
        #SECTION #9 - combine all buys and sells
        self.myBuys = combineLists(self.BTSRbuys, self.vioBuys)
        self.mySells = combineLists(self.STBRsells, self.vioSells)

        #SECTION #10 - clean buys and sells
        self.myBuys, self.mySells = self.cleanBuysAndSells(self.myBuys, self.mySells)
        
    def checkProfits(self):
        #SECTION #11 - calculate profits
        if(self.doWeShort):
            return self.calcFiatProfitsWithShorting(self.myBuys, self.mySells, self.fullPrice)
        else:
            return self.calcFiatProfits(self.myBuys, self.mySells, self.fullPrice)

    def cleanBuysAndSells(self, inpList1, inpList2, lag=10):
        realList1 = [self.startSec]
        if(len(inpList1) > 0):
            if(inpList1[0] > self.startSec):
                realList1.extend(inpList1)

        l1 = len(realList1)
        l2 = len(inpList2)

        if(l2 == 0):
            return [self.startSec], []
        else:
            #both lists have at least 1 element
            idx1 = 0
            idx2 = 0
            currOnList1 = False if inpList2[0] < realList1[0] else True
            outList1 = []
            outList2 = []
            if(currOnList1):
                outList1.append(realList1[0])
                idx1 += 1
                currOnList1 = False
            else:
                outList2.append(inpList2[0]+lag)
                idx2 += 1
                currOnList1 = True

            while(idx1 < l1 and idx2 < l2):
                if(currOnList1):
                    valToBeat = outList2[-1]
                    while(idx1 < l1 and realList1[idx1] <= valToBeat):
                        idx1 += 1
                    if(idx1 >= l1):
                        return outList1, outList2
                    else:
                        outList1.append(realList1[idx1]+lag)
                        currOnList1 = False
                else:
                    valToBeat = outList1[-1]
                    while(idx2 < l2 and inpList2[idx2] <= valToBeat):
                        idx2 += 1
                    if(idx2 >= l2):
                        return outList1, outList2
                    else:
                        outList2.append(inpList2[idx2]+lag)
                        currOnList1 = True

        

        if(len(outList1) > 0):
            while(outList1[-1] >= self.endSec):
                outList1.pop()
        if(len(outList2) > 0):
            while(outList2[-1] >= self.endSec):
                outList2.pop()

        return outList1, outList2


    def changeBTSRinterval(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeSTBRinterval(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeBTSRcutoff(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeSTBRcutoff(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeBTSRreturn(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeSTBRreturn(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeBTSRMOAS(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeSTBRMOAS(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeVolumeInterval(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatBTSR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatSTBR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")


        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeVolumeCutoff(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatBTSR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatSTBR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeVolumeReturn(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatBTSR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatSTBR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeVolumeMOAS(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatBTSR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatSTBR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeViolenceBuyInterval(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeViolenceBuyThreshold(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeViolenceBuyReturn(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeViolenceSellInterval(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeViolenceSellThreshold(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeViolenceSellReturn(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeBTSRwindowForwardLen(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatBTSR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatSTBR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")


        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeBTSRwindowBackLen(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatBTSR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        if not self.cheatSTBR:
            #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
            print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()
    
    def changeReactSellCut(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()
        
    def changeReactBuyCut(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeReactBuyWindowLenForward(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def changeReactSellWindowLenForward(self, newValue):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()    

    def changeDoWeReactByBuying(self):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()


    def changeDoWeReactBySelling(self):
        #THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE :)
        print("THIS IS WHERE THE FUN STUFF HAPPENS, BUT I'M NOT WILLING TO SHARE THIS CODE")

        self.recombineBuysAndSells()
        return self.checkProfits()

    def printVariables(self):
        printString = ''
        printString += ' ' + str(self.BTSRinterval)
        printString += ' ' + str(self.BTSRcutoff)
        printString += ' ' + str(self.BTSRreturn)
        printString += ' ' + str(self.BTSRMOAS)
        printString += ' ' + str(self.STBRinterval)
        printString += ' ' + str(self.STBRcutoff)
        printString += ' ' + str(self.STBRreturn)
        printString += ' ' + str(self.STBRMOAS)
        printString += ' ' + str(self.VolumeInterval)
        printString += ' ' + str(self.VolumeCutoff)
        printString += ' ' + str(self.VolumeReturn)
        printString += ' ' + str(self.VolumeMOAS)
        printString += ' ' + str(self.ViolenceBuyInterval)
        printString += ' ' + str(self.ViolenceBuyThreshold)
        printString += ' ' + str(self.ViolenceBuyReturn)
        printString += ' ' + str(self.ViolenceSellInterval)
        printString += ' ' + str(self.ViolenceSellThreshold)
        printString += ' ' + str(self.ViolenceSellReturn)
        printString += ' ' + str(self.BTSRwindowForwardLen)
        printString += ' ' + str(self.BTSRwindowBackLen)
        printString += ' ' + str(self.doWeReactBySelling)
        printString += ' ' + str(self.doWeReactByBuying)
        printString += ' ' + str(self.reactSellCut)
        printString += ' ' + str(self.reactBuyCut)
        printString += ' ' + str(self.reactBuyWindowLenForward)
        printString += ' ' + str(self.reactSellWindowLenForward)
        print(printString)










    def multiPlot(self, *rplots): #buyFuncArr=[], sellFuncArr=[]): #, plotter1=[], plotter2=[], plotter3=[], plotter4=[]): #, buy2FuncArr=[]):
        xticksProfit = np.arange(self.startSec, self.endSec, (len(self.btcDateArr) / .65))
        btcPrettyDateArr = []
        for dateTick in xticksProfit:
            btcPrettyDate = prettifyDate(int(dateTick))
            btcPrettyDateArr.append(btcPrettyDate)

        colorArray = ['g', 'r', 'b', '#00FF00', '#FF80FF', '#00E6E6', '#FFA319', '#FFFF00', '#6600CC', '#663300']
        #           green  red  blue  neon-green   pink     baby-blue    orange    yellow    purple    brown

        markColorArray = ['r', 'b', '#00FF00', '#FF80FF', '#00E6E6', '#FFA319', '#FFFF00', '#6600CC', '#663300']
        #                 red  blue neon-green   pink    baby-blue    orange     yellow    purple      brown

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        plt.xticks(xticksProfit, btcPrettyDateArr)
        ax2.plot(range(self.startSec, self.endSec), self.stretchData(self.btcPriceArr), 'g')
        
        argKeeperTracker = 0
        markKeeperTracker = 0
        justMarks = False
        profPlot = False
        nextIsBuyList = False
        nextIsSellList = False
        alreadyHaveBuyList = False
        alreadyHaveSellList = False
        multicolors = False
        haveMultiString = False
        nextIsMultiString = False
        multiString = ''
        buyList1 = []
        buyList2 = []
        sellList1 = []
        sellList2 = []

        rplots = list(rplots)
        for plotter in rplots:
            if(isinstance(plotter, basestring)):
                if(plotter == '.'):
                    justMarks = True
                elif(plotter == 'pp'):
                    profPlot = True
                elif(plotter == 'b'):
                    multicolors = True
                    nextIsBuyList = True
                elif(plotter == 's'):
                    multicolors = True
                    nextIsSellList = True
                elif(plotter == 'l'):
                    haveMultiString = True
                    nextIsMultiString = True
                elif(haveMultiString):
                    if(nextIsMultiString):
                        multiString = str(plotter)
                        nextIsMultiString = False
            elif(hasattr(plotter, "__len__") and len(plotter) > 0 and hasattr(plotter[0], "__len__") and len(plotter[0]) > 0):
                #i.e. if plotter is a list of lists [[],[]]
                for expandableMiniPlotter in plotter:
                    rplots.append(expandableMiniPlotter)
            elif(justMarks):
                if(len(plotter) < 6000): #otherwise it tends to run out of memory and crash, or take waaaaaay too long
                    for i in range(len(plotter)):
                        plt.axvline(x=plotter[i], color=markColorArray[markKeeperTracker])
                    markKeeperTracker += 1
                justMarks = False
            elif(multicolors):
                if(nextIsBuyList):
                    if(alreadyHaveBuyList):
                        buyList2 = plotter
                    else:
                        buyList1 = plotter
                        alreadyHaveBuyList = True
                    nextIsBuyList = False
                if(nextIsSellList):
                    if(alreadyHaveSellList):
                        sellList2 = plotter
                    else:
                        sellList1 = plotter
                        alreadyHaveSellList = True
                    nextIsSellList = False
            else:
                argKeeperTracker += 1
                ax1.plot(self.fitData(plotter), plotter, colorArray[argKeeperTracker])

        if(profPlot):

            #ax1.plot(range(self.startSec, (self.endSec)),self.profitRatioArr, color="#21dd1b")
            ax1.plot(range(self.startSec, (self.endSec)),self.profitRatioArr, color="black")

            if(len(self.myBuys) > 0 and len(self.mySells) > 0):

                colorInt = 0
                endOnGreen = True

                if(multicolors):
                    whichLB = whichList(np.add(10,buyList1), np.add(10,buyList2))
                    whichLS = whichList(np.add(10,sellList1), np.add(10,sellList2))
                else:
                    whichLB = [[], [], []]
                    whichLS = [[], [], []]
                if(self.myBuys[0] <= self.mySells[0]):
                    if(len(self.myBuys) <= len(self.mySells)):
                        endOnGreen = False
                    while(colorInt < len(self.myBuys) and colorInt < len(self.mySells)):
                        if(self.myBuys[colorInt] in whichLB[0]):
                            plt.axvspan(self.myBuys[colorInt], self.mySells[colorInt], facecolor='#00FF00', alpha=0.4)
                        elif(self.myBuys[colorInt] in whichLB[1]):
                            plt.axvspan(self.myBuys[colorInt], self.mySells[colorInt], facecolor='g', alpha=0.4)
                        elif(self.myBuys[colorInt] in whichLB[2]):
                            plt.axvspan(self.myBuys[colorInt], self.mySells[colorInt], facecolor='#009980', alpha=0.4)
                        else:
                            plt.axvspan(self.myBuys[colorInt], self.mySells[colorInt], facecolor='g', alpha=0.2)
                            #print('sit1, c=', colorInt, 'mB[c]=', self.myBuys[colorInt])
                        if((colorInt + 1) < len(self.myBuys)):
                            if(self.mySells[colorInt] in whichLS[0]):
                                plt.axvspan(self.mySells[colorInt], self.myBuys[colorInt + 1], facecolor='#FF3300', alpha=0.5)
                            elif(self.mySells[colorInt] in whichLS[1]):
                                plt.axvspan(self.mySells[colorInt], self.myBuys[colorInt + 1], facecolor='r', alpha=0.2)
                            elif(self.mySells[colorInt] in whichLS[2]):
                                plt.axvspan(self.mySells[colorInt], self.myBuys[colorInt + 1], facecolor='r', alpha=0.6)
                            else: #this should mean it's in both
                                plt.axvspan(self.mySells[colorInt], self.myBuys[colorInt + 1], facecolor='r', alpha=0.4)
                                #print('sit2, c=', colorInt, 'mS[c]=', self.mySells[colorInt])

                            #plt.axvspan(self.mySells[colorInt], self.myBuys[colorInt + 1], facecolor='r', alpha=0.5)
                        colorInt += 1
                    if(endOnGreen):
                        if(self.myBuys[colorInt] in whichLB[0]):
                            plt.axvspan(self.myBuys[colorInt], self.endSec, facecolor='#00FF00', alpha=0.4)
                        elif(self.myBuys[colorInt] in whichLB[1]):
                            plt.axvspan(self.myBuys[colorInt], self.endSec, facecolor='g', alpha=0.4)
                        elif(self.myBuys[colorInt] in whichLB[2]):
                            plt.axvspan(self.myBuys[colorInt], self.endSec, facecolor='#009980', alpha=0.4)
                        else: #this should mean it's in both
                            plt.axvspan(self.myBuys[colorInt], self.endSec, facecolor='g', alpha=0.2)
                            #print('sit3, c=', colorInt, 'mB[c]=', self.myBuys[colorInt])
                        #plt.axvspan(self.myBuys[colorInt], self.endSec, facecolor='g', alpha=0.5)
                    else:
                        #if(colorInt < len(self.mySells)):
                        #print('COLOR INT IS ', colorInt)
                        if(self.mySells[-1] in whichLS[0]):
                            plt.axvspan(self.mySells[colorInt-1], self.endSec, facecolor='#FF3300', alpha=0.5)
                        elif(self.mySells[-1] in whichLS[1]):
                            plt.axvspan(self.mySells[colorInt-1], self.endSec, facecolor='r', alpha=0.2)
                        elif(self.mySells[-1] in whichLS[2]):
                            plt.axvspan(self.mySells[colorInt-1], self.endSec, facecolor='r', alpha=0.6)
                        else: #this should mean it's in both
                            plt.axvspan(self.mySells[colorInt-1], self.endSec, facecolor='r', alpha=0.4)
                            #print('sit4, c=', colorInt, 'mS[c-1]=', self.mySells[colorInt-1])
                        #plt.axvspan(self.mySells[colorInt-1], self.endSec, facecolor='r', alpha=0.5)
                        #FF3300 = orange
                        #00FF00 = light green
                        #'r' = red
                        #009933 = dark green
                        #facecolor='r', alpha=0.7 ... when both
                        #facecolor='g', alpha=0.7 ... when both
                else:
                    print('WE FUCKED UP - somehow self.mySells[0] < self.myBuys[0]')

            
        ax2.format_coord = make_format(ax2, ax1)
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())

        def on_button_press(event):
            if(self.isDPressed):
                plt.figtext(0.92, (0.88-(0.05*self.textDropper)), str(int(event.xdata))) #, event.ydata
                self.textDropper += 1
                plt.draw()
            if(self.isYPressed):
                plt.figtext(0.95, (0.88-(0.05*self.textDropper)), str(event.ydata)) #, event.ydata
                self.textDropper += 1
                plt.draw()
            if(self.isBPressed):
                print('BEGIN: ', str(int(event.xdata)), str(round(event.ydata, 2)))
            if(self.isEPressed):
                print('END: ', str(int(event.xdata)), str(round(event.ydata, 2)))
            if(self.isMPressed):
                plt.axvline(x=event.xdata)
                plt.draw()

        def keypress(event):
            if(event.key=='d'):
                self.isDPressed = True
            if(event.key=='y'):
                self.isYPressed = True
            if(event.key=='m'):
                self.isMPressed = True
            if(event.key=='b'):
                self.isBPressed = True
            if(event.key=='e'):
                self.isEPressed = True
            if(event.key=='v'):
                ax1.grid()

        def keyrelease(event):
            if(event.key=='d'):
                self.isDPressed = False
            if(event.key=='y'):
                self.isYPressed = False
            if(event.key=='m'):
                self.isMPressed = False
            if(event.key=='b'):
                self.isBPressed = False
            if(event.key=='e'):
                self.isEPressed = False

        def handle_close(event):
            self.quit()


        fig.canvas.mpl_connect('button_press_event', on_button_press)
        fig.canvas.mpl_connect('key_press_event', keypress)
        fig.canvas.mpl_connect('key_release_event', keyrelease)
        fig.canvas.mpl_connect('close_event', handle_close)


        cursor = MultiCursor(fig.canvas, (ax1,ax2), color='purple', linewidth=1)
        plt.subplots_adjust(left=0.05, right=0.85, top=0.9, bottom=0.1)
        #colorStrings = ["Red", "Blue", "Green", "Pink", "Baby-Blue", "Orange", "Yellow", "Purple"]
            
        textplacer = 0.05
        #for colS in colorStrings:
        #    plt.figtext(textplacer, 0.97, colS)
        #    textplacer += 0.07
        #textplacer = 0.05
        marktextplacer = 0.05
        bgtextplacer = 0.05
        if(len(multiString) > 0):
            actString = multiString.split()
            whichC = 1
            whichCM = 0
            isAMark = False
            nextIsBuy = False
            nextIsSell = False
            whichBList = 0
            whichSList = 0
            for multS in actString:
                if(multS == "'.',"):
                    plt.figtext(0.01, 0.96, 'marks:')
                    isAMark = True
                elif(isAMark):
                    plt.figtext(marktextplacer, 0.96, multS, color=markColorArray[whichCM])
                    whichCM += 1
                    isAMark = False
                    marktextplacer += 0.07
                elif(nextIsBuy):
                    plt.figtext(bgtextplacer, 0.94, multS)
                    if(whichBList < 1):
                        plt.figtext(bgtextplacer, 0.91, '███', color='#00FF00', alpha=0.4, backgroundcolor='white', size='x-large')
                    elif(whichBList < 2):
                        plt.figtext(bgtextplacer, 0.91, '███', color='g', alpha=0.4, backgroundcolor='white', size='x-large')
                    elif(whichBList < 3):
                        plt.figtext(bgtextplacer, 0.91, '███', color='#009980', alpha=0.4, backgroundcolor='white', size='x-large')
                    else:
                        plt.figtext(bgtextplacer, 0.91, '███', color='g', alpha=0.2, backgroundcolor='white', size='x-large')
                    bgtextplacer += 0.07
                    nextIsBuy = False
                    whichBList += 1
                elif(nextIsSell):
                    plt.figtext(bgtextplacer, 0.94, multS)
                    if(whichSList < 1):
                        plt.figtext(bgtextplacer, 0.91, '███', color='#FF3300', alpha=0.5, backgroundcolor='white', size='x-large')
                    elif(whichSList < 2):
                        plt.figtext(bgtextplacer, 0.91, '███', color='r', alpha=0.2, backgroundcolor='white', size='x-large')
                    elif(whichSList < 3):
                        plt.figtext(bgtextplacer, 0.91, '███', color='r', alpha=0.6, backgroundcolor='white', size='x-large')
                    else:
                        plt.figtext(bgtextplacer, 0.91, '███', color='r', alpha=0.4, backgroundcolor='white', size='x-large')
                    bgtextplacer += 0.07
                    nextIsSell = False
                    whichSList += 1
                elif(multS == "'pp',"):
                    pass
                elif(multS == "'b',"):
                    plt.figtext(0.01, 0.93, 'bg:')
                    nextIsBuy = True
                elif(multS == "'s',"):
                    plt.figtext(0.01, 0.93, 'bg:')
                    nextIsSell = True
                else:
                    if(whichC < len(colorArray)):
                        plt.figtext(textplacer, 0.98, multS, color=colorArray[whichC])
                    else:
                        plt.figtext(textplacer, 0.98, multS)
                    textplacer += 0.07
                    whichC += 1

        plt.show()
        #plt.close(fig)

    def fitData(self, plotter = []):
        if(len(plotter) == len(self.btcDateArr)):
            return self.btcDateArr
        else:
            if(len(plotter) == len(self.fullPrice)):
                cleanResult = range(self.startSec, self.endSec, 1)
            else:
                intervalLen = (self.endSec - self.startSec) / len(plotter)
                if((self.endSec - self.startSec) % len(plotter) > 0):
                    intervalLen += 1
                cleanResult = range(self.startSec, self.endSec, int(intervalLen))
            return cleanResult

    def stretchData(self, inpArr = []):
        stretchArr = []
        for val in range(len(self.btcDateArr)-1):
            numVals = self.btcDateArr[val+1] - self.btcDateArr[val]
            if(numVals <= 1):
                stretchArr.append(inpArr[val])
            else:
                stretchArr.extend([inpArr[val]] * numVals)
        return stretchArr


    def preciseVolArr(self):
        fullVolumeArr = [0] * (self.endSec - self.startSec)
        for trade in range(len(self.btcDateArr)):
            addr = (self.btcDateArr[trade] - self.startSec)
            if(addr < len(fullVolumeArr)):
                fullVolumeArr[addr] += self.btcVolumeArr[trade]
        return fullVolumeArr


    def calcFiatProfits(self, buyArr = [], sellArr = [], fullPriceArr = [], bleed=0.005):
        self.profitRatioArr = []
        #profitRatioArr = []
        initPortfolio = fullPriceArr[0]
        rightShift = self.startSec
        myBTC = 1.0
        myFiat = 0.0
        currSellIdx = 0
        currBuyIdx = 0
        builderIdx = 0
        integral = 0
        currROI = 0.0
        lfp = len(fullPriceArr)
        lsa = len(sellArr)
        lba = len(buyArr)
        bloodloss = (1.0 - bleed)
        weAreBuying = False
        weAreSelling = False
        howManyActions = 4
        bitcoinSpectrum = howManyActions
        spacesApart = 8
        lastBuy = 0
        lastSell = 0


        while(builderIdx < lfp):
            currDate = builderIdx + rightShift
            if(currSellIdx < lsa and currDate == sellArr[currSellIdx]):
                currSellIdx += 1
                weAreSelling = True
                weAreBuying = False
            elif(currBuyIdx < lba and currDate == buyArr[currBuyIdx]):
                if(currBuyIdx == 0): #we always call the first moment a 'buy'
                    myBTC = 1.0
                    myFiat = 0.0
                else:
                    weAreSelling = False
                    weAreBuying = True
                currBuyIdx += 1
            if(weAreSelling and bitcoinSpectrum > 0): #we are not already fully in fiat
                if(builderIdx >= lastSell + spacesApart):
                    myFiat += bloodloss*(((1 / bitcoinSpectrum)*myBTC)*fullPriceArr[builderIdx])
                    myBTC -= (1 / bitcoinSpectrum)*myBTC
                    lastSell = builderIdx
                    bitcoinSpectrum -= 1
            elif(weAreSelling): #this means bitcoinSpectrum <= 0, so we're fully in fiat and can stop selling
                weAreSelling = False
            elif(weAreBuying and bitcoinSpectrum < howManyActions):
                if(builderIdx >= lastBuy + spacesApart):
                    myBTC += bloodloss*(((1 / (howManyActions - bitcoinSpectrum))*myFiat) / fullPriceArr[builderIdx])
                    myFiat -= (1 / (howManyActions - bitcoinSpectrum))*myFiat
                    lastBuy = builderIdx
                    bitcoinSpectrum += 1
            elif(weAreBuying): #this means bitcoinSpectrum >= howManyActions, so we're fully in BTC and can stop buying
                weAreBuying = False

            currROI = ((myBTC * fullPriceArr[builderIdx]) + myFiat) / initPortfolio
            #print('myBTC = ', myBTC, 'myFiat = ', myFiat, 'currROI = ', currROI, 'on ', currDate)
            integral += currROI
            self.profitRatioArr.append(currROI)
            builderIdx += 1

        integral = (integral / len(self.profitRatioArr))
        finalBalance = (myBTC * fullPriceArr[-1]) + myFiat
        print(str(integral), '|', (finalBalance/initPortfolio), '|', finalBalance, '|', (finalBalance/fullPriceArr[-1]), '|', (len(buyArr)+len(sellArr)))
        self.myIntegral = integral
        self.myReturn = (finalBalance/initPortfolio)
        return integral



    def calcFiatProfitsWithShorting(self, buyArr = [], sellArr = [], fullPriceArr = [], bleed=0.004):
        self.profitRatioArr = []
        initPortfolio = fullPriceArr[0]
        rightShift = self.startSec
        myBTC = 1.0
        myFiat = 0.0
        currSellIdx = 0
        currBuyIdx = 0
        builderIdx = 0
        integral = 0
        currROI = 0.0
        lfp = len(fullPriceArr)
        lsa = len(sellArr)
        lba = len(buyArr)
        bloodloss = (1.0 - bleed)
        weAreBuying = False
        weAreSelling = False
        howManyActions = 2
        
        bitcoinSpectrum = howManyActions
        spacesApart = 8
        lastBuy = 0
        lastSell = 0
    
        #print('buyA = ', buyArr)
        #print('sellA = ', sellArr)
    
        while(builderIdx < lfp):
            currDate = builderIdx + rightShift
            if(currSellIdx < lsa and currDate == sellArr[currSellIdx]):
                currSellIdx += 1
                weAreSelling = True
                weAreBuying = False
            elif(currBuyIdx < lba and currDate == buyArr[currBuyIdx]):
                if(currBuyIdx == 0): #we always call the first moment a 'buy'
                    myBTC = 1.0
                    myFiat = 0.0
                else:
                    weAreSelling = False
                    weAreBuying = True
                currBuyIdx += 1
            if(weAreSelling and bitcoinSpectrum > (-howManyActions)): #we are not already fully short
                if(builderIdx >= lastSell + spacesApart):
                    bitcoinSpectrum -= 1
                    if(bitcoinSpectrum == -2):
                        myFiat += (myBTC * fullPriceArr[builderIdx])
                        myBTC = -(myFiat / fullPriceArr[builderIdx])
                        myFiat *= (bloodloss*2)
                    elif(bitcoinSpectrum == -1): 
                        myBTC = -((myFiat / 2) / fullPriceArr[builderIdx])
                        myFiat *= (bloodloss*1.5)
                    elif(bitcoinSpectrum == 0):
                        myFiat += bloodloss*(myBTC*fullPriceArr[builderIdx])
                        myBTC = 0.0
                    elif(bitcoinSpectrum == 1):
                        myFiat = bloodloss*(myBTC * fullPriceArr[builderIdx]) / 2
                        myBTC /= 2
                    else: 
                        print('bitcoinSpectrum is ', bitcoinSpectrum, 'and currDate = ', currDate)
                    lastSell = builderIdx
            elif(weAreSelling): #this means bitcoinSpectrum <= 0, so we're fully in fiat and can stop selling
                weAreSelling = False
            elif(weAreBuying and bitcoinSpectrum < howManyActions):
                if(builderIdx >= lastBuy + spacesApart):
                    bitcoinSpectrum += 1
                    if(bitcoinSpectrum == -1):
                        myFiat += (myBTC * fullPriceArr[builderIdx])
                        myBTC = -(myFiat / 2) / fullPriceArr[builderIdx]
                        myFiat *= (bloodloss*1.5)
                    elif(bitcoinSpectrum == 0): 
                        myFiat += (myBTC * fullPriceArr[builderIdx])
                        myBTC = 0.0
                        myFiat *= bloodloss
                    elif(bitcoinSpectrum == 1):
                        myBTC = bloodloss*((myFiat / 2) / fullPriceArr[builderIdx])
                        myFiat /= 2
                    elif(bitcoinSpectrum == 2):
                        myBTC += bloodloss*(myFiat / fullPriceArr[builderIdx])
                        myFiat = 0.0
                    else: 
                        print('bitcoinSpectrum is ', bitcoinSpectrum, 'and currDate = ', currDate)
                    lastBuy = builderIdx
            elif(weAreBuying): #this means bitcoinSpectrum >= howManyActions, so we're fully in BTC and can     stop buying
                weAreBuying = False
    
            currROI = ((myBTC * fullPriceArr[builderIdx]) + myFiat) / initPortfolio
            #print('myBTC = ', myBTC, 'myFiat = ', myFiat, 'currROI = ', currROI, 'on ', currDate,  'bitcoinSpectrum =', bitcoinSpectrum)
            integral += currROI
            self.profitRatioArr.append(currROI)
            builderIdx += 1
    
        integral = (integral / len(self.profitRatioArr))
        finalBalance = (myBTC * fullPriceArr[-1]) + myFiat
        print(str(integral), '|', (finalBalance/initPortfolio), '|', finalBalance,  '|', (finalBalance/fullPriceArr[-1]), '|', (len(buyArr)+len(sellArr)))
        self.myIntegral = integral
        self.myReturn = (finalBalance/initPortfolio)
        return integral



class Minion:
    def __init__(self, app, whichVar, currVal, startVal, distance):
        self.app = app
        self.whichVar = whichVar
        self.currVal = currVal
        self.startVal = startVal
        self.distance = distance

        self.distanceMultiplier = (2/5)
        self.testsPerRound = 10

        self.testWindow = []
        self.resultsArr = []
        print('BEGIN MINION - Variable #', self.whichVar)
        #self.buildTestWindow()
        #self.maximizeIntegral()
        #print(app.BTSRinterval2.get())

    def buildTestWindow(self):
        del self.testWindow [:]
        self.testWindow.append(self.currVal)
        for i in range(0, self.testsPerRound):
            self.testWindow.append((self.startVal + (i*self.distance)))

    def maximizeIntegral(self):
        self.buildTestWindow()
        del self.resultsArr [:]
        self.app.myTester.printVariables()
        self.app.myTester.checkProfits()
        #self.resultsArr.append(self.app.myTester.myIntegral) #lay down the current best result as buildTestWindow[0]

        for testVal in self.testWindow:
            self.app.myTester.printVariables()
            self.changeAppropriateVariable(testVal)
            self.resultsArr.append(self.app.myTester.myIntegral)
            
        newValIdx = self.resultsArr.index(max(self.resultsArr))
        print('BEST: ', newValIdx)
        self.app.myTester.printVariables()
        self.changeAppropriateVariable(self.testWindow[newValIdx])
        self.changeAppropriateEntry(self.testWindow[newValIdx])

    def maximizeReturn(self):
        self.buildTestWindow()
        del self.resultsArr [:]
        #self.app.myTester.printVariables()
        #self.app.myTester.checkProfits()
        #self.resultsArr.append(self.app.myTester.myReturn) #lay down the current best result as buildTestWindow[0]

        for testVal in self.testWindow:
            self.app.myTester.printVariables()
            self.changeAppropriateVariable(testVal)
            self.resultsArr.append(self.app.myTester.myReturn)

        newValIdx = self.resultsArr.index(max(self.resultsArr))
        print('BEST: ', newValIdx)
        self.app.myTester.printVariables()
        self.changeAppropriateVariable(self.testWindow[newValIdx])
        self.changeAppropriateEntry(self.testWindow[newValIdx])

    def maximizeReturnQueue(self, q):
        self.buildTestWindow()
        del self.resultsArr [:]
        #self.app.myTester.printVariables()
        #self.app.myTester.checkProfits()

        #self.resultsArr.append(self.app.myTester.myReturn) #lay down the current best result as buildTestWindow[0]

        for testVal in self.testWindow:
            self.app.myTester.printVariables()
            self.changeAppropriateVariable(testVal)
            self.resultsArr.append(self.app.myTester.myReturn)

        newValIdx = self.resultsArr.index(max(self.resultsArr))
        print('BEST: ', newValIdx)
        self.app.myTester.printVariables()


        self.changeAppropriateVariable(self.testWindow[newValIdx])
        q.put(self.changeAppropriateEntry(self.testWindow[newValIdx]))


    def changeAppropriateVariable(self, inputVal):
        if(self.whichVar == 0 or self.whichVar == 3 or self.whichVar == 4 or self.whichVar == 7 or self.whichVar == 8 or self.whichVar == 11 or self.whichVar == 12 or self.whichVar == 15 or self.whichVar == 18 or self.whichVar == 19 or self.whichVar == 21 or self.whichVar == 23):
            #these are all interval lengths, so input shouldn't be a float
            inputVal = int(inputVal)
        if(self.whichVar == 0):
            self.app.myTester.changeBTSRinterval(inputVal)
        elif(self.whichVar == 1):
            self.app.myTester.changeBTSRcutoff(inputVal)
        elif(self.whichVar == 2):
            self.app.myTester.changeBTSRreturn(inputVal)
        elif(self.whichVar == 3):
            self.app.myTester.changeBTSRMOAS(inputVal)
        elif(self.whichVar == 4):
            self.app.myTester.changeSTBRinterval(inputVal)
        elif(self.whichVar == 5):
            self.app.myTester.changeSTBRcutoff(inputVal)
        elif(self.whichVar == 6):
            self.app.myTester.changeSTBRreturn(inputVal)
        elif(self.whichVar == 7):
            self.app.myTester.changeSTBRMOAS(inputVal)
        elif(self.whichVar == 8):
            self.app.myTester.changeVolumeInterval(inputVal)
        elif(self.whichVar == 9):
            self.app.myTester.changeVolumeCutoff(inputVal)
        elif(self.whichVar == 10):
            self.app.myTester.changeVolumeReturn(inputVal)
        elif(self.whichVar == 11):
            self.app.myTester.changeVolumeMOAS(inputVal)
        elif(self.whichVar == 12):
            self.app.myTester.changeViolenceBuyInterval(inputVal)
        elif(self.whichVar == 13):
            self.app.myTester.changeViolenceBuyThreshold(inputVal)
        elif(self.whichVar == 14):
            self.app.myTester.changeViolenceBuyReturn(inputVal)
        elif(self.whichVar == 15):
            self.app.myTester.changeViolenceSellInterval(inputVal)
        elif(self.whichVar == 16):
            self.app.myTester.changeViolenceSellThreshold(inputVal)
        elif(self.whichVar == 17):
            self.app.myTester.changeViolenceSellReturn(inputVal)
        elif(self.whichVar == 18):
            self.app.myTester.changeBTSRwindowForwardLen(inputVal)
        elif(self.whichVar == 19):
            self.app.myTester.changeBTSRwindowBackLen(inputVal)
        elif(self.whichVar == 20):
            self.app.myTester.changeReactSellCut(inputVal)
        elif(self.whichVar == 21):
            self.app.myTester.changeReactSellWindowLenForward(inputVal)
        elif(self.whichVar == 22):
            self.app.myTester.changeReactBuyCut(inputVal)
        elif(self.whichVar == 23):
            self.app.myTester.changeReactBuyWindowLenForward(inputVal)



    def changeAppropriateEntry(self, newVal):
        newDistance = self.distance * self.distanceMultiplier
        newStartVal = newVal - (newDistance*2)
        if(self.whichVar == 0 or self.whichVar == 3 or self.whichVar == 4 or self.whichVar == 7 or self.whichVar == 8 or self.whichVar == 11 or self.whichVar == 12 or self.whichVar == 15 or self.whichVar == 18 or self.whichVar == 19 or self.whichVar == 21 or self.whichVar == 23):
            #these are all interval lengths, so they shouldn't be floats
            newDistance = int(newDistance)
            newVal = int(newVal)
            newStartVal = int(newStartVal)
            if(self.whichVar == 18 or self.whichVar == 19 or self.whichVar == 21 or self.whichVar == 23):
                pass
            elif(newStartVal < 10):
                newStartVal = 10


        return [self.whichVar, newVal, newStartVal, newDistance]


