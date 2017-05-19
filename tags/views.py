from django.shortcuts import render

from common import commonviews
from tables import TagsTable

import random
import collections

from authentication.login_decorator import login_required


@login_required
def tags(request):
    context = dict()

    context.update(commonviews.side_menu('Tags'))

    keys = {
        'Security': [
            'Everything is a Target. Your Health Data is Next.',
            'Shadow Brokers Attack Tools Light Up Chinese and Russian Darknet',
            'APT28: A Window into Russia\'s Cyber Espionage Operations?',
            'Russian hacker squad Apt 29 is using Twitter to steal valuable data',
        ],
        'Antivirus': [
            'Hackerii de la CIA: "Bitdefender rezista nebuneste"',
            'Bitdefender - Cybersecurity Solutions for Business and Personal Use',
            'Collected Lastbench by Antivirus Production (Paperback)',
            'The AV-TEST Security Report 2015/2016',
            'Internet of Things: Security Evaluation of 7 Fitness Trackers on Android and the Apple Watch',
            'Google vs. Bing: Search Engines Deliver Infected Websites as Their Top Results.',
            'Testing Exploit-Prevention Mechanisms in Anti-Malware Products.',
            'The WildList is Dead, Long Live the WildList!',
            'Antivirus outbreak response testing and impact.',
            'Rescue Me: Updating Anti-Virus Rescue Systems.'
        ],
        'Special': [
            'Hecarii bitdefendar au dat in spaima la bolnavii de cardieshe de la CIA',
            'Un IT-ist roman a creat smart-ghiulul, cu care dai bani la lautari contactless',
            'In sfarsit! Savantii moldoveni au reusit sa teleporteze un cartus de tigari de la Chisinau la Iasi',
            'Romania a creat un robot inteligent, care merge cu trenul fara bilet si da 5 lei la nas',
            'Un corporatist din Iasi are planuri ambitioase pentru minivacanta de 1 Mai: "Cobor la o tigara!"',
            'Studiu: In plin secol XXI, multi romani inca isi deviruseaza PC-urile folosind leacuri babesti',
        ]
    }

    context['tags'] = [key for key in keys]

    if request.method == 'POST':
        tags = request.POST.getlist('values')
        tag_data = collections.OrderedDict()

        tag_data = []
        for key in tags:
            for item in keys[key]:
                tag_data.append({
                    'info': item
                })

        tag_table = collections.OrderedDict()

        uid = hex(random.randint(-10000, 10000))[2:]

        tag_table = {
            'id': uid,
            'table': TagsTable(tag_data)
        }

        context['prefered_tags'] = tag_table

    return render(request, 'tags/tags.html', context)
