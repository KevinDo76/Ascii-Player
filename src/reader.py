import scamble as en
from PIL import Image
import math
import os
framescount=4002
key=1234
Shade=["@","#","W","w","l","o","c","i",";",":","*",",","."," "]
ShadeF=len(Shade)
rang=255/ShadeF
fps=25
size=[]
data=[]
uncompressed=[]
def clamp(n,min,max):
  if n<min:
    return min
  elif n>max:
    return max
  else:
    return n

def interframeCreateInstruction(lastframe, thisframe):
    output=""
    chunkContinuous=False
    lastindexFound=0
    for index in range(len(thisframe)):
        if lastframe[index]!=thisframe[index]:
            if not chunkContinuous:
                output+=str(index)+thisframe[index]
                lastindexFound=index
                chunkContinuous=True
            elif abs(lastindexFound-index)>1:
                output+=str(index)+thisframe[index]
                lastindexFound=index
                chunkContinuous=True
            else:
                output+=thisframe[index]
                lastindexFound=index
    return output

def runlengthCompress(text,min):
  out=""
  currentchar=text[0]
  whole=text[0]
  runlength=1
  read=1
  while (read<len(text)):
    if text[read]==currentchar:
      runlength+=1
      whole+=text[read]
    else:
      if runlength>=min:
        out+="r"+str(runlength)+"r"+currentchar
      else:
        out+=whole
      runlength=1
      whole=text[read]
      currentchar=text[read]
    read+=1
  if runlength>=min:
    out+="r"+str(runlength)+"r"+currentchar
    whole=""
  return out+whole

for i in range(framescount):
    data.insert(i,"")
    uncompressed.insert(i,"")
    img=Image.open(os.getcwd()+"\\rick\\scene"+str(i+1).zfill(5)+".jpg")
    pix=img.load()
    size.append(img.size[0])
    size.append(img.size[1])
    for y in range(img.size[1]):
        t=""
        for x in range(img.size[0]):
            color=pix[x,y]
            temp={}
            temp[0]=255-color[0]**1.8/255**1.8*color[0]
            temp[1]=255-color[1]**1.8/255**1.8*color[1]
            temp[2]=255-color[2]**1.8/255**1.8*color[2]
            color=temp
            bl=math.floor(((color[0]+color[1]+color[2])/3)/rang)
            t+=Shade[clamp(int(bl),0,ShadeF-1)]
        data[i]+=t
        uncompressed[i]+=t
    print(i)
    runlength=runlengthCompress(data[i],5)
    if i>0:
      changes=interframeCreateInstruction(uncompressed[i-1],data[i])
      if len(runlength)<len(changes):
        data[i]=runlength
      else:
        data[i]="IN"+changes
    else:
      data[i]=runlength



final="FR".join(data)
final=en.Encrypt("DECRYPTSUCCESS",key)+"SEP"+str(img.size[0])+"SEP"+str(img.size[1])+"SEP"+str(fps)+"SEP"+str(framescount)+"SEP"+en.Encrypt(final,key)
print(len(final)/(64*64))
file=open(os.getcwd()+"\\data4.txt","w")
print(str(size[0]*size[1]*framescount)+" "+str(len(final))+" "+str(len(final)/len("FR".join(uncompressed))))
file.write(final)
file.close()
