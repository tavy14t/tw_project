import random, os
lista = os.listdir('.')

for item in range(200):
    print 'INSERT INTO RESTAPI_AVATARS VALUES (' + \
        str(item) + ',' + str(item) + ', "' + \
        lista[random.randint(0, len(lista) - 1)] + '");'
