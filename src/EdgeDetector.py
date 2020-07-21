from abc import ABC, abstractmethod

class EdgeDetector(ABC):
    
    @abstractmethod
    def getEdges(self, image):
        pass