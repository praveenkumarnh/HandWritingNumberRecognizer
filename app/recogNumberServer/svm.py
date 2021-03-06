import os
import math
import copy
from filterImage import ImageFilter

class Verify1:
    def __init__(self, verifynumber, samples):
        self.samples = samples
        self.number = verifynumber
        self.updateSampleLabel()
        self.a_param, self.b_param = self.loadParam()
    
    def updateSampleLabel(self):
        for sample in self.samples:
            if sample.num == self.number:
                sample.label = 1.0
            else:
                sample.label = -1.0

    def parse_file(self, path):
        data = []
        file = open(path, "r")
        for line in file.readlines():
            data.append(float(line))
        file.close()
        return data

    def loadParam(self):
        a_path = str(os.path.join(os.path.dirname(__file__), '../svmmodel/%d_a.model' % int(self.number)).replace('\\', '/'))
        b_path = str(os.path.join(os.path.dirname(__file__), '../svmmodel/%d_b.model' % int(self.number)).replace('\\', '/'))
        return self.parse_file(a_path), self.parse_file(b_path)

    def kernel(self, mj, mi):
        if mj == mi:
            return math.exp(0)
        dlt = 10
        ret = 0.0
        for i in range(len(mj.data)):
            for j in range(len(mj.data[i])):
                ret += math.pow(int(mj.data[i][j]) - int(mi.data[i][j]), 2)
        ret = math.exp(-ret/(2*dlt*dlt))
        return ret

    def predict(self, m):
        pred = 0.0
        for j in range(len(self.samples)):
            if self.a_param[j] != 0:
                pred += self.a_param[j] * self.samples[j].label * self.kernel(self.samples[j],m)
        pred += self.b_param[0]
        return pred

class Image:
    def __init__(self):
        self.data = []
        self.num = -1
        self.label = 0

def parse_image(path):
    img_map = []
    fp = open(path, "r") 
    for line in fp:
        #line = line[:-2]
        line = line[:-1]
        img_map.append(line)
    return img_map

def loaddata(dirpath):
    sampleList = []
    dirs = os.listdir(dirpath)
    for dir in dirs:
        files = os.listdir(dirpath + dir)
        for file in files:
            img = Image()
            img.data = parse_image(dirpath + dir + '/' + file)
            img.num = int(dir[0])
            sampleList.append(img)
    return sampleList

def loaddatasimple(dirpath, testnumber):
    sampleList = []
    files = os.listdir(dirpath)
    for file in files:
        img = Image()
        img.data = parse_image(dirpath + file)
        img.num = int(testnumber)
        sampleList.append(img)
    return sampleList

def svmdecision(targetdata):
    target = Image()
    target.data = targetdata

    source = str(os.path.join(os.path.dirname(__file__), '../semeionsamples/').replace('\\', '/'))
    sampleList = loaddata(source)
    verifyList = []
    for i in xrange(10):
        verify = Verify1(i, copy.deepcopy(sampleList))
        verifyList.append(verify)
    
    resultList = []
    for i in xrange(10):
        result = verifyList[i].predict(target)
        resultList.append(result)
        
    resultmax = max(resultList)
    decisionNumber = resultList.index(resultmax)
    if resultmax > 0:
        return decisionNumber
    else:
        print 'unknown'
        return decisionNumber

if __name__ == '__main__':
    imagesource = "../testsamples/cleantha.png"
    imagefilter = ImageFilter(imagesource)
    print svmdecision(imagefilter.getArrayNew())
