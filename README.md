# Notes on Joey's fork of Adafruit GFX Library

This fork of the Adafruit GFX Library intends to support the display of Unicode characters in the basic multilingual plane (BMP). It achieves this by replacing the standard 5x7 font with [GNU Unifont](http://unifoundry.com/unifont/index.html), an 8x16 (in some cases 16x16) pixel font that includes glyphs for every code point in the BMP. It also removes all support for graphic fonts.

This should function as a drop-in replacement for the Adafruit GFX Library, as long as you're not using graphic fonts. You can display a Unicode code point by calling `display.writeCodepoint(c)`, where c represents the Unicode code point (not its UTF-8 or UTF-16 representation). You can display a UTF-8 encoded string with the `display.printUTF8(s)` method; I've included a [Very Strict UTF-8 Decoder](https://github.com/douglascrockford/JSON-c/blob/master/utf8_decode.c) that will turn well-formed UTF-8 into code points suitable for display with `writeCodepoint`.

The BMP covers code points from U+0000 to U+FFFF. Currently this library works with most code points from U+0020 to U+32FF, with some caveats:

* This is very much a work in progress and I haven't gotten around to niceities like bounds checking; you'll almost certainly crash if you try to display glyphs outside of the included range.
* I also haven't gotten to double-width glyphs yet; they're marked as "truncated" in the font file and appear garbled.
* Right to left scripts don't work, and in particular Arabic appears as isolated letterforms instead of connected script.
* **The font is HUGE.** This is less than a quarter of the BMP and it will fill almost all of the 256 kilobytes of flash on a [Feather M0](https://www.adafruit.com/product/2772). You'd likely need a megabyte of program memory to hold the whole Unifont.


# Original README: Adafruit GFX Library # [![Build Status](https://travis-ci.org/adafruit/Adafruit-GFX-Library.svg?branch=master)](https://travis-ci.org/adafruit/Adafruit-GFX-Library)

This is the core graphics library for all our displays, providing a common set of graphics primitives (points, lines, circles, etc.). It needs to be paired with a hardware-specific library for each display device we carry (to handle the lower-level functions).

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Written by Limor Fried/Ladyada for Adafruit Industries.
BSD license, check license.txt for more information.
All text above must be included in any redistribution.

Recent Arduino IDE releases include the Library Manager for easy installation. Otherwise, to download, click the DOWNLOAD ZIP button, uncompress and rename the uncompressed folder Adafruit_GFX. Confirm that the Adafruit_GFX folder contains Adafruit_GFX.cpp and Adafruit_GFX.h. Place the Adafruit_GFX library folder your ArduinoSketchFolder/Libraries/ folder. You may need to create the Libraries subfolder if its your first library. Restart the IDE.

# Useful Resources

- Image2Code: This is a handy Java GUI utility to convert a BMP file into the array code necessary to display the image with the drawBitmap function. Check out the code at ehubin's GitHub repository: https://github.com/ehubin/Adafruit-GFX-Library/tree/master/Img2Code

- drawXBitmap function: You can use the GIMP photo editor to save a .xbm file and use the array saved in the file to draw a bitmap with the drawXBitmap function. See the pull request here for more details: https://github.com/adafruit/Adafruit-GFX-Library/pull/31

- 'Fonts' folder contains bitmap fonts for use with recent (1.1 and later) Adafruit_GFX. To use a font in your Arduino sketch, \#include the corresponding .h file and pass address of GFXfont struct to setFont(). Pass NULL to revert to 'classic' fixed-space bitmap font.

- 'fontconvert' folder contains a command-line tool for converting TTF fonts to Adafruit_GFX header format.

---

### Roadmap

The PRIME DIRECTIVE is to maintain backward compatibility with existing Arduino sketches -- many are hosted elsewhere and don't track changes here, some are in print and can never be changed! This "little" library has grown organically over time and sometimes we paint ourselves into a design corner and just have to live with it or add ungainly workarounds.

Highly unlikely to merge any changes for additional or incompatible font formats (see Prime Directive above). There are already two formats and the code is quite bloaty there as it is (this also creates liabilities for tools and documentation). If you *must* have a more sophisticated font format, consider creating a fork with the features required for your project. For similar reasons, also unlikely to add any more bitmap formats, it's getting messy.

Please don't reformat code for the sake of reformatting code. The resulting large "visual diff" makes it impossible to untangle actual bug fixes from merely rearranged lines.
