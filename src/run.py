import os
import sys
import random
import time
import math
import threading
#decrypt functions
def Wrap(cn):
  if cn>126:
    return(((cn-32)%95)+32)
  elif cn<32:
    return 126-((((32-cn)-1)%95))
  else:
    return cn


def Decrypt(Text):
  a=""
  for i in range(len(Text)):
    n=-random.randint(-1000,1000)
    a+=chr(Wrap(ord(Text[i])+n))
  return a

def reconstructFrame(lastframe, changedata):
    parse=[]
    temp=["",""]
    read=0
    chunkread=False
    output=""
    while (read<len(changedata)):
        if not chunkread and changedata[read].isdigit():
            chunkread=True
            while changedata[read].isdigit():
                temp[0]+=changedata[read]
                read+=1
        elif chunkread and changedata[read].isdigit():
            chunkread=False
            parse.append(temp)
            temp=["",""]
        else:
            temp[1]+=changedata[read]
            read+=1
    parse.append(temp)
    lastInsert=0
    if len(parse)==1 and parse[0][1]=="":
        return lastframe
    else:
        for i in parse:
            output+=lastframe[lastInsert:int(i[0])]+i[1]
            lastInsert=int(i[0])+len(i[1])
        output+=lastframe[lastInsert:len(lastframe)]
    return output

def runLengthDecomp(text):
  read=0
  outtext=""
  while (read<len(text)):
    if text[read]=="r":
      start=read
      end=read+1
      while (text[end]!="r"):
        end+=1
      repeat=text[start+1:end]
      character = text[end+1]
      for i in range(int(repeat)):
        outtext+=character
      read=end+2
    else:
      outtext+=text[read]
      read+=1
  return outtext

frames=""
currentDecrypt=0
def run():
  global frames
  global currentDecrypt
  import winsound
  #load data
  musicpath="data"
  file=open(str(os.getcwd())+"\data4.txt","r")
  frames=file.read()
  file.close()
  #reading resolution/framerate
  tmp=frames.split("SEP")
  decryptConfirm=tmp[0] ; tmp.pop(0)
  resolutionX=int(tmp[0]) ; tmp.pop(0)
  resolutionY=int(tmp[0]) ; tmp.pop(0)
  framerate=int(tmp[0]) ; tmp.pop(0)
  frameCount=int(tmp[0]) ; tmp.pop(0)
  os.system(f"mode con: cols={resolutionX*2+65} lines={resolutionY}")
  encryptedframes="SEP".join(tmp)
  decryptchunk=2000
  characterLen=len(frames)
  grabCount=resolutionX*resolutionY
  decryptSuccess=False
  timeTable={}
  fps=0
  fpshis=[]
  frames=""
  lastframe=""
  def checkEncryptInterval():
    global frames
    global currentDecrypt
    while (len(frames.split("FR"))<3 and currentDecrypt<len(encryptedframes)):
      frames+=Decrypt(encryptedframes[currentDecrypt:currentDecrypt+decryptchunk])
      currentDecrypt+=min(decryptchunk,len(encryptedframes))

  #thread

  def music():
    winsound.PlaySound(musicpath, winsound.SND_FILENAME)

  #main code
  while (not decryptSuccess):
    key=int(input("Enter key: "))
    random.seed(key-len("DECRYPTSUCCESS")%600000000)
    if Decrypt(decryptConfirm)=="DECRYPTSUCCESS":
      print("header decrypted, data is ready")
      decryptSuccess=True
    else:
      print("Incorrect decryption key, unable to access file contents")
  print("key: "+str(key))
  while (1):
    while True:
        result=input("are you ready?(yes): ")
        if result=="yes":
            break
    print("Character count: "+str(characterLen))
    print("Frame Count: "+str(frameCount))
    random.seed(key-len(encryptedframes)%600000000)
    checkEncryptInterval()
    print("dbuffer is ready")
    print(frames)
    time.sleep(0.5)
    start=time.time()
    for i in range(int(frameCount)):
      timeTable[i]=start+(i*(1/framerate))
    
    sound = threading.Thread(target=music)
    sound.start()
    for frame in range(int(frameCount)):
      if len(frames)%400==0:
         os.system(f"mode con: cols={resolutionX*2+65} lines={resolutionY}")
      fstart=time.time()
      chunks=frames.split("FR")
      compressType=""
      if chunks[0][0:2]=="IN":
        decompressedData=reconstructFrame(lastframe,chunks[0][2:len(chunks[0])])
        chunks.pop(0)
        compressType="Interframe"
      else:
        decompressedData = runLengthDecomp(chunks[0]) ; chunks.pop(0)
        compressType="RunLength"
      frames="FR".join(chunks)
      checkEncryptInterval()
      out=""
      lastframe=decompressedData
      for line in range(0,resolutionY):
        temp=(decompressedData[line*resolutionX:(line+1)*resolutionX])
        for character in temp:
          out+=character+character
        if line==2:
          out+=str("frame: "+str(frame)+" fps: "+str("%.2f" % fps)+" dbuffer: "+str(len(frames))+" compression: "+compressType)
        out+="\n"
      while (time.time()<timeTable[frame]):
        pass
      sys.stdout.write(out)
      sys.stdout.flush()
      if time.time()-fstart>0:
        fpshis.append(1/(time.time()-fstart))
      if len(fpshis)>15:
        fpshis.pop(0)
      fps=0
      for i in fpshis:
        fps+=i
      fps=(fps/len(fpshis))
    os.system("cls")
    print("Playtime: "+str(time.time()-start)+"sec")
    currentDecrypt=0
    frames=""

if __name__=="__main__" and os.name=="nt":
  run()
