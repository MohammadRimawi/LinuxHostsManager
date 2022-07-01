class InvalidIPv4(Exception):
    """Exception raised when providing an invalid IPv4"""
    def __init__(self, ip):
        self.message = f'{ip} is not a valid IPv4'
    def __str__(self):
        return str(self.message)

class InvalidIPv6(Exception):
    """Exception raised when providing an invalid IPv6"""
    def __init__(self, ip):
        self.message = f'{ip} is not a valid IPv6'
    def __str__(self):
        return str(self.message)

class DuplicateHost(Exception):
    """Exception raised when providing an and already existing host with the same ip version"""
    def __init__(self, host_name,ip_version):
        self.message = f'The host name: "{host_name}" is already assigned to and existing {ip_version} address before!'
    def __str__(self):
        return str(self.message)

class HostDoesNotExists(Exception):
    """Exception raised when providing an and already existing host with the same ip version"""
    def __init__(self, host_name,ip_version,include_commented_hosts =False):
        self.message = f'The host with name: "{host_name}" with the ip version {ip_version} was not found in hosts{" or it is commented" if not include_commented_hosts else ""}!'
    def __str__(self):
        return str(self.message)
