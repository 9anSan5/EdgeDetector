import numpy as np
from PIL import Image
class MetricsFunction():

    @staticmethod
    def prattFigureMerit(groundTruth, edges):
        edges = Image.fromarray(edges)  
        Ea = np.array(groundTruth, dtype=np.double)
        Ed = np.array(edges, dtype=np.double)
        a = 0.111 # edge shift penalty constant;
        
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

        return F


    @staticmethod
    def evaluate(groundTruth, edges):
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for x in range(edges.shape[0]):
            for y in range(edges.shape[1]):
                e = edges[x,y]
                g = groundTruth.getpixel((y,x))
                if e != 0 and g == 255:
                    TP += 1
                elif e == 255 and g == 0:
                    FP += 1
                elif e == 0 and g == 0:
                    TN += 1
                elif e == 0 and g == 255:
                    FN += 1
        return TP, FP, TN, FN

    @staticmethod
    def mapQuality(groundTruth, edges):
        tp, fp, tn, fn = MetricsFunction.evaluate(groundTruth, edges)
        return tp, fp, tn, fn, tp/(tp+fn+fp)

    @staticmethod
    def meanAbsoluteError(groundTruth, edges):
        groundTruth = groundTruth.convert('L')
        return np.mean(np.abs(edges - groundTruth))