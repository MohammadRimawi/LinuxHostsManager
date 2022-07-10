from .main import read_hosts,update_host,write_hosts,list_lines,format_lines
from .ip_enum import IP

def update_host_interface(host_name,ip_version = IP.V4,host_ip:str = None, description:str = None):
    lines = read_hosts()

    update_host(lines, host_name,ip_version,host_ip, description)
    
    list_lines(lines)


    new_hosts = format_lines(lines)
    write_hosts(new_hosts)