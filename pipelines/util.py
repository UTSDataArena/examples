def vmCheck():
    """Checks to see if this module is being run from within a virtual machine

    :return: instantiated object
    :rtype: bool
    """

    from platform import system as psys
    if psys() == "Linux":
        from os import system as osys
        # old method
        ##out = osys("grep -q \"^flags.*\ hypervisor\" /proc/cpuinfo")
        # slightly more reliable method:
        out = osys("dmesg | grep -q \"DMI:.*VirtualBox\"")
        return out == 0
    else:
        return False


