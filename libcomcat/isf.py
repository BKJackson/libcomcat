#!/usr/bin/env python

#stdlib imports
from xml.dom.minidom import parseString
import sys
import datetime
import math

#third party imports
import numpy as np
from pagerio import fixed

ORIGINHDR = [((4,7),'a4'),
             ((15,18),'a4'),
             ((27,29),'a3'),
             ((33,35),'a3'),
             ((37,44),'a8'),
             ((46,54),'a9'),
             ((57,60),'a4'),
             ((63,66),'a4'),
             ((69,70),'a2'),
             ((72,76),'a5'),
             ((80,82),'a3'),
             ((84,87),'a4'),
             ((89,92),'a4'),
             ((94,96),'a3'),
             ((99,103),'a5'),
             ((106,110),'a5'),
             ((112,115),'a4'),
             ((119,124),'a6'),
             ((131,136),'a6')]

ORIGINFMT = [((1,4),'i4'),
          ((5,5),'a1'),
          ((6,7),'i2'),
          ((8,8),'a1'),
          ((9,10),'i2'),
          ((12,13),'i2'),
          ((14,14),'a1'),
          ((15,16),'i2'),
          ((17,17),'a1'),
          ((18,22),'f5.2'),
          ((23,23),'a1'),
          ((25,29),'f5.2'),
          ((31,35),'f5.2'),
          ((37,44),'f8.4'),
          ((46,54),'f9.4'),
          ((55,55),'a1'),
          ((56,60),'f5.1'),
          ((62,66),'f5.1'),
          ((68,70),'i3'),
          ((72,76),'f5.1'),
          ((77,77),'a1'),
          ((79,82),'f4.1'),
          ((84,87),'i4'),
          ((89,92),'i4'),
          ((94,96),'i3'),
          ((98,103),'f6.2'),
          ((105,110),'f6.2'),
          ((112,112),'a1'),
          ((114,114),'a1'),
          ((116,117),'a2'),
          ((119,127),'a9'),
          ((129,136),'a8')]

MAGHDR = [((1,9),'a9'),
          ((12,14),'a3'),
          ((16,19),'a4'),
          ((21,26),'a6'),
          ((33,38),'a6')]

MAGFMT = [((1,5),'a5'),
          ((6,6),'a1'),
          ((7,10),'f4.1'),
          ((12,14),'f3.1'),
          ((16,19),'i4'),
          ((21,29),'a9'),
          ((31,38),'a8')]
           

PHASEHDR = [((1,3),'a3'),
            ((9,12),'a4'),
            ((15,18),'a4'),
            ((20,24),'a5'),
            ((33,36),'a4'),
            ((43,46),'a4'),
            ((49,52),'a4'),
            ((54,58),'a5'),
            ((62,65),'a4'),
            ((69,72),'a4'),
            ((74,76),'a3'),
            ((80,82),'a3'),
            ((90,92),'a3'),
            ((96,98),'a3'),
            ((100,103),'a4'),
            ((105,113),'a9'),
            ((118,122),'a5')]

PHASELBL = ['Sta','Dist','EvAz','Phase','Time','TRes','Azim','AzRes','Slow',
            'SRes','Def','SNR','Amp','Per','Qual','Magnitude','ArrID']

PHASEFMT = [((1,5),'a5'),
            ((7,12),'f6.2'),
            ((14,18),'f5.1'),
            ((20,27),'a8'),
            ((29,30),'i2'),
            ((31,31),'a1'),
            ((32,33),'i2'),
            ((34,34),'a1'),
            ((35,40),'f6.3'),
            ((42,46),'f5.1'),
            ((48,52),'f5.1'),
            ((54,58),'f5.1'),
            ((60,64),'f5.1'),
            ((67,71),'f5.1'),
            ((74,74),'a1'),
            ((75,75),'a1'),
            ((76,76),'a1'),
            ((78,82),'f5.1'),
            ((84,92),'f9.1'),
            ((94,98),'f5.2'),
            ((100,100),'a1'),
            ((101,101),'a1'),
            ((102,102),'a1'),
            ((104,108),'a5'),
            ((109,109),'a1'),
            ((110,113),'f4.1'),
            ((115,122),'a8')]

MOMENTHDR1 = [((2,2),'a1'), #(
              ((3,10),'a8'), #MOMTENS
              ((12,13),'a2'), #sc
              ((18,19),'a2'), #M0
              ((21,25),'a5'), #fCLVD
              ((30,32),'a3'), #MRR
              ((37,39),'a3'), #MTT
              ((44,46),'a3'), #MPP
              ((51,53),'a3'), #MRT
              ((58,60),'a3'), #MTP
              ((65,67),'a3'), #MPR
              ((69,72),'a4'), #NST1
              ((74,77),'a4'), #NST2
              ((79,84),'a6')] #Author

MOMENTLBL1 = ['(','#MOMTENS','sc','M0','fCLVD','MRR','MTT','MPP',
              'MRT','MTP','MPR','NST1','NST2','Author']

MOMENTHDR2 = [((2,2),'a1'),
              ((3,3),'a1'),
              ((17,19),'a3'),
              ((21,25),'a5'),
              ((30,32),'a3'),
              ((37,39),'a3'),
              ((44,46),'a3'),
              ((51,53),'a3'),
              ((58,60),'a3'),
              ((65,67),'a3'),
              ((69,72),'a4'),
              ((74,77),'a4'),
              ((79,86),'a8')]

MOMENTLBL2 = ['(','#','eM0','eCLVD','eRR','eTT','ePP',
              'eRT','eTP','ePR','NCO1','NCO2','Duration']

MOMENTFMT1 = [((2,2),'a1'),
              ((3,3),'a1'),
              ((12,13),'i2'),
              ((15,19),'f5.3'),
              ((21,25),'f5.3'),
              ((27,32),'f6.3'),
              ((34,39),'f6.3'),
              ((41,46),'f6.3'),
              ((48,53),'f6.3'),
              ((55,60),'f6.3'),
              ((62,67),'f6.3'),
              ((69,72),'i4'),
              ((74,77),'i4'),
              ((79,87),'a9')]

MOMENTFMT2 = [((2,2),'a1'),
              ((3,3),'a1'),
              ((15,19),'f5.3'),
              ((21,25),'f5.3'),
              ((27,32),'f6.3'),
              ((34,39),'f6.3'),
              ((41,46),'f6.3'),
              ((48,53),'f6.3'),
              ((55,60),'f6.3'),
              ((62,67),'f6.3'),
              ((69,72),'i4'),
              ((74,77),'i4'),
              ((79,86),'f8.2')]

def readQuakeML(quakemlfile):
    data = open(quakemlfile,'rt').read()
    return readQuakeMLData(data)

def getNSCL(waveform):
    nc = waveform.getAttribute('networkCode')
    sta = waveform.getAttribute('stationCode')
    comp = waveform.getAttribute('channelCode')
    loc = waveform.getAttribute('locationCode')
    REPL = '--'
    if nc == '':
        nc = REPL
    if sta == '':
        sta = REPL
    if comp == '':
        comp = REPL
    if loc == '':
        loc = REPL
    nscl = '%s.%s.%s.%s' % (nc,sta,comp,loc)
    return nscl
    
def getStationInfo(origin,event):
    arrivals = origin.getElementsByTagName('arrival')
    stations = []
    mindist = 99999999999999
    maxdist = -99999999999999
    for arrival in arrivals:
        arrid = arrival.getElementsByTagName('pickID')[0].firstChild.data
        picks = event.getElementsByTagName('pick')
        station = None
        for pick in picks:
            pickid = pick.getAttribute('publicID')
            if pickid == arrid:
                station = getNSCL(pick.getElementsByTagName('waveformID')[0])
                break
        if station is None:
            continue
        if station not in stations:
            stations.append(station)
        adist = float(arrival.getElementsByTagName('distance')[0].firstChild.data)
        if adist < mindist:
            mindist = adist
        if adist > maxdist:
            maxdist = adist
    return (len(stations),mindist,maxdist)

def getOrigin(origin,event):
    originid = origin.getAttribute('catalog:eventid')
    timestr = origin.getElementsByTagName('time')[0].getElementsByTagName('value')[0].firstChild.data
    timestr = timestr.rstrip('Z')
    timeel = origin.getElementsByTagName('time')[0]
    if len(timeel.getElementsByTagName('uncertainty')):
        errortime = float(timeel.getElementsByTagName('uncertainty')[0].firstChild.data)
    else:
        errortime = float('nan')
    if len(timestr) > 19:
        time = datetime.datetime.strptime(timestr,'%Y-%m-%dT%H:%M:%S.%f')
    else:
        time = datetime.datetime.strptime(timestr,'%Y-%m-%dT%H:%M:%S')
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    second = float(time.second) + float(time.microsecond)/1e6
    lat = float(origin.getElementsByTagName('latitude')[0].getElementsByTagName('value')[0].firstChild.data)
    lon = float(origin.getElementsByTagName('longitude')[0].getElementsByTagName('value')[0].firstChild.data)
    depth = float(origin.getElementsByTagName('depth')[0].getElementsByTagName('value')[0].firstChild.data)/1000.0
    depthel = origin.getElementsByTagName('depth')[0]
    if len(depthel.getElementsByTagName('uncertainty')):
        deptherr = float(depthel.getElementsByTagName('uncertainty')[0].firstChild.data)/1000.0
    else:
        deptherr = float('nan')
    if len(origin.getElementsByTagName('quality')):
        rms = float(origin.getElementsByTagName('quality')[0].getElementsByTagName('standardError')[0].firstChild.data)
        if len(origin.getElementsByTagName('quality')[0].getElementsByTagName('usedPhaseCount')):
            ndef = int(origin.getElementsByTagName('quality')[0].getElementsByTagName('usedPhaseCount')[0].firstChild.data)
        else:
            ndef = float('nan')
        azgap = float(origin.getElementsByTagName('quality')[0].getElementsByTagName('azimuthalGap')[0].firstChild.data)
    else:
        rms = float('nan')
        ndef = float('nan')
        azgap = float('nan')
    
    nst,mindist,maxdist = getStationInfo(origin,event)
    
    timefixed = ' '
    epifixed = ' '
    depthfixed = ' '
    if len(origin.getElementsByTagName('creationInfo')):
        author = origin.getElementsByTagName('creationInfo')[0].getElementsByTagName('agencyID')[0].firstChild.data.upper()
    else:
        author = ''
    if len(origin.getElementsByTagName('evaluationMode')):
        status = origin.getElementsByTagName('evaluationMode')[0].firstChild.data
    else:
        status = 'automatic'
    if status == 'manual':
        status = 'm'
    else:
        status = 'a'
    locmethod = 'i'
    if len(origin.getElementsByTagName('type')):
        event_type = origin.getElementsByTagName('type')[0].firstChild.data
    else:
        event_type = 'earthquake'

    if event_type == 'earthquake':
        event_type = 'ke'
    else:
        event_type = 'se'
    smaj = float('nan')
    smin = float('nan')
    az = 0
    orig = {'time':time,'year':year,'month':month,'day':day,'hour':hour,'minute':minute,'second':second,'timefixed':timefixed,
            'time_error':errortime,'timerms':rms,'lat':lat,'lon':lon,'epifixed':epifixed,'semimajor':smaj,
            'semiminor':smin,'errorazimuth':az,'depth':depth,'depthfixed':depthfixed,'deptherr':deptherr,
            'numphases':ndef,'numstations':nst,'azgap':azgap,'mindist':mindist,'maxdist':maxdist,
            'analysistype':status,'locmethod':locmethod,'event_type':event_type,'author':author,'originid':originid}
    return orig

def getPhase(pick,origin,event):
    phase = {}
    waveform = pick.getElementsByTagName('waveformID')[0]
    nc = waveform.getAttribute('networkCode')
    sta = waveform.getAttribute('stationCode')
    comp = waveform.getAttribute('channelCode')
    loc = waveform.getAttribute('locationCode')
    nscl = '%s.%s.%s.%s' % (nc,sta,comp,loc)
    pickid = pick.getAttribute('publicID')
    dist = None
    azimuth = None
    ptype = None
    ptimestr = (pick.getElementsByTagName('time')[0].getElementsByTagName('value')[0].firstChild.data)
    ptimestr = ptimestr.rstrip('Z')
    if len(ptimestr) > 19:
        ptime = datetime.datetime.strptime(ptimestr,'%Y-%m-%dT%H:%M:%S.%f')
    else:
        ptime = datetime.datetime.strptime(ptimestr,'%Y-%m-%dT%H:%M:%S')
    ptres = None
    picktype = None
    for arrival in origin.getElementsByTagName('arrival'):
        arrid = arrival.getElementsByTagName('pickID')[0].firstChild.data
        if arrid == pickid:
            dist = float(arrival.getElementsByTagName('distance')[0].firstChild.data)
            azimuth = float(arrival.getElementsByTagName('azimuth')[0].firstChild.data)
            ptype = arrival.getElementsByTagName('phase')[0].firstChild.data
            ptres = float(arrival.getElementsByTagName('timeResidual')[0].firstChild.data)
            if len(arrival.getElementsByTagName('creationInfo')):
                authors = arrival.getElementsByTagName('creationInfo')[0].getElementsByTagName('author')
                if len(authors):
                    try:
                        picktype = authors[0].firstChild.data
                        if picktype == 'manual':
                            picktype = 'm'
                        else:
                            picktype = 'a'
                    except:
                        pass
                else:
                    picktype = 'a'
                break
            else:
                picktype = 'a'
    if ptres is None:
        return None
    amp = None
    period = None
    phasemag = None
    for amplitude in event.getElementsByTagName('amplitude'):
        ampid = amplitude.getElementsByTagName('waveformID')
        nc = waveform.getAttribute('networkCode')
        sta = waveform.getAttribute('stationCode')
        comp = waveform.getAttribute('channelCode')
        loc = waveform.getAttribute('locationCode')
        amp_nscl = '%s.%s.%s.%s' % (nc,sta,comp,loc)
        if amp_nscl == nscl:
            amp = float(amplitude.getElementsByTagName('genericAmplitude')[0].getElementsByTagName('value')[0].firstChild.data)
            period = float(amplitude.getElementsByTagName('period')[0].getElementsByTagName('value')[0].firstChild.data)
            magtype = amplitude.getElementsByTagName('magnitudeHint')[0].firstChild.data
            break
    if not len(event.getElementsByTagName('amplitude')):
        amp = float('nan')
        period = float('nan')
        magtype = ' '
    phase['stationcode'] = sta
    phase['stationdist'] = dist
    phase['stationaz'] = azimuth
    phase['phasecode'] = ptype
    phase['time'] = ptime
    phase['hour'] = ptime.hour
    phase['minute'] = ptime.minute
    phase['second'] = float(ptime.second) + float(ptime.microsecond)/1000000.0
    phase['timeres'] = ptres
    phase['azimuth'] = azimuth
    phase['azres'] = float('nan')
    phase['slowness'] = float('nan')
    phase['slowres'] = float('nan')
    phase['timeflag'] = '_'
    phase['azflag'] = '_'
    phase['slowflag'] = '_'
    phase['snr'] = float('nan')
    phase['amplitude'] = amp
    phase['period'] = period
    phase['picktype'] = picktype
    phase['direction'] = '_'
    phase['quality'] = '_'
    phase['magtype'] = magtype
    phase['minmax'] = ' '
    phase['mag'] = float('nan')
    phase['arrid'] = ' '
    return phase    

def getMomentTensor(momentTensor):
    mdict = {}
    m0 = float(momentTensor.getElementsByTagName('scalarMoment')[0].getElementsByTagName('value')[0].firstChild.data)
    exponent = math.floor(math.log10(m0))
    scalarMoment = m0/math.pow(10,exponent)
    if fclvd > 1:
        fclvd = float(momentTensor.getElementsByTagName('clvd')[0].firstChild.data)/100.0
    else:
        fclvd = float(momentTensor.getElementsByTagName('clvd')[0].firstChild.data)
    tensor = momentTensor.getElementsByTagName('tensor')[0]
    mrr = float(tensor.getElementsByTagName('Mrr')[0].getElementsByTagName('value')[0].firstChild.data)/math.pow(10,exponent)
    mtt = float(tensor.getElementsByTagName('Mtt')[0].getElementsByTagName('value')[0].firstChild.data)/math.pow(10,exponent)
    mpp = float(tensor.getElementsByTagName('Mpp')[0].getElementsByTagName('value')[0].firstChild.data)/math.pow(10,exponent)
    mrt = float(tensor.getElementsByTagName('Mrt')[0].getElementsByTagName('value')[0].firstChild.data)/math.pow(10,exponent)
    mrp = float(tensor.getElementsByTagName('Mrp')[0].getElementsByTagName('value')[0].firstChild.data)/math.pow(10,exponent)
    mtp = float(tensor.getElementsByTagName('Mtp')[0].getElementsByTagName('value')[0].firstChild.data)/math.pow(10,exponent)

    nbodystations = 0
    nsurfacestations = 0
    
    momenterror = float('nan')
    clvderror = float('nan')
    errormrr = float('nan')/math.pow(10,exponent)
    errormtt = float('nan')/math.pow(10,exponent)
    errormpp = float('nan')/math.pow(10,exponent)
    errormrp = float('nan')/math.pow(10,exponent)
    errormrt = float('nan')/math.pow(10,exponent)
    errormtp = float('nan')/math.pow(10,exponent)

    #find the number of components used
    if len(momentTensor.getElementsByTagName('dataUsed')):
        data_used = momentTensor.getElementsByTagName('dataUsed')[0]
        wavetype = data_used.getElementsByTagName('waveType')[0].firstChild.data

        if wavetype == 'body waves':
            nsurface = 0
            nbody = int(data_used.getElementsByTagName('componentCount')[0].firstChild.data)
        else:
            nbody = 0
            nsurface = int(data_used.getElementsByTagName('componentCount')[0].firstChild.data)
    else:
        nsurface = float('nan')
        nbody = float('nan')

    #Get the duration, if provided
    sourcetimelist = momentTensor.getElementsByTagName('sourceTimeFunction')
    if len(sourcetimelist):
        duration = float(sourcetimelist[0].getElementsByTagName('duration')[0].firstChild.data)
    else:
        duration = float('nan')

    #get the author
    if len(momentTensor.getElementsByTagName('creationInfo')):
        author = momentTensor.getElementsByTagName('creationInfo')[0].getElementsByTagName('agencyID')[0].firstChild.data
    else:
        author = ''
        
    mdict = {'m0':m0,'exponent':exponent,'scalarmoment':scalarMoment,'fclvd':fclvd,
             'mrr':mrr,'mtt':mtt,'mpp':mpp,'mrt':mrt,'mrp':mrp,'mtp':mtp,
             'nbodystations':nbodystations,'nsurfacestations':nsurfacestations,
             'momenterror':momenterror,'clvderror':clvderror,
             'errormrr':errormrr,'errormtt':errormtt,'errormpp':errormpp,
             'errormrt':errormrt,'errormrp':errormrp,'errormtp':errormtp,
             'nbody':nbody,'nsurface':nsurface,'duration':duration,'author':author}
    return mdict
    
def getMagnitude(magnitude):
    mag = float(magnitude.getElementsByTagName('mag')[0].getElementsByTagName('value')[0].firstChild.data)
    if len(magnitude.getElementsByTagName('mag')[0].getElementsByTagName('uncertainty')):
        magerr = float(magnitude.getElementsByTagName('mag')[0].getElementsByTagName('uncertainty')[0].firstChild.data)
    else:
        magerr = float('nan')
    if len(magnitude.getElementsByTagName('mag')[0].getElementsByTagName('stationCount')):
        nstations = int(magnitude.getElementsByTagName('mag')[0].getElementsByTagName('stationCount'))
    else:
        nstations = float('nan')
    try:
        author = magnitude.getElementsByTagName('creationInfo')[0].getElementsByTagName('author')[0].firstChild.data
    except:
        author = ''
    mtype = magnitude.getElementsByTagName('type')[0].firstChild.data
    magdict = {}
    magdict['mag'] = mag
    magdict['magtype'] = mtype
    magdict['magerr'] = magerr
    magdict['nstations'] = nstations
    magdict['author'] = author
    magdict['magid'] = ''
    return magdict

def readQuakeMLData(data):
    dom = parseString(data)
    event = dom.getElementsByTagName('eventParameters')[0].getElementsByTagName('event')[0]
    originelements = event.getElementsByTagName('origin')
    eqdict = {}
    eqdict['eventcode'] = event.getAttribute('catalog:dataid')
    eqdict['location'] = ''
    eqdict['url'] = ''

    #fetch the origin elements
    origins = []
    for origin in originelements:
        orig = getOrigin(origin,event)
        origins.append(orig.copy())
    eqdict['origins'] = origins

    #fetch the magnitude elements
    magnitudes = event.getElementsByTagName('magnitude')
    maglist = []
    for magnitude in magnitudes: 
        magdict = getMagnitude(magnitude)
        maglist.append(magdict.copy())
    eqdict['magnitudes'] = maglist

    #get the moment tensors, if there are any
    momentTensors = []
    mechs = event.getElementsByTagName('focalMechanism')
    for mech in mechs:
        tensors = mech.getElementsByTagName('momentTensor')
        for tensor in tensors:
            mdict = getMomentTensor(tensor)
            momentTensors.append(mdict.copy())

    eqdict['tensors'] = momentTensors

    #get the phases
    picks = event.getElementsByTagName('pick')
    phases = []
    for pick in picks:
        phase = getPhase(pick,originelements[0],event)
        if phase is not None:
            phases.append(phase.copy())
    eqdict['phases'] = phases    
    
    dom.unlink()
    return eqdict

def renderISF(eqdict):
    #render ISF as a string
    isf = 'BEGIN IMS2.0\n'
    isf += 'MSG_TYPE DATA\n'
    isf += 'MSG_ID %s\n' % eqdict['eventcode'].upper()
    isf += 'DATA_TYPE BULLETIN IMS2.0:SHORT\n'
    if eqdict['origins'][0]['analysistype'] == 'm':
        isf += 'The following is a MANUALLY REVIEWED LOCATION from the USGS/NEIC National Seismic Network System\n'
    else:
        isf += 'The following is an AUTOMATICALLY REVIEWED LOCATION from the USGS/NEIC National Seismic Network System\n'
    isf += 'Event   %s %s\n\n' % (eqdict['eventcode'].upper(),eqdict['location'])

    #if there is a url field, render that as a comment.  This should help with QA/QC
    if eqdict['url']:
        isf += ' (%s)' % eqdict['url']
        isf += '\n\n'
    
    #render the origin block
    hdrvalues = ('Date','Time','Err','RMS','Latitude','Longitude',
               'Smaj','Smin','Az','Depth','Err','Ndef','Nst',
               'Gap','mdist','Mdist','Qual','Author','OrigID')
    line = fixed.getFixedFormatString(ORIGINHDR,hdrvalues)
    isf += line+'\n'

    for o in eqdict['origins']:
        vlist = [o['year'],'/',o['month'],'/',o['day'],
        o['hour'],':',o['minute'],':',o['second'],o['timefixed'],
        o['time_error'],o['timerms'],o['lat'],o['lon'],o['epifixed'],o['semimajor'],
        o['semiminor'],o['errorazimuth'],o['depth'],o['depthfixed'],o['deptherr'],
        o['numphases'],o['numstations'],o['azgap'],o['mindist'],o['maxdist'],
        o['analysistype'],o['locmethod'],o['event_type'],o['author'],o['originid']]
        line = fixed.getFixedFormatString(ORIGINFMT,vlist)
        isf += line+'\n'

    isf += '\n'
       
    #render the magnitude block
    line = fixed.getFixedFormatString(MAGHDR,['Magnitude','Err','Nsta','Author','OrigID'])
    isf += line + '\n'
    for m in eqdict['magnitudes']:
        vlist = [m['magtype'],' ',m['mag'],m['magerr'],m['nstations'],m['author'],m['magid']]
        line = fixed.getFixedFormatString(MAGFMT,vlist)
        isf += line+'\n'

    
        
    line = fixed.getFixedFormatString(PHASEHDR,PHASELBL)
    isf += line + '\n'
    for p in eqdict['phases']:
        vlist = [p['stationcode'],p['stationdist'],p['stationaz'],p['phasecode'],
                 p['hour'],':',p['minute'],':',p['second'],p['timeres'],
                 p['azimuth'],p['azres'],p['slowness'],p['slowres'],p['timeflag'],
                 p['azflag'],p['slowflag'],p['snr'],p['amplitude'],p['period'],
                 p['picktype'],p['direction'],p['quality'],p['magtype'],
                 p['minmax'],p['mag'],p['arrid']]
        line = fixed.getFixedFormatString(PHASEFMT,vlist)
        isf += line+'\n'

    isf += '\n'
    for m in eqdict['tensors']:
        line = fixed.getFixedFormatString(MOMENTHDR1,MOMENTLBL1)
        isf += line+'\n'
        line = fixed.getFixedFormatString(MOMENTHDR2,MOMENTLBL2)
        isf += line+'\n'
        vlist = ['(','#',m['exponent'],m['scalarmoment'],m['fclvd'],
                 m['mrr'],m['mtt'],m['mpp'],m['mrt'],m['mtp'],m['mrp'],
                 m['nbodystations'],m['nsurfacestations'],m['author']]
        line = fixed.getFixedFormatString(MOMENTFMT1,vlist)
        isf += line + '\n'
        vlist = ['(','#',m['momenterror'],m['clvderror'],
                 m['errormrr'],m['errormtt'],m['errormpp'],
                 m['errormrt'],m['errormrp'],m['errormtp'],
                 m['nbody'],m['nsurface'],m['duration']]
        line = fixed.getFixedFormatString(MOMENTFMT2,vlist)
        isf += line + '\n'
    isf += '\nSTOP\n'
    return isf

def quakemlToISF(quakemlfile,outfolder=None):
    eqdict = readQuakeML(quakemlfile)
    if outfolder is None:
        outfolder = os.cwd()
    fpath,ffile = os.path.split(quakemlfile)
    fname,fext = os.path.splitext(ffile)
    outfilename = os.path.join(outfolder,fname+'.isf')
    outfile = open(outfilename,'wt')
    isftext = renderISF(eqdict)
    outfile.write(isftext)
    outfile.close()
    
    

# def errcon(numphases,depthfixed,stderr,axes):
#     #    /********************************************************************************
#     # * errcon                                                                       *
#     # *                                                                              *
#     # * Errcon returns the principal axes for the two dimensional tangential error   *
#     # * ellipse. If depth is held fixed, the principal axes are unchanged. If        *
#     # * depth is free, the error matrix is reconstituted from the principal axes,    *
#     # * re-decomposed, and the two dimensional principal axes are recomputed.        *
#     # *                                                                              *
#     # * variables:                                                                   *
#     # * numphases - number of phases used                                            *
#     # * depthfixed - 1 for a free depth solution and >1 for a fixed depth solution.  *
#     # * stderr - standard error                                                      *
#     # * axes - principal axes of the error ellipse (3x3 matrix)                      *
#     # *  Note that axes[i][0] is the azimuth of the ith principal axis in degrees,   *
#     # *            axes[i][1] is the dip of the ith principal axis in degrees, and   *
#     # *            axes[i][2] is the length of the ith semi-axis in kilometers (at   *
#     # *                      the 90% confidence level)                               *
#     # *                                                                              *
#     # * Ported from FORTRAN code written by Ray Buland
#     # Re-ported to Python from C++ code written by Hydra team                        *
#     # *                                                                              *
#     # ********************************************************************************/
#     #/* initialize some values */
#     nFree = 8
#     tol   = 1.0e-15
#     tol2  = 2.0e-15
#     m     = 3
#     m1    = 2
#     m2    = 4

#     # /* Take care of the easy case (fixed depth). 
#     #  * Nothing to do; just return */
#     if depthfixed > 1:
#         return axes

#     a = np.zeros(m1,m1)
#     # /* Fisher F distribution */
#     s2  = (nFree + (n-m2)*se*se)/(nFree + n - m2)
#     f10,rc = Fisher10(m, nFree + n - m2)
#     if (not rc):
#         return rc
#     fac = 1.0/(m * s2 * f10);

# def fisher10(nu1, nu2):
#     xnu = np.array([1.0/30.0, 1.0/40.0, 1.0/60.0, 1.0/120.0, 0.0])
#     tab = np.array([49.50,  9.00,  5.46,  4.32,  3.78,  3.46,  3.26,  3.11,
#                          3.01,  2.92,  2.86,  2.81,  2.76,  2.73,  2.70,  2.67,
#                          2.64,  2.62,  2.61,  2.59,  2.57,  2.56,  2.55,  2.54,
#                          2.53,  2.52,  2.51,  2.50,  2.50,  2.49,  2.44,  2.39,
#                          2.35,  2.30, 53.59,  9.16,  5.39,  4.19,  3.62,  3.29, 
#                          3.07,  2.92,  2.81,  2.73,  2.66,  2.61,  2.56,  2.52, 
#                          2.49,  2.46,  2.44,  2.42,  2.40,  2.38,  2.36,  2.35, 
#                          2.34,  2.33,  2.32,  2.31,  2.30,  2.29,  2.28,  2.28, 
#                          2.23,  2.18,  2.13,  2.08, 55.83,  9.24,  5.34,  4.11, 
#                          3.52,  3.18,  2.96,  2.81,  2.69,  2.61,  2.54,  2.48, 
#                          2.43,  2.39,  2.36,  2.33,  2.31,  2.29,  2.27,  2.25, 
#                          2.23,  2.22,  2.21,  2.19,  2.18,  2.17,  2.17,  2.16, 
#                          2.15,  2.14,  2.09,  2.04,  1.99,  1.94};
#     return (rc,f10)
    
if __name__ == '__main__':
    eqdict = readQuakeML(sys.argv[1])
    isf = renderISF(eqdict)
    print isf
        
    
