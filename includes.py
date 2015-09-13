import time, datetime
import numpy as np
import pandas as pd
import smtplib, os
import math
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

def prettifyDate(d):
    return datetime.datetime.fromtimestamp(int(d)).strftime('%m/%d/%y')


def longPrettifyDate(d):
    return datetime.datetime.fromtimestamp(int(d)).strftime('%m/%d/%y (%H:%M)')


def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[:-(N-1)]
def runningMeanP(x, N):
    return pd.stats.moments.rolling_mean(pd.Series(x), N)

def combineLists(a = [], b = [], verbose=False, atitle='', btitle=''):
    if(verbose):
        print(atitle, ':', sorted(list(set(a).difference(set(b)))))
        print(btitle, ':', sorted(list(set(b).difference(set(a)))))
        print(atitle, '&', btitle, ':', sorted(list(set(a).union(set(b)))))

    return sorted(list(set(a) | set(b)))



def helperCombiner(upArr = [], downArr = []):
    lenup = len(upArr)
    lendown = len(downArr)
    resultArr = np.zeros(lenup, dtype=bool)
    canAdd = True
    for idx, (upTrue, downTrue) in enumerate(zip(upArr, downArr)):
        if(canAdd):
            if(upTrue):
                resultArr[idx] = True
                canAdd = False
        else:
            if(downTrue):
                canAdd = True
    return resultArr

def booleanDates(boolArr = [], thisSecond = 0):
    resultArr = []
    for truthVal in boolArr:
        if(truthVal):
            resultArr.append(thisSecond)
        thisSecond += 1
    return resultArr


def precisePeriodSum(inpArr = [], interval=60):
    resultArr = []
    for inp in range(len(inpArr)):
        if(inp < interval):
            if(inp == 0):
                resultArr.append(inpArr[inp])
            else:
                resultArr.append(inpArr[inp] + resultArr[inp-1])
        else:
            resultArr.append((inpArr[int(inp)] + resultArr[int(inp)-1] - inpArr[int(inp) - int(interval)]))
    return resultArr


def twoThreshMark(inpArr = [], threshold = 1.0, bounceThresh = 0.1, dateMarks = []):
    resultArr = []
    canMark = True
    for i, val in enumerate(inpArr):
        if(canMark):
            if(val > threshold):
                resultArr.append(dateMarks[i])
                canMark = False
        elif(val < bounceThresh):
            canMark = True
    return resultArr

def antiTwoThreshMark(inpArr = [], threshold = -1.0, bounceThresh = -0.1, dateMarks = []):
    resultArr = []
    canMark = True
    for i, val in enumerate(inpArr):
        if(canMark):
            if(val < threshold):
                resultArr.append(dateMarks[i])
                canMark = False
        elif(val > bounceThresh):
            canMark = True
    return resultArr



def windowFilter(triggerArr = [], filterArr = [], forwardWindow = 200, backWindow = 0):
    lf = len(filterArr)
    lt = len(triggerArr)
    filtidx = 0
    trigidx = 0
    resultArr = []
    while(filtidx < lf and trigidx < lt):
        if(triggerArr[trigidx] < filterArr[filtidx]):
            #we have a trigger, look FORWARD for filter to finish the combo
            if(filterArr[filtidx] <= (triggerArr[trigidx] + forwardWindow)):
                #add that sucka, and let's plod ever-onward!
                resultArr.append(filterArr[filtidx])
                #catch our trigs up now
                while(trigidx < lt and triggerArr[trigidx] <= filterArr[filtidx]):
                    trigidx += 1
                filtidx += 1
            else:
                trigidx += 1
        elif(filterArr[filtidx] < triggerArr[trigidx]):
            if(triggerArr[trigidx] <= (filterArr[filtidx] + backWindow)):
                resultArr.append(triggerArr[trigidx])
                while(filtidx < lf and filterArr[filtidx] <= triggerArr[trigidx]):
                    filtidx += 1
                trigidx += 1
            else:
                filtidx += 1
        else:
            #they're both equal, so just add them and increment both
            resultArr.append(filterArr[filtidx])
            filtidx += 1
            trigidx += 1
    return resultArr

def isBuy(priceArr = [], x = 0):
    if(x <= 0):
        return True
    elif(priceArr[x] > priceArr[x-1]):
        return True
    elif(priceArr[x] < priceArr[x-1]):
        return False
    else:
        return isBuy(priceArr, (x-1))

def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1")

def whichList(a = [], b = []): #returns array of length 3... [0] = in first list (but not second), [1] = in second list (but not first), [2] = both
    resultArr = []

    resultArr.append(sorted(list(set(a).difference(set(b)))))
    resultArr.append(sorted(list(set(b).difference(set(a)))))
    resultArr.append(sorted(list(set(a).union(set(b)))))

    return resultArr


def make_format(current, other):
    # current and other are axes
    def format_coord(x, y):
        # x, y are data coordinates
        # convert to display coords
        display_coord = current.transData.transform((x,y))
        inv = other.transData.inverted()
        # convert back to data coords with respect to ax
        ax_coord = inv.transform(display_coord)
        coords = [ax_coord, (x, y)]
        return ('Left: {:<40}    Right: {:<}'
                .format(*['({:.0f}, {:.2f})'.format(x, y) for x,y in coords]))
    return format_coord



def mailer(inputfile):
    SERVER = "localhost"

    FROM = "hannemennah@example.com"
    TO = "hannemennah@gmail.com" # must be a list

    SUBJECT = "Superminion Results"

    TEXT = "This message was generated on " + str(datetime.datetime.now())

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = SUBJECT

    msg.attach( MIMEText(TEXT) )

    # Send the mail
    if(inputfile):
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(inputfile,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(inputfile)))
        msg.attach(part)

    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()



