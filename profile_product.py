import re


def profile_ap_sku(x):
    '''
    Takes in "Enterprise SKU" and if it is for an AP, profiles the type of AP it is.  
    
    INPUT:
        str : x :  Enterprise SKU
    OUTPUT:
        str : Profile type : AX-High, AX-Low, AC2-Med, etc...
        str : "N/A" : Did not match
    '''
    if bool(re.search("C91..AX", x)):
        if bool(re.search("(.*DNA)|(.*ADJ)", x)):
            return("N/A")
        elif bool(re.search("C91[01].AX[IEW]", x)):
            return("AX-Low")
        elif bool(re.search("C9120AX[IE]", x)):
            return("AX-Med")
        elif bool(re.search("C913.AX[IE]", x)):
            return("AX-Med")
        else:
            return("N/A")
    elif bool(re.search("AIR-[C]?AP[1-4]8..", x)):
        if bool(re.search("AIR-[C]?AP18..[IEWMT]", x)):
            return("AC2-Low")
        elif bool(re.search("AIR-[C]?AP28..[IE]", x)):
            return("AC2-Med")
        elif bool(re.search("AIR-[C]?AP38..[IEP]", x)):
            return("AC2-High")
        elif bool(re.search("AIR-[C]?AP48..", x)):
            return("AC2-High")
    elif bool(re.search("AIR-AP15..", x)):
        if bool(re.search("AIR-AP157.", x)):
            return("AC1-Outdoor")
        if bool(re.search("AIR-AP15[46].", x)):
            return("AC2-Outdoor")
    elif bool(re.search("AIR-[C]?AP[1-3]7..", x)):
        if bool(re.search("AIR-[C]?AP17..[IE]", x)):
            return("AC1-Low")
        elif bool(re.search("AIR-[C]?AP27..[IE]", x)):
            return("AC1-Med")
        elif bool(re.search("AIR-[C]?AP37..[IE]", x)):
            return("AC1-High")
    elif bool(re.search("MR.*-HW", x)):
        if bool(re.search("MR[2-3][0-9]", x)):
            suffix = 'Low'
        elif bool(re.search("MR4[0-9]", x)):
            suffix = 'Med'
        elif bool(re.search("MR5[0-9]", x)):
            suffix = 'High'
        elif bool(re.search("MR[7-8][0-9]", x)):
            suffix = 'Outdoor'
        else:
            suffix = ""
        if bool(re.search("MR[2-8]0", x)):
            prefix = 'AC1'
        elif bool(re.search("MR[2-8][2-3]", x)):
            prefix = 'AC2'
        elif bool(re.search("MR[2-8][4-6]", x)):
            prefix = 'AX'
        else:
            prefix = ""
        if ((len(prefix) > 0) & (len(suffix) > 0)):
            return(f"{prefix}-{suffix}")
        else:
            return("N/A")
    else:
        return("N/A")


