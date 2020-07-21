import numpy as np
from PIL import Image
class MetricsFunction():

    @staticmethod
    def PrattFigureMerit(groundTruth, edges):
        edges = Image.fromarray(edges)  
        gt = groundTruth.convert('1')
        e = edges.convert('1')
        Ea = np.array(gt, dtype=np.double)
        Ed = np.array(e, dtype=np.double)
        (N,M) = Ea.shape
        if not (N,M) == Ed.shape:
            print('Actual and detected edge image sizes must be same')
            return
        a = 0.11 # edge shift penalty constant;
        
        fac = len(np.where((Ea-Ed) == -1)) #False Alarm Count
        msc = len(np.where((Ea-Ed) == 1))  #Miss Count

        Na = sum(sum(Ea))
        Nd = sum(sum(Ed))

        c = 1/max(Na,Nd)
        [ia,ja] = np.where(Ea == 1.0)
        Aes = []
        l = 0
        while l < Na:
            Aes.append(Ed[ia[l],ja[l]])
            l += 1
        mi = ia[np.argwhere(Aes == 0.0)]
        mj = ja[np.argwhere(Aes == 0.0)]

        F=c*sum(Aes)
        k = 0
        while k < len(mi):
            n1 = 0
            n2 = 0
            m1 = 0
            m2 = 0 
            while sum(sum(Ed[mi[k]-n1 : mi[k] + n2, mj[k] - m1 : mj[k] + m2])) < 1:
                if mi[k]-n1>1:
                    n1=n1+1
                if mi[k]+n2<N:
                    n2=n2+1
                if mj[k]-m1>1:
                    m1=m1+1
                if mj[k]+m2<M:
                    m2=m2+1 
            di=max([n1, n2, m1, m2])
            F=F+c/(1+a*di^2)

        #F = F*100
        return [F, fac, msc]


    @staticmethod
    def evaluate(groundTruth, edges):
        max_e = 255
        max_g = 255
        edges = Image.fromarray(edges.astype(np.uint8))
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for x in range(edges.size[0]):
            for y in range(edges.size[1]):
                e = edges.getpixel((x,y))
                g = groundTruth.getpixel((x,y))
                if e == max_e and g == max_g:
                    TP += 1
                elif e == max_e and g == 0:
                    FP += 1
                elif e == 0 and g == 0:
                    TN += 1
                elif e == 0 and g == max_g:
                    FN += 1
        return TP, FP, TN, FN

    @staticmethod
    def MeanAbsoluteError(groundTruth, edges):
        return np.mean(np.abs(edges - groundTruth))