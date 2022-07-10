
from pprint import pprint
from re import sub
from .exceptions import DuplicateHost, HostDoesNotExists, InvalidIPv4, InvalidIPv6
from .ip_enum import IP
from .regex_patterns import IPV4_PATTERN, IPV6_PATTERN
from .interface import update_host_interface