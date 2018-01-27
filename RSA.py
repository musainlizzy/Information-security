

from Crypto.PublicKey import RSA




# egcd copied from
# https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


e = 65537
p = 61580027889114958695156433075022921625111716838026065218930264174982155928493667457473178789199096388330104168562339964452798883
q = 61580027889114958695156433075022921625111716838026065218930264174982155928493667457473178789199096388330104168562339964452798983
n=3792099834824176115628645611456939155686624866889813355200736094518084851951738802106988293638946637260624086540770503053865320129396360551964085692698583123009340475467436314894933277834707830212268369702982497158299358615015777719280655569943697725935989
e=65537L
d=modinv(e,(p-1)*(q-1))
key=RSA.construct((n,e,d,p,q))
flag = 2695332229584677643955456273806620223248113646319071765538638556860048054409809122495402006963309545938644506359833262731656772900139609016315019438863326190216244218707223284467850772397846545739297905773177955881654797619006374933394458240620119806734583
print key.decrypt(flag)
a =83090569650065304147971362820551236810
print hex(a)
