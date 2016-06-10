import sys
import os

class DataGroup():
    def __init__(self):
        self.statesets = []

    def output(self, outdir):
        for ss in self.statesets:
            ss.output(outdir)

    def appendFile(self, afilename):
        with open(afilename, 'r') as ifile:
            sdict = {}
            onestate = ""
            statename = ""
            for line in ifile:
                if(line.startswith("DROPSTATE")):
                    if(len(statename) > 0):
                        if(not (statename in sdict)):
                            sdict[statename] = StateSet(statename)
                        s = State.buildFromString(onestate)
                        sdict[statename].states.append(s)
                    statename = line.split(":")[1]
                else:
                    onestate = onestate + line
            if(len(statename) > 0):
                if(not(statename in sdict)):
                    sdict[statename] = StateSet(statename)
                s = State.buildFromString(onestate)
                sdict[statename].states.append(s)

        for skey in sdict:
            found = False
            for ss in self.statesets:
                if(ss.name == skey):
                    found = True
                    ss.states = ss.states + sdict[skey].states
                    break
            if(not found):
                self.statesets.append(sdict[skey])

    def hashcopy(self):
        varsets = {}
        ret = DataGroup()
        for stateset in self.statesets:
            nss = StateSet(stateset.name)
            for state in stateset.states:
                nss.states.append(State())
                for varkey in state.vartable:
                    if not varkey in varsets:
                        varsets[varkey] = []
                    varval = state.vartable[varkey]
                    if not varval.value in varsets[varval.name]:
                        varsets[varval.name].append(varval.value)
            ret.statesets.append(nss)

        varkeys = list(varsets.keys())
        print(varkeys)

        for i in range(len(self.statesets)):
            for j in range(len(self.statesets[i].states)):
                for varkey in self.statesets[i].states[j].vartable:
                    baseval = self.statesets[i].states[j].vartable[varkey].value
                    ind = varsets[varkey].index(baseval)
                    hv = VarVal()
                    hv.name = self.statesets[i].states[j].vartable[varkey].name
                    hv.typ = self.statesets[i].states[j].vartable[varkey].typ
                    hv.value = str(ind)
                    ret.statesets[i].states[j].vartable[varkey] = hv
        return ret

class StateSet():
    def __init__(self, inname):
        self.name = inname
        self.states = []
    
    def output(self, outdir):
        print("output state:"+self.name)
        fname = outdir + self.name
        with open(fname, 'w') as ofile:
            kl = None
            for s in self.states:
                if(kl == None):
                    kl = s.vartable.keys()
                ofile.write(s.output(kl))

class State():
    def __init__(self):
        self.vartable = {}
        
    @staticmethod
    def buildFromString(strin):
        retval = State()
        vals = strin.split("\n")
        for val in vals:
            
            vs = val.split(",")
            if(val.startswith("DROPSTATE")):
                continue
            if(val.startswith("GLOBAL") or val.startswith("LOCAL")):
                v = VarVal()
                v.name = vs[0]
                v.typ = vs[1]
                v.value = vs[2]
                retval.vartable[v.name] = v
        return retval

    def output(self, kl):
        sval = ""
        for k in kl:
            sval = sval + str(self.vartable[k].value) + " "
        return sval[:-1] + "\n"

class VarVal():
    def __init__(self):
        self.name = ""
        self.typ = ""
        self.value = ""

def getOutFile(infilename, outfiledir):
    lastslashind = infilename.rfind("/")
    ifname = infilename[lastslashind+1:]
    ifname = outfiledir+"parsed_"+ifname
    return ifname

infiledir = sys.argv[1]
outfiledir = sys.argv[2]

dg = DataGroup()
for infilename in os.listdir(infiledir):

    infilename = infiledir + infilename
    dg.appendFile(infilename)

hdg = dg.hashcopy()
hdg.output(outfiledir)
