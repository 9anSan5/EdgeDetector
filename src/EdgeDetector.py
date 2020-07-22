from abc import ABC, abstractmethod

class EdgeDetector(ABC):
    
    @abstractmethod
    def getEdges(self, image):
        pass
    
    @abstractmethod
    def getMask(self):
        pass
    
    @abstractmethod
    def getName(self):
        pass
    
    @abstractmethod
    def getThreshold(self):
        pass
