from enum import Enum

class IP(Enum):
    """IP version enum"""
    
    V4 = "IPv4"
    V6 = "IPv6"

    def __str__(self):
        return str(self.value)