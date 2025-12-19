# txttobasic
Allows you to read various text files on your TI graphing calculator!

**Supported File Types**
- .epub
- .txt
- .pdf

**Dependencies**:
- Python 3
- pyperclip
- pdfminer.six
- tivars
- epub2txt

## devlog:


**most recent update - 12/19/2025**

- set show page numbers while reading to default to False because no one wants it on anyways
- added dynamic tokenizing to get the maximum sized blocks you can for each one instead of my shitty earlier method
- fixed an error that happens if you disable page number showing
- fixed monochrome calculator support (i actually don't know if it errored in the first place but uhh i hope i fixed it anyways)

**12/11/2025**

- just added more comments to make my code easier to read
- also silenced epub2txt's warning


**12/10/2025**

- pretty big update today! it now spits out an 8xp file
- fixed issue where big files broke the program, because 8xp files can only be so large
- so now it splits it into multiple 8xps if needed
