# The unifont.bin File Format

Up to April of 2019 the unifont.bin file was just a straight concatenation of glyph data and width bitmasks, with indexes into the file hard-coded in `glcdfont.c`. In the interest of making this format more general and future-proof, I'm adopting a more specific format that people can use to encode other Unicode fonts for microcontrollers. This document outlines that format.

## Bytes `0` through `7`: Font Header

This section describes global information about the font. Values are unsigned decimal integers unless hex or binary notation is given.

| Offset | Length | Typical Value | Contents |
|--------|--------|---------------|----------|
| 0      | 2      | 0x0000        | **Reserved**: two zero bytes. CircuitPython looks for width and height in these fields; `00 00` can serve as an indicator that this is a Unicode font, or we can use this for something else later. |
| 2      | 1      | 8             | Width of a standard-sized glyph. Marked as _w_ in the tables below. For the moment, the only supported value is 8. |
| 3      | 1      | 16            | Height of a standard-sized glyph. Marked as _h_ in the tables below. For the moment, the only supported value is 16. |
| 4      | 1      | 0b00000001    | Font-wide flags. Currently only the least significant bit matters: if flags & 1, the font has both single- and double-width glyphs, and a _multiplier_ of 2 is applied to any blocks that are not exclusively single-width. |
| 5      | 1      | 2             | Number of bitmasks (_numBitmasks_) available for each block. At the end of each block's glyph data, there are this many 32-byte (256-bit) bitmasks that describe some attribute of every character in the font. Currently we have two bitmasks at the end: whether the codepoint is a non-spacing mark, and whether it should be treated as a double-wide glyph. |
| 6      | 2      | 223           | Number of blocks included in this file. Marked as _numBlocks_ in the following tables. |
| 8      | -      | -             | End of font header. |

## Bytes 8 through the start of font data : Block Headers

Each entry in this section is four bytes long and encodes information about the Unicode block that resides at this index.

| Offset              | Length | Typical Value | Contents |
|---------------------|--------|---------------|----------|
| 8                   | 1      | 0x00 or 0x01  | The Unicode plane for the block at this index. The Basic Multilingual Plane is Plane 0; the Supplementary Multilingual Plane is 1. For example, the block "Braille Patterns" (U+2800 - U+28FF) would have 0x00 in this field, whereas the emojis in U+1F300 to U+1F3FF would have 0x01. |
| 9                   | 1      | 0x00 - 0xFF   | The Unicode block at this index. For example, the block "Braille Patterns" (U+2800 - U+28FF) would have 0x28 in this field. |
| 10                  | 1      | 0b00000???    | Flags specific to this block. See Flags below. |
| 11                  | 1      | 0             | **Reserved for future use.** This wastes about 223 bytes but leaves plenty of room to expand in the future if need be. |
| ...                 | ...    | ...           | ... |
| 8 + (numBlocks * 4) | -      | -             | End of block headers, start of font data. |

### Flags

The flags byte encodes information that applies to the entire block. Currently four flags are defined:

| Flag position     | Meaning |
|-------------------|---------|
| 0b00000001 (1<<0) | This block contains non-spacing marks. You will need to check the spacing table to determine whether to advance. |
| 0b00000010 (1<<1) | This block contains exclusively single-width glyphs. You do not need to check the widths table; all spacing characters advance by _w_ pixels. |
| 0b00000100 (1<<2) | This block contains exclusively double-width glyphs. You do not need to check the widths table; all spacing characters advance by _w * multiplier_ pixels . |
| 0b10000000 (1<<7) | **Reserved for internal use** once the font metadata is loaded into memory. Its value will be discarded but should be set to 0. |

If both of the width flags are 0 (i.e. 0b00000000), the block contains a mixture of single- and double-width glyphs. You will need to check the width bitmasks at the end of the file to determine the appropriate advance.

It is an invalid condition for both of the width flags to be 1 (i.e. 0b00000110); implementations may choose to silently ignore codepoints in blocks configured this way.

# The Font Data

The font data. This is simply a concatenation of 256 glyphs per block for each of the blocks, with _numBitmasks_ bitmasks at the end of each. For exclusively single-width blocks, a character is `w\*h/8` bytes long (16 bytes for Unifont). For double- or mixed-width blocks, a character is `w\*h\*multiplier/8` bytes (for Unifont, that's 32).

There are always 256 glyphs in a page, giving a page width of 4096 or 8192 for Unifont

To simplify this, I'm going to show these offsets for Unifont in particular; block 0 is single-width, so its bitmasks begin 4096 bytes after `FONTDATA_START`.

| Offset                                    | Length | Contents |
|-------------------------------------------|--------|----------|
| `FONTDATA_START`                          | 16     | Glyph for codepoint 00 in the block described at index 0. |
| `FONTDATA_START` + 32                     | 16     | Glyph for codepoint 01 in the block described at index 0. |
| `FONTDATA_START` + 64                     | 16     | Glyph for codepoint 02 in the block described at index 0. |
| ...                                       | ...    | ... |
| `FONTDATA_START` + 4080                   | 16     | Glyph for codepoint FF in the block described at index 0. |
| `FONTDATA_START` + 4096                   | 32     | Spacing bitmask for codepoints in the block described at index 0. |
| `FONTDATA_START` + 4128                   | 32     | Width bitmask for codepoints in the block described at index 0. |
| `FONTDATA_START` + 4160                   | 16     | Glyph for codepoint 00 in the block described at index 1. |
| `FONTDATA_START` + 4176                   | 16     | Glyph for codepoint 01 in the block described at index 1. |
| `FONTDATA_START` + 4192                   | 16     | Glyph for codepoint 02 in the block described at index 1. |
| ...                                       | ...    | ... |

On and on, except that double-width blocks will have a glyph length of 32.

Implementations may want to calculate all of the offsets and store them in some kind of data structure. With the width, height, multiplier, flags and number of bitmasks for each block, it is simple to loop through and calculate these once when loading the font and then cache the values.
