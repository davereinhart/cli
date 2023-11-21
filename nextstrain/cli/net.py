"""
Network handling.
"""
from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import Optional, Set, Union
from socket import getaddrinfo, getnameinfo, gaierror, AddressFamily, AF_UNSPEC, NI_NUMERICHOST


def is_loopback(host: Optional[str]) -> Optional[bool]:
    """
    Check if *host* points to only loopback IPs.

    Returns True if so, otherwise False.  Returns None if *host* is None or on
    host resolution error (e.g. DNS error).
    """
    if host is None:
        return None

    try:
        ips = resolve_host(host)
    except gaierror:
        return None

    return all(ip.is_loopback for ip in ips)


def resolve_host(host: str, family: AddressFamily = AF_UNSPEC) -> Set[Union[IPv4Address, IPv6Address]]:
    """
    Resolves a named or numeric *host* to a set of IP addresses.

    By default, all IPv4 and IPv6 addresses are resolved, as applicable
    depending on the local IP stack and DNS records for the named host.  A
    specific address family can be chosen by providing *family*.
    """
    return {
        # XXX TODO: I *think* NI_NUMERICHOST works on Windows, but it's not
        # entirely clear to me.  Should test it…
        #   -trs, 21 Nov 2023
        ip_address(getnameinfo(sockaddr, NI_NUMERICHOST)[0])
            for _, _, _, _, sockaddr
             in getaddrinfo(host, None, family = family) }
