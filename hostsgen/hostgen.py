import os
import importlib

try:
    os.replace('/etc/hosts', '/etc/hosts.backup')
    print('The old hosts file is backed up at /etc/hosts.backup')
except IOError:
    print('You need to be priviledged to perform this action')
    exit()
hosts = open('/etc/hosts', 'w')

localhost = """127.0.0.1    localhost localhost.localdomain localhost4 localhost4.localdomain4
::1    localhost localhost.localdomain localhost6 localhost6.localdomain6"""

hosts.write(localhost + '\n')

me = importlib.import_module('socket').gethostname()

for i in range(1, 9):
    if me == 'gpu' + str(i):
        hosts.write('127.0.0.1 gpu{0}\n'.format(i))
    else:
        hosts.write('192.168.1.4{0} gpu{0}\n'.format(i))

for i in range(1, 9):
    if 'ib' + me == 'ibgpu' + str(i):
        hosts.write('127.0.0.1 ibgpu{0}\n'.format(i))
    else:
        hosts.write('10.0.0.4{0} ibgpu{0}\n'.format(i))
