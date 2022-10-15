from array import array
import os, glob, shutil
iconnamelist = ['l_', 'p_', 'sla_', 'sprt_', 'vs_']
baseiconlist = ['base\\ui\\flash\\OTHER\\charicon_l\\', 'base\\ui\\flash\\OTHER\\charicon_p\\', 'base\\ui\\flash\\OTHER\\charicon_sla\\', 'base\\ui\\flash\\OTHER\\charicon_sprt\\', 'base\\ui\\flash\\OTHER\\charicon_vs\\']
newiconlist = ['output\\ui\\flash\\OTHER\\charicon_l\\', 'output\\ui\\flash\\OTHER\\charicon_p\\', 'output\\ui\\flash\\OTHER\\charicon_sla\\', 'output\\ui\\flash\\OTHER\\charicon_sprt\\', 'output\\ui\\flash\\OTHER\\charicon_vs\\']
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

def write_png_to_xfbin(pngpath: str, xfbinpath: str):
        file = open(xfbinpath + '.xfbin',"rb")
        file_size = os.path.getsize(xfbinpath + '.xfbin')
        numbers = list(file.read(file_size))
        pngoffset = find_pngoffset(numbers, file_size)
        filesize1offset = pngoffset - 4
        filesize2offset = pngoffset - 16
        png = open(pngpath + '.png',"rb")
        png_size = os.path.getsize(pngpath + '.png')
        pnglist = list(png.read(png_size))
        retlist = []
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
        file = open(xfbinpath + '.xfbin',"wb")
        file.write(bytearray([i for i in retlist]))
        file.close()

def change_xfbin_name(xfbinpath: str, newname: str, iconname: str):
    file = open(xfbinpath, "rb")
    file_size = os.path.getsize(xfbinpath)
    gamelist = list(file.read(file_size))
    namearr = [int(newname[x].encode('ansi').hex(), 16) for x in range(0, len(newname))]
    retlist = []
    match iconname:
        case 'l':
            for x in range(0, len(gamelist)):
                if (155 <= x <= 158):
                    retlist.append(namearr[x - 155])
                elif (167 <= x <= 170):
                    retlist.append(namearr[x - 167])
                else:
                    retlist.append(gamelist[x])
        case 'p':
            for x in range(0, len(gamelist)):
                
                if (155 <= x <= 158):
                    retlist.append(namearr[x - 155])
                elif (167 <= x <= 170):
                    retlist.append(namearr[x - 167])
                else:
                    retlist.append(gamelist[x])
        case 'sla':
            for x in range(0, len(gamelist)):
                if (159 <= x <= 162):
                    retlist.append(namearr[x - 159])
                elif (173 <= x <= 176):
                    retlist.append(namearr[x - 173])
                else:
                    retlist.append(gamelist[x])
        case 'sprt':
            for x in range(0, len(gamelist)):
                if (161 <= x <= 164):
                    retlist.append(namearr[x - 161])
                elif (176 <= x <= 179):
                    retlist.append(namearr[x - 176])
                else:
                    retlist.append(gamelist[x])
        case 'vs':
            for x in range(0, len(gamelist)):
                if (157 <= x <= 160):
                    retlist.append(namearr[x - 157])
                elif (170 <= x <= 173):
                    retlist.append(namearr[x - 170])
                else:
                    retlist.append(gamelist[x])
        
    file.close()
    file = open(xfbinpath, "wb")
    file.write(bytearray([i for i in retlist]))
    file.close()

if __name__ == '__main__':
    pngfilelist = glob.glob("input\\" + "*.png")
    namelist = []
    nameset = set()
    for x in pngfilelist:
        nameset.add(os.path.splitext(x)[0][6:])
    print('Starting operation')
    for n in nameset:
        for i in range(0, len(iconnamelist)):
            if n.startswith(iconnamelist[i]) and len(n.split('_')[1]) == 4:
                shutil.copy(os.getcwd() + '\\' + baseiconlist[i] + iconnamelist[i] + 'base.xfbin', newiconlist[i] + iconnamelist[i] + n.split('_')[1] + '.xfbin')
                write_png_to_xfbin("input\\" + n, os.getcwd() + '\\' + newiconlist[i] + iconnamelist[i] + n.split('_')[1])
                change_xfbin_name(newiconlist[i] + iconnamelist[i] + n.split('_')[1] + '.xfbin', n.split('_')[1], iconnamelist[i][:-1])
    print('The operation was completed!')