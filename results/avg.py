import json
from functools import reduce


boxData = {}
def addDataEntries(data, boxData):

    for x in data:
        if x['url'] == 'https://video1.thierryve.nl':
            t = 'video'
        elif x['url'] == 'https://crm.thierryve.nl':
            t = 'crm'
        elif x['url'] == 'https://chat.thierryve.nl':
            t = 'chat'
        elif x['url'] == 'https://master-thesis-quic.appspot.com':
            t = 'guestbook'
        elif x['url'] == 'https://www.google.nl':
            t = 'google'
        elif x['url'] == 'https://crm.thierryve.nl/index.php?action=Login&module=Users':
            t = 'crm'
        elif x['url'] == 'https://static.thierryve.nl/100kb.html':
            t = 'static caddy'
        elif x['url'] == 'https://master-thesis-quic.appspot.com/static/100kb.html':
            t = 'static gae'
        elif x['url'] == 'https://akaunting.thierryve.nl/index.php/auth/login':
            t = 'akaunting login page'
        elif x['url'] == 'https://djangocms.thierryve.nl/en/':
            t = 'Django cms page'
        key = '{} {}'.format(t, x['platform'].lower())
        if not key in boxData:
            boxData.update({key: {}})

        if not x['network'] in boxData.get(key):
            boxData.get(key).update({x['network']: {}})

        if not x['protocol'] in boxData.get(key).get(x['network']):
            boxData.get(key).get(x['network']).update({x['protocol']: []})

        boxData.get(key).get(x['network']).get(x['protocol']).append(x['duration'])

    return boxData


def average(data):
    data.sort()
    data = data[:-1]
    data.pop(0)
    return round(reduce(lambda x, y: x + y, data) / len(data))

def cell(data):
    return "{} / {}".format(average(data.get("QUIC")), average(data.get("HTTPS")))

def createTable(data):
    for key, value in data.items():
        print("{} & {} & {} & {} & {} & {} & {} \\\\".format(key,
                                cell(value.get("none")),
                                cell(value.get("latency_200")),
                                cell(value.get("packetloss_1")),
                                cell(value.get("packetlossburst_125")),
                                cell(value.get("duplication_10")),
                                cell(value.get("corruption_1")),
                                    ))

boxData = addDataEntries(json.load(open('djangocms/defaultnetwork_djangocms.json')), boxData)
boxData = addDataEntries(json.load(open('djangocms/latency200_djangocms.json')), boxData)
boxData = addDataEntries(json.load(open('djangocms/packetloss1_djangocms.json')), boxData)
boxData = addDataEntries(json.load(open('djangocms/packetlossburst125_djangocms.json')), boxData)
boxData = addDataEntries(json.load(open('djangocms/duplication10_djangocms.json')), boxData)
boxData = addDataEntries(json.load(open('djangocms/corruption1_akaunting.json')), boxData)


#Print latex table
print("\\begin{table}[h!]")
print("\\centering")
print("\\label{start-test-table}")
print("\\resizebox{\\textwidth}{!}{")
print("\\begin{tabular}{||c c c c c c c||}")
print("\\hline")
print("Name & None & Latency & Packetloss & Packetlossburst & Duplication & Corruption \\\\ [0.5ex]")
print("\\hline\\hline")
createTable(boxData)
print("\\hline")
print("\\end{tabular}}")
print("\\caption{Average page load time over 10 requests. First value is \\acrshort{QUIC} second value is \\acrshort{HTTPS} page load time. header shows the different network simulation options that where used.} ")
print("\\end{table}")