import binascii
import os

# This utility dumps the Unifont to raw binary data for putting on SPI flash.
# The output is explicitly different from the Arduino code generator; Namely:
#  * all tables are the same size (8192 bytes of glyph data + 32 bytes of length bitmask).
#  * the five exclusively single-width tables, however, still obey the rules for 
#    single-wide tables, not variable width tables.
#  * Specifically, the characters are not padded with zeroes. Instead, the table all fits
#    in the first 4096 bytes, and is padded with 4096 zeroes at the end.
#  * All blocks are followed by 32 bytes of length data, even the ones that are constant
#    width. This is so that all tables will be the same length.
#  * Tables start at block 01; it's assumed that block 00 is always in program memory.
# As I write these comments I'm assuming this code is going to be a mess too! Making this
# script clean and pretty is a distant future goal, for now I just want to get a bin file
# to hack on.

stop_at = 0x100
filepath = 'unifont.hex'
outpath = 'unifont.bin'
shortblocks = [0x00, 0x01, 0x02, 0x1E, 0x1F, 0x28]

with open(filepath) as fp:
    outfile = open(outpath, 'w')
    line = fp.readline()
    currentBlock = None
    blockStarted = None
    lastCharacter = None
    hasSingleWideCharacters = False
    hasDoubleWideCharacters = False
    blocks = dict()
    widthMode = dict()
    widths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while line:
        line = fp.readline().strip().split(":")
        if len(line) < 2:
            break
        codepoint = line[0]
        data = line[1]
        blockNum = codepoint[:2]
        if int(blockNum, 16) == 0:
            print("skipping block 0")
            continue
        idx = codepoint[2:]
        if currentBlock != blockNum:
            if hasSingleWideCharacters and hasDoubleWideCharacters:
                widthMode[currentBlock] = 0
            elif hasSingleWideCharacters:
                widthMode[currentBlock] = 1
            elif hasDoubleWideCharacters:
                widthMode[currentBlock] = 2

            if currentBlock is not None:
                if int(currentBlock, 16) in shortblocks:
                    for i in range(0, 4096):
                        outfile.write(binascii.unhexlify('00'))
                if int(currentBlock, 16) <= stop_at:
                    outfile.write(bytearray(widths))
                    outfile.flush()
                    print("At block {}".format(currentBlock))
                    print(os.fstat(outfile.fileno()).st_size)
                    print(os.fstat(outfile.fileno()).st_size % 8224)
                if False:
                    print("static const uint8_t block_{}_widths[] PROGMEM = {{{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}}};\n".format(currentBlock, widths[0], widths[1], widths[2], widths[3], widths[4], widths[5], widths[6], widths[7], widths[8], widths[9], widths[10], widths[11], widths[12], widths[13], widths[14], widths[15], widths[16], widths[17], widths[18], widths[19], widths[20], widths[21], widths[22], widths[23], widths[24], widths[25], widths[26], widths[27], widths[28], widths[29], widths[30], widths[31]))
                blocks[currentBlock] = blockStarted
                widths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            currentBlock = blockNum
            blockStarted = idx
            hasSingleWideCharacters = False
            hasDoubleWideCharacters = False
        if data[:8] == "00007FFE":
            if int(blockNum, 16) <= stop_at:
              if int(blockNum, 16) in shortblocks:
                  for i in range(0, 16):
                      outfile.write(binascii.unhexlify('FF'))
              else:
                  for i in range(0, 32):
                      outfile.write(binascii.unhexlify('FF'))
            hasSingleWideCharacters = True
        elif data[:8] == "AAAA0001":
            if int(blockNum, 16) <= stop_at:
                if int(blockNum, 16) in shortblocks:
                    for i in range(0, 16):
                        outfile.write(binascii.unhexlify('00'))
                else:
                    for i in range(0, 32):
                        outfile.write(binascii.unhexlify('00'))
            hasSingleWideCharacters = True
        elif len(data) > 32:
            if int(blockNum, 16) <= stop_at:
                outfile.write(binascii.unhexlify(data[0:2]))
                outfile.write(binascii.unhexlify(data[2:4]))
                outfile.write(binascii.unhexlify(data[4:6]))
                outfile.write(binascii.unhexlify(data[6:8]))
                outfile.write(binascii.unhexlify(data[8:10]))
                outfile.write(binascii.unhexlify(data[10:12]))
                outfile.write(binascii.unhexlify(data[12:14]))
                outfile.write(binascii.unhexlify(data[14:16]))
                outfile.write(binascii.unhexlify(data[16:18]))
                outfile.write(binascii.unhexlify(data[18:20]))
                outfile.write(binascii.unhexlify(data[20:22]))
                outfile.write(binascii.unhexlify(data[22:24]))
                outfile.write(binascii.unhexlify(data[24:26]))
                outfile.write(binascii.unhexlify(data[26:28]))
                outfile.write(binascii.unhexlify(data[28:30]))
                outfile.write(binascii.unhexlify(data[30:32]))
                outfile.write(binascii.unhexlify(data[32:34]))
                outfile.write(binascii.unhexlify(data[34:36]))
                outfile.write(binascii.unhexlify(data[36:38]))
                outfile.write(binascii.unhexlify(data[38:40]))
                outfile.write(binascii.unhexlify(data[40:42]))
                outfile.write(binascii.unhexlify(data[42:44]))
                outfile.write(binascii.unhexlify(data[44:46]))
                outfile.write(binascii.unhexlify(data[46:48]))
                outfile.write(binascii.unhexlify(data[48:50]))
                outfile.write(binascii.unhexlify(data[50:52]))
                outfile.write(binascii.unhexlify(data[52:54]))
                outfile.write(binascii.unhexlify(data[54:56]))
                outfile.write(binascii.unhexlify(data[56:58]))
                outfile.write(binascii.unhexlify(data[58:60]))
                outfile.write(binascii.unhexlify(data[60:62]))
                outfile.write(binascii.unhexlify(data[62:64]))
            hasDoubleWideCharacters = True
            charIndex = int(idx, 16)
            widths[charIndex / 8] |= 1 << (7 - charIndex % 8)
        else:
            if int(blockNum, 16) <= stop_at:
                if int(blockNum, 16) in shortblocks:
                    outfile.write(binascii.unhexlify(data[0:2]))
                    outfile.write(binascii.unhexlify(data[2:4]))
                    outfile.write(binascii.unhexlify(data[4:6]))
                    outfile.write(binascii.unhexlify(data[6:8]))
                    outfile.write(binascii.unhexlify(data[8:10]))
                    outfile.write(binascii.unhexlify(data[10:12]))
                    outfile.write(binascii.unhexlify(data[12:14]))
                    outfile.write(binascii.unhexlify(data[14:16]))
                    outfile.write(binascii.unhexlify(data[16:18]))
                    outfile.write(binascii.unhexlify(data[18:20]))
                    outfile.write(binascii.unhexlify(data[20:22]))
                    outfile.write(binascii.unhexlify(data[22:24]))
                    outfile.write(binascii.unhexlify(data[24:26]))
                    outfile.write(binascii.unhexlify(data[26:28]))
                    outfile.write(binascii.unhexlify(data[28:30]))
                    outfile.write(binascii.unhexlify(data[30:32]))
                else:
                    outfile.write(binascii.unhexlify(data[0:2]))
                    outfile.write(binascii.unhexlify(data[2:4]))
                    outfile.write(binascii.unhexlify(data[4:6]))
                    outfile.write(binascii.unhexlify(data[6:8]))
                    outfile.write(binascii.unhexlify(data[8:10]))
                    outfile.write(binascii.unhexlify(data[10:12]))
                    outfile.write(binascii.unhexlify(data[12:14]))
                    outfile.write(binascii.unhexlify(data[14:16]))
                    outfile.write(binascii.unhexlify(data[16:18]))
                    outfile.write(binascii.unhexlify(data[18:20]))
                    outfile.write(binascii.unhexlify(data[20:22]))
                    outfile.write(binascii.unhexlify(data[22:24]))
                    outfile.write(binascii.unhexlify(data[24:26]))
                    outfile.write(binascii.unhexlify(data[26:28]))
                    outfile.write(binascii.unhexlify(data[28:30]))
                    outfile.write(binascii.unhexlify(data[30:32]))
                    for i in range(0, 16):
                        outfile.write(binascii.unhexlify('00'))
            hasSingleWideCharacters = True

    # U+FFFE and U+FFFE are not valid, this is just to push the widths out to where we want them.
    for i in range(0, 64):
        outfile.write(binascii.unhexlify('FF'))
    if int(blockNum, 16) <= stop_at:
        outfile.write(bytearray(widths))
        outfile.flush()
        print("At block {}".format(currentBlock))
        print(os.fstat(outfile.fileno()).st_size)
        print(os.fstat(outfile.fileno()).st_size % 8224)
