from array import array
import os, glob

ender = [0, 0, 0, 8, 0, 0, 0, 2, 0, 121, 24, 0, 0, 0, 0, 4, 0, 0, 0, 0]
def find_pngoffset(gamelist: list[int], size: int) -> list[int]:
    arraycount = 0
    while True:
        if gamelist[arraycount] == 137:
            if gamelist[arraycount + 1] == 80:
                if gamelist[arraycount + 2] == 78:
                    if gamelist[arraycount + 3] == 71:
                        return arraycount
        if (gamelist[arraycount] == size):
            raise Exception("File formatted incorrectly")
        arraycount += 1


if __name__ == '__main__':
    #os.remove("tt.xfbin")
    xfbinfilelist = glob.glob("*.xfbin")
    pngfilelist = glob.glob("*.png")
    listlen = len(pngfilelist)
    if len(xfbinfilelist) > len(pngfilelist):
        listlen = len(xfbinfilelist)
    namelist = []
    nameset = set()
    for x in xfbinfilelist:
        nameset.add(os.path.splitext(x)[0])
    for x in pngfilelist:
        nameset.add(os.path.splitext(x)[0])
    namelist = []
    for x in nameset:
        if x + '.xfbin' in xfbinfilelist:
            if x + '.png' in pngfilelist:
                namelist.append(x)
    for n in namelist:
        file = open(n + '.xfbin',"rb")
        file_size = os.path.getsize(n + '.xfbin')
        numbers = list(file.read(file_size))
        pngoffset = find_pngoffset(numbers, file_size)
        filesize1offset = pngoffset - 4
        filesize2offset = pngoffset - 16
        png = open(n + '.png',"rb")
        png_size = os.path.getsize(n + '.png')
        pnglist = list(png.read(png_size))
        retlist = []
        print(len(pnglist))
        for x in range(0, pngoffset):
            retlist.append(numbers[x])
        for x in range(0, len(pnglist)):
            retlist.append(pnglist[x])
        for x in range(0, len(ender)):
            retlist.append(ender[x])
        file.close()
        filesize1 = str(hex(png_size)).replace('0x', '')
        filesize2og = png_size + 4
        filesize2 = ''
        if len(str(png_size)) < 8:
            filesize1 = '0' * (8 - len(hex(png_size).replace('0x', ''))) + str(hex(png_size)).replace('0x', '')
        if len(str(filesize2og)) < 8:
            filesize2 = '0' * (8 - len(hex(filesize2og).replace('0x', ''))) + str(hex(filesize2og)).replace('0x', '')
        else:
            filesize2 = str(hex(filesize2)).replace('0x', '')
        filesize1_list = []
        filesize2_list = []
        count = 0
        while True:
            if count == 8:
                break
            if count > 8:
                raise Exception("oof size")
            filesize1_list.append(int(filesize1[count:count + 2], base = 16))
            count += 2
        count = 0
        while True:
            if count == 8:
                break
            if count > 8:
                raise Exception("oof size")
            filesize2_list.append(int(filesize2[count:count + 2], base = 16))
            count += 2
        for x in range(0, 4):
            retlist[filesize1offset + x] = filesize1_list[x]
            retlist[filesize2offset + x] = filesize2_list[x]
        file = open(n + '.xfbin',"wb")
        file.write(bytearray([i for i in retlist]))
        file.close()
        