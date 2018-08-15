a= "bl.standard=0&betlevel.standard=1&denomination.standard=24"


def my_split(response):
    jss = {}

    b = response.split('&')
    for i in b:
        k =i.split("=")
        jss[k[0]]=k[1]

    bl_standard_first = jss['bl.standard'].split('%2C')[0]
    bl_standard_last = jss['bl.standard'].split('%2C')[-1]
    betlevel_standard = jss['betlevel.standard']
    denomination_standard = jss['denomination.standard']

    return {'bl_standard_first':bl_standard_first,
            'bl_standard_last':bl_standard_last,
            'betlevel_standard':betlevel_standard,
            'denomination_standard':denomination_standard}


print my_split(a)