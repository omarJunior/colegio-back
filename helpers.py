GROUPS = []
GROUP_NAMES = [
    ('Docentes', "Docentes"),
    ('Estudiantes', "Estudiantes"),
    ('Rector', "Rector"),
]


def hasGroup(user, g):
    res = [item[1] for item in GROUPS if item[0] == g]
    if len(res) > 0:
        us = [gr for gr in user.groups.all() if gr.pk == res[0]]
        if len(us) > 0:
            return True
        else:
            return False
    else:
        return False    


def getGroupNames(user):
    groupNames = ""
    for gr in user.groups.all():
        name = [item[1] for item in GROUP_NAMES if item[0] == gr.name]
        if len(name) > 0:
            groupNames += f"{name[0]}, "

    groupNames = groupNames[:-2]
    return groupNames
