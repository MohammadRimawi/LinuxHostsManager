
from pprint import pprint
from re import sub
from exceptions import DuplicateHost, HostDoesNotExists, InvalidIPv4, InvalidIPv6
from ip_enum import IP
from regex_patterns import IPV4_PATTERN, IPV6_PATTERN

HOSTS_FILE = "hosts"

def is_valid_ipv4(ip:str) -> bool:
    """validates if valid ipv4 ip"""
    return bool(IPV4_PATTERN.search(ip))


def is_valid_ipv6(ip:str) -> bool:
    """validates if valid ipv6 ip"""
    return bool(IPV6_PATTERN.search(ip))


def validate_ip(ip:str) -> str:
    """validates if valid ipv4 or ipv6 ip and return empty string if neither"""
    ipv4 = IP.V4 if is_valid_ipv4(ip) else ""
    ipv6 = IP.V6 if is_valid_ipv6(ip) else ""
    return str(ipv4)+str(ipv6) 


def match_host(line,host_name,ip_version,include_disabled_hosts = False):
    """
    return true if host_name and ip_version are matched
    with the host name and ip version in the provided line
    """
    if "comment" in line.keys() : return False
    if not include_disabled_hosts and line["disabled"]:return False

    return line["host_name"].lower() == host_name.lower() and line["ip_version"] == str(ip_version)


def format_lines(lines:list) -> str:
    """formats the lines"""

    new_hosts = ""
    for line in lines:
        new_hosts += _format_line(line,new_line_comment = True)
    return new_hosts


def _format_line(line:dict,new_line_comment:bool = False) -> str:
    """formats a single line"""

    if "comment" in line.keys() : return ("\n"if new_line_comment else "") + f'# {line["comment"]}\n'
    else : return f'{("# " if line["disabled"] else "")+line["host_ip"]:<25}{line["host_name"]:<25}\t{("# " if line["description"] else "")}{line["description"]}\n'


def parse_line(line:dict) -> list:
    """returns host_ip, disabled,host_names,description,and None if not a valid host"""

    #>    # normal comment
    #>    0.0.0.0 abc 
    #>    0.0.0.0 abc # tailing comment
    #>    # 0.0.0.0 abc 
    #>    # 0.0.0.0 abc # tailing comment

    line = line.strip()

    disabled = line.startswith("#")
    
    line = line[1:].strip().split("#") if disabled else line.split("#")
    host = line[0].strip()
    description = line[1].strip() if len(line) == 2 else ""
    
    if host == "" : return [{'comment':line[0]}]
    host_ip,*host_names = host.split() 

    ip_version = validate_ip(host_ip)
    if ip_version != "":
        return  [{
                'host_ip':host_ip,
                'disabled':disabled,
                'host_name':host_name,
                'description':description,
                "ip_version":ip_version
                } for host_name in host_names]
           
    else:
        return [{'comment':line[0]}]


def read_hosts() -> list:
    """reads and returns a list of all hosts in HOSTS_FILE"""

    lines = []
    with open(HOSTS_FILE,'r') as hosts:
        for host in hosts:
            if host.strip() == "" : continue # empty line
            for line in parse_line(host):
                lines.append(line)
        hosts.close()
    return lines
    

def write_hosts(new_hosts:str) :
    """writes back the formated lines to HOSTS_FILE"""

    with open(HOSTS_FILE,'w') as writer:
        writer.write(new_hosts)
        writer.close()


def add_host(lines,host_ip, host_name,ip_version = IP.V4,description=""):
    """adds new host the the hosts lists"""
    
    if ip_version == IP.V4 and not is_valid_ipv4(host_ip) : raise InvalidIPv4(host_ip)
    if ip_version == IP.V6 and not is_valid_ipv6(host_ip) : raise InvalidIPv6(host_ip)

    for line in lines:
        if match_host(line,host_name,ip_version):
            raise DuplicateHost(host_name,str(ip_version))

    # TODO use insert line
    lines.append({
                'host_ip':host_ip,
                'disabled':False,
                'host_name':host_name,
                'description':description,
                "ip_version":str(ip_version)
                })
                

def update_host(lines,host_name,ip_version = IP.V4,host_ip:str = None, description:str = None):
    """"""
    
    if host_ip != None and ip_version == IP.V4 and not is_valid_ipv4(host_ip): 
        raise InvalidIPv4(host_ip)
    if host_ip != None and ip_version == IP.V6 and not is_valid_ipv6(host_ip): 
        raise InvalidIPv6(host_ip)

    for line in lines:
        if match_host(line,host_name,ip_version):
            line["host_ip"] = host_ip if host_ip != None else line["host_ip"]
            line["description"] = description if description != None else line["description"]
            break
    else:
        raise HostDoesNotExists(host_name,str(ip_version))


def delete_host(lines, host_name,ip_version = IP.V4):
    """"""
    for idx,line in enumerate(lines):
        if match_host(line,host_name,ip_version,include_disabled_hosts=True):
            #TODO Promte confirm delete
            lines.pop(idx)
            break
    else:
        raise HostDoesNotExists(host_name,str(ip_version))


def delete_line(lines,line_index):
    """"""

    #TODO Promte confirm delete
    lines.pop(line_index-1)
    
    
def disable_host(lines, host_name,ip_version = IP.V4):
    """"""
    for line in lines:
        if match_host(line,host_name,ip_version):
            line["disabled"] = True
            break
    else:
        raise HostDoesNotExists(host_name,str(ip_version))


def enable_host(lines, host_name,ip_version = IP.V4):
    """"""
    for line in lines:
        if match_host(line,host_name,ip_version,include_disabled_hosts=True):
            line["disabled"] = False
            break
    else:
        raise HostDoesNotExists(host_name,str(ip_version),include_disabled_hosts = True)
  

def list_hosts(lines):
    """"""
    
    header = f'|{" idx":<{3+len(str(len(lines)))}}|{" Host IP":<24}|{" Host name":<30}|{" Description":<50}|'
    print(sub('[^"|"]','-',header).replace("|","+"))
    print(header)
    print(sub('[^"|"]','-',header).replace("|","+"))

    for idx,line in enumerate(lines): 
        if "comment" not in line.keys():
            print(f' {str(idx+1)+")":<{4+len(str(len(lines)))}}{_format_line(line)}',end="")

def list_lines(lines):
    """"""

    for idx,line in enumerate(lines): 
        print(f' {str(idx+1)+")":<{4+len(str(len(lines)))}}{_format_line(line)}',end="")


def comment_line(lines,line_index):
    """"""  

    if("comment" in lines[line_index-1].keys()):
        print("Already Commented!")
        return
    
    lines[line_index-1]["disabled"] = True





def insert_line(lines,line_index,line):
    """"""
    lines.insert(line_index,line)
    



if __name__ == '__main__':
    lines = read_hosts()

    update_host(lines, host_name="rimawihome",host_ip="1.1.1.1",description="RimawiHome redirect ip")
    
    list_lines(lines)


    # new_hosts = format_lines(lines)
    # write_hosts(new_hosts)
