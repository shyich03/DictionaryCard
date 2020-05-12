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


def TransformText(text, point, font, width=0):
    # find line width
    print(text)
    print("total width", GetTextDimensions(text, point, font)[0] )
    width = width == 0 and(GetTextDimensions(text, point, font)[0] < 1500 and 460 or 600) or width
    res = []
    cur = ""
    for word in text.split(" "):
        temp = cur + word + " "
        if GetTextDimensions(temp, point, font)[0]>width:
            res += [cur]
            cur = word+" "
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

    titleSize = 100
    maxTitleWidth = 630
    descSize = 32
    linebreak = 7
    step = 0
    count = 1
    with open('text.txt') as file:
        for line in file:
            if step == 0:
                #image size/color
                # img = Image.new('RGB', (680, 680), color = (233, 235, 232))
                img = Image.open("background.jpg")
                img = img.resize((680,680))
                d = ImageDraw.Draw(img)
                fontSize, lineLength = GetFont(line, titleSize, maxTitleWidth, "Dubai-Medium")
                titleFont = ImageFont.truetype('fonts/Dubai-Medium.ttf', fontSize)
                # title = line[len(line)-2]=="." and line.rsplit(' ', 1)[0] or line[0:len(line)-1]
                # d.text(pos, line, font=font, fill=(0, 0, 1))
                title = line
                titleX = (720-lineLength)/2
                titleY = 0
            elif step == 1:
                posY = 165
                width,descText = TransformText(line, descSize, 'Dubai-Regular')
                descFont = ImageFont.truetype('fonts/Dubai-Regular.ttf', descSize)
                descX = (690-width)/2
                descY = []
                for text in descText:
                    if text!="\n ":
                        # d.text(pos, text, font=font, fill=(0, 0, 1))
                        descY += [posY]
                        posY+=descSize+linebreak
            elif step == 2:
                posY += descSize+linebreak
                exampleText = TransformText(line, descSize, 'Dubai-Light', width)[1]
                exampleX = (690-width)/2
                exampleY = []
                exampleFont = ImageFont.truetype('fonts/Dubai-Light.ttf', descSize)
                for text in exampleText:
                    if text!="\n ":
                        # pos = (posX,posY)
                        # d.text(pos, text, font=font, fill=(0, 0, 1))
                        exampleY += [posY]
                        posY+=descSize+linebreak
            else:
                if line == "\n":
                    baseHeight = (620-posY)/2
                    d.text((titleX,titleY+baseHeight), title, font=titleFont, fill=(0, 0, 1))
                    for i in range(len(descText)):
                        text = descText[i]
                        if text!="\n ":
                            d.text((descX, descY[i]+baseHeight), text, font=descFont, fill=(0, 0, 1))
                    for i in range(len(exampleText)):
                        text = exampleText[i]
                        if text!="\n ":
                            d.text((exampleX, exampleY[i]+baseHeight), text, font=exampleFont, fill=(0, 0, 1))
                    img.save('img/'+str(count)+'.png')
                    count+=1
                else:
                    print(line)
                    print ("Error with text file while create png for ",title)
                    break
            
            step = (step + 1)%4


 

