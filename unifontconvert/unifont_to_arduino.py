# This utility dumps Unifont data to code suitable for use on the Arduino.
# It's a mess! Evolved into spaghetti along with my theories on how to make this work.
# The gist: set stop_at to the last page you want to include in your program memory.
# Above stop_at, the output will include a null pointer for each additional page, as well
# as a width mode of 1, 2 or 0 for pages that are entirely single-wide, entirely double-
# wide, or require lookup from the width tables in the flash memory (TODO!)
stop_at = 0x10
filepath = 'unifont.hex'
shortblocks = [0x00, 0x01, 0x02, 0x1E, 0x1F, 0x28]

print("typedef struct {\n       const unsigned char* glyphs; ///< beginning of the font data\n       const uint8_t* width;       ///< TEMPORARY: 1 or 2 for single or double width, or a pointer to bitmasks indicating which glyphs are double-wide.\n} UnifontBlock;\n")
with open(filepath) as fp:
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
        idx = codepoint[2:]
        if lastCharacter is not None and int(idx, 16) > lastCharacter + 1:
            print("// WE ARE MISSING SOME CODEPOINTS HERE")
        if currentBlock != blockNum:
            if hasSingleWideCharacters and hasDoubleWideCharacters:
                widthMode[currentBlock] = 0
            elif hasSingleWideCharacters:
                widthMode[currentBlock] = 1
            elif hasDoubleWideCharacters:
                widthMode[currentBlock] = 2

            if currentBlock is not None:
                if int(currentBlock, 16) <= stop_at:
                    print("};")
                if hasSingleWideCharacters and hasDoubleWideCharacters and int(currentBlock, 16) <= stop_at:
                    print("static const uint8_t block_{}_widths[] PROGMEM = {{{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}}};\n".format(currentBlock, widths[0], widths[1], widths[2], widths[3], widths[4], widths[5], widths[6], widths[7], widths[8], widths[9], widths[10], widths[11], widths[12], widths[13], widths[14], widths[15], widths[16], widths[17], widths[18], widths[19], widths[20], widths[21], widths[22], widths[23], widths[24], widths[25], widths[26], widths[27], widths[28], widths[29], widths[30], widths[31]))
                blocks[currentBlock] = blockStarted
                widths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            currentBlock = blockNum
            blockStarted = idx
            if int(blockNum, 16) <= stop_at:
                print("\n// starts at {}".format(blockStarted))
                print("static const unsigned char block_{}_data[] PROGMEM = {{".format(currentBlock))
            hasSingleWideCharacters = False
            hasDoubleWideCharacters = False
        if data[:8] == "00007FFE":
            if int(blockNum, 16) <= stop_at:
              if int(blockNum, 16) in shortblocks:
                  print("    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, // Codepoint {} is reserved or does not have a visible representation".format(codepoint))
              else:
                  print("    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, // Codepoint {} is reserved or does not have a visible representation".format(codepoint))
            hasSingleWideCharacters = True
        elif data[:8] == "AAAA0001":
            if int(blockNum, 16) <= stop_at:
                if int(blockNum, 16) == 0 and int(codepoint, 16) < 0x20:
                    print("    // Special handling for block 0: skipping control character glyph {}".format(codepoint))
                else:
                    if int(blockNum, 16) in shortblocks:
                        print("    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // Codepoint {} appears to be a control character".format(codepoint))
                    else:
                        print("    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // Codepoint {} appears to be a control character".format(codepoint))
            hasSingleWideCharacters = True
        elif len(data) > 32:
            if int(blockNum, 16) <= stop_at:
                print("    0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, // Codepoint {} (double width)".format(data[0:2], data[2:4], data[4:6], data[6:8], data[8:10], data[10:12], data[12:14], data[14:16], data[16:18], data[18:20], data[20:22], data[22:24], data[24:26], data[26:28], data[28:30], data[30:32], data[32:34], data[34:36], data[36:38], data[38:40], data[40:42], data[42:44], data[44:46], data[46:48], data[48:50], data[50:52], data[52:54], data[54:56], data[56:58], data[58:60], data[60:62], data[62:64], codepoint))
            hasDoubleWideCharacters = True
            charIndex = int(idx, 16)
            widths[charIndex / 8] |= 1 << (7 - charIndex % 8)
        else:
            if int(blockNum, 16) <= stop_at:
                if int(blockNum, 16) in shortblocks:
                    print("    0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, // Codepoint {}".format(data[0:2], data[2:4], data[4:6], data[6:8], data[8:10], data[10:12], data[12:14], data[14:16], data[16:18], data[18:20], data[20:22], data[22:24], data[24:26], data[26:28], data[28:30], data[30:32], codepoint))
                else:
                    print("    0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x{}, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // Codepoint {}".format(data[0:2], data[2:4], data[4:6], data[6:8], data[8:10], data[10:12], data[12:14], data[14:16], data[16:18], data[18:20], data[20:22], data[22:24], data[24:26], data[26:28], data[28:30], data[30:32], codepoint))
            hasSingleWideCharacters = True

    if int(blockNum, 16) <= stop_at:
        print("};\n")
    # TODO: Widths and such
    print("\nconst UnifontBlock Unifont[] PROGMEM = {")
    for key in sorted(blocks.keys()):
        if int(key, 16) <= stop_at:
            print("    {{block_{}_data, {}}},".format(key, "block_{}_widths".format(key) if widthMode[key] == 0 else "(const uint8_t*){}".format(widthMode[key])))
        else:
            print("    {{(const unsigned char*)0, {}}},".format("(const uint8_t*){}".format(widthMode[key])))

    print("};")
