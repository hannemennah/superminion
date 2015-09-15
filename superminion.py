from tkinter import *

import numpy as np
import multiprocessing
import threading
import shlex
import subprocess
import random
from backtester import *
import sys, os

variablesArr = []

class MyApp(threading.Thread):
    def __init__(self):#, parent):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root=Tk()
        self.root.title("Superminion")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        button_width = 14           
        button_height = 2
        button_padx = "2m"     
        button_pady = "1m"     
        buttons_frame_padx =  "3m"    
        buttons_frame_pady =  "2m"        
        buttons_frame_ipadx = "3m"    
        buttons_frame_ipady = "1m"

        vcmd = (self.root.register(self.validate), '%d', '%P', '%s', '%S', '%v', '%V', '%W')
        self.whichExchange = IntVar(); self.whichExchange.set(1)
        self.btcDA=[]
        self.btcPA=[]
        self.btcVA=[]
        
        global variablesArr

        self.BTSRcheatVarEnabled = IntVar(); self.BTSRcheatVarEnabled.set(1)
        self.STBRcheatVarEnabled = IntVar(); self.STBRcheatVarEnabled.set(1)
        self.vioBuysCheatVarEnabled = IntVar(); self.vioBuysCheatVarEnabled.set(1)
        self.vioSellsCheatVarEnabled = IntVar(); self.vioSellsCheatVarEnabled.set(1)
        self.BTSRintervalVarEnabled = IntVar(); self.BTSRintervalVarEnabled.set(1)
        self.BTSRthresholdVarEnabled = IntVar(); self.BTSRthresholdVarEnabled.set(1)
        self.BTSRreturnVarEnabled = IntVar(); self.BTSRreturnVarEnabled.set(1)
        self.BTSRMOASVarEnabled = IntVar(); self.BTSRMOASVarEnabled.set(1)
        self.STBRintervalVarEnabled = IntVar(); self.STBRintervalVarEnabled.set(1)
        self.STBRthresholdVarEnabled = IntVar(); self.STBRthresholdVarEnabled.set(1)
        self.STBRreturnVarEnabled = IntVar(); self.STBRreturnVarEnabled.set(1)
        self.STBRMOASVarEnabled = IntVar(); self.STBRMOASVarEnabled.set(1)
        self.volumeIntervalVarEnabled = IntVar(); self.volumeIntervalVarEnabled.set(1)
        self.volumeThresholdVarEnabled = IntVar(); self.volumeThresholdVarEnabled.set(1)
        self.volumeReturnVarEnabled = IntVar(); self.volumeReturnVarEnabled.set(1)
        self.volumeMOASVarEnabled = IntVar(); self.volumeMOASVarEnabled.set(1)
        self.violenceBuysIntervalVarEnabled = IntVar(); self.violenceBuysIntervalVarEnabled.set(1)
        self.violenceBuysThresholdVarEnabled = IntVar(); self.violenceBuysThresholdVarEnabled.set(1)
        self.violenceBuysReturnVarEnabled = IntVar(); self.violenceBuysReturnVarEnabled.set(1)
        self.doWeReactBySelling = IntVar(); self.doWeReactBySelling.set(0)
        self.reactSellsChangeVarEnabled = IntVar(); self.reactSellsChangeVarEnabled.set(0)
        self.violenceSellsIntervalVarEnabled = IntVar(); self.violenceSellsIntervalVarEnabled.set(1)
        self.violenceSellsThresholdVarEnabled = IntVar(); self.violenceSellsThresholdVarEnabled.set(1)
        self.violenceSellsReturnVarEnabled = IntVar(); self.violenceSellsReturnVarEnabled.set(1)
        self.doWeReactByBuying = IntVar(); self.doWeReactByBuying.set(0)
        self.reactBuysChangeVarEnabled = IntVar(); self.reactBuysChangeVarEnabled.set(0)
        self.BTSRwindowLengthsForwardVarEnabled = IntVar(); self.BTSRwindowLengthsForwardVarEnabled.set(1)
        self.BTSRwindowLengthsBackVarEnabled = IntVar(); self.BTSRwindowLengthsBackVarEnabled.set(1)
        self.reactSellsWindowLengthsForwardVarEnabled = IntVar(); self.reactSellsWindowLengthsForwardVarEnabled.set(0)
        self.reactBuysWindowLengthsForwardVarEnabled = IntVar(); self.reactBuysWindowLengthsForwardVarEnabled.set(0)
        self.multiplotBTSREnabled = IntVar()
        self.multiplotSTBREnabled = IntVar()
        self.multiplotVolumeEnabled = IntVar()
        self.multiplot1secondVolumeEnabled = IntVar()
        self.multiplotViolenceBuyMAEnabled = IntVar()
        self.multiplotViolenceSellMAEnabled = IntVar()
        self.multiplotPPEnabled = IntVar(); self.multiplotPPEnabled.set(1)
        self.multiplotBTSRspikesEnabled = IntVar()
        self.multiplotSTBRspikesEnabled = IntVar()
        self.multiplotVolumeSpikesEnabled = IntVar()
        self.multiplotVioBuySpikesEnabled = IntVar()
        self.multiplotVioSellSpikesEnabled = IntVar()
        self.multiplotRainbowEnabled = IntVar(); self.multiplotRainbowEnabled.set(1)
        self.doWeShort = IntVar(); self.doWeShort.set(0)

        self.isPaused = True
    
        self.startBTSRinterval = StringVar(); self.startBTSRinterval.set(str(variablesArr[0][0]))
        self.startBTSRcutoff = StringVar(); self.startBTSRcutoff.set(str(variablesArr[1][0]))
        self.startBTSRreturn = StringVar(); self.startBTSRreturn.set(str(variablesArr[2][0]))
        self.startBTSRMOAS = StringVar(); self.startBTSRMOAS.set(str(variablesArr[3][0]))
        self.startSTBRinterval = StringVar(); self.startSTBRinterval.set(str(variablesArr[4][0]))
        self.startSTBRcutoff = StringVar(); self.startSTBRcutoff.set(str(variablesArr[5][0]))
        self.startSTBRreturn = StringVar(); self.startSTBRreturn.set(str(variablesArr[6][0]))
        self.startSTBRMOAS = StringVar(); self.startSTBRMOAS.set(str(variablesArr[7][0]))
        self.startVolumeInterval = StringVar(); self.startVolumeInterval.set(str(variablesArr[8][0]))
        self.startVolumeCutoff = StringVar(); self.startVolumeCutoff.set(str(variablesArr[9][0]))
        self.startVolumeReturn = StringVar(); self.startVolumeReturn.set(str(variablesArr[10][0]))
        self.startVolumeMOAS = StringVar(); self.startVolumeMOAS.set(str(variablesArr[11][0]))
        self.startViolenceBuyInterval = StringVar(); self.startViolenceBuyInterval.set(str(variablesArr[12][0]))
        self.startViolenceBuyThreshold = StringVar(); self.startViolenceBuyThreshold.set(str(variablesArr[13][0]))
        self.startViolenceBuyReturn = StringVar(); self.startViolenceBuyReturn.set(str(variablesArr[14][0]))
        self.startViolenceSellInterval = StringVar(); self.startViolenceSellInterval.set(str(variablesArr[15][0]))
        self.startViolenceSellThreshold = StringVar(); self.startViolenceSellThreshold.set(str(variablesArr[16][0]))
        self.startViolenceSellReturn = StringVar(); self.startViolenceSellReturn.set(str(variablesArr[17][0]))
        self.startBTSRwindowForwardLen = StringVar(); self.startBTSRwindowForwardLen.set(str(variablesArr[18][0]))
        self.startBTSRwindowBackLen = StringVar(); self.startBTSRwindowBackLen.set(str(variablesArr[19][0]))
        self.startReactSellsCutoff = StringVar(); self.startReactSellsCutoff.set(str(variablesArr[20][0]))
        self.startReactSellsWindowLen = StringVar(); self.startReactSellsWindowLen.set(str(variablesArr[21][0]))
        self.startReactBuysCutoff = StringVar(); self.startReactBuysCutoff.set(str(variablesArr[22][0]))
        self.startReactBuysWindowLen = StringVar(); self.startReactBuysWindowLen.set(str(variablesArr[23][0]))

        self.BTSRinterval1 = StringVar(); self.BTSRinterval1.set(str(variablesArr[0][1]))
        self.BTSRcutoff1 = StringVar(); self.BTSRcutoff1.set(str(variablesArr[1][1]))
        self.BTSRreturn1 = StringVar(); self.BTSRreturn1.set(str(variablesArr[2][1]))
        self.BTSRMOAS1 = StringVar(); self.BTSRMOAS1.set(str(variablesArr[3][1]))
        self.STBRinterval1 = StringVar(); self.STBRinterval1.set(str(variablesArr[4][1]))
        self.STBRcutoff1 = StringVar(); self.STBRcutoff1.set(str(variablesArr[5][1]))
        self.STBRreturn1 = StringVar(); self.STBRreturn1.set(str(variablesArr[6][1]))
        self.STBRMOAS1 = StringVar(); self.STBRMOAS1.set(str(variablesArr[7][1]))
        self.VolumeInterval1 = StringVar(); self.VolumeInterval1.set(str(variablesArr[8][1]))
        self.VolumeCutoff1 = StringVar(); self.VolumeCutoff1.set(str(variablesArr[9][1]))
        self.VolumeReturn1 = StringVar(); self.VolumeReturn1.set(str(variablesArr[10][1]))
        self.VolumeMOAS1 = StringVar(); self.VolumeMOAS1.set(str(variablesArr[11][1]))
        self.ViolenceBuyInterval1 = StringVar(); self.ViolenceBuyInterval1.set(str(variablesArr[12][1]))
        self.ViolenceBuyThreshold1 = StringVar(); self.ViolenceBuyThreshold1.set(str(variablesArr[13][1]))
        self.ViolenceBuyReturn1 = StringVar(); self.ViolenceBuyReturn1.set(str(variablesArr[14][1]))
        self.ViolenceSellInterval1 = StringVar(); self.ViolenceSellInterval1.set(str(variablesArr[15][1]))
        self.ViolenceSellThreshold1 = StringVar(); self.ViolenceSellThreshold1.set(str(variablesArr[16][1]))
        self.ViolenceSellReturn1 = StringVar(); self.ViolenceSellReturn1.set(str(variablesArr[17][1]))
        self.BTSRwindowForwardLen1 = StringVar(); self.BTSRwindowForwardLen1.set(str(variablesArr[18][1]))
        self.BTSRwindowBackLen1 = StringVar(); self.BTSRwindowBackLen1.set(str(variablesArr[19][1]))
        self.reactSellsCutoff1 = StringVar(); self.reactSellsCutoff1.set(str(variablesArr[20][1]))
        self.reactSellsWindowLen1 = StringVar(); self.reactSellsWindowLen1.set(str(variablesArr[21][1]))
        self.reactBuysCutoff1 = StringVar(); self.reactBuysCutoff1.set(str(variablesArr[22][1]))
        self.reactBuysWindowLen1 = StringVar(); self.reactBuysWindowLen1.set(str(variablesArr[23][1]))

        self.BTSRinterval2 = StringVar(); self.BTSRinterval2.set(str(variablesArr[0][2]))
        self.BTSRcutoff2 = StringVar(); self.BTSRcutoff2.set(str(variablesArr[1][2]))
        self.BTSRreturn2 = StringVar(); self.BTSRreturn2.set(str(variablesArr[2][2]))
        self.BTSRMOAS2 = StringVar(); self.BTSRMOAS2.set(str(variablesArr[3][2]))
        self.STBRinterval2 = StringVar(); self.STBRinterval2.set(str(variablesArr[4][2]))
        self.STBRcutoff2 = StringVar(); self.STBRcutoff2.set(str(variablesArr[5][2]))
        self.STBRreturn2 = StringVar(); self.STBRreturn2.set(str(variablesArr[6][2]))
        self.STBRMOAS2 = StringVar(); self.STBRMOAS2.set(str(variablesArr[7][2]))
        self.VolumeInterval2 = StringVar(); self.VolumeInterval2.set(str(variablesArr[8][2]))
        self.VolumeCutoff2 = StringVar(); self.VolumeCutoff2.set(str(variablesArr[9][2]))
        self.VolumeReturn2 = StringVar(); self.VolumeReturn2.set(str(variablesArr[10][2]))
        self.VolumeMOAS2 = StringVar(); self.VolumeMOAS2.set(str(variablesArr[11][2]))
        self.ViolenceBuyInterval2 = StringVar(); self.ViolenceBuyInterval2.set(str(variablesArr[12][2]))
        self.ViolenceBuyThreshold2 = StringVar(); self.ViolenceBuyThreshold2.set(str(variablesArr[13][2]))
        self.ViolenceBuyReturn2 = StringVar(); self.ViolenceBuyReturn2.set(str(variablesArr[14][2]))
        self.ViolenceSellInterval2 = StringVar(); self.ViolenceSellInterval2.set(str(variablesArr[15][2]))
        self.ViolenceSellThreshold2 = StringVar(); self.ViolenceSellThreshold2.set(str(variablesArr[16][2]))
        self.ViolenceSellReturn2 = StringVar(); self.ViolenceSellReturn2.set(str(variablesArr[17][2]))
        self.BTSRwindowForwardLen2 = StringVar(); self.BTSRwindowForwardLen2.set(str(variablesArr[18][2]))
        self.BTSRwindowBackLen2 = StringVar(); self.BTSRwindowBackLen2.set(str(variablesArr[19][2]))
        self.reactSellsCutoff2 = StringVar(); self.reactSellsCutoff2.set(str(variablesArr[20][2]))
        self.reactSellsWindowLen2 = StringVar(); self.reactSellsWindowLen2.set(str(variablesArr[21][2]))
        self.reactBuysCutoff2 = StringVar(); self.reactBuysCutoff2.set(str(variablesArr[22][2]))
        self.reactBuysWindowLen2 = StringVar(); self.reactBuysWindowLen2.set(str(variablesArr[23][2]))

        self.startCurrentTestVar = IntVar(); self.startCurrentTestVar.set(15)
        self.startNextTestVar = IntVar(); self.startNextTestVar.set(15)
        self.currentframe = 0
        self.diceArr = []

        self.outputFile = StringVar(); self.outputFile.set('myOutputFile.txt')

        self.myParent = self.root#parent 
        self.root.geometry("1150x660")

        self.myUpperContainer = Frame(self.root) 
        self.myUpperContainer.pack(expand=YES, fill=BOTH)
        self.myMainContainer = Frame(self.root) 
        self.myMainContainer.pack(expand=YES, fill=BOTH)
        self.myMiddleContainer = Frame(self.root) 
        self.myMiddleContainer.pack(expand=YES, fill=BOTH)
        self.myLowerContainer = Frame(self.root) 
        self.myLowerContainer.pack(expand=YES, fill=BOTH)


        #WHICH EXCHANGE (top left) setup
        self.exchangePick_control_frame = Frame(self.myUpperContainer, borderwidth=2, relief='groove')
        self.exchangePick_control_frame.pack(side=LEFT, expand=NO,  padx=20, pady=5, ipadx=5, ipady=5, anchor=N)
        bfxChosen = Radiobutton(self.exchangePick_control_frame, text="Bitfinex", variable=self.whichExchange, value=0)
        bfxChosen.grid(row=0, column=0)
        bsChosen = Radiobutton(self.exchangePick_control_frame, text="Bitstamp", variable=self.whichExchange, value=1)
        bsChosen.grid(row=0, column=1)




        #TIME INTERVAL (top middle) setup
        self.timeInterval_control_frame = Frame(self.myUpperContainer, borderwidth=2, relief='groove')
        self.timeInterval_control_frame.pack(side=LEFT, expand=NO,  padx=(180, 10), pady=5, ipadx=5, ipady=5, anchor=W)
        Label(self.timeInterval_control_frame, text="Begin:", justify=RIGHT).grid(row=0)
        self.tBegin = StringVar()
        self.tEnd = StringVar()
        self.timeIntervalBegin = Entry(self.timeInterval_control_frame, width=10, textvariable=self.tBegin)
        self.tBegin.set('1383824400')
        self.tEnd.set('1387512400')
        self.timeIntervalBegin.grid(row=0, column=1)
        Label(self.timeInterval_control_frame, text="End:", justify=RIGHT).grid(row=0, column=2)
        self.timeIntervalEnd = Entry(self.timeInterval_control_frame, width=10, textvariable=self.tEnd)
        self.timeIntervalEnd.grid(row=0, column=3)

        self.prettytBegin = StringVar(); self.prettytBegin.set(longPrettifyDate(self.timeIntervalBegin.get()))
        self.prettytEnd = StringVar(); self.prettytEnd.set(longPrettifyDate(self.timeIntervalEnd.get()))
        self.prettyBeginDate = Label(self.timeInterval_control_frame, textvariable=self.prettytBegin, font="arial 10 bold", justify=CENTER)
        self.prettyBeginDate.grid(row=1, column=1)
        self.prettyEndDate = Label(self.timeInterval_control_frame, textvariable=self.prettytEnd, font="arial 10 bold", justify=CENTER)
        self.prettyEndDate.grid(row=1, column=3)

        self.timeIntervalBegin.bind(sequence='<KeyRelease>', func=self.updateDateText())
        self.timeIntervalEnd.bind(sequence='<KeyRelease>', func=self.updateDateText())

        self.refresh_control_frame = Frame(self.myUpperContainer)
        self.refresh_control_frame.pack(side=LEFT, expand=NO,  padx=(0, 150), pady=5, ipadx=5, ipady=5, anchor=W)
        self.refreshImage = PhotoImage(file="./images/refresh.png")
        self.refreshButton = Button(self.refresh_control_frame,
          image=self.refreshImage, relief='flat',
          padx=10,
          pady=10
          )
        self.refreshButton.pack(side=TOP, anchor=N)
        self.refreshButton.bind("<Button-1>", self.refreshButtonClick)   
        self.refreshButton.bind("<Return>", self.refreshButtonClick) 


        #MISCELLANEOUS CHOICES (top right) setup
        self.extraChoices_control_frame = Frame(self.myUpperContainer, borderwidth=2, relief='groove')
        self.extraChoices_control_frame.pack(side=LEFT, expand=NO,  padx=20, pady=5, ipadx=5, ipady=5, anchor=E)
        yesWeShortRadio = Radiobutton(self.extraChoices_control_frame, text="Short", variable=self.doWeShort, value=1)
        yesWeShortRadio.grid(row=0, column=0)
        noWeDontShortRadio = Radiobutton(self.extraChoices_control_frame, text="Just Sell", variable=self.doWeShort, value=0)
        noWeDontShortRadio.grid(row=0, column=1)


        #BTSR (left frame) setup
        self.BTSR_control_frame = Frame(self.myMainContainer, borderwidth=3, relief='groove')
        self.BTSR_control_frame.pack(side=LEFT, expand=NO,  padx=(20, 10), pady=5, ipadx=5, ipady=5, anchor=N)

        Label(self.BTSR_control_frame, text="BTSR", font="times 16 bold", justify=CENTER).pack(side=TOP, anchor=N)
        BTSRcheatCheckbox = Checkbutton(self.BTSR_control_frame, text="Cheat?", variable=self.BTSRcheatVarEnabled, command=self.BTSRcheatOnClick)
        BTSRcheatCheckbox.pack(pady=8)

        self.BTSR_vars_frame = Frame(self.BTSR_control_frame)
        self.BTSR_vars_frame.pack()

        Label(self.BTSR_vars_frame, text="BTSR interval length", font="arial 10 bold").grid(row=0, columnspan=4, sticky=W)
        Label(self.BTSR_vars_frame, text="(0)", font="arial 10 bold").grid(row=0, column=3, sticky=N)
        Label(self.BTSR_vars_frame, text="BTSR threshold cutoff", font="arial 10 bold").grid(row=2, columnspan=4, sticky=W)
        Label(self.BTSR_vars_frame, text="(1)", font="arial 10 bold").grid(row=2, column=3, sticky=N)
        Label(self.BTSR_vars_frame, text="BTSR return value", font="arial 10 bold").grid(row=4, columnspan=4, sticky=W)
        Label(self.BTSR_vars_frame, text="(2)", font="arial 10 bold").grid(row=4, column=3, sticky=N)
        Label(self.BTSR_vars_frame, text="BTSR MOAS interval", font="arial 10 bold").grid(row=6, columnspan=4, sticky=W)
        Label(self.BTSR_vars_frame, text="(3)", font="arial 10 bold").grid(row=6, column=3, sticky=N)


        BTSR00 = Entry(self.BTSR_vars_frame, width=5, background="#b6fcd5", textvariable=self.startBTSRinterval)
        BTSR01 = Entry(self.BTSR_vars_frame, width=5, textvariable=self.BTSRinterval1)
        BTSR02 = Entry(self.BTSR_vars_frame, width=5, textvariable=self.BTSRinterval2)
        BTSR0checkbox = Checkbutton(self.BTSR_vars_frame, variable=self.BTSRintervalVarEnabled)#, command=self.BTSRcheatOnClick)
        BTSR10 = Entry(self.BTSR_vars_frame, width=5, background="#b6fcd5", textvariable=self.startBTSRcutoff)
        BTSR11 = Entry(self.BTSR_vars_frame, width=5, textvariable=self.BTSRcutoff1)
        BTSR12 = Entry(self.BTSR_vars_frame, width=5, textvariable=self.BTSRcutoff2)
        BTSR1checkbox = Checkbutton(self.BTSR_vars_frame, variable=self.BTSRthresholdVarEnabled)#, command=self.BTSRcheatOnClick)
        BTSR20 = Entry(self.BTSR_vars_frame, width=5, background="#b6fcd5", textvariable=self.startBTSRreturn)
        BTSR21 = Entry(self.BTSR_vars_frame, width=5, textvariable=self.BTSRreturn1)
        BTSR22 = Entry(self.BTSR_vars_frame, width=5, textvariable=self.BTSRreturn2)
        BTSR2checkbox = Checkbutton(self.BTSR_vars_frame, variable=self.BTSRreturnVarEnabled)#, command=self.BTSRcheatOnClick)
        BTSR30 = Entry(self.BTSR_vars_frame, width=5, background="#b6fcd5", textvariable=self.startBTSRMOAS)
        BTSR31 = Entry(self.BTSR_vars_frame, width=5, textvariable=self.BTSRMOAS1)
        BTSR32 = Entry(self.BTSR_vars_frame, width=5, textvariable=self.BTSRMOAS2)
        BTSR3checkbox = Checkbutton(self.BTSR_vars_frame, variable=self.BTSRMOASVarEnabled)#, command=self.BTSRcheatOnClick)


        BTSR00.grid(row=1, column=0, sticky=W)
        BTSR01.grid(row=1, column=1, sticky=W)
        BTSR02.grid(row=1, column=2, sticky=W)
        BTSR0checkbox.grid(row=1, column=3, sticky=W)
        BTSR10.grid(row=3, column=0, sticky=W)
        BTSR11.grid(row=3, column=1, sticky=W)
        BTSR12.grid(row=3, column=2, sticky=W)
        BTSR1checkbox.grid(row=3, column=3, sticky=W)
        BTSR20.grid(row=5, column=0, sticky=W)
        BTSR21.grid(row=5, column=1, sticky=W)
        BTSR22.grid(row=5, column=2, sticky=W)
        BTSR2checkbox.grid(row=5, column=3, sticky=W)
        BTSR30.grid(row=7, column=0, sticky=W)
        BTSR31.grid(row=7, column=1, sticky=W)
        BTSR32.grid(row=7, column=2, sticky=W)
        BTSR3checkbox.grid(row=7, column=3, sticky=W)







        #STBR (second-from-left frame) setup
        self.STBR_control_frame = Frame(self.myMainContainer, borderwidth=3, relief='groove') 
        self.STBR_control_frame.pack(side=LEFT, expand=NO,  padx=15, pady=5, ipadx=5, ipady=5, anchor=N)  

        Label(self.STBR_control_frame, text="STBR", font="times 16 bold", justify=CENTER).pack(side=TOP, anchor=N)
        STBRcheatCheckbox = Checkbutton(self.STBR_control_frame, text="Cheat?", variable=self.STBRcheatVarEnabled, command=self.STBRcheatOnClick)
        STBRcheatCheckbox.pack(pady=8)

        self.STBR_vars_frame = Frame(self.STBR_control_frame)
        self.STBR_vars_frame.pack()

        Label(self.STBR_vars_frame, text="STBR interval length", font="arial 10 bold").grid(row=0, columnspan=4, sticky=W)
        Label(self.STBR_vars_frame, text="(4)", font="arial 10 bold").grid(row=0, column=3, sticky=N)
        Label(self.STBR_vars_frame, text="STBR threshold cutoff", font="arial 10 bold").grid(row=2, columnspan=4, sticky=W)
        Label(self.STBR_vars_frame, text="(5)", font="arial 10 bold").grid(row=2, column=3, sticky=N)
        Label(self.STBR_vars_frame, text="STBR return value", font="arial 10 bold").grid(row=4, columnspan=4, sticky=W)
        Label(self.STBR_vars_frame, text="(6)", font="arial 10 bold").grid(row=4, column=3, sticky=N)
        Label(self.STBR_vars_frame, text="STBR MOAS interval", font="arial 10 bold").grid(row=6, columnspan=4, sticky=W)
        Label(self.STBR_vars_frame, text="(7)", font="arial 10 bold").grid(row=6, column=3, sticky=N)


        STBR00 = Entry(self.STBR_vars_frame, width=5, background="#b6fcd5", textvariable=self.startSTBRinterval)
        STBR01 = Entry(self.STBR_vars_frame, width=5, textvariable=self.STBRinterval1)
        STBR02 = Entry(self.STBR_vars_frame, width=5, textvariable=self.STBRinterval2)
        STBR0checkbox = Checkbutton(self.STBR_vars_frame, variable=self.STBRintervalVarEnabled)#, command=self.STBRcheatOnClick)
        STBR10 = Entry(self.STBR_vars_frame, width=5, background="#b6fcd5", textvariable=self.startSTBRcutoff)
        STBR11 = Entry(self.STBR_vars_frame, width=5, textvariable=self.STBRcutoff1)
        STBR12 = Entry(self.STBR_vars_frame, width=5, textvariable=self.STBRcutoff2)
        STBR1checkbox = Checkbutton(self.STBR_vars_frame, variable=self.STBRthresholdVarEnabled)#, command=self.STBRcheatOnClick)
        STBR20 = Entry(self.STBR_vars_frame, width=5, background="#b6fcd5", textvariable=self.startSTBRreturn)
        STBR21 = Entry(self.STBR_vars_frame, width=5, textvariable=self.STBRreturn1)
        STBR22 = Entry(self.STBR_vars_frame, width=5, textvariable=self.STBRreturn2)
        STBR2checkbox = Checkbutton(self.STBR_vars_frame, variable=self.STBRreturnVarEnabled)#, command=self.STBRcheatOnClick)
        STBR30 = Entry(self.STBR_vars_frame, width=5, background="#b6fcd5", textvariable=self.startSTBRMOAS)
        STBR31 = Entry(self.STBR_vars_frame, width=5, textvariable=self.STBRMOAS1)
        STBR32 = Entry(self.STBR_vars_frame, width=5, textvariable=self.STBRMOAS2)
        STBR3checkbox = Checkbutton(self.STBR_vars_frame, variable=self.STBRMOASVarEnabled)#, command=self.BTSRcheatOnClick)


        STBR00.grid(row=1, column=0, sticky=W)
        STBR01.grid(row=1, column=1, sticky=W)
        STBR02.grid(row=1, column=2, sticky=W)
        STBR0checkbox.grid(row=1, column=3, sticky=W)
        STBR10.grid(row=3, column=0, sticky=W)
        STBR11.grid(row=3, column=1, sticky=W)
        STBR12.grid(row=3, column=2, sticky=W)
        STBR1checkbox.grid(row=3, column=3, sticky=W)
        STBR20.grid(row=5, column=0, sticky=W)
        STBR21.grid(row=5, column=1, sticky=W)
        STBR22.grid(row=5, column=2, sticky=W)
        STBR2checkbox.grid(row=5, column=3, sticky=W)
        STBR30.grid(row=7, column=0, sticky=W)
        STBR31.grid(row=7, column=1, sticky=W)
        STBR32.grid(row=7, column=2, sticky=W)
        STBR3checkbox.grid(row=7, column=3, sticky=W)







        #volume (middle frame) setup
        self.volume_control_frame = Frame(self.myMainContainer, borderwidth=3, relief='groove') 
        self.volume_control_frame.pack(side=LEFT, expand=NO,  padx=10, pady=5, ipadx=5, ipady=5, anchor=N)  

        Label(self.volume_control_frame, text="Volume", font="times 16 bold", justify=CENTER).pack(side=TOP, anchor=N)
        Label(self.volume_control_frame, text=" ", font="times 20 bold", justify=CENTER).pack(side=TOP, anchor=N)

        self.volume_vars_frame = Frame(self.volume_control_frame)
        self.volume_vars_frame.pack()

        Label(self.volume_vars_frame, text="Volume interval length", font="arial 10 bold").grid(row=0, columnspan=4, sticky=W)
        Label(self.volume_vars_frame, text="(8)", font="arial 10 bold").grid(row=0, column=3, sticky=N)
        Label(self.volume_vars_frame, text="Volume threshold cutoff", font="arial 10 bold").grid(row=2, columnspan=4, sticky=W)
        Label(self.volume_vars_frame, text="(9)", font="arial 10 bold").grid(row=2, column=3, sticky=N)
        Label(self.volume_vars_frame, text="Volume return value", font="arial 10 bold").grid(row=4, columnspan=4, sticky=W)
        Label(self.volume_vars_frame, text="(10)", font="arial 10 bold").grid(row=4, column=3, sticky=N)
        Label(self.volume_vars_frame, text="Volume MOAS interval", font="arial 10 bold").grid(row=6, columnspan=4, sticky=W)
        Label(self.volume_vars_frame, text="(11)", font="arial 10 bold").grid(row=6, column=3, sticky=N)


        volume00 = Entry(self.volume_vars_frame, width=5, background="#b6fcd5", textvariable=self.startVolumeInterval)
        volume01 = Entry(self.volume_vars_frame, width=5, textvariable=self.VolumeInterval1)
        volume02 = Entry(self.volume_vars_frame, width=5, textvariable=self.VolumeInterval2)
        volume0checkbox = Checkbutton(self.volume_vars_frame, variable=self.volumeIntervalVarEnabled)#, command=self.volumecheatOnClick)
        volume10 = Entry(self.volume_vars_frame, width=5, background="#b6fcd5", textvariable=self.startVolumeCutoff)
        volume11 = Entry(self.volume_vars_frame, width=5, textvariable=self.VolumeCutoff1)
        volume12 = Entry(self.volume_vars_frame, width=5, textvariable=self.VolumeCutoff2)
        volume1checkbox = Checkbutton(self.volume_vars_frame, variable=self.volumeThresholdVarEnabled)#, command=self.volumecheatOnClick)
        volume20 = Entry(self.volume_vars_frame, width=5, background="#b6fcd5", textvariable=self.startVolumeReturn)
        volume21 = Entry(self.volume_vars_frame, width=5, textvariable=self.VolumeReturn1)
        volume22 = Entry(self.volume_vars_frame, width=5, textvariable=self.VolumeReturn2)
        volume2checkbox = Checkbutton(self.volume_vars_frame, variable=self.volumeReturnVarEnabled)#, command=self.volumecheatOnClick)
        volume30 = Entry(self.volume_vars_frame, width=5, background="#b6fcd5", textvariable=self.startVolumeMOAS)
        volume31 = Entry(self.volume_vars_frame, width=5, textvariable=self.VolumeMOAS1)
        volume32 = Entry(self.volume_vars_frame, width=5, textvariable=self.VolumeMOAS2)
        volume3checkbox = Checkbutton(self.volume_vars_frame, variable=self.volumeMOASVarEnabled)#, command=self.volumecheatOnClick)


        volume00.grid(row=1, column=0, sticky=W)
        volume01.grid(row=1, column=1, sticky=W)
        volume02.grid(row=1, column=2, sticky=W)
        volume0checkbox.grid(row=1, column=3, sticky=W)
        volume10.grid(row=3, column=0, sticky=W)
        volume11.grid(row=3, column=1, sticky=W)
        volume12.grid(row=3, column=2, sticky=W)
        volume1checkbox.grid(row=3, column=3, sticky=W)
        volume20.grid(row=5, column=0, sticky=W)
        volume21.grid(row=5, column=1, sticky=W)
        volume22.grid(row=5, column=2, sticky=W)
        volume2checkbox.grid(row=5, column=3, sticky=W)
        volume30.grid(row=7, column=0, sticky=W)
        volume31.grid(row=7, column=1, sticky=W)
        volume32.grid(row=7, column=2, sticky=W)
        volume3checkbox.grid(row=7, column=3, sticky=W)







        #violenceBuys (second-from-right frame) setup
        self.violenceBuys_control_frame = Frame(self.myMainContainer, borderwidth=3, relief='groove') 
        self.violenceBuys_control_frame.pack(side=LEFT, expand=NO,  padx=15, pady=5, ipadx=5, ipady=5, anchor=N)  

        Label(self.violenceBuys_control_frame, text="Violence Buys", font="times 16 bold", justify=CENTER).pack(side=TOP, anchor=N)

        vioBuysCheatCheckbox = Checkbutton(self.violenceBuys_control_frame, text="Cheat?", variable=self.vioBuysCheatVarEnabled)#, command=self.BTSRcheatOnClick)
        vioBuysCheatCheckbox.pack(pady=8)

        self.violenceBuys_vars_frame = Frame(self.violenceBuys_control_frame)
        self.violenceBuys_vars_frame.pack()

        Label(self.violenceBuys_vars_frame, text="vioBuy Interval Length", font="arial 10 bold").grid(row=0, columnspan=4, sticky=W)
        Label(self.violenceBuys_vars_frame, text="(12)", font="arial 10 bold").grid(row=0, column=3, sticky=N)
        Label(self.violenceBuys_vars_frame, text="vioBuy Threshold Cutoff", font="arial 10 bold").grid(row=2, columnspan=4, sticky=W)
        Label(self.violenceBuys_vars_frame, text="(13)", font="arial 10 bold").grid(row=2, column=3, sticky=N)
        Label(self.violenceBuys_vars_frame, text="vioBuy Return Value", font="arial 10 bold").grid(row=4, columnspan=4, sticky=W)
        Label(self.violenceBuys_vars_frame, text="(14)", font="arial 10 bold").grid(row=4, column=3, sticky=N)

        violenceBuys00 = Entry(self.violenceBuys_vars_frame, width=5, background="#b6fcd5", textvariable=self.startViolenceBuyInterval)
        violenceBuys01 = Entry(self.violenceBuys_vars_frame, width=5, textvariable=self.ViolenceBuyInterval1)
        violenceBuys02 = Entry(self.violenceBuys_vars_frame, width=5, textvariable=self.ViolenceBuyInterval2)
        violenceBuys0checkbox = Checkbutton(self.violenceBuys_vars_frame, variable=self.violenceBuysIntervalVarEnabled)#, command=self.violenceBuyscheatOnClick)
        violenceBuys10 = Entry(self.violenceBuys_vars_frame, width=5, background="#b6fcd5", textvariable=self.startViolenceBuyThreshold)
        violenceBuys11 = Entry(self.violenceBuys_vars_frame, width=5, textvariable=self.ViolenceBuyThreshold1)
        violenceBuys12 = Entry(self.violenceBuys_vars_frame, width=5, textvariable=self.ViolenceBuyThreshold2)
        violenceBuys1checkbox = Checkbutton(self.violenceBuys_vars_frame, variable=self.violenceBuysThresholdVarEnabled)#, command=self.violenceBuyscheatOnClick)
        violenceBuys20 = Entry(self.violenceBuys_vars_frame, width=5, background="#b6fcd5", textvariable=self.startViolenceBuyReturn)
        violenceBuys21 = Entry(self.violenceBuys_vars_frame, width=5, textvariable=self.ViolenceBuyReturn1)
        violenceBuys22 = Entry(self.violenceBuys_vars_frame, width=5, textvariable=self.ViolenceBuyReturn2)
        violenceBuys2checkbox = Checkbutton(self.violenceBuys_vars_frame, variable=self.violenceBuysReturnVarEnabled)#, command=self.violenceBuyscheatOnClick)


        violenceBuys00.grid(row=1, column=0, sticky=W)
        violenceBuys01.grid(row=1, column=1, sticky=W)
        violenceBuys02.grid(row=1, column=2, sticky=W)
        violenceBuys0checkbox.grid(row=1, column=3, sticky=W)
        violenceBuys10.grid(row=3, column=0, sticky=W)
        violenceBuys11.grid(row=3, column=1, sticky=W)
        violenceBuys12.grid(row=3, column=2, sticky=W)
        violenceBuys1checkbox.grid(row=3, column=3, sticky=W)
        violenceBuys20.grid(row=5, column=0, sticky=W)
        violenceBuys21.grid(row=5, column=1, sticky=W)
        violenceBuys22.grid(row=5, column=2, sticky=W)
        violenceBuys2checkbox.grid(row=5, column=3, sticky=W)

        reactSellsCheckbox = Checkbutton(self.violenceBuys_control_frame, text="React?", variable=self.doWeReactBySelling, command=self.doWeReactBySellingOnClick)
        reactSellsCheckbox.pack()




        #violenceSells (right frame) setup
        self.violenceSells_control_frame = Frame(self.myMainContainer, borderwidth=3, relief='groove') 
        self.violenceSells_control_frame.pack(side=LEFT, expand=NO,  padx=(10,20), pady=5, ipadx=5, ipady=5, anchor=N)  

        Label(self.violenceSells_control_frame, text="Violence Sells", font="times 16 bold", justify=CENTER).pack(side=TOP, anchor=N)

        vioSellsCheatCheckbox = Checkbutton(self.violenceSells_control_frame, text="Cheat?", variable=self.vioSellsCheatVarEnabled)#, command=self.BTSRcheatOnClick)
        vioSellsCheatCheckbox.pack(pady=8)

        self.violenceSells_vars_frame = Frame(self.violenceSells_control_frame)
        self.violenceSells_vars_frame.pack()

        Label(self.violenceSells_vars_frame, text="vioSell Interval Length", font="arial 10 bold").grid(row=0, columnspan=4, sticky=W)
        Label(self.violenceSells_vars_frame, text="(15)", font="arial 10 bold").grid(row=0, column=3, sticky=N)
        Label(self.violenceSells_vars_frame, text="vioSell Threshold Cutoff", font="arial 10 bold").grid(row=2, columnspan=4, sticky=W)
        Label(self.violenceSells_vars_frame, text="(16)", font="arial 10 bold").grid(row=2, column=3, sticky=N)
        Label(self.violenceSells_vars_frame, text="vioSell Return Value", font="arial 10 bold").grid(row=4, columnspan=4, sticky=W)
        Label(self.violenceSells_vars_frame, text="(17)", font="arial 10 bold").grid(row=4, column=3, sticky=N)

        violenceSells00 = Entry(self.violenceSells_vars_frame, width=5, background="#b6fcd5", textvariable=self.startViolenceSellInterval)
        violenceSells01 = Entry(self.violenceSells_vars_frame, width=5, textvariable=self.ViolenceSellInterval1)
        violenceSells02 = Entry(self.violenceSells_vars_frame, width=5, textvariable=self.ViolenceSellInterval2)
        violenceSells0checkbox = Checkbutton(self.violenceSells_vars_frame, variable=self.violenceSellsIntervalVarEnabled)#, command=self.violenceSellscheatOnClick)
        violenceSells10 = Entry(self.violenceSells_vars_frame, width=5, background="#b6fcd5", textvariable=self.startViolenceSellThreshold)
        violenceSells11 = Entry(self.violenceSells_vars_frame, width=5, textvariable=self.ViolenceSellThreshold1)
        violenceSells12 = Entry(self.violenceSells_vars_frame, width=5, textvariable=self.ViolenceSellThreshold2)
        violenceSells1checkbox = Checkbutton(self.violenceSells_vars_frame, variable=self.violenceSellsThresholdVarEnabled)#, command=self.violenceSellscheatOnClick)
        violenceSells20 = Entry(self.violenceSells_vars_frame, width=5, background="#b6fcd5", textvariable=self.startViolenceSellReturn)
        violenceSells21 = Entry(self.violenceSells_vars_frame, width=5, textvariable=self.ViolenceSellReturn1)
        violenceSells22 = Entry(self.violenceSells_vars_frame, width=5, textvariable=self.ViolenceSellReturn2)
        violenceSells2checkbox = Checkbutton(self.violenceSells_vars_frame, variable=self.violenceSellsReturnVarEnabled)#, command=self.violenceSellscheatOnClick)


        violenceSells00.grid(row=1, column=0, sticky=W)
        violenceSells01.grid(row=1, column=1, sticky=W)
        violenceSells02.grid(row=1, column=2, sticky=W)
        violenceSells0checkbox.grid(row=1, column=3, sticky=W)
        violenceSells10.grid(row=3, column=0, sticky=W)
        violenceSells11.grid(row=3, column=1, sticky=W)
        violenceSells12.grid(row=3, column=2, sticky=W)
        violenceSells1checkbox.grid(row=3, column=3, sticky=W)
        violenceSells20.grid(row=5, column=0, sticky=W)
        violenceSells21.grid(row=5, column=1, sticky=W)
        violenceSells22.grid(row=5, column=2, sticky=W)
        violenceSells2checkbox.grid(row=5, column=3, sticky=W)

        reactBuysCheckbox = Checkbutton(self.violenceSells_control_frame, text="React?", variable=self.doWeReactByBuying, command=self.doWeReactByBuyingOnClick)
        reactBuysCheckbox.pack()





        
        #BTSR Window Lengths setup (bottom-left)
        self.BTSRwindowLengths_control_frame = Frame(self.myMiddleContainer, borderwidth=3, relief='groove') 
        self.BTSRwindowLengths_control_frame.pack(side=LEFT, expand=NO,  padx=(25, 15), pady=5, ipadx=5, ipady=5, anchor=N)
        Label(self.BTSRwindowLengths_control_frame, text="BTSR Window Lengths", font="times 16 bold", justify=CENTER).pack(side=TOP, anchor=N)

        self.BTSRwindowLengths_vars_frame = Frame(self.BTSRwindowLengths_control_frame)
        self.BTSRwindowLengths_vars_frame.pack()

        Label(self.BTSRwindowLengths_vars_frame, text="Forward", font="arial 10 bold").grid(row=0, columnspan=4, sticky=W)
        Label(self.BTSRwindowLengths_vars_frame, text="(18)", font="arial 10 bold").grid(row=0, column=3, sticky=N)
        Label(self.BTSRwindowLengths_vars_frame, text="Back", font="arial 10 bold").grid(row=2, columnspan=4, sticky=W)
        Label(self.BTSRwindowLengths_vars_frame, text="(19)", font="arial 10 bold").grid(row=2, column=3, sticky=N)


        BTSRwindowLengths00 = Entry(self.BTSRwindowLengths_vars_frame, width=5, background="#b6fcd5", textvariable=self.startBTSRwindowForwardLen)
        BTSRwindowLengths01 = Entry(self.BTSRwindowLengths_vars_frame, width=5, textvariable=self.BTSRwindowForwardLen1)
        BTSRwindowLengths02 = Entry(self.BTSRwindowLengths_vars_frame, width=5, textvariable=self.BTSRwindowForwardLen2)
        BTSRwindowLengths0checkbox = Checkbutton(self.BTSRwindowLengths_vars_frame, variable=self.BTSRwindowLengthsForwardVarEnabled)#, command=self.BTSRwindowLengthscheatOnClick)
        BTSRwindowLengths10 = Entry(self.BTSRwindowLengths_vars_frame, width=5, background="#b6fcd5", textvariable=self.startBTSRwindowBackLen)
        BTSRwindowLengths11 = Entry(self.BTSRwindowLengths_vars_frame, width=5, textvariable=self.BTSRwindowBackLen1)
        BTSRwindowLengths12 = Entry(self.BTSRwindowLengths_vars_frame, width=5, textvariable=self.BTSRwindowBackLen2)
        BTSRwindowLengths1checkbox = Checkbutton(self.BTSRwindowLengths_vars_frame, variable=self.BTSRwindowLengthsBackVarEnabled)#, command=self.BTSRwindowLengthscheatOnClick)
        

        BTSRwindowLengths00.grid(row=1, column=0, sticky=W)
        BTSRwindowLengths01.grid(row=1, column=1, sticky=W)
        BTSRwindowLengths02.grid(row=1, column=2, sticky=W)
        BTSRwindowLengths0checkbox.grid(row=1, column=3, sticky=W)
        BTSRwindowLengths10.grid(row=3, column=0, sticky=W)
        BTSRwindowLengths11.grid(row=3, column=1, sticky=W)
        BTSRwindowLengths12.grid(row=3, column=2, sticky=W)
        BTSRwindowLengths1checkbox.grid(row=3, column=3, sticky=W)






        #MULTIPLOT (bottom middle frame) setup
        self.multiplotButtonFrame = Frame(self.myMiddleContainer)
        self.multiplotButtonFrame.pack(side=LEFT)#, expand=YES)
        
        self.multiplotVarsFrame = Frame(self.myMiddleContainer)
        self.multiplotVarsFrame.pack(side=LEFT)

        self.multiplotImage = PhotoImage(file="./images/bubblechart.gif")
        self.multiplotButton = Button(self.multiplotButtonFrame,
          image=self.multiplotImage, compound="center", text="Multiplot", font="times 12 bold",
          #width=button_width, height=button_height,
          padx=button_padx, 
          pady=button_pady 
          )
        self.multiplotButton.pack()
        self.multiplotButton.bind("<Button-1>", self.multiplotButtonClick)   
        self.multiplotButton.bind("<Return>", self.multiplotButtonClick) 

        multiplotPPCheckbox = Checkbutton(self.multiplotVarsFrame, text="Profits", variable=self.multiplotPPEnabled)#, command=self.BTSRcheatOnClick)
        multiplotPPCheckbox.grid(sticky=W)
        multiplotBTSRCheckbox = Checkbutton(self.multiplotVarsFrame, text="BTSR", variable=self.multiplotBTSREnabled)#, command=self.BTSRcheatOnClick)
        multiplotBTSRCheckbox.grid(sticky=W)
        multiplotSTBRCheckbox = Checkbutton(self.multiplotVarsFrame, text="STBR", variable=self.multiplotSTBREnabled)#, command=self.BTSRcheatOnClick)
        multiplotSTBRCheckbox.grid(sticky=W)
        multiplotVolumeCheckbox = Checkbutton(self.multiplotVarsFrame, text="Volume", variable=self.multiplotVolumeEnabled)#, command=self.BTSRcheatOnClick)
        multiplotVolumeCheckbox.grid(sticky=W)
        multiplot1secondVolumeCheckbox = Checkbutton(self.multiplotVarsFrame, text="1-sec Volume", variable=self.multiplot1secondVolumeEnabled)#, command=self.BTSRcheatOnClick)
        multiplot1secondVolumeCheckbox.grid(sticky=W)
        multiplotViolenceBuyMACheckbox = Checkbutton(self.multiplotVarsFrame, text="VioBuy MA", variable=self.multiplotViolenceBuyMAEnabled)#, command=self.BTSRcheatOnClick)
        multiplotViolenceBuyMACheckbox.grid(sticky=W)
        multiplotViolenceSellMACheckbox = Checkbutton(self.multiplotVarsFrame, text="VioSell MA", variable=self.multiplotViolenceSellMAEnabled)#, command=self.BTSRcheatOnClick)
        multiplotViolenceSellMACheckbox.grid(sticky=W)

        multiplotRainbowCheckbox = Checkbutton(self.multiplotVarsFrame, text="Multicolors", variable=self.multiplotRainbowEnabled)#, command=self.BTSRcheatOnClick)
        multiplotRainbowCheckbox.grid(row=0, column=1, sticky=W)
        Label(self.multiplotVarsFrame, text="  Marks", font="arial 11 bold").grid(row=1, column=1, sticky=W)
        multiplotBTSRspikesCheckbox = Checkbutton(self.multiplotVarsFrame, text="BTSR spikes", variable=self.multiplotBTSRspikesEnabled)#, command=self.BTSRcheatOnClick)
        multiplotBTSRspikesCheckbox.grid(row=2, column=1, sticky=W)
        multiplotSTBRspikesCheckbox = Checkbutton(self.multiplotVarsFrame, text="STBR spikes", variable=self.multiplotSTBRspikesEnabled)#, command=self.BTSRcheatOnClick)
        multiplotSTBRspikesCheckbox.grid(row=3, column=1, sticky=W)
        multiplotVolumeSpikesCheckbox = Checkbutton(self.multiplotVarsFrame, text="Volume spikes", variable=self.multiplotVolumeSpikesEnabled)#, command=self.BTSRcheatOnClick)
        multiplotVolumeSpikesCheckbox.grid(row=4, column=1, sticky=W)
        multiplotVioBuySpikesCheckbox = Checkbutton(self.multiplotVarsFrame, text="VioBuy cross", variable=self.multiplotVioBuySpikesEnabled)#, command=self.BTSRcheatOnClick)
        multiplotVioBuySpikesCheckbox.grid(row=5, column=1, sticky=W)
        multiplotVioSellSpikesCheckbox = Checkbutton(self.multiplotVarsFrame, text="VioSell cross", variable=self.multiplotVioSellSpikesEnabled)#, command=self.BTSRcheatOnClick)
        multiplotVioSellSpikesCheckbox.grid(row=6, column=1, sticky=W)





        #reactive Sells (second-from-right bottom)
        self.reactSells_control_frame = Frame(self.myMiddleContainer, borderwidth=3, relief='groove') 
        self.reactSells_control_frame.pack(side=LEFT, expand=NO,  padx=20, pady=5, ipadx=5, ipady=5, anchor=W)
        Label(self.reactSells_control_frame, text="Reactive Sells", font="times 16 bold", justify=CENTER).pack(side=TOP, anchor=N)

        self.reactSells_vars_frame = Frame(self.reactSells_control_frame)
        self.reactSells_vars_frame.pack()

        Label(self.reactSells_vars_frame, text="Threshold", font="arial 10 bold").grid(row=0, columnspan=4, sticky=W)
        Label(self.reactSells_vars_frame, text="(20)", font="arial 10 bold").grid(row=0, column=3, sticky=N)

        reactSells00 = Entry(self.reactSells_vars_frame, width=5, background="#b6fcd5", textvariable=self.startReactSellsCutoff)
        reactSells00.configure(state='readonly')
        reactSells01 = Entry(self.reactSells_vars_frame, width=5, textvariable=self.reactSellsCutoff1)
        reactSells01.configure(state='readonly')
        reactSells02 = Entry(self.reactSells_vars_frame, width=5, textvariable=self.reactSellsCutoff2)
        reactSells02.configure(state='readonly')
        reactSells0checkbox = Checkbutton(self.reactSells_vars_frame, variable=self.reactSellsChangeVarEnabled)#, command=self.violenceBuyscheatOnClick)
        reactSells0checkbox.configure(state='disabled')

        reactSells00.grid(row=1, column=0, sticky=W)
        reactSells01.grid(row=1, column=1, sticky=W)
        reactSells02.grid(row=1, column=2, sticky=W)
        reactSells0checkbox.grid(row=1, column=3, sticky=W)

        Label(self.reactSells_vars_frame, text="Window Length", font="arial 10 bold").grid(row=2, columnspan=4, sticky=W)
        Label(self.reactSells_vars_frame, text="(21)", font="arial 10 bold").grid(row=2, column=3, sticky=N)


        reactSellsWindowLengths00 = Entry(self.reactSells_vars_frame, width=5, background="#b6fcd5", textvariable=self.startReactSellsWindowLen)
        reactSellsWindowLengths01 = Entry(self.reactSells_vars_frame, width=5, textvariable=self.reactSellsWindowLen1)
        reactSellsWindowLengths02 = Entry(self.reactSells_vars_frame, width=5, textvariable=self.reactSellsWindowLen2)
        reactSellsWindowLengths0checkbox = Checkbutton(self.reactSells_vars_frame, variable=self.reactSellsWindowLengthsForwardVarEnabled)#, command=self.violenceSellReactWindowLengthscheatOnClick)
        

        reactSellsWindowLengths00.grid(row=3, column=0, sticky=W); reactSellsWindowLengths00.configure(state='readonly')
        reactSellsWindowLengths01.grid(row=3, column=1, sticky=W); reactSellsWindowLengths01.configure(state='readonly')
        reactSellsWindowLengths02.grid(row=3, column=2, sticky=W); reactSellsWindowLengths02.configure(state='readonly')
        reactSellsWindowLengths0checkbox.grid(row=3, column=3, sticky=W)
        reactSellsWindowLengths0checkbox.configure(state='disabled')



        #reactive buys (bottom right)
        self.reactBuys_control_frame = Frame(self.myMiddleContainer, borderwidth=3, relief='groove') 
        self.reactBuys_control_frame.pack(side=LEFT, expand=NO,  padx=15, pady=5, ipadx=5, ipady=5, anchor=W)
        Label(self.reactBuys_control_frame, text="Reactive Buys", font="times 16 bold", justify=CENTER).pack(side=TOP, anchor=N)

        self.reactBuys_vars_frame = Frame(self.reactBuys_control_frame)
        self.reactBuys_vars_frame.pack()

        Label(self.reactBuys_vars_frame, text="Threshold", font="arial 10 bold").grid(row=0, columnspan=4, sticky=W)
        Label(self.reactBuys_vars_frame, text="(22)", font="arial 10 bold").grid(row=0, column=3, sticky=N)

        reactBuys00 = Entry(self.reactBuys_vars_frame, width=5, background="#b6fcd5", textvariable=self.startReactBuysCutoff)
        reactBuys00.configure(state='readonly')
        reactBuys01 = Entry(self.reactBuys_vars_frame, width=5, textvariable=self.reactBuysCutoff1)
        reactBuys01.configure(state='readonly')
        reactBuys02 = Entry(self.reactBuys_vars_frame, width=5, textvariable=self.reactBuysCutoff2)
        reactBuys02.configure(state='readonly')
        reactBuys0checkbox = Checkbutton(self.reactBuys_vars_frame, variable=self.reactBuysChangeVarEnabled)#, command=self.violenceSellscheatOnClick)
        reactBuys0checkbox.configure(state='disabled')

        reactBuys00.grid(row=1, column=0, sticky=W)
        reactBuys01.grid(row=1, column=1, sticky=W)
        reactBuys02.grid(row=1, column=2, sticky=W)
        reactBuys0checkbox.grid(row=1, column=3, sticky=W)


        Label(self.reactBuys_vars_frame, text="Window Length", font="arial 10 bold").grid(row=2, columnspan=4, sticky=W)
        Label(self.reactBuys_vars_frame, text="(23)", font="arial 10 bold").grid(row=2, column=3, sticky=N)


        reactBuysWindowLengths00 = Entry(self.reactBuys_vars_frame, width=5, background="#b6fcd5", textvariable=self.startReactBuysWindowLen)
        reactBuysWindowLengths01 = Entry(self.reactBuys_vars_frame, width=5, textvariable=self.reactBuysWindowLen1)
        reactBuysWindowLengths02 = Entry(self.reactBuys_vars_frame, width=5, textvariable=self.reactBuysWindowLen2)
        reactBuysWindowLengths0checkbox = Checkbutton(self.reactBuys_vars_frame, variable=self.reactBuysWindowLengthsForwardVarEnabled)#, command=self.reactBuyscheatOnClick)
        

        reactBuysWindowLengths00.grid(row=3, column=0, sticky=W); reactBuysWindowLengths00.configure(state='readonly')
        reactBuysWindowLengths01.grid(row=3, column=1, sticky=W); reactBuysWindowLengths01.configure(state='readonly')
        reactBuysWindowLengths02.grid(row=3, column=2, sticky=W); reactBuysWindowLengths02.configure(state='readonly')
        reactBuysWindowLengths0checkbox.grid(row=3, column=3, sticky=W)
        reactBuysWindowLengths0checkbox.configure(state='disabled')


        self.bottom_control_frame = Frame(self.myLowerContainer, borderwidth=2, relief='groove')
        self.bottom_control_frame.pack(side=TOP, expand=NO, fill=X, ipadx=5, ipady=5, anchor=W)

        self.thoroughButtonFrame = Frame(self.bottom_control_frame, padx=5)
        self.thoroughButtonFrame.pack(side=LEFT)#, expand=YES)
        
        self.thoroughButton = Button(self.thoroughButtonFrame,
          text="Thorough Test", font="times 13 bold", background="#8dcd91", activebackground='green', 
          width=button_width, height=button_height,
          padx=10, 
          pady=10
          )
        self.thoroughButton.pack(side=LEFT, anchor=E)
        self.thoroughButton.bind("<Button-1>", self.thoroughButtonClick)   
        self.thoroughButton.bind("<Return>", self.thoroughButtonClick) 

        '''self.oneTestButtonFrame = Frame(self.bottom_control_frame, padx=5)
        self.oneTestButtonFrame.pack(side=LEFT)#, expand=YES)
        
        self.oneTestButton = Button(self.oneTestButtonFrame,
          text="1", font="times 13 bold", background="#00dd88", activebackground='green', 
          width=1, height=button_height,
          padx=10, 
          pady=10
          )
        self.oneTestButton.pack(side=LEFT, anchor=E)
        self.oneTestButton.bind("<Button-1>", self.oneTestButtonClick)   
        self.oneTestButton.bind("<Return>", self.oneTestButtonClick) 
        '''
        self.gifFrame = Frame(self.bottom_control_frame, padx=25, pady=10)
        self.gifFrame.pack(side=LEFT)#, expand=YES)

        self.currentTestFrame = Frame(self.bottom_control_frame, padx=10)
        self.currentTestFrame.pack(side=LEFT, expand=NO)
   
        Label(self.currentTestFrame, text="Current:", font="times 13 bold").grid(row=0, padx=10, sticky=W)
        Label(self.currentTestFrame, text="Next:", font="times 13 bold").grid(row=0, column=1, padx=10, sticky=W)

        self.currentTestVar = Entry(self.currentTestFrame, width=3, textvariable=self.startCurrentTestVar, justify=CENTER, state='readonly')
        self.currentTestVar.grid(row=1, padx=10)
        self.nextTestVar = Entry(self.currentTestFrame, width=3, textvariable=self.startNextTestVar, justify=CENTER)
        self.nextTestVar.grid(row=1, column=1, padx=10)

        self.nextTestVar.bind(sequence='<KeyRelease>', func=self.updateNextVar())

        self.cancelButtonFrame = Frame(self.bottom_control_frame, padx=5)
        self.cancelButtonFrame.pack(side=RIGHT)#, expand=YES)
        
        self.cancelButton = Button(self.cancelButtonFrame,
          text="EXIT", font="times 13 bold", background="#ff6666", activebackground='red', 
          width=button_width, height=button_height,
          padx=10,
          pady=10
          )
        self.cancelButton.pack(side=RIGHT, anchor=E)
        self.cancelButton.bind("<Button-1>", self.cancelButtonClick)   
        self.cancelButton.bind("<Return>", self.cancelButtonClick) 



        self.bottomButtonFrame = Frame(self.bottom_control_frame, padx=10)
        self.bottomButtonFrame.pack(side=RIGHT, expand=NO)
        self.emailImage = PhotoImage(file="./images/emailicon.png")
        self.emailButton = Button(self.bottomButtonFrame,
          image=self.emailImage, relief='flat',
          #width=button_width, height=button_height,
          padx=10,
          pady=10
          )
        self.emailButton.pack(side=TOP, anchor=N)
        self.emailButton.bind("<Button-1>", self.emailButtonClick)   
        self.emailButton.bind("<Return>", self.emailButtonClick) 

        self.writeImage = PhotoImage(file="./images/write.gif")
        self.writeButton = Button(self.bottomButtonFrame,
          image=self.writeImage, relief='flat',
          padx=10,
          pady=10
          )
        self.writeButton.pack(side=TOP, anchor=N)
        self.writeButton.bind("<Button-1>", self.writeButtonClick)   
        self.writeButton.bind("<Return>", self.writeButtonClick) 



        self.outputFileFrame = Frame(self.bottom_control_frame, padx=5)
        self.outputFileFrame.pack(side=RIGHT)

        #threading.Thread.__init__(self)

        Label(self.outputFileFrame, text="Output File:", font="times 12 bold", justify=CENTER).pack(side=TOP, anchor=W)

        outputFileEntry = Entry(self.outputFileFrame, width=20, textvariable=self.outputFile, justify=CENTER)
        outputFileEntry.pack(side=RIGHT)

        self.holder = Canvas(self.gifFrame, width=140, height=80)
        self.holder.pack()
        self.holder.bind("<Key>", self.pauseRun)
        self.holder.bind("<Button-1>", self.pauseRun)
 
        self.StaticFrame=[] #create empty
 
        #Import the images (naming convention "tmp-0123.gif")
        for i in range(0,123):
            filename="images/tmp-"+str(i)+".gif"
            self.StaticFrame+=[PhotoImage(file=filename)]

        run_as_thread(self.animation, 0)

        sys.stdout = Logger(self.outputFile.get())

        run_as_thread(self.feedVariables)

        self.root.mainloop()

        
 
    def animation(self, currentframe):
        def change_image():
            self.holder.create_image(0,0,anchor=NW,image=self.StaticFrame[self.currentframe], tag='Animate')
            # Delete the current picture if one exists
        self.holder.delete('Animate')

        try:
            change_image()
        except IndexError:
            # When you get to the end of the list of images - it simply resets itself back to zero and then we start again
            self.currentframe = 0
            change_image()
        if(not self.isPaused):
            self.holder.update_idletasks() #Force redraw
            self.currentframe = self.currentframe + 1
            # Call loop again to keep the animation running in a continuous loop
            self.root.after(75, self.animation, self.currentframe)
        else:
            change_image()


    def feedVariables(self):
        with self.lock:
            self.getData()
            self.myTester = Backtester(btcDA=self.btcDA, btcPA=self.btcPA, btcVA=self.btcVA, whichVar=int(self.startNextTestVar.get()), BTSRint=int(self.startBTSRinterval.get()), BTSRcut=float(self.startBTSRcutoff.get()), BTSRret=float(self.startBTSRreturn.get()), BTSRmoas=int(self.startBTSRMOAS.get()), STBRint=int(self.startSTBRinterval.get()), STBRcut=float(self.startSTBRcutoff.get()), STBRret=float(self.startSTBRreturn.get()), STBRmoas=int(self.startSTBRMOAS.get()), volInt=int(self.startVolumeInterval.get()), volCut=float(self.startVolumeCutoff.get()), volRet=float(self.startVolumeReturn.get()), volMOAS=int(self.startVolumeMOAS.get()), vioBuyInt=int(self.startViolenceBuyInterval.get()), vioBuyCut=float(self.startViolenceBuyThreshold.get()), vioBuyRet=float(self.startViolenceBuyReturn.get()), vioSellInt=int(self.startViolenceSellInterval.get()), vioSellCut=float(self.startViolenceSellThreshold.get()), vioSellRet=float(self.startViolenceSellReturn.get()), BTSRwindowLenForward=int(self.startBTSRwindowForwardLen.get()), BTSRwindowLenBack=int(self.startBTSRwindowBackLen.get()), reactToVioBuy=self.doWeReactBySelling.get(), reactToVioSell=self.doWeReactByBuying.get(), reactToVioBuyCut=float(self.startReactSellsCutoff.get()), reactToVioSellCut=float(self.startReactBuysCutoff.get()), reactToVioBuyForward=int(self.startReactSellsWindowLen.get()), reactToVioSellForward=int(self.startReactBuysWindowLen.get()), whichExchange=('Bitstamp' if self.whichExchange.get() else 'Bitfinex'), cheatBTSR=self.BTSRcheatVarEnabled.get(), cheatSTBR=self.STBRcheatVarEnabled.get(), cheatVioBuys=self.vioBuysCheatVarEnabled.get(), cheatVioSells=self.vioSellsCheatVarEnabled.get(), doWeShort=self.doWeShort.get())
        os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')

    def refeedVariables(self):
        self.myTester = Backtester(btcDA=self.btcDA, btcPA=self.btcPA, btcVA=self.btcVA, whichVar=int(self.startNextTestVar.get()), BTSRint=int(self.startBTSRinterval.get()), BTSRcut=float(self.startBTSRcutoff.get()), BTSRret=float(self.startBTSRreturn.get()), BTSRmoas=int(self.startBTSRMOAS.get()), STBRint=int(self.startSTBRinterval.get()), STBRcut=float(self.startSTBRcutoff.get()), STBRret=float(self.startSTBRreturn.get()), STBRmoas=int(self.startSTBRMOAS.get()), volInt=int(self.startVolumeInterval.get()), volCut=float(self.startVolumeCutoff.get()), volRet=float(self.startVolumeReturn.get()), volMOAS=int(self.startVolumeMOAS.get()), vioBuyInt=int(self.startViolenceBuyInterval.get()), vioBuyCut=float(self.startViolenceBuyThreshold.get()), vioBuyRet=float(self.startViolenceBuyReturn.get()), vioSellInt=int(self.startViolenceSellInterval.get()), vioSellCut=float(self.startViolenceSellThreshold.get()), vioSellRet=float(self.startViolenceSellReturn.get()), BTSRwindowLenForward=int(self.startBTSRwindowForwardLen.get()), BTSRwindowLenBack=int(self.startBTSRwindowBackLen.get()), reactToVioBuy=self.doWeReactBySelling.get(), reactToVioSell=self.doWeReactByBuying.get(), reactToVioBuyCut=float(self.startReactSellsCutoff.get()), reactToVioSellCut=float(self.startReactBuysCutoff.get()), reactToVioBuyForward=int(self.startReactSellsWindowLen.get()), reactToVioSellForward=int(self.startReactBuysWindowLen.get()), whichExchange=('Bitstamp' if self.whichExchange.get() else 'Bitfinex'), cheatBTSR=self.BTSRcheatVarEnabled.get(), cheatSTBR=self.STBRcheatVarEnabled.get(), cheatVioBuys=self.vioBuysCheatVarEnabled.get(), cheatVioSells=self.vioSellsCheatVarEnabled.get(), doWeShort=self.doWeShort.get())


    def getData(self):
        del self.btcDA [:]
        del self.btcPA [:]
        del self.btcVA [:]
        if(self.whichExchange.get()==0):
            self.btcDA, self.btcPA, self.btcVA = buildArrays(ifile="data/bitfinex.csv", beginTime=int(self.tBegin.get()), endTime=int(self.tEnd.get()))
        else:
            self.btcDA, self.btcPA, self.btcVA = buildArrays(ifile="data/bitstamp.csv", beginTime=int(self.tBegin.get()), endTime=int(self.tEnd.get()))


    def validate(self, action, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if(False):
            return True
        else:
            if text in '0123456789.-':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False

    def updateDateText(self):
        self.prettytBegin.set(longPrettifyDate(self.tBegin.get()))
        self.prettytEnd.set(longPrettifyDate(self.tEnd.get()))
        self.root.update_idletasks()  

    def updateNextVar(self):
        self.startNextTestVar.set(self.nextTestVar.get())
        self.root.update_idletasks()  

    def BTSRcheatOnClick(self):  
        if self.BTSRcheatVarEnabled.get():
            for child in self.BTSR_vars_frame.winfo_children():
                child.configure(state='disabled')
            self.BTSRintervalVarEnabled.set(0)
            self.BTSRthresholdVarEnabled.set(0)
            self.BTSRreturnVarEnabled.set(0)
            self.BTSRMOASVarEnabled.set(0)
            if self.STBRcheatVarEnabled.get():
                for child in self.BTSRwindowLengths_vars_frame.winfo_children():
                    child.configure(state='disabled')
                self.BTSRwindowLengthsForwardVarEnabled.set(0)
                self.BTSRwindowLengthsBackVarEnabled.set(0)
                for child in self.volume_vars_frame.winfo_children():
                    child.configure(state='disabled')
                self.volumeIntervalVarEnabled.set(0)
                self.volumeThresholdVarEnabled.set(0)
                self.volumeReturnVarEnabled.set(0)
                self.volumeMOASVarEnabled.set(0)
        else:
            for child in self.BTSR_vars_frame.winfo_children():
                child.configure(state='normal')
            if self.STBRcheatVarEnabled.get():
                for child in self.BTSRwindowLengths_vars_frame.winfo_children():
                    child.configure(state='normal')
                for child in self.volume_vars_frame.winfo_children():
                    child.configure(state='normal')

    def STBRcheatOnClick(self):   
        if self.STBRcheatVarEnabled.get():
            for child in self.STBR_vars_frame.winfo_children():
                child.configure(state='disabled')
            self.STBRintervalVarEnabled.set(0)
            self.STBRthresholdVarEnabled.set(0)
            self.STBRreturnVarEnabled.set(0)
            self.STBRMOASVarEnabled.set(0)
            if self.BTSRcheatVarEnabled.get():
                for child in self.BTSRwindowLengths_vars_frame.winfo_children():
                    child.configure(state='disabled')
                self.BTSRwindowLengthsForwardVarEnabled.set(0)
                self.BTSRwindowLengthsBackVarEnabled.set(0)
                for child in self.volume_vars_frame.winfo_children():
                    child.configure(state='disabled')
                self.volumeIntervalVarEnabled.set(0)
                self.volumeThresholdVarEnabled.set(0)
                self.volumeReturnVarEnabled.set(0)
                self.volumeMOASVarEnabled.set(0)
        else:
            for child in self.STBR_vars_frame.winfo_children():
                child.configure(state='normal')
            if self.BTSRcheatVarEnabled.get():
                for child in self.BTSRwindowLengths_vars_frame.winfo_children():
                    child.configure(state='normal')
                for child in self.volume_vars_frame.winfo_children():
                    child.configure(state='normal')

    def doWeReactByBuyingOnClick(self):
        if(self.doWeReactByBuying.get()):
            for child in self.reactBuys_vars_frame.winfo_children():
                child.configure(state='normal')
        else:
            for child in self.reactBuys_vars_frame.winfo_children():
                child.configure(state='disabled')
            self.reactBuysChangeVarEnabled.set(0)
            self.reactBuysWindowLengthsForwardVarEnabled.set(0)

        self.myTester.changeDoWeReactByBuying()

    def doWeReactBySellingOnClick(self):
        if(self.doWeReactBySelling.get()):
            for child in self.reactSells_vars_frame.winfo_children():
                child.configure(state='normal')
        else:
            for child in self.reactSells_vars_frame.winfo_children():
                child.configure(state='disabled')
            self.reactSellsChangeVarEnabled.set(0)
            self.reactSellsWindowLengthsForwardVarEnabled.set(0)

        self.myTester.changeDoWeReactBySelling()

    def disableSellReacts(self):
        for child in childList:
            child.configure(state='enable')
    
    def cancelButtonClick(self, event): 
        #self.root.destroy()   
        self.root.quit()
        exit()

    def pauseRun(self, event): 
        self.isPaused = not self.isPaused 
        if(not self.isPaused):
            self.animation(self.currentframe)

    def emailButtonClick(self, event): 
        mailer(self.outputFile.get())
        sys.stdout = Logger(self.outputFile.get())


    def writeButtonClick(self, event): 
        f = open('minitialization.txt', 'a')
        f.write(self.getVarString())
        f.close()

    def getVarString(self):
        stringToWrite = ''
        stringToWrite += str(self.startBTSRinterval.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRinterval1.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRinterval2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startBTSRcutoff.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRcutoff1.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRcutoff2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startBTSRreturn.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRreturn1.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRreturn2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startBTSRMOAS.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRMOAS1.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRMOAS2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startSTBRinterval.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRinterval1.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRinterval2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startSTBRcutoff.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRcutoff1.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRcutoff2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startSTBRreturn.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRreturn1.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRreturn2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startSTBRMOAS.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRMOAS1.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRMOAS2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startVolumeInterval.get())
        stringToWrite += ' '
        stringToWrite += str(self.VolumeInterval1.get())
        stringToWrite += ' '
        stringToWrite += str(self.VolumeInterval2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startVolumeCutoff.get())
        stringToWrite += ' '
        stringToWrite += str(self.VolumeCutoff1.get())
        stringToWrite += ' '
        stringToWrite += str(self.VolumeCutoff2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startVolumeReturn.get())
        stringToWrite += ' '
        stringToWrite += str(self.VolumeReturn1.get())
        stringToWrite += ' '
        stringToWrite += str(self.VolumeReturn2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startVolumeMOAS.get())
        stringToWrite += ' '
        stringToWrite += str(self.VolumeMOAS1.get())
        stringToWrite += ' '
        stringToWrite += str(self.VolumeMOAS2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startViolenceBuyInterval.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceBuyInterval1.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceBuyInterval2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startViolenceBuyThreshold.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceBuyThreshold1.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceBuyThreshold2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startViolenceBuyReturn.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceBuyReturn1.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceBuyReturn2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startViolenceSellInterval.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceSellInterval1.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceSellInterval2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startViolenceSellThreshold.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceSellThreshold1.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceSellThreshold2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startViolenceSellReturn.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceSellReturn1.get())
        stringToWrite += ' '
        stringToWrite += str(self.ViolenceSellReturn2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startBTSRwindowForwardLen.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRwindowForwardLen1.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRwindowForwardLen2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startBTSRwindowBackLen.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRwindowBackLen1.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRwindowBackLen2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startReactSellsCutoff.get())
        stringToWrite += ' '
        stringToWrite += str(self.reactSellsCutoff1.get())
        stringToWrite += ' '
        stringToWrite += str(self.reactSellsCutoff2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startReactSellsWindowLen.get())
        stringToWrite += ' '
        stringToWrite += str(self.reactSellsWindowLen1.get())
        stringToWrite += ' '
        stringToWrite += str(self.reactSellsWindowLen2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startReactBuysCutoff.get())
        stringToWrite += ' '
        stringToWrite += str(self.reactBuysCutoff1.get())
        stringToWrite += ' '
        stringToWrite += str(self.reactBuysCutoff2.get())
        stringToWrite += ' '
        stringToWrite += str(self.startReactBuysWindowLen.get())
        stringToWrite += ' '
        stringToWrite += str(self.reactBuysWindowLen1.get())
        stringToWrite += ' '
        stringToWrite += str(self.reactBuysWindowLen2.get())
        stringToWrite += ' '
        stringToWrite += ('data/bitstamp.csv' if self.whichExchange.get() else 'data/bitfinex.csv')
        stringToWrite += ' '
        stringToWrite += str(self.doWeReactBySelling.get())
        stringToWrite += ' '
        stringToWrite += str(self.doWeReactByBuying.get())
        stringToWrite += ' '
        stringToWrite += str(self.BTSRcheatVarEnabled.get())
        stringToWrite += ' '
        stringToWrite += str(self.STBRcheatVarEnabled.get())
        stringToWrite += ' '
        stringToWrite += str(self.vioBuysCheatVarEnabled.get())
        stringToWrite += ' '
        stringToWrite += str(self.vioSellsCheatVarEnabled.get())
        stringToWrite += ' '
        stringToWrite += str(self.doWeShort.get())
        stringToWrite += '\n'
        return stringToWrite

    def diceRoll(self):
        del self.diceArr [:]
        if(self.BTSRintervalVarEnabled.get()):
            self.diceArr.append(0)
        if(self.BTSRthresholdVarEnabled.get()):
            self.diceArr.append(1)
        if(self.BTSRreturnVarEnabled.get()):
            self.diceArr.append(2)
        if(self.BTSRMOASVarEnabled.get()):
            self.diceArr.append(3)
        if(self.STBRintervalVarEnabled.get()):
            self.diceArr.append(4)
        if(self.STBRthresholdVarEnabled.get()):
            self.diceArr.append(5)
        if(self.STBRreturnVarEnabled.get()):
            self.diceArr.append(6)
        if(self.STBRMOASVarEnabled.get()):
            self.diceArr.append(7)
        if(self.volumeIntervalVarEnabled.get()):
            self.diceArr.append(8)
        if(self.volumeThresholdVarEnabled.get()):
            self.diceArr.append(9)
        if(self.volumeReturnVarEnabled.get()):
            self.diceArr.append(10)
        if(self.volumeMOASVarEnabled.get()):
            self.diceArr.append(11)
        if(self.violenceBuysIntervalVarEnabled.get()):
            self.diceArr.append(12)
        if(self.violenceBuysThresholdVarEnabled.get()):
            self.diceArr.append(13)
        if(self.violenceBuysReturnVarEnabled.get()):
            self.diceArr.append(14)
        if(self.violenceSellsIntervalVarEnabled.get()):
            self.diceArr.append(15)
        if(self.violenceSellsThresholdVarEnabled.get()):
            self.diceArr.append(16)
        if(self.violenceSellsReturnVarEnabled.get()):
            self.diceArr.append(17)
        if(self.BTSRwindowLengthsForwardVarEnabled.get()):
            self.diceArr.append(18)
        if(self.BTSRwindowLengthsBackVarEnabled.get()):
            self.diceArr.append(19)
        if(self.reactSellsChangeVarEnabled.get()):
            self.diceArr.append(20)
        if(self.reactSellsWindowLengthsForwardVarEnabled.get()):
            self.diceArr.append(21)
        if(self.reactBuysChangeVarEnabled.get()):
            self.diceArr.append(22)
        if(self.reactBuysWindowLengthsForwardVarEnabled.get()):
            self.diceArr.append(23)

        if(len(self.diceArr) < 1):
            #no more variables to loop; time to expand our windows!
            self.expandWindowsRandomly()
            self.reEnableAll()
            self.diceArr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        nextDiceRoll = random.randint(0, (len(self.diceArr)-1)) #roll the dice
        #while(self.diceArr[nextDiceRoll] == thisDiceVal): #...and keep rolling, if this is the same old variable
        #    nextDiceRoll = random.randint(0, (len(self.diceArr)-1)) 
        thisDiceVal = self.diceArr[nextDiceRoll]
        return thisDiceVal

    def reEnableAll(self):
        self.BTSRintervalVarEnabled.set(1)
        self.BTSRthresholdVarEnabled.set(1)
        self.BTSRreturnVarEnabled.set(1)
        self.BTSRMOASVarEnabled.set(1)
        self.STBRintervalVarEnabled.set(1)
        self.STBRthresholdVarEnabled.set(1)
        self.STBRreturnVarEnabled.set(1)
        self.STBRMOASVarEnabled.set(1)
        self.volumeIntervalVarEnabled.set(1)
        self.volumeThresholdVarEnabled.set(1)
        self.volumeReturnVarEnabled.set(1)
        self.volumeMOASVarEnabled.set(1)
        self.violenceBuysIntervalVarEnabled.set(1)
        self.violenceBuysThresholdVarEnabled.set(1)
        self.violenceBuysReturnVarEnabled.set(1)
        self.violenceSellsIntervalVarEnabled.set(1)
        self.violenceSellsThresholdVarEnabled.set(1)
        self.violenceSellsReturnVarEnabled.set(1)
        self.BTSRwindowLengthsForwardVarEnabled.set(1)
        self.BTSRwindowLengthsBackVarEnabled.set(1)
        if(self.doWeReactBySelling.get()):
            self.reactSellsChangeVarEnabled.set(1)
            self.reactSellsWindowLengthsForwardVarEnabled.set(1)
        if(self.doWeReactByBuying.get()):
            self.reactBuysChangeVarEnabled.set(1)
            self.reactBuysWindowLengthsForwardVarEnabled.set(1)

    def expandWindowsRandomly(self):
        self.BTSRinterval1.set(str(abs(round(np.random.normal(800, 750)))))
        self.BTSRcutoff1.set(str(abs(np.random.normal(3, 2.5))))
        self.BTSRreturn1.set(str(abs(float(self.BTSRcutoff1.get()) - abs(np.random.normal(0.8, 0.4)))))
        self.BTSRMOAS1.set(str(abs(round(np.random.normal(800, 750)))))
        self.STBRinterval1.set(str(abs(round(np.random.normal(800, 750)))))
        self.STBRcutoff1.set(str(abs(np.random.normal(3, 2.5))))
        self.STBRreturn1.set(str(abs(float(self.STBRcutoff1.get()) - abs(np.random.normal(0.8, 0.4)))))
        self.STBRMOAS1.set(str(abs(round(np.random.normal(800, 750)))))
        self.VolumeInterval1.set(str(abs(round(np.random.normal(800, 750)))))
        self.VolumeCutoff1.set(str(abs(np.random.normal(5, 3.5))))
        self.VolumeReturn1.set(str(abs(float(self.VolumeCutoff1.get()) - abs(np.random.normal(1.5, 0.7)))))
        self.VolumeMOAS1.set(str(abs(round(np.random.normal(800, 750)))))
        self.ViolenceBuyInterval1.set(str(abs(round(np.random.normal(1000, 1500)))))
        self.ViolenceBuyThreshold1.set(str(-abs(np.random.normal(0.03, 0.02))))
        self.ViolenceBuyReturn1.set(str(float(self.ViolenceBuyThreshold1.get()) + abs(np.random.normal(0.01, 0.02))))
        self.ViolenceSellInterval1.set(str(abs(round(np.random.normal(1000, 1500)))))
        self.ViolenceSellThreshold1.set(str(abs(np.random.normal(0.01, 0.02))))
        self.ViolenceSellReturn1.set(str(abs(abs(np.random.normal(0.01, 0.02)) - abs(np.random.normal(0.01, 0.02)))))
        self.BTSRwindowForwardLen1.set(str(abs(round(np.random.normal(800, 750)))))
        self.BTSRwindowBackLen1.set(str(abs(round(np.random.normal(500, 750)))))
        self.reactSellsCutoff1.set(str(abs(np.random.normal(0.008, 0.02))))
        self.reactSellsWindowLen1.set(str(abs(round(np.random.normal(800, 750)))))
        self.reactBuysCutoff1.set(str(-abs(np.random.normal(0.008, 0.02))))
        self.reactBuysWindowLen1.set(str(abs(round(np.random.normal(800, 750)))))

        self.BTSRinterval2.set(str(abs(round(np.random.normal(800, 750)))))
        self.BTSRcutoff2.set(str(abs(np.random.normal(1, 0.5))))
        self.BTSRreturn2.set(str(abs(float(self.BTSRcutoff1.get()) - abs(np.random.normal(0.8, 0.4)))))
        self.BTSRMOAS2.set(str(abs(round(np.random.normal(800, 750)))))
        self.STBRinterval2.set(str(abs(round(np.random.normal(800, 750)))))
        self.STBRcutoff2.set(str(abs(np.random.normal(1, 0.5))))
        self.STBRreturn2.set(str(abs(float(self.STBRcutoff1.get()) - abs(np.random.normal(0.8, 0.4)))))
        self.STBRMOAS2.set(str(abs(round(np.random.normal(800, 750)))))
        self.VolumeInterval2.set(str(abs(round(np.random.normal(800, 750)))))
        self.VolumeCutoff2.set(str(abs(np.random.normal(1, 0.5))))
        self.VolumeReturn2.set(str(abs(float(self.VolumeCutoff2.get()) - abs(np.random.normal(1.5, 0.7)))))
        self.VolumeMOAS2.set(str(abs(round(np.random.normal(800, 750)))))
        self.ViolenceBuyInterval2.set(str(abs(round(np.random.normal(1000, 1500)))))
        self.ViolenceBuyThreshold2.set(str(abs(np.random.normal(0.01, 0.02))))
        self.ViolenceBuyReturn2.set(str(abs(np.random.normal(0.01, 0.02))))
        self.ViolenceSellInterval2.set(str(abs(round(np.random.normal(600, 950)))))
        self.ViolenceSellThreshold2.set(str(abs(np.random.normal(0.01, 0.02))))
        self.ViolenceSellReturn2.set(str(abs(np.random.normal(0.01, 0.02))))
        self.BTSRwindowForwardLen2.set(str(abs(round(np.random.normal(800, 750)))))
        self.BTSRwindowBackLen2.set(str(abs(round(np.random.normal(500, 750)))))
        self.reactSellsCutoff2.set(str(abs(np.random.normal(0.008, 0.02))))
        self.reactSellsWindowLen2.set(str(abs(round(np.random.normal(800, 750)))))
        self.reactBuysCutoff2.set(str(abs(np.random.normal(0.008, 0.02))))
        self.reactBuysWindowLen2.set(str(abs(round(np.random.normal(800, 750)))))


    def updateVarEntry(self, minVar, newVal, newStartVal, newDistance):
        if(minVar == 0):
            self.startBTSRinterval.set(newVal)
            self.BTSRinterval1.set(newStartVal)
            self.BTSRinterval2.set(newDistance)
            self.myTester.changeBTSRinterval(newVal)
            if(newDistance < 0.00005):
                self.BTSRintervalVarEnabled.set(0)
        elif(minVar == 1):
            self.startBTSRcutoff.set(newVal)
            self.BTSRcutoff1.set(newStartVal)
            self.BTSRcutoff2.set(newDistance)
            self.myTester.changeBTSRcutoff(newVal)
            if(newDistance < 0.00005):
                self.BTSRthresholdVarEnabled.set(0)
        elif(minVar == 2):
            self.startBTSRreturn.set(newVal)
            self.BTSRreturn1.set(newStartVal)
            self.BTSRreturn2.set(newDistance)
            self.myTester.changeBTSRreturn(newVal)
            if(newDistance < 0.00005):
                self.BTSRreturnVarEnabled.set(0)
        elif(minVar == 3):
            self.startBTSRMOAS.set(newVal)
            self.BTSRMOAS1.set(newStartVal)
            self.BTSRMOAS2.set(newDistance)
            self.myTester.changeBTSRMOAS(newVal)
            if(newDistance < 0.00005):
                self.BTSRMOASVarEnabled.set(0)
        elif(minVar == 4):
            self.startSTBRinterval.set(newVal)
            self.STBRinterval1.set(newStartVal)
            self.STBRinterval2.set(newDistance)
            self.myTester.changeSTBRinterval(newVal)
            if(newDistance < 0.00005):
                self.STBRintervalVarEnabled.set(0)
        elif(minVar == 5):
            self.startSTBRcutoff.set(newVal)
            self.STBRcutoff1.set(newStartVal)
            self.STBRcutoff2.set(newDistance)
            self.myTester.changeSTBRcutoff(newVal)
            if(newDistance < 0.00005):
                self.STBRthresholdVarEnabled.set(0)
        elif(minVar == 6):
            self.startSTBRreturn.set(newVal)
            self.STBRreturn1.set(newStartVal)
            self.STBRreturn2.set(newDistance)
            self.myTester.changeSTBRreturn(newVal)
            if(newDistance < 0.00005):
                self.STBRreturnVarEnabled.set(0)
        elif(minVar == 7):
            self.startSTBRMOAS.set(newVal)
            self.STBRMOAS1.set(newStartVal)
            self.STBRMOAS2.set(newDistance)
            self.myTester.changeSTBRMOAS(newVal)
            if(newDistance < 0.00005):
                self.STBRMOASVarEnabled.set(0)
        elif(minVar == 8):
            self.startVolumeInterval.set(newVal)
            self.VolumeInterval1.set(newStartVal)
            self.VolumeInterval2.set(newDistance)
            self.myTester.changeVolumeInterval(newVal)
            if(newDistance < 0.00005):
                self.volumeIntervalVarEnabled.set(0)
        elif(minVar == 9):
            self.startVolumeCutoff.set(newVal)
            self.VolumeCutoff1.set(newStartVal)
            self.VolumeCutoff2.set(newDistance)
            self.myTester.changeVolumeCutoff(newVal)
            if(newDistance < 0.00005):
                self.volumeThresholdVarEnabled.set(0)
        elif(minVar == 10):
            self.startVolumeReturn.set(newVal)
            self.VolumeReturn1.set(newStartVal)
            self.VolumeReturn2.set(newDistance)
            self.myTester.changeVolumeReturn(newVal)
            if(newDistance < 0.00005):
                self.volumeReturnVarEnabled.set(0)
        elif(minVar == 11):
            self.startVolumeMOAS.set(newVal)
            self.VolumeMOAS1.set(newStartVal)
            self.VolumeMOAS2.set(newDistance)
            self.myTester.changeVolumeMOAS(newVal)
            if(newDistance < 0.00005):
                self.volumeMOASVarEnabled.set(0)
        elif(minVar == 12):
            self.startViolenceBuyInterval.set(newVal)
            self.ViolenceBuyInterval1.set(newStartVal)
            self.ViolenceBuyInterval2.set(newDistance)
            self.myTester.changeViolenceBuyInterval(newVal)
            if(newDistance < 0.00005):
                self.violenceBuysIntervalVarEnabled.set(0)
        elif(minVar == 13):
            self.startViolenceBuyThreshold.set(newVal)
            self.ViolenceBuyThreshold1.set(newStartVal)
            self.ViolenceBuyThreshold2.set(newDistance)
            self.myTester.changeViolenceBuyThreshold(newVal)
            if(newDistance < 0.00005):
                self.violenceBuysThresholdVarEnabled.set(0)
        elif(minVar == 14):
            self.startViolenceBuyReturn.set(newVal)
            self.ViolenceBuyReturn1.set(newStartVal)
            self.ViolenceBuyReturn2.set(newDistance)
            self.myTester.changeViolenceBuyReturn(newVal)
            if(newDistance < 0.00005):
                self.violenceBuysReturnVarEnabled.set(0)
        elif(minVar == 15):
            self.startViolenceSellInterval.set(str(newVal))
            self.ViolenceSellInterval1.set(str(newStartVal))
            self.ViolenceSellInterval2.set(str(newDistance))
            self.myTester.changeViolenceSellInterval(newVal)
            if(newDistance < 0.00005):
                self.violenceSellsIntervalVarEnabled.set(0)
        elif(minVar == 16):
            self.startViolenceSellThreshold.set(newVal)
            self.ViolenceSellThreshold1.set(newStartVal)
            self.ViolenceSellThreshold2.set(newDistance)
            self.myTester.changeViolenceSellThreshold(newVal)
            if(newDistance < 0.00005):
                self.violenceSellsThresholdVarEnabled.set(0)
        elif(minVar == 17):
            self.startViolenceSellReturn.set(newVal)
            self.ViolenceSellReturn1.set(newStartVal)
            self.ViolenceSellReturn2.set(newDistance)
            self.myTester.changeViolenceSellReturn(newVal)
            if(newDistance < 0.00005):
                self.violenceSellsReturnVarEnabled.set(0)
        elif(minVar == 18):
            self.startBTSRwindowForwardLen.set(newVal)
            self.BTSRwindowForwardLen1.set(newStartVal)
            self.BTSRwindowForwardLen2.set(newDistance)
            self.myTester.changeBTSRwindowForwardLen(newVal)
            if(newDistance < 0.00005):
                self.BTSRwindowLengthsForwardVarEnabled.set(0)
        elif(minVar == 19):
            self.startBTSRwindowBackLen.set(newVal)
            self.BTSRwindowBackLen1.set(newStartVal)
            self.BTSRwindowBackLen2.set(newDistance)
            self.myTester.changeBTSRwindowBackLen(newVal)
            if(newDistance < 0.00005):
                self.BTSRwindowLengthsBackVarEnabled.set(0)
        elif(minVar == 20):
            self.startReactSellsCutoff.set(newVal)
            self.reactSellsCutoff1.set(newStartVal)
            self.reactSellsCutoff2.set(newDistance)
            self.myTester.changeReactSellCut(newVal)
            if(newDistance < 0.00005):
                self.reactSellsChangeVarEnabled.set(0)
        elif(minVar == 21):
            self.startReactSellsWindowLen.set(newVal)
            self.reactSellsWindowLen1.set(newStartVal)
            self.reactSellsWindowLen2.set(newDistance)
            self.myTester.changeReactSellWindowLenForward(newVal)
            if(newDistance < 0.00005):
                self.reactSellsWindowLengthsForwardVarEnabled.set(0)
        elif(minVar == 22):
            self.startReactBuysCutoff.set(newVal)
            self.reactBuysCutoff1.set(newStartVal)
            self.reactBuysCutoff2.set(newDistance)
            self.myTester.changeReactBuyCut(newVal)
            if(newDistance < 0.00005):
                self.reactBuysChangeVarEnabled.set(0)
        elif(minVar == 23):
            self.startReactBuysWindowLen.set(newVal)
            self.reactBuysWindowLen1.set(newStartVal)
            self.reactBuysWindowLen2.set(newDistance)
            self.myTester.changeReactBuyWindowLenForward(newVal)
            if(newDistance < 0.00005):
                self.reactBuysWindowLengthsForwardVarEnabled.set(0)


    def multiplotButtonClick(self, event): 
        self.plotgo()

    def plotgo(self):
        self.getData()

        multiPass = []
        multiString = ''
        usingMultiString = False
        
        multiSettings = []
        multiSettings.append(self.multiplotBTSREnabled.get()) #0
        multiSettings.append(self.multiplotSTBREnabled.get()) #1
        multiSettings.append(self.multiplotVolumeEnabled.get()) #2
        multiSettings.append(self.multiplot1secondVolumeEnabled.get()) #3
        multiSettings.append(self.multiplotViolenceBuyMAEnabled.get()) #4
        multiSettings.append(self.multiplotViolenceSellMAEnabled.get()) #5
        multiSettings.append(self.multiplotPPEnabled.get()) #6
        multiSettings.append(self.multiplotRainbowEnabled.get()) #7
        multiSettings.append(self.multiplotBTSRspikesEnabled.get()) #8
        multiSettings.append(self.multiplotSTBRspikesEnabled.get()) #9
        multiSettings.append(self.multiplotVolumeSpikesEnabled.get()) #10
        multiSettings.append(self.multiplotVioBuySpikesEnabled.get()) #11
        multiSettings.append(self.multiplotVioSellSpikesEnabled.get()) #12
 
        fp = open('plotminitialization.txt', 'a')
        fp.write(self.getVarString())
        fp.close()

        f = open('plotsettings.txt', 'a')
        f.write(str(multiSettings))
        f.write('\n')
        f.close()
        plotRunString = "python3 justplot.py -b "
        plotRunString += str(self.timeIntervalBegin.get())
        plotRunString += " -e "
        plotRunString += str(self.timeIntervalEnd.get())
        os.system(plotRunString)
        #plotTester.multiPlot(multiPass)

    def refreshButtonClick(self, event):
        if(not self.isPaused): 
            self.pauseRun(event)
            wasPaused = False
        else:
            wasPaused = True
        self.prettytBegin.set(longPrettifyDate(self.timeIntervalBegin.get()))
        self.prettytEnd.set(longPrettifyDate(self.timeIntervalEnd.get()))

        self.feedVariables()

        if(self.isPaused): 
            if(not wasPaused):
                self.pauseRun(event)

    def oneTestButtonClick(self, event):
        if(not self.isPaused): 
            self.pauseRun(event)
            wasPaused = False
        else:
            wasPaused = True

        self.getData()
        self.feedVariables()

        if(self.isPaused): 
            if(not wasPaused):
                self.pauseRun(event)


    def originalThoroughButtonClick(self, event):
        if(not self.isPaused): 
            self.pauseRun(event)
        print('BEGINNING THOROUGH RUN')
        origBegin = int(self.tBegin.get())
        origEnd = int(self.tEnd.get())
        thoroughBegin = 1364878800 #'Apr 2 2013'
        thoroughEnd = 1368334800 #'May 12 2013'
        timeBetween = thoroughEnd - thoroughBegin
        while(thoroughEnd < 1420351200): #'Jan 4 2015'
            print('Starting on ', str(prettifyDate(thoroughBegin)), 'and ending on ', str(prettifyDate(thoroughEnd)), '(', str(thoroughBegin), '-', str(thoroughEnd), ')')
            self.tBegin.set(str(thoroughBegin))
            self.tEnd.set(str(thoroughEnd))
            self.getData()
            self.thoroughTester = Backtester(btcDA=self.btcDA, btcPA=self.btcPA, btcVA=self.btcVA, whichVar=int(self.startNextTestVar.get()), BTSRint=int(self.startBTSRinterval.get()), BTSRcut=float(self.startBTSRcutoff.get()), BTSRret=float(self.startBTSRreturn.get()), BTSRmoas=int(self.startBTSRMOAS.get()), STBRint=int(self.startSTBRinterval.get()), STBRcut=float(self.startSTBRcutoff.get()), STBRret=float(self.startSTBRreturn.get()), STBRmoas=int(self.startSTBRMOAS.get()), volInt=int(self.startVolumeInterval.get()), volCut=float(self.startVolumeCutoff.get()), volRet=float(self.startVolumeReturn.get()), volMOAS=int(self.startVolumeMOAS.get()), vioBuyInt=int(self.startViolenceBuyInterval.get()), vioBuyCut=float(self.startViolenceBuyThreshold.get()), vioBuyRet=float(self.startViolenceBuyReturn.get()), vioSellInt=int(self.startViolenceSellInterval.get()), vioSellCut=float(self.startViolenceSellThreshold.get()), vioSellRet=float(self.startViolenceSellReturn.get()), BTSRwindowLenForward=int(self.startBTSRwindowForwardLen.get()), BTSRwindowLenBack=int(self.startBTSRwindowBackLen.get()), reactToVioBuy=self.doWeReactBySelling.get(), reactToVioSell=self.doWeReactByBuying.get(), reactToVioBuyCut=float(self.startReactSellsCutoff.get()), reactToVioSellCut=float(self.startReactBuysCutoff.get()), reactToVioBuyForward=int(self.startReactSellsWindowLen.get()), reactToVioSellForward=int(self.startReactBuysWindowLen.get()), whichExchange=('Bitstamp' if self.whichExchange.get() else 'Bitfinex'), cheatBTSR=self.BTSRcheatVarEnabled.get(), cheatSTBR=self.STBRcheatVarEnabled.get(), cheatVioBuys=self.vioBuysCheatVarEnabled.get(), cheatVioSells=self.vioSellsCheatVarEnabled.get(), doWeShort=self.doWeShort.get())
    
            thoroughBegin += timeBetween
            thoroughEnd += timeBetween

        print('THOROUGH RUN FINISHED')
        #RESET THINGS BACK TO HOW THEY WERE
        self.tBegin.set(str(origBegin))
        self.tEnd.set(str(origEnd))
        self.getData()
        if(self.isPaused): 
            self.pauseRun(event)



    def thoroughButtonClick(self, event):
        if(not self.isPaused): 
            self.pauseRun(event)
            wasPaused = False
        else:
            wasPaused = True
        print('BEGINNING THOROUGH RUN')
        fp = open('thoroughminitialization.txt', 'a')
        fp.write(self.getVarString())
        fp.close()

        os.system('./thoroughButton.sh')

        print('THOROUGH RUN FINISHED')
        if(self.isPaused): 
            if(not wasPaused):
                self.pauseRun(event)





    def returnCurrVarValue(self, varNumber, mode='curr'):
                                            #'curr', 'init', 'dist'
        if(varNumber == 0):
            if(mode == 'init'):
                return int(self.BTSRinterval1.get())
            elif(mode == 'dist'):
                return int(self.BTSRinterval2.get())
            else:
                return int(self.startBTSRinterval.get())
        elif(varNumber == 1):
            if(mode == 'init'):
                return float(self.BTSRcutoff1.get())
            elif(mode == 'dist'):
                return float(self.BTSRcutoff2.get())
            else:
                return float(self.startBTSRcutoff.get())
        elif(varNumber == 2):
            if(mode == 'init'):
                return float(self.BTSRreturn1.get())
            elif(mode == 'dist'):
                return float(self.BTSRreturn2.get())
            else:
                return float(self.startBTSRreturn.get())
        elif(varNumber == 3):
            if(mode == 'init'):
                return int(self.BTSRMOAS1.get())
            elif(mode == 'dist'):
                return int(self.BTSRMOAS2.get())
            else:
                return int(self.startBTSRMOAS.get())
        elif(varNumber == 4):
            if(mode == 'init'):
                return int(self.STBRinterval1.get())
            elif(mode == 'dist'):
                return int(self.STBRinterval2.get())
            else:
                return int(self.startSTBRinterval.get())
        elif(varNumber == 5):
            if(mode == 'init'):
                return float(self.STBRcutoff1.get())
            elif(mode == 'dist'):
                return float(self.STBRcutoff2.get())
            else:
                return float(self.startSTBRcutoff.get())
        elif(varNumber == 6):
            if(mode == 'init'):
                return float(self.STBRreturn1.get())
            elif(mode == 'dist'):
                return float(self.STBRreturn2.get())
            else:
                return float(self.startSTBRreturn.get())
        elif(varNumber == 7):
            if(mode == 'init'):
                return int(self.STBRMOAS1.get())
            elif(mode == 'dist'):
                return int(self.STBRMOAS2.get())
            else:
                return int(self.startSTBRMOAS.get())
        elif(varNumber == 8):
            if(mode == 'init'):
                return int(self.VolumeInterval1.get())
            elif(mode == 'dist'):
                return int(self.VolumeInterval2.get())
            else:
                return int(self.startVolumeInterval.get())
        elif(varNumber == 9):
            if(mode == 'init'):
                return float(self.VolumeCutoff1.get())
            elif(mode == 'dist'):
                return float(self.VolumeCutoff2.get())
            else:
                return float(self.startVolumeCutoff.get())
        elif(varNumber == 10):
            if(mode == 'init'):
                return float(self.VolumeReturn1.get())
            elif(mode == 'dist'):
                return float(self.VolumeReturn2.get())
            else:
                return float(self.startVolumeReturn.get())
        elif(varNumber == 11):
            if(mode == 'init'):
                return int(self.VolumeMOAS1.get())
            elif(mode == 'dist'):
                return int(self.VolumeMOAS2.get())
            else:
                return int(self.startVolumeMOAS.get())
        elif(varNumber == 12):
            if(mode == 'init'):
                return int(self.ViolenceBuyInterval1.get())
            elif(mode == 'dist'):
                return int(self.ViolenceBuyInterval2.get())
            else:
                return int(self.startViolenceBuyInterval.get())
        elif(varNumber == 13):
            if(mode == 'init'):
                return float(self.ViolenceBuyThreshold1.get())
            elif(mode == 'dist'):
                return float(self.ViolenceBuyThreshold2.get())
            else:
                return float(self.startViolenceBuyThreshold.get())
        elif(varNumber == 14):
            if(mode == 'init'):
                return float(self.ViolenceBuyReturn1.get())
            elif(mode == 'dist'):
                return float(self.ViolenceBuyReturn2.get())
            else:
                return float(self.startViolenceBuyReturn.get())
        elif(varNumber == 15):
            if(mode == 'init'):
                return int(self.ViolenceSellInterval1.get())
            elif(mode == 'dist'):
                return int(self.ViolenceSellInterval2.get())
            else:
                return int(self.startViolenceSellInterval.get())
        elif(varNumber == 16):
            if(mode == 'init'):
                return float(self.ViolenceSellThreshold1.get())
            elif(mode == 'dist'):
                return float(self.ViolenceSellThreshold2.get())
            else:
                return float(self.startViolenceSellThreshold.get())
        elif(varNumber == 17):
            if(mode == 'init'):
                return float(self.ViolenceSellReturn1.get())
            elif(mode == 'dist'):
                return float(self.ViolenceSellReturn2.get())
            else:
                return float(self.startViolenceSellReturn.get())
        elif(varNumber == 18):
            if(mode == 'init'):
                return int(self.BTSRwindowForwardLen1.get())
            elif(mode == 'dist'):
                return int(self.BTSRwindowForwardLen2.get())
            else:
                return int(self.startBTSRwindowForwardLen.get())
        elif(varNumber == 19):
            if(mode == 'init'):
                return int(self.BTSRwindowBackLen1.get())
            elif(mode == 'dist'):
                return int(self.BTSRwindowBackLen2.get())
            else:
                return int(self.startBTSRwindowBackLen.get())
        elif(varNumber == 20):
            if(mode == 'init'):
                return float(self.reactSellsCutoff1.get())
            elif(mode == 'dist'):
                return float(self.reactSellsCutoff2.get())
            else:
                return float(self.startReactSellsCutoff.get())
        elif(varNumber == 21):
            if(mode == 'init'):
                return int(self.reactSellsWindowLen1.get())
            elif(mode == 'dist'):
                return int(self.reactSellsWindowLen2.get())
            else:
                return int(self.startReactSellsWindowLen.get())
        elif(varNumber == 22):
            if(mode == 'init'):
                return float(self.reactBuysCutoff1.get())
            elif(mode == 'dist'):
                return float(self.reactBuysCutoff2.get())
            else:
                return float(self.startReactBuysCutoff.get())
        elif(varNumber == 23):
            if(mode == 'init'):
                return int(self.reactBuysWindowLen1.get())
            elif(mode == 'dist'):
                return int(self.reactBuysWindowLen2.get())
            else:
                return int(self.startReactBuysWindowLen.get())


        


def buildArrays(ifile="data/bitfinex.csv", howFarBack=0, beginTime=1392786050, endTime=1393414657):# beginTime=None, endTime=None):
    btcDateArr=[]
    btcPriceArr=[]
    btcVolumeArr=[]
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

def run_as_process(func, *args):
    p = multiprocessing.Process(target=func, args=args)
    try:
        p.start()
        p.join()
    finally:
        p.terminate()

def return_with_process(func, *args):
    q = multiprocessing.Queue()
    g = list(args)
    g.append(q)
    p = multiprocessing.Process(target=func, args=g)
    try:
        p.start()
        p.join()
        return q.get(timeout=250)
    finally:
        p.terminate()


def run_as_thread(func, *args):
    t = threading.Thread(target = func, args=args)
    t.start()


def minitialize(minitfile):
    global variablesArr
    try:
        rawData = open(minitfile, 'r').read()
        try:
            rawDataLines = rawData.split('\n'); del rawDataLines[-1]

            #singleLine = random.choice(rawDataLines)
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
                    if(topLevelVal == 24): #73
                        variablesArr.append(str(values[valIdx])) #dataFile
                    if(topLevelVal == 25): #74
                        variablesArr.append(str2bool(values[valIdx])) #doWeReactBySelling
                    if(topLevelVal == 26): #75
                        variablesArr.append(str2bool(values[valIdx])) #doWeReactByBuying
                    if(topLevelVal == 27): #76 
                        variablesArr.append(str2bool(values[valIdx])) #doWeCheatBTSR
                    if(topLevelVal == 28): #77
                        variablesArr.append(str2bool(values[valIdx])) #doWeCheatSTBR
                    if(topLevelVal == 29): #78
                        variablesArr.append(str2bool(values[valIdx])) #doWeCheatVioBuys
                    if(topLevelVal == 30): #79
                        variablesArr.append(str2bool(values[valIdx])) #doWeCheatVioSells
                    if(topLevelVal == 31): #80
                        variablesArr.append(str2bool(values[valIdx])) #doWeShort
                    valIdx += 1



            if(len(variablesArr) > 0):
                nonEmptiness = True
            else:
                print("Empty minitialize array - no data in array")
                sys.exit()

            #print(variablesArr)

        except Exception as e:
            print('failed raw minit', str(e))
            sys.exit()
            

    except Exception as e:
        print('failed to even open the minit file...', str(e))
        sys.exit()




class Logger(object):
    def __init__(self, outFile):
        self.terminal = sys.stdout
        self.log = open(outFile, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def runrunrun(app):
    i = 0.01
    while(i < 0.09):
        app.myTester.changeViolenceSellThreshold(i)
        i += 0.005

    app.myTester.changeViolenceSellThreshold(i)
    j = 100
    while(j < 2000):
        app.myTester.changeBTSRinterval(j)
        j += 100


if __name__ == "__main__":

    minitialize('minitialization.txt')

    myapp = MyApp()
  
    time.sleep(6)
    while(True):
        if(not myapp.isPaused):
            varToTestWith = int(myapp.startNextTestVar.get())
            myapp.startCurrentTestVar.set(varToTestWith)
            myMinion = Minion(app=myapp, whichVar=varToTestWith, currVal=myapp.returnCurrVarValue(varToTestWith), startVal=myapp.returnCurrVarValue(varToTestWith, mode='init'), distance=myapp.returnCurrVarValue(varToTestWith, mode='dist'))
            try:
                weGotBack = return_with_process(myMinion.maximizeReturnQueue)
                myapp.updateVarEntry(weGotBack[0], weGotBack[1], weGotBack[2], weGotBack[3])
            except Exception as e:
                print('problem with return')
            time.sleep(1)
            myapp.startNextTestVar.set(myapp.diceRoll())
        else:
            time.sleep(1)
    

