import random
import math

def Wrap(cn):
  if cn>126:
    return(((cn-32)%95)+32)
  elif cn<32:
    return 126-((((32-cn)-1)%95))
  else:
    return cn
def KeyGen(txt):
  n=1
  for i in range(len(txt)):
    e=0
    n=(n+ord(txt[i])/10)*(i+1)%200000000
    e+=math.pi+ord(txt[i])/100
  e=e-math.floor(e)
  return n*e
def Encrypt(Text,Key):
  random.seed(Key-len(Text)%10000)
  finaltxt=""
  for i in range(len(Text)):
    if ord(Text[i])==10:
      boi=" "
    else:
      boi=Text[i]
    n=random.randint(-1000,1000)
    finaltxt+=chr(Wrap(ord(boi)+n))
  return finaltxt
#lol bad encryption, using python random lib security 10/10
def Decrypt(Text,Key):
  a=""    
  random.seed(Key-len(Text)%100000)
  for i in range(len(Text)):
    n=-random.randint(-1000,1000)
    a+=chr(Wrap(ord(Text[i])+n))
  return a
