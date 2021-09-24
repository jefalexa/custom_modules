import re


def profile_ap_sku(x):
    '''
    Takes in "Enterprise SKU" and if it is for an AP, profiles the type of AP it is.  
    
    INPUT:
        str : x :  Enterprise SKU
    OUTPUT:
        dict : 
        	"type_1": Access Point
        	"type_2": AX, AC, etc
        	"class_type": High/Med/Low
    '''
    if bool(re.search("C91..AX", x)):
        type_1 = "Access Point"
        type_2 = 'AX'
        if bool(re.search("(.*DNA)|(.*ADJ)", x)):
            type_1 = "N/A"
            type_2 = 'N/A'
            class_type = 'N/A'
        elif bool(re.search("C91[01].AX[IEW]", x)):
            class_type = "Low"
        elif bool(re.search("C9120AX[IE]", x)):
            class_type = "Medium"
        elif bool(re.search("C913.AX[IE]", x)):
            class_type = "High"
        else:
            type_1 = "N/A"
            type_2 = 'N/A'
            class_type = 'N/A'
    elif bool(re.search("AIR-[C]?AP[1-4]8..", x)):
        type_1 = "Access Point"
        type_2 = 'AC2'
        if bool(re.search("AIR-[C]?AP18..[IEWMT]", x)):
            class_type = "Low"
        elif bool(re.search("AIR-[C]?AP28..[IE]", x)):
            class_type = "Medium"
        elif bool(re.search("AIR-[C]?AP38..[IEP]", x)):
            class_type = "High"
        elif bool(re.search("AIR-[C]?AP48..", x)):
            class_type = "High"
        else:
            class_type = "N/A"
    elif bool(re.search("AIR-AP15..", x)):
        type_1 = "Access Point"
        if bool(re.search("AIR-AP157.", x)):
            type_2 = "AC1"
            class_type = "Outdoor"
        elif bool(re.search("AIR-AP15[46].", x)):
            type_2 = "AC2"
            class_type = "Outdoor"
        else:
            type_2 = 'N/A'
            class_type = 'N/A'
    elif bool(re.search("AIR-[C]?AP[1-3]7..", x)):
        type_1 = "Access Point"
        type_2 = 'AC1'
        if bool(re.search("AIR-[C]?AP17..[IE]", x)):
            class_type = "Low"
        elif bool(re.search("AIR-[C]?AP27..[IE]", x)):
            class_type = "Medium"
        elif bool(re.search("AIR-[C]?AP37..[IE]", x)):
            class_type = "High"
        else:
            class_type = 'N/A'
    elif bool(re.search("MR.*-HW", x)):
        type_1 = "Access Point"
        if bool(re.search("MR[2-3][0-9]", x)):
            class_type = "Low"
        elif bool(re.search("MR4[0-9]", x)):
            class_type = "Medium"
        elif bool(re.search("MR5[0-9]", x)):
            class_type = "High"
        elif bool(re.search("MR[7-8][0-9]", x)):
            class_type = "Outdoor"
        else:
            class_type = 'N/A'
        if bool(re.search("MR[2-8]0", x)):
            type_2 = 'AC1'
        elif bool(re.search("MR[2-8][2-3]", x)):
            type_2 = 'AC2'
        elif bool(re.search("MR[2-8][4-6]", x)):
            type_2 = 'AX'
        else:
            type_2 = 'N/A'
    else:
        type_1 = "N/A"
        type_2 = 'N/A'
        class_type = 'N/A'
        
    return({"type_1":type_1, "type_2":type_2, "class_type":class_type})



def profile_switch_sku(x):
    '''
    Takes in "Enterprise SKU" and if it is for an switch, profiles the type of switch it is.  
    
    INPUT:
        str : x :  Enterprise SKU
    OUTPUT:
        dict : 
            str : switch_type
            str : port_count
            str : port_type
            bool : mgig
    '''
    
    port_count_exp = re.compile("([0-9]*)([A-Z])(.*)")
    port_type_dict = {'T':'Data', 'S':'SFP-1G', 'P':"PoE+", 'U':'UPoE', 'H':'UPoE+', "C":"QSFP28-100G", "Q":"QSFP+-40G", "Y":"SFP28-1/10/25G", "X":"SFP/SPF+-1/10G"}
    meraki_port_count_exp = re.compile("([0-9]*)([A-Z]?[A-Z]?)(.*)")
    meraki_port_type_dict = {'P':"PoE+", 'LP':"PoE+", 'FP':"PoE+", 'U':'UPoE', 'X':'UPoE', 'UX':'UPoE'}
    
    mgig = False

    if bool(re.search("^C9[23]00[LX]?-[0-9]+[A-Z]+", x)):
        switch_type = 'stackable'
        port_config = x.split("-")[1]
        port_count = re.match(port_count_exp, port_config)[1]
        port_type = re.match(port_count_exp, port_config)[2]
        if port_type in port_type_dict:
            port_type = port_type_dict[port_type]
        else:
            port_type = "N/A"
        port_remainder = re.match(port_count_exp, port_config)[3]
        if bool(re.search('.*X.*', port_remainder)):
            mgig = True
        else:
            mgig = False
    
    elif bool(re.search("^C94[0-9]+[R-]", x)):
        if bool(re.search("^C94[0-9]+R", x)):
            switch_type = 'chassis'
            port_count = 0
            port_type = "N/A"
        elif bool(re.search("^C94[0-9]+-SUP", x)):
            switch_type = 'supervisor'
            port_count = 0
            port_type = "N/A"
        elif bool(re.search("^C94[0-9]+-LC", x)):
            switch_type = 'linecard'
            port_config = x.split("-")[2]
            port_count = re.match(port_count_exp, port_config)[1]
            port_type = re.match(port_count_exp, port_config)[2]
            if port_type in port_type_dict:
                port_type = port_type_dict[port_type]
            else:
                port_type = "N/A"
            port_remainder = re.match(port_count_exp, port_config)[3]
            if bool(re.search('.*X.*', port_remainder)):
                mgig = True
            else:
                mgig = False
        else:
            switch_type = "N/A"
            port_count = 0
            port_type = "N/A"
    
    elif bool(re.search("^C9500-[0-9]+", x)):
        switch_type = "stackable"
        port_config = x.split("-")[1]
        port_count = re.match(port_count_exp, port_config)[1]
        port_type = re.match(port_count_exp, port_config)[2]
        if port_type in port_type_dict:
            port_type = port_type_dict[port_type]
        else:
            port_type = "N/A"
        port_remainder = re.match(port_count_exp, port_config)[3]
        if bool(re.search('.*X.*', port_remainder)):
            mgig = True
        else:
            mgig = False
    
    elif bool(re.search("^C96[0-9]+[R-]", x)):
        if bool(re.search("^C96[0-9]+R", x)):
            switch_type = 'chassis'
            port_count = 0
            port_type = "N/A"
        elif bool(re.search("^C96[0-9]+-SUP", x)):
            switch_type = 'supervisor'
            port_count = 0
            port_type = "N/A"
        elif bool(re.search("^C96[0-9]+-LC", x)):
            switch_type = 'linecard'
            port_config = x.split("-")[2]
            port_count = re.match(port_count_exp, port_config)[1]
            port_type = re.match(port_count_exp, port_config)[2]
            if port_type in port_type_dict:
                port_type = port_type_dict[port_type]
            else:
                port_type = "N/A"
            port_remainder = re.match(port_count_exp, port_config)[3]
            if bool(re.search('.*X.*', port_remainder)):
                mgig = True
            else:
                mgig = False
        else:
            switch_type = "N/A"
            port_count = 0
            port_type = "N/A"
            
    elif bool(re.search("^MS.*-HW$", x)):
        switch_type = 'stackable'
        port_config = x.split("-")[1]
        port_count = re.match(meraki_port_count_exp, port_config)[1]
        port_type = re.match(meraki_port_count_exp, port_config)[2]
        if bool(re.search('.*X.*', port_config)):
            mgig = True
        else:
            mgig = False
        if len(port_type) == 0:
            if bool(re.search("^MS41.*-HW$", x)):
                port_type = "SFP-1G"
            elif bool(re.search("^MS42.*-HW$", x)):
                port_type = "SFP+-10G"
            elif bool(re.search("^MS45.*-HW$", x)):
                port_type = "QSFP+-40G"
            else:
                port_type = "Data"
        elif port_type in meraki_port_type_dict:
            port_type = meraki_port_type_dict[port_type]
        else:
            port_type = "N/A"
    
            
    elif bool(re.search("^GS[1-9].*-HW", x)):
        switch_type = 'stackable'
        port_config = x.split("-")[1]
        port_count = re.match(meraki_port_count_exp, port_config)[1]
        port_type = re.match(meraki_port_count_exp, port_config)[2]
        if bool(re.search('.*X.*', port_config)):
            mgig = True
        else:
            mgig = False
        if len(port_type) == 0:
        	port_type = "Data"
        elif port_type in meraki_port_type_dict:
            port_type = meraki_port_type_dict[port_type]
        else:
            port_type = "N/A"
    else:
        switch_type = "N/A"
        port_count = 0
        port_type = "N/A"

    return({'switch_type':switch_type, 'port_count':port_count , 'port_type':port_type, 'mgig':mgig})



def profile_dna_sku(x):
    '''
    Takes in "Enterprise SKU" and if it is for DNA, profiles it.
    
    INPUT:
        str : x :  Enterprise SKU
    OUTPUT:
        dict : 
            'license_type': Switching, Wireless, Routing
            'buying_type': ALC, EA
            'device_type': AP or Switch Type
            'license_tier': Ess, Adv, Prem
            'years': 3, 5, 7
    '''
    
    sw_exp = re.compile("^C([1-9][A-Z,0-9]*)-DNA-.*([E,A,P])(.*)([1,3,5,7])[Y,R]")
    air_exp = re.compile("^(AIR|EDU)-DNA-([E,A,P])-([1,3,5,7])[Y,R]")
    spaces_exp = re.compile("^D-(CISCODNAS|DNAS)-(.*)-([1-9])[Y,R]")
    ea_sw_exp = re.compile("^E2N-C([A-Z,0-9]*)-(.*)-([E,A,P])$")
    ea_air_exp = re.compile("^E2N-AIRWLAN-(.*)-([E,A,P])$")
    ea_spaces_exp = re.compile("^E2N-DNAS-([A-Z]*)")


    if bool(re.search(sw_exp, x)):
        m = re.match(sw_exp, x)
        license_type = "Switching"
        buying_type = "ALC"
        device_type = m[1]
        license_tier = m[2]
        years = m[4]

    elif bool(re.search(air_exp, x)):
        m = re.match(air_exp, x)
        license_type = "Wireless"
        buying_type = "ALC"
        device_type = "AP"
        license_tier = m[2]
        years = m[3]

    elif bool(re.search(spaces_exp, x)):
        m = re.match(spaces_exp, x)
        license_type = "Wireless"
        buying_type = "ALC"
        device_type = "DNA Spaces"
        license_tier = m[2]
        years = m[3]

    elif bool(re.search(ea_sw_exp, x)):
        m = re.match(ea_sw_exp, x)
        license_type = "Switching"
        buying_type = "EA"
        device_type = m[1]
        license_tier = m[3]
        years = 'N/A'

    elif bool(re.search(ea_air_exp, x)):
        m = re.match(ea_air_exp, x)
        license_type = "Wireless"
        buying_type = "EA"
        device_type = "AP"
        license_tier = m[2]
        years = 'N/A'

    elif bool(re.search(ea_spaces_exp, x)):
        m = re.match(ea_spaces_exp, x)
        license_type = "Wireless"
        buying_type = "EA"
        device_type = "DNA Spaces"
        license_tier = m[1]
        years = 'N/A'
    
    else:
        license_type = 'N/A'
        buying_type = 'N/A'
        device_type = 'N/A'
        license_tier = 'N/A'
        years = 'N/A'

    return({'license_type': license_type, 'buying_type': buying_type, 'device_type': device_type, 'license_tier': license_tier, 'years': years})
        
