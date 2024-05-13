# GdocAsciiConverter
Created by Pontus Martinsson

## Requirements:

- Python 3.10.7 or greater
- The pip package management tool
- A Google account connected to NTI-Gymnasiet

## How to use:

1. If you haven't already, run **install_requirements.bat** and wait for it to finish
2. Place the image you want to convert into the **img** folder
3. Run **RUN.bat** and follow the instructions in the terminal
4. Done! Your image/document should have appeared on your Google drive

## WARNING!

When you've given the program access to your drive, the file **token.json** will be created
**DO NOT SHARE THIS FILE** as anyone who posess it has full access to your Google drive

## General info:

## Manual setup info:

### Quality
**Low quality mode** will use the entire range (`0-255`) from completely black (`0`) to completely black (`255`) regardless of what pixels actually exist in the image. This means that some of the chosen characters might be excluded. This mode generally works well with only a few characters (5 or so), but I suggest you play around a bit and see what works best for you.

**Examples:** (characters, values)

"abc", `[0, 100, 200, 255]`     --> abcc

"abc", `[200, 200, 255, 255]`   --> bbcc

"abc", `[255, 0, 0, 255]`       --> caac

"abc", `[0, 1, 2, 3]`           --> aaaa

"abc", `[255, 254, 253, 252]`   --> cccc

**High quality mode** will find the darkest and lightest pixels in the image and only use that range when converting it to characters. This means that all chosen characters will usually be included, it is still possible for characters to be excluded. This mode generally works well with as many different characters as possible, but I once again suggest you play around for a bit and see what works best for you.

**Examples:** (characters, values)

"abc", `[0, 100, 200, 255]`     --> abcc

"abc", `[200, 200, 255, 255]`   --> aacc

"abc", `[255, 0, 0, 255]`       --> caac

"abc", `[0, 1, 2, 3]`           --> abbc

"abc", `[255, 254, 253, 252]`   --> cbba

### Characters
Avoid special characters such as åäöûüáé, this does not apply to characters such as &#@$?!<% which should work. Space is allowed. The same character is allowed more than once, but will consequently occupy a greater range.

**Examples:** (characters, values)

"abc", `[0, 100, 200, 255]`     --> abcc

"aabc", `[0, 100, 200, 255]`    --> aabc

### Font size

### Width

### Row spacing