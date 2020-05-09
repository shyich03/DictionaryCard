from PIL import Image, ImageDraw, ImageFont
import os.path
import ctypes
import string

def slugify(value):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in value if c in valid_chars)

def GetTextDimensions(text, points, font):
    # class SIZE(ctypes.Structure):
    #     _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

    # hdc = ctypes.windll.user32.GetDC(0)
    # hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
    # hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

    # size = SIZE(0, 0)
    # ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

    # ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
    # ctypes.windll.gdi32.DeleteObject(hfont)

    # return (size.cx, size.cy)
    font = ImageFont.truetype('fonts/'+font+'.ttf', points)
    size = font.getsize(text)  
    return size


def TransformText(text, point, font):
    # find line width
    print(text)
    print("total width", GetTextDimensions(text, point, font)[0] )
    width = GetTextDimensions(text, point, font)[0] < 1200 and 460 or 600
    res = []
    cur = ""
    for word in text.split(" "):
        temp = cur + word + " "
        if GetTextDimensions(temp, point, font)[0]>width:
            res += [cur]
            cur = word
        else:
            cur = temp
    if cur!="":
        res += [cur]
    return (width,res)

def GetFont(text, initPoint, maxLength, font):
    dimensions = GetTextDimensions(text, initPoint, font)
    lineLength = dimensions[0]
    point = initPoint
    while lineLength>maxLength:
        point -= 1
        dimensions = GetTextDimensions(text, point, font)
        lineLength = dimensions[0]
    return (point, lineLength)
if __name__ == "__main__":

    step = 0
    with open('text.txt') as file:
        for line in file:
            if step == 0:
                #image size/color
                img = Image.new('RGB', (680, 680), color = (233, 235, 232))
                d = ImageDraw.Draw(img)
                fontSize, lineLength = GetFont(line, 60, 650, "Dubai-Medium")
                posX = (690-lineLength)/2
                posY = 20
                font = ImageFont.truetype('fonts/Dubai-Medium.ttf', fontSize)
                pos = (posX,posY)
                title = line[len(line)-2]=="." and line.rsplit(' ', 1)[0] or line[0:len(line)-1]
                d.text(pos, line, font=font, fill=(0, 0, 1))
            elif step == 1:
                posY = 120
                width,texts = TransformText(line, 24, 'Dubai-Regular')
                font = ImageFont.truetype('fonts/Dubai-Regular.ttf', 24)
                print(width, texts)
                posX = (690-width)/2
                for text in texts:
                    if text!="\n ":
                        pos = (posX,posY)
                        d.text(pos, text, font=font, fill=(0, 0, 1))
                        posY+=27
            elif step == 2:
                posY += 30
                texts = TransformText(line, 24, 'Dubai-Light')[1]
                posX = (690-width)/2
                font = ImageFont.truetype('fonts/Dubai-Light.ttf', 24)
                print(width, texts)
                for text in texts:
                    if text!="\n ":
                        pos = (posX,posY)
                        d.text(pos, text, font=font, fill=(0, 0, 1))
                        posY+=27
            else:
                if line == "\n":
                    mewImg = img.crop((0, 0,680, posY+55))
                    mewImg.save('img/'+slugify(title)+'.png')
                else:
                    print(line)
                    print ("Error with text file while create png for ",title)
                    break
            
            step = (step + 1)%4


 

