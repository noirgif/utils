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

for i in range(8):
    if me == 'gpu' + str(i):
        hosts.write('gpu{0} 127.0.0.1\n'.format(i))
    else:
        hosts.write('gpu{0} 192.168.1.4{0}\n'.format(i))

for i in range(1, 8):
    if 'ib' + me == 'ibgpu' + str(i):
        hosts.write('ibgpu{0} 127.0.0.1\n'.format(i))
    else:
        hosts.write('ibgpu{0} 10.0.0.4{0}\n'.format(i))
