from enum import Enum

class ResponseVersion(Enum):
    """Enum for CFDI response versions"""
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"
    V4 = "v4"
    
    def __str__(self):
        return self.value 