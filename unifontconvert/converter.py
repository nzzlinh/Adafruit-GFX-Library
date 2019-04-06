import binascii

class UnicodeBlock:
    def __init__(self, block_number):
        self.number = int(block_number, 16)
        self.include_in_progmem = block_number == '00'
        self.is_short_block = block_number in short_blocks
        self.glyphs = list()
        self.block_width_mode = None
        self.has_nonspacing_marks = False
        self.widths = [0] * 32
        self.spacings = [0] * 32
        
    def flags(self):
        flags = 0
        if self.include_in_progmem:
            flags |= 1
        if self.is_short_block:
            flags |= 1 << 1
        if self.block_width_mode == 2:
            flags |= 1 << 2
        if self.has_nonspacing_marks:
            flags |= 1 << 3
        return flags

    def __repr__(self):
        return "\nBlock {}: {} {} glyphs with width mode {}\nWidth:   {}\nSpacing: {}".format(hex(self.number)[2:].upper(), bin(self.flags()), len(self.glyphs), self.block_width_mode, binascii.hexlify(bytearray(self.widths)), binascii.hexlify(bytearray(self.spacings)))


short_blocks = ["00", "01", "02", "1E", "1F", "28"]
nonspacing_codepoints = ["0300", "0301", "0302", "0303", "0304", "0305", "0306", "0307", "0308", "0309", "030A", "030B", "030C", "030D", "030E", "030F", "0310", "0311", "0312", "0313", "0314", "0315", "0316", "0317", "0318", "0319", "031A", "031B", "031C", "031D", "031E", "031F", "0320", "0321", "0322", "0323", "0324", "0325", "0326", "0327", "0328", "0329", "032A", "032B", "032C", "032D", "032E", "032F", "0330", "0331", "0332", "0333", "0334", "0335", "0336", "0337", "0338", "0339", "033A", "033B", "033C", "033D", "033E", "033F", "0340", "0341", "0342", "0343", "0344", "0345", "0346", "0347", "0348", "0349", "034A", "034B", "034C", "034D", "034E", "034F", "0350", "0351", "0352", "0353", "0354", "0355", "0356", "0357", "0358", "0359", "035A", "035B", "035C", "035D", "035E", "035F", "0360", "0361", "0362", "0363", "0364", "0365", "0366", "0367", "0368", "0369", "036A", "036B", "036C", "036D", "036E", "036F", "0483", "0484", "0485", "0486", "0487", "0488", "0489", "0591", "0592", "0593", "0594", "0595", "0596", "0597", "0598", "0599", "059A", "059B", "059C", "059D", "059E", "059F", "05A0", "05A1", "05A2", "05A3", "05A4", "05A5", "05A6", "05A7", "05A8", "05A9", "05AA", "05AB", "05AC", "05AD", "05AE", "05AF", "05B0", "05B1", "05B2", "05B3", "05B4", "05B5", "05B6", "05B7", "05B8", "05B9", "05BA", "05BB", "05BC", "05BD", "05BF", "05C1", "05C2", "05C4", "05C5", "05C7", "0610", "0611", "0612", "0613", "0614", "0615", "0616", "0617", "0618", "0619", "061A", "064B", "064C", "064D", "064E", "064F", "0650", "0651", "0652", "0653", "0654", "0655", "0656", "0657", "0658", "0659", "065A", "065B", "065C", "065D", "065E", "065F", "0670", "06D6", "06D7", "06D8", "06D9", "06DA", "06DB", "06DC", "06DF", "06E0", "06E1", "06E2", "06E3", "06E4", "06E7", "06E8", "06EA", "06EB", "06EC", "06ED", "0711", "0730", "0731", "0732", "0733", "0734", "0735", "0736", "0737", "0738", "0739", "073A", "073B", "073C", "073D", "073E", "073F", "0740", "0741", "0742", "0743", "0744", "0745", "0746", "0747", "0748", "0749", "074A", "07A6", "07A7", "07A8", "07A9", "07AA", "07AB", "07AC", "07AD", "07AE", "07AF", "07B0", "07EB", "07EC", "07ED", "07EE", "07EF", "07F0", "07F1", "07F2", "07F3", "07FD", "0816", "0817", "0818", "0819", "081B", "081C", "081D", "081E", "081F", "0820", "0821", "0822", "0823", "0825", "0826", "0827", "0829", "082A", "082B", "082C", "082D", "0859", "085A", "085B", "08D3", "08D4", "08D5", "08D6", "08D7", "08D8", "08D9", "08DA", "08DB", "08DC", "08DD", "08DE", "08DF", "08E0", "08E1", "08E3", "08E4", "08E5", "08E6", "08E7", "08E8", "08E9", "08EA", "08EB", "08EC", "08ED", "08EE", "08EF", "08F0", "08F1", "08F2", "08F3", "08F4", "08F5", "08F6", "08F7", "08F8", "08F9", "08FA", "08FB", "08FC", "08FD", "08FE", "08FF", "0900", "0901", "0902", "093A", "093C", "0941", "0942", "0943", "0944", "0945", "0946", "0947", "0948", "094D", "0951", "0952", "0953", "0954", "0955", "0956", "0957", "0962", "0963", "0981", "09BC", "09C1", "09C2", "09C3", "09C4", "09CD", "09E2", "09E3", "09FE", "0A01", "0A02", "0A3C", "0A41", "0A42", "0A47", "0A48", "0A4B", "0A4C", "0A4D", "0A51", "0A70", "0A71", "0A75", "0A81", "0A82", "0ABC", "0AC1", "0AC2", "0AC3", "0AC4", "0AC5", "0AC7", "0AC8", "0ACD", "0AE2", "0AE3", "0AFA", "0AFB", "0AFC", "0AFD", "0AFE", "0AFF", "0B01", "0B3C", "0B3F", "0B41", "0B42", "0B43", "0B44", "0B4D", "0B56", "0B62", "0B63", "0B82", "0BC0", "0BCD", "0C00", "0C04", "0C3E", "0C3F", "0C40", "0C46", "0C47", "0C48", "0C4A", "0C4B", "0C4C", "0C4D", "0C55", "0C56", "0C62", "0C63", "0C81", "0CBC", "0CCC", "0CCD", "0CE2", "0CE3", "0D00", "0D01", "0D3B", "0D3C", "0D41", "0D42", "0D43", "0D44", "0D4D", "0D62", "0D63", "0DCA", "0DD2", "0DD3", "0DD4", "0DD6", "0E31", "0E34", "0E35", "0E36", "0E37", "0E38", "0E39", "0E3A", "0E47", "0E48", "0E49", "0E4A", "0E4B", "0E4C", "0E4D", "0E4E", "0EB1", "0EB4", "0EB5", "0EB6", "0EB7", "0EB8", "0EB9", "0EBA", "0EBB", "0EBC", "0EC8", "0EC9", "0ECA", "0ECB", "0ECC", "0ECD", "0F18", "0F19", "0F35", "0F37", "0F39", "0F71", "0F72", "0F73", "0F74", "0F75", "0F76", "0F77", "0F78", "0F79", "0F7A", "0F7B", "0F7C", "0F7D", "0F7E", "0F80", "0F81", "0F82", "0F83", "0F84", "0F86", "0F87", "0F8D", "0F8E", "0F8F", "0F90", "0F91", "0F92", "0F93", "0F94", "0F95", "0F96", "0F97", "0F99", "0F9A", "0F9B", "0F9C", "0F9D", "0F9E", "0F9F", "0FA0", "0FA1", "0FA2", "0FA3", "0FA4", "0FA5", "0FA6", "0FA7", "0FA8", "0FA9", "0FAA", "0FAB", "0FAC", "0FAD", "0FAE", "0FAF", "0FB0", "0FB1", "0FB2", "0FB3", "0FB4", "0FB5", "0FB6", "0FB7", "0FB8", "0FB9", "0FBA", "0FBB", "0FBC", "0FC6", "102D", "102E", "102F", "1030", "1032", "1033", "1034", "1035", "1036", "1037", "1039", "103A", "103D", "103E", "1058", "1059", "105E", "105F", "1060", "1071", "1072", "1073", "1074", "1082", "1085", "1086", "108D", "109D", "135D", "135E", "135F", "1712", "1713", "1714", "1732", "1733", "1734", "1752", "1753", "1772", "1773", "17B4", "17B5", "17B7", "17B8", "17B9", "17BA", "17BB", "17BC", "17BD", "17C6", "17C9", "17CA", "17CB", "17CC", "17CD", "17CE", "17CF", "17D0", "17D1", "17D2", "17D3", "17DD", "180B", "180C", "180D", "1885", "1886", "18A9", "1920", "1921", "1922", "1927", "1928", "1932", "1939", "193A", "193B", "1A17", "1A18", "1A1B", "1A56", "1A58", "1A59", "1A5A", "1A5B", "1A5C", "1A5D", "1A5E", "1A60", "1A62", "1A65", "1A66", "1A67", "1A68", "1A69", "1A6A", "1A6B", "1A6C", "1A73", "1A74", "1A75", "1A76", "1A77", "1A78", "1A79", "1A7A", "1A7B", "1A7C", "1A7F", "1AB0", "1AB1", "1AB2", "1AB3", "1AB4", "1AB5", "1AB6", "1AB7", "1AB8", "1AB9", "1ABA", "1ABB", "1ABC", "1ABD", "1ABE", "1B00", "1B01", "1B02", "1B03", "1B34", "1B36", "1B37", "1B38", "1B39", "1B3A", "1B3C", "1B42", "1B6B", "1B6C", "1B6D", "1B6E", "1B6F", "1B70", "1B71", "1B72", "1B73", "1B80", "1B81", "1BA2", "1BA3", "1BA4", "1BA5", "1BA8", "1BA9", "1BAB", "1BAC", "1BAD", "1BE6", "1BE8", "1BE9", "1BED", "1BEF", "1BF0", "1BF1", "1C2C", "1C2D", "1C2E", "1C2F", "1C30", "1C31", "1C32", "1C33", "1C36", "1C37", "1CD0", "1CD1", "1CD2", "1CD4", "1CD5", "1CD6", "1CD7", "1CD8", "1CD9", "1CDA", "1CDB", "1CDC", "1CDD", "1CDE", "1CDF", "1CE0", "1CE2", "1CE3", "1CE4", "1CE5", "1CE6", "1CE7", "1CE8", "1CED", "1CF4", "1CF8", "1CF9", "1DC0", "1DC1", "1DC2", "1DC3", "1DC4", "1DC5", "1DC6", "1DC7", "1DC8", "1DC9", "1DCA", "1DCB", "1DCC", "1DCD", "1DCE", "1DCF", "1DD0", "1DD1", "1DD2", "1DD3", "1DD4", "1DD5", "1DD6", "1DD7", "1DD8", "1DD9", "1DDA", "1DDB", "1DDC", "1DDD", "1DDE", "1DDF", "1DE0", "1DE1", "1DE2", "1DE3", "1DE4", "1DE5", "1DE6", "1DE7", "1DE8", "1DE9", "1DEA", "1DEB", "1DEC", "1DED", "1DEE", "1DEF", "1DF0", "1DF1", "1DF2", "1DF3", "1DF4", "1DF5", "1DF6", "1DF7", "1DF8", "1DF9", "1DFB", "1DFC", "1DFD", "1DFE", "1DFF", "20D0", "20D1", "20D2", "20D3", "20D4", "20D5", "20D6", "20D7", "20D8", "20D9", "20DA", "20DB", "20DC", "20DD", "20DE", "20DF", "20E0", "20E1", "20E2", "20E3", "20E4", "20E5", "20E6", "20E7", "20E8", "20E9", "20EA", "20EB", "20EC", "20ED", "20EE", "20EF", "20F0", "2CEF", "2CF0", "2CF1", "2D7F", "2DE0", "2DE1", "2DE2", "2DE3", "2DE4", "2DE5", "2DE6", "2DE7", "2DE8", "2DE9", "2DEA", "2DEB", "2DEC", "2DED", "2DEE", "2DEF", "2DF0", "2DF1", "2DF2", "2DF3", "2DF4", "2DF5", "2DF6", "2DF7", "2DF8", "2DF9", "2DFA", "2DFB", "2DFC", "2DFD", "2DFE", "2DFF", "302A", "302B", "302C", "302D", "3099", "309A", "A66F", "A670", "A671", "A672", "A674", "A675", "A676", "A677", "A678", "A679", "A67A", "A67B", "A67C", "A67D", "A69E", "A69F", "A6F0", "A6F1", "A802", "A806", "A80B", "A825", "A826", "A8C4", "A8C5", "A8E0", "A8E1", "A8E2", "A8E3", "A8E4", "A8E5", "A8E6", "A8E7", "A8E8", "A8E9", "A8EA", "A8EB", "A8EC", "A8ED", "A8EE", "A8EF", "A8F0", "A8F1", "A8FF", "A926", "A927", "A928", "A929", "A92A", "A92B", "A92C", "A92D", "A947", "A948", "A949", "A94A", "A94B", "A94C", "A94D", "A94E", "A94F", "A950", "A951", "A980", "A981", "A982", "A9B3", "A9B6", "A9B7", "A9B8", "A9B9", "A9BC", "A9BD", "A9E5", "AA29", "AA2A", "AA2B", "AA2C", "AA2D", "AA2E", "AA31", "AA32", "AA35", "AA36", "AA43", "AA4C", "AA7C", "AAB0", "AAB2", "AAB3", "AAB4", "AAB7", "AAB8", "AABE", "AABF", "AAC1", "AAEC", "AAED", "AAF6", "ABE5", "ABE8", "ABED", "FB1E", "FE00", "FE01", "FE02", "FE03", "FE04", "FE05", "FE06", "FE07", "FE08", "FE09", "FE0A", "FE0B", "FE0C", "FE0D", "FE0E", "FE0F", "FE20", "FE21", "FE22", "FE23", "FE24", "FE25", "FE26", "FE27", "FE28", "FE29", "FE2A", "FE2B", "FE2C", "FE2D", "FE2E", "FE2F"]

blocks = dict()
current_block = None
has_single_width_glyphs = False
has_double_width_glyphs = False

for line in open('unifont.hex', 'r'):
    line = line.strip().split(":")
    if len(line) < 2:
        break
    codepoint = line[0]
    data = line[1]
    block_name = codepoint[:2]
    char_hex = codepoint[2:]
    char_num = int(char_hex, 16)

    # handle moving to the next block
    if block_name not in blocks:
        # do housekeeping on the block we just closed
        if current_block is not None:
            if current_block.is_short_block:
                # hard-coded from experience, only six blocks are exclusively single-width
                # the conditional would be: if has_single_width_glyphs and not has_double_width_glyphs
                current_block.block_width_mode = 1
            elif has_single_width_glyphs and has_double_width_glyphs:
                current_block.block_width_mode = 0
            else:
                current_block.block_width_mode = 2
        # now create the new block and clear previous state
        blocks[block_name] = UnicodeBlock(block_name)
        current_block = blocks[block_name]
        has_single_width_glyphs = False
        has_double_width_glyphs = False

    if data[:8] == "00007FFE":
        if current_block.is_short_block:
            current_block.glyphs.append(bytearray(b'\xff') * 16)
        else:
            current_block.glyphs.append(bytearray(b'\xff') * 32)
    elif data[:8] == "AAAA0001":
        if current_block.is_short_block:
            current_block.glyphs.append(bytearray(b'\x00') * 16)
        else:
            current_block.glyphs.append(bytearray(b'\x00') * 32)
    else:
        current_block.glyphs.append(bytes.fromhex(data))
    if len(data) > 32:
        has_double_width_glyphs = True
        current_block.widths[char_num // 8] |= 1 << (7 - char_num % 8)
    else:
        has_single_width_glyphs = True

    if codepoint in nonspacing_codepoints:
        current_block.has_nonspacing_marks = True
    else:
        current_block.spacings[char_num // 8] |= 1 << (7 - char_num % 8)

# block FF needs two more glyphs to make all the tables the same length.
current_block.glyphs.append(bytearray(b'\xff') * 32)
current_block.glyphs.append(bytearray(b'\xff') * 32)
# finally the little bit of housekeeping we missed on the last iteration of the loop:
current_block.spacings[31] |= 1 << 1
current_block.spacings[31] |= 1
current_block.block_width_mode = 0

def toggle_progmem_blocks():
    done = False
    while not done:
        for block_name in blocks:
            block = blocks[block_name]
            print("{}: {}".format(block_name, '✅' if block.include_in_progmem else '❌'), end = '\t')
            if (block.number + 1) % 16 == 0:
                print()
        block_to_toggle = input("Toggle which block? ('done' when finished) ").upper()
        # add leading zero if it was missing
        if len(block_to_toggle) == 1:
            block_to_toggle = "0{}".format(block_to_toggle)
        if block_to_toggle == '00':
            print("Block 00 must always reside in PROGMEM.")
        elif block_to_toggle == 'DONE':
            return
        elif block_to_toggle not in blocks:
            print("Invalid block.")
        else:
            blocks[block_to_toggle].include_in_progmem ^= True

def generate_unifont_c():
    outfile = open('glcdfont.c', 'w')
    print("""#ifndef FONT8x16_H
#define FONT8x16_H

#ifdef __AVR__
 #include <avr/io.h>
 #include <avr/pgmspace.h>
#elif defined(ESP8266)
 #include <pgmspace.h>
#else
 #define PROGMEM
#endif

#include <stdint.h>

// GNU Unifont 8x16 font

#define UNIFONT_BLOCK_IN_PROGMEM (1)
#define UNIFONT_BLOCK_IS_NARROW (1<<1)
#define UNIFONT_BLOCK_IS_WIDE (1<<2)
#define UNIFONT_BLOCK_HAS_NON_SPACING_MARKS (1<<3)

#define UNIFONT_NARROW_BLOCK_LENGTH (4096)
#define UNIFONT_WIDE_BLOCK_LENGTH (8192)
#define UNIFONT_BITMASK_LENGTH (32)

typedef union {
    const uint8_t* location;
    const int32_t offset;
} UnifontLocation;

typedef struct {
       const UnifontLocation glyphs;// If low bit of flags is set, use the location pointer.
                                    // Otherwise, use the offset and look in the unifont.bin file.
       const uint8_t flags;         // 0b0000xxxx
                                    //       |||\_ This block is included in PROGMEM
                                    //       ||\__ This block contains exclusively narrow (16-byte) glyphs
                                    //       |\___ This block contains exclusively wide (32-byte) glyphs
                                    //       |     (if both of these are 0, all glyphs are 32 bytes but some are
                                    //       |      half-width, check width bitmasks after glyph data for advance)
                                    //       \____ This block contains non-spacing code points
                                    //             (check spacing data after length data to determine advance)

} UnifontBlock;

""", file=outfile)
    for block_name in blocks:
        block = blocks[block_name]
        if block.include_in_progmem:
            print("static const uint8_t block_{}_data[] PROGMEM = {{".format(block_name), file=outfile)
            char_num = 0
            for glyph in block.glyphs:
                if block_name == '00' and char_num < 0x20:
                    char_num += 1
                    continue
                glyph_text = binascii.hexlify(glyph).decode('ascii').upper()
                bytes = [glyph_text[i:i+2] for i in range(0, len(glyph_text), 2)]
                print("    ", end='', file=outfile)
                for byte in bytes:
                    print("0x{}".format(byte), end=", ", file=outfile)
                if len(glyph) < 32 and block.block_width_mode == 0:
                    # it's a waste of space but we have to pad out these blocks so they're easily indexed.
                    for i in range(0, 16):
                        print("0x00", end=", ", file=outfile)
                print(" // Code point {}{:02X}".format(block_name, char_num), file=outfile)
                char_num += 1
            if block.has_nonspacing_marks or block.block_width_mode == 0:
                # we need to include both widths and spacing if either need to be consulted
                print("\n    // Character spacing bitmasks\n    ", end='', file=outfile)
                for spacing in block.spacings:
                    print("0x{:02X}".format(spacing), end=", ", file=outfile)
                print("    // Character width bitmasks\n    ", end='', file=outfile)
                for width in block.widths:
                    print("0x{:02X}".format(width), end=", ", file=outfile)
            print("\n};\n", file=outfile)

    print("\nconst UnifontBlock Unifont[] PROGMEM = {", file=outfile)
    offset = 900
    for block_name in blocks:
        block = blocks[block_name]
        print("    {", end='', file=outfile)
        if block.include_in_progmem:
            print("block_{}_data, ".format(block_name), end='', file=outfile)
        else:
            print("(const unsigned char*){}, ".format(offset), end='', file=outfile)
        print("{:#010b}}},".format(block.flags()), end='', file=outfile)
        print(" // Block {}".format(block_name), file=outfile)
        if block.is_short_block:
            offset += 4096 + 64
        else:
            offset += 8192 + 64
    print("};", file=outfile)
    print("\n#endif // FONT8x16_H", file=outfile)


def generate_unifont_bin():
    output = bytearray()

    # Global Font Header
    output.append(0)           # Reserved byte
    output.append(0)           # Reserved byte
    output.append(8)           # Glyph width in pixels
    output.append(16)          # Glyph height in pixels
    output.append(1)           # Flags. 0b00000001 indicates the presence of double-width glyphs.
    output.append(2)           # Number of bitmasks per block. We have two.
    output.append(len(blocks)) # Number of blocks in font, lower byte of two-byte short.
    output.append(0)           # upper byte of numBlocks

    # Block Headers
    for block_name in blocks:
        block = blocks[block_name]
        output.append(block.number) # Unicode block number within plane.
        output.append(0)            # Unicode plane number. This script only handles Plane 0.
        flags = 0
        if block.has_nonspacing_marks:
            flags |= 1
        if block.block_width_mode == 1:
            flags |= 2
        elif block.block_width_mode == 2:
            flags |= 4
        output.append(flags)        # Flags for this block.
        output.append(0)            # Reserved for future use.

    # Font Data
    for block_name in blocks:
        block = blocks[block_name]
        for glyph in block.glyphs:
            output += glyph
            if len(glyph) < 32 and block.block_width_mode == 0:
                orig_len = len(output)
                for i in range(0, 16):
                    output += b'\x00'
        output += bytearray(block.spacings)
        output += bytearray(block.widths)
    outfile = open('unifont.bin', 'wb')
    outfile.write(output)

while 1:
    print("\033[;1mUnifont Converter\033[0;0m\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")
    print("Commands:")
    print("\t1. Print block information")
    print("\t2. Select blocks to include in glcdfont.c")
    print("\t3. Generate glcdfont.c")
    print("\t4. Generate unifont.bin")
    print("\tQ. Quit")
    command = input("What do you want to do? ")
    if command == '1':
        for block_name in blocks:
            print(blocks[block_name])
        print("\nLoaded data for {} blocks.\n\n".format(len(blocks)))
    elif command == '2':
        toggle_progmem_blocks()
    elif command == '3':
        generate_unifont_c()
    elif command == '4':
        generate_unifont_bin()
    elif command.upper() == 'Q':
        exit(0)

