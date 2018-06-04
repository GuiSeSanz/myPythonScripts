import os
import requests
import multiprocessing as mp


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class LNC(object):
    __metaclass__ = IterRegistry
    _registry = []
    def __init__(self, Name, Chromosome, Start, End):
        self._registry.append(self)
        self.Name = str(Name)
        self.Chromosome = Chromosome
        self.Start = Start
        self.End = End
    def setEnhancer(self, Boolean):
        self.Enhancer = bool(Boolean)
    def setBracketingGenes(self, genes):
        self.BracketingGenes = str(genes)
    def setEnhPosition(self, position):
        self.EnhPosition = str(position)




# namesFile = os.path.join(os.getcwd(), "Data", "ToGuillermoLNC.txt.csv")

# with open(namesFile, 'rb') as inFl:
#     lines = inFl.readlines()
# lncNames = map(lambda x: x.split(",")[2], lines)


coordFiles = os.path.join(os.getcwd(),"Data", "hglft_genome_1442_fa7c80.bed")
LNClist = []
inFl = open(coordFiles, 'rb')
counter = 0
for line in inFl:
    counter += 1
    spline = line.strip('\n').split('\t')
    LNClist.append(LNC(spline[3], spline[0] , spline[1] , spline[2] ))

inFl.close()
print "Parsed {} lines/Lnc genes".format(counter)



searchParameters = {'search.org' : 'Human' , 'keyword' : 'NONE', 'form' : 'searchGene', 'action' : 'search',  'experiment' : '1'}

def SearchFastAndFurious(lnc):
    humanPos = "NONE"
    mousePos = "NONE"
    humanGenes = "NONE"
    mouseGenes = "NONE"
    searchingPosition = str(lnc.Chromosome + ':' + lnc.Start + '-' + lnc.End).lower()
    # searchingPosition = "chr1:3000000-5000000"
    searchTerm = {'keyword': searchingPosition}
    searchParameters.update(searchTerm)
    r = requests.post("https://enhancer.lbl.gov/cgi-bin/imagedb3.pl?", data=searchParameters)
    print 'For {} i have {} sc'.format(lnc.Name, r.status_code)
    if r.status_code == 200:
        text = r.text.encode('ascii')
        positions = re.findall(r'(?<!chrom=)chr[0-9-:,]+', text)
        # positions = map(lambda x: x.encode('ascii'), positions)
        bracketGenes = re.findall(r'(?<=\t)[A-Za-z0-9-]{2,}-?[A-Za-z0-9()-]{2,}(?=\n)', text)
        # bracketGenes = map(lambda x: x.encode('ascii'), bracketGenes)
        if len(positions)!=0 or len(bracketGenes)!=0:
            print 'I have ONE!!!!    {}'.format(lnc.Name)
            humanPos = positions[0]
            # mousePos = positions[1]
            humanGenes = bracketGenes[0]
            # mouseGenes = bracketGenes[1]
            # line = '''=====================================\nLNC:: {}\nHumanPosition::{}\nHumanBracketGenes::{}\nMousePosition::{}\nMouseBracketGenes::{}\n'''.format(lnc, humanPos, humanGenes, mousePos, mouseGenes)
            lnc.setEnhancer(1)
            lnc.setBracketingGenes(humanGenes)
            lnc.setEnhPosition(humanPos)
            return lnc
        else:
            lnc.setEnhancer(0)
            return lnc

NewList = []
pool = mp.Pool(10)
NewList.extend(pool.map(SearchFastAndFurious, LNClist))
pool.close()
pool.join()

enhancers = filter(lambda x: x.Enhancer, NewList)

outFl = open(os.path.join(os.getcwd(), 'Data', 'VistaEnhancersOut.txt'), 'wb')
for lnc in enhancers:
    print lnc.Name
    outFl.write("============================\n")
    outFl.write("LNC with name:: {}\n".format(lnc.Name))
    outFl.write("At position:: {} in hg19\n".format(str(lnc.Chromosome + ':' + lnc.Start + '-' + lnc.End).lower()))
    outFl.write("The bracketing genes are:: {}\n".format(lnc.BracketingGenes))
    outFl.write("Enhacenment zone:: {}\n".format(lnc.EnhPosition))

outFl.close()
