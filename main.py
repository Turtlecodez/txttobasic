# This program converts a .pdf or .txt file to code readable by Texas Instruments TI-83 and TI-84 series calculators.
# Created by turtle boi/frootdaproot
# Module dependencies: pyperclip, pdfminer.six, epub2txt, and tivars
# It is recommended to use pip install module to install the dependencies. If you aren't familiar with pip, copy the following command: pip install pyperclip pdfminer.six

# most recent update - 12/10/2025
# made it output a .8xp file instead of a .txt you need to put through ti connect
# Realized that any story over 21kb in plaintext data would bork my program
# So I made it split the stories into multiple programs
# And I added .epub support!

# Importing modules
import pyperclip
import textwrap
from textwrap import wrap
from tivars.models import *
from tivars.types import *
from tivars.types import TIProgram
from epub2txt import epub2txt
from pdfminer.high_level import extract_text
import os
import sys

# Initializing variables
supported_characters = ''' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890+-='"()[]:;,./\n?\!<>'''
page_number_variable = "Z"
prgm_name = "BOOK"
save_page_number = True
show_page_number = True
tutorial = False
output_to_txt = False

# define functions
def copy(text):
    pyperclip.copy(text)

def change_page_variable():
    # Changes the page variable to user input
    print("What would you like to change the variable to? Supported variables are any uppercase English letter.")
    chosen_variable = input("> ")
    if chosen_variable in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and len(chosen_variable) == 1:
        page_number_variable = chosen_variable
    else:
        print("Variable left unchanged. Reason: Invalid input.")

# Get filename from user and convert into a string
while True:
    print("what is the filename of the file you would like to convert?")
    file_name = input("> ")
    split_file_name = file_name.split(".")
    if len(split_file_name) != 2:
        print("Invalid filename.")
        continue
    if split_file_name[1] != 'txt' and split_file_name[1] != 'pdf' and split_file_name[1] != 'epub':
        print("Invalid file extension.")
        continue
    if not(os.path.exists(file_name)):
        print("File does not exist.")
        continue
    if split_file_name[1] == 'txt':
        with open(file_name, "r", encoding="utf-8") as f:
            unformatted_data = f.read()
        break
    elif split_file_name[1] == 'pdf':
        try:
            print("Grabbing PDF data...")
            unformatted_data = extract_text(file_name)
        except Exception as ex:
            print("There was an error extracting data from the PDF. Make sure the")
            print("text in your PDF file is selectable.")
            print("The exception is printed below:")
            print(ex)
            continue
        else:
            print("PDF data has been successfully grabbed.")
            break
    elif split_file_name[1] == 'epub':
        try:
            print("Grabbing EPUB data...")
            print("Please ignore any 'FutureWarning' error below. It does not affect the program.")
            unformatted_data = epub2txt(file_name)
            print("Please ignore any 'FutureWarning' error above. It does not affect the program.")
        except Exception as ex:
            print("There was an error extracting data from the EPUB.")
            print("The exception is printed below:")
            print(ex)
        else:
            print("EPUB data has been successfully grabbed.")
            break

# advanced configuration settings
adv_config = input("Enable advanced configuration settings? [default n] (y/n)")
adv_config = adv_config.upper()
if adv_config != "Y" and adv_config != "N" or adv_config == "N":
    adv_config == "N"
    print("n")
if adv_config == "Y":
    while True:
        print("this is advanced configuration mode")
        print("please select a number")
        print("")
        print(f"1. edit the variable your page number is stored in (current variable: {page_number_variable})")
        if save_page_number == True:
            print("2. save page number to variable (currently on) (reduces file size when off)")
        if save_page_number == False:
            print("2. save page number to variable (currently off) (reduces file size when off)")
        if show_page_number == True:
            print("3. show page numbers while reading (currently on) (reduces file size when off)")
        if show_page_number == False:
            print("3. show page numbers while reading (currently off) (reduces file size when off)")
        print(f"4. change name of program on-calculator (current name: {prgm_name})")
        print(f"5. Enable output to a .txt file as well as a .8xp file (current value: {output_to_txt})")
        print("6. quit and continue")
        user_choice = input("> ")
        if user_choice == "1":
            change_page_variable()
            continue
        if user_choice == "2":
            if save_page_number == False:
                save_page_number = True
            else:
                save_page_number = False
        if user_choice == "3":
            if show_page_number == False:
                show_page_number = True
            else:
                show_page_number = False
        if user_choice == "4":
            print("Enter new name below. Max 8 characters.")
            new_name = input("> ")
            new_name = new_name.upper()
            valid = True
            for char in new_name:
                if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    valid = False
            if len(new_name) <= 8 and valid == True:
                print(f"Confirm name change to {new_name}?")
                user_choice = input("(y/n) > ")
                if user_choice.lower() == "y":
                    print("Name changed.")
                    prgm_name = new_name
                else:
                    print("Aborted.")
        if user_choice == "5":
            if output_to_txt == False:
                output_to_txt = True
            else:
                output_to_txt = False
        if user_choice == "6":
            break


# Get other required information from user like calculator model
while True:
    print("What is the model of your calculator? Type the number that corresponds to it")
    print("1. TI-83, TI-84 Plus, or TI-84 Plus Silver Edition")
    print("2. TI-84 Plus C Silver Edition, TI-84 Plus CE, or any other calculator with 'CE' in its name")
    user_answer = input("> ")
    if user_answer == "1":
        real_total_chars = 128
        total_chars = 112
        row_length = 16
        break
    elif user_answer == "2":
        real_total_chars = 260
        total_chars = 234
        row_length = 26
        break
    else:
        continue

print("Formatting started. Beginning step 1...")
# Remove unsupported characters from data
data_format_step1 = ""
for char in unformatted_data:
    if char in supported_characters:
        if char == '"':
            data_format_step1 = data_format_step1 + "'"
        else:
            data_format_step1 = data_format_step1 + char
        

print("Step 1 completed. Beginning step 2...")
# make it a string :)
data_format_step2 = ""
for block in data_format_step1:
    data_format_step2 += block

print("Step 2 completed. Beginning step 3...")
# wrap the text so that everything fits into a row of row_length
data_format_step3 = []
# wrap the lines seperated by newlines seperately so that newlines get preserved
for paragraph in data_format_step2.split('\n'):
    words = paragraph.split(' ')
    fixed_words = []
    for w in words:
        if len(w) > row_length:
            w = ' '.join(w[i:i+row_length] for i in range(0, len(w), row_length))
        fixed_words.append(w)

    paragraph = ' '.join(fixed_words)
    wrapped = textwrap.wrap(
        paragraph,
        width=row_length,
        break_long_words=False,
        break_on_hyphens=False
    )

    if not wrapped:
        data_format_step3.append("")
    else:
        for block in wrapped:
            data_format_step3.append(block)

print("Step 3 completed. Beginning step 4...")
# format the lines with whitespace so that each line is exactly 26 characters (put stuff here later i guess)
data_format_step4 = []
for block in data_format_step3:
    space_count = row_length - len(block)
    if space_count < 0:
        space_count = 0
        old_block = block
        block = ""
        for char in old_block:
            if len(block) <= row_length:
                block = block + char
    data_format_step4.append(block + " "*space_count)

print("Step 4 completed. Beginning step 5...")
# put 9 lines together into a block (if show page numbers is ON)
if show_page_number == True:
    data_format_step5 = []
    current_block = ""
    block_number = 1
    total_data_len = len(data_format_step4)
    for i, line in enumerate(data_format_step4):
        current_block += line
        if len(current_block) == total_chars:
            label = f"Block {block_number}"
            current_block += label + " " * (row_length - len(label))
            data_format_step5.append(current_block)
            current_block = ""
            block_number += 1

    # do the final block if needed
    if current_block != "":
        if len(current_block) < total_chars:
            current_block += " " * (total_chars - len(current_block))
        label = f"Final block ({block_number})"
        current_block += label + " " * (row_length - len(label))
        data_format_step5.append(current_block)

#put 10 lines together into a block (if show page numbers is OFF)
if show_page_number == False:
    data_format_step5 = []
    current_block = ""
    block_number = 1
    total_data_len = len(data_format_step4)
    total_chars = real_total_chars
    for i, line in enumerate(data_format_step4):
        current_block += line
        if len(current_block) == total_chars:
            data_format_step5.append(current_block)
            current_block = ""
            block_number += 1

    # do the final block if needed
    if current_block != "":
        data_format_step5.append(current_block)

print("Step 5 completed. Beginning step 6...")
b = 0
a = 1
# put the blocks into the BASIC code
data_format_step6 = [[]]
for i, block in enumerate(data_format_step5):
    if a == 1: # this part is only to append the header to the file
        a = 2
        if save_page_number == True:
            if row_length == 26:
                header = f"""Lbl Q
ClrHome
Menu("turtle's ebook reader","Restart book",A,"Continue book",B,"Tutorial",C,"Quit",D)
Lbl C
ClrHome
Output(1,1,"Welcome to turtle's eBook reader! To navigate the   menu, use the down and up arrow keys to move and theEnter key to select.")
Output(10,1,"Press Enter to continue.")
Pause 
Output(1,1,"To navigate the book,     simply use the Enter key  to go forward a page. The page you are on will be   saved when you exit the   program.")
Output(10,1,"Press Enter to continue.")
Pause 
ClrHome
Output(1,1,"If you want to restart thebook, select Restart from   the menu. If you want to  continue from where you   left off, select Continue.")
Output(10,1,"Press Enter to continue.")
Pause 
ClrHome
Output(1,1,"WARNING:                  Do NOT overwrite the      variable {page_number_variable}, that is the   variable in which the pagenumber is stored in for   this program.")
Output(10,1,"Press Enter to quit.")
Pause 
Goto Q
Lbl A
ClrHome
Output(1,1,"Are you sure you want to  restart the book? This    will delete your saved    page number. Press 2nd to confirm and Alpha to go   back.")
Lbl E
getKey→K
If K=21
Goto F
If K=31
Goto Q
Goto E
Lbl F
1→{page_number_variable}
Lbl B"""
                data_format_step6[b].append(header)
                data_format_step6[b].append(f"""ClrHome
If {page_number_variable}<{i+2}
Then
Output(1,1,"{block}")
{i+1}→{page_number_variable}
Pause 
End""")
            elif row_length == 16:
                header = f"""Lbl Q
ClrHome
Menu("turtle's ebook reader","Restart book",A,"Continue book",B,"Tutorial",C,"Quit",D)
Lbl C
ClrHome
Output(1,1,"To navigate the menu, use the   down and up     arrow keys to   move and the    Enter key to    select.         ")
Output(8,1,"enter 2 continue")
Pause 
ClrHome
Output(1,1,"To navigate the book, use the   Enter key to go forward a page.")
Output(8,1,"enter 2 continue")
Pause 
ClrHome
Output(1,1,"The page you    left off on willautomatically besaved when you  exit the        program.")
Output(8,1,"enter 2 continue")
Pause 
ClrHome
Output(1,1,"To wipe your    saved page,     select Restart  from the menu.")
Output(8,1,"enter 2 continue")
Pause 
ClrHome
Output(1,1,"To continue fromwhere you left  off, select     Continue        instead.")
Output(8,1,"enter 2 continue")
Pause 
ClrHome
Output(1,1,"Do not overwritethe variable {page_number_variable}, that is where   your page numberis stored.")
Output(8,1,"enter 2 quit")
Pause 
Goto Q
Lbl A
ClrHome
Output(1,1,"Are you sure youwant to restart the book? Press 2nd to confirm  and Alpha to    exit.")
Lbl E
getKey→K
If K=21
Goto F
If K=31
Goto Q
Goto E
Lbl F
1→Z
Lbl B"""
                data_format_step6[b].append(header)
                data_format_step6[b].append(f"""ClrHome
If {page_number_variable}<{i+2}
Then
Output(1,1,"{block}")
{i+1}→{page_number_variable}
Pause 
End""")
        elif save_page_number == False:
            if row_length == 26:
                data_format_step6[b].append(f"""Lbl Q
ClrHome
Menu("turtle's ebook reader","Restart book",A,"Tutorial",C,"Quit",D)
Lbl C
ClrHome
Output(1,1,"Welcome to turtle's eBook reader! To navigate the   menu, use the down and up arrow keys to move and theEnter key to select.")
Output(10,1,"Press Enter to continue.")
Pause 
Output(1,1,"To navigate the book,     simply use the Enter key  to go forward a page. The page you are on won't be  saved when you exit the   program.")
Output(10,1,"Press Enter to continue.")
Pause 
ClrHome
Output(1,1,"If you want to start      reading the book, select  Start from the menu.")
Output(10,1,"Press Enter to quit.")
Pause 
Goto Q
Lbl D
Stop
Lbl A
ClrHome
If {page_number_variable}<{i+2}
Then
Output(1,1,"{block}")
{i+1}→{page_number_variable}
Pause 
End""")
            elif row_length == 16:
                data_format_step6[b].append(f"""Lbl Q
ClrHome
Menu("turtle's ebook reader","Restart book",A,"Tutorial",C,"Quit",D)
Lbl C
ClrHome
Output(1,1,"To navigate the menu, use the   down and up     arrow keys to   move and the    Enter key to    select.         ")
Output(8,1,"Enter 2 continue")
Pause 
Output(1,1,"To navigate the book, use the   Enter key to go forward a page.")
Output(8,1,"Enter 2 continue")
Pause 
ClrHome
Output(1,1,"The page you    left off on willNOT be saved    when you exit   the program.")
Output(8,1,"Enter 2 continue")
ClrHome
Output(1,1,"If you want to start      reading the book, select  Start from the menu.")
Output(8,1,"Enter to quit.")
Pause 
Goto Q
Lbl D
Stop
Lbl A
ClrHome
If {page_number_variable}<{i+2}
Then
Output(1,1,"{block}")
{i+1}→{page_number_variable}
Pause 
End""")
    elif i+1 == len(data_format_step5): # and this part appends every other part of the file
        data_format_step6[b].append(f"""
ClrHome
If Z<{i+2}
Then
Output(1,1,"{block}")
{i+1}→Z
Pause 
End
ClrHome
""")
    else:
        if save_page_number == True:
            data_format_step6[b].append(f"""
ClrHome
If Z<{i+2}
Then
Output(1,1,"{block}")
{i+1}→Z
Pause 
End""")
        elif save_page_number == False:
            data_format_step6[b].append(f"""
ClrHome
Output(1,1,"{block}")
Pause """)
            
    # move output to the next block if current block is getting too big
    if save_page_number == True:
        if (i - ((b+1)*140)) + 1 >= -5:
            data_format_step6.append([])
            b += 1
            a = 1
    if save_page_number == False:
        if len(data_format_step6[b].split()) >= 470:
            data_format_step6.append([])
            b += 1
            a = 1

# Put the smaller blocks together into bigger seperated blocks
data_format_step7 = []
for block in data_format_step6:
    shard = ""
    for mini_block in block:
        shard += mini_block
    data_format_step7.append(shard)

# put full data into string data
data = ""
for piece in data_format_step6:
    block = ""
    for mini_block in piece:
        block += mini_block
    data += block

# output to a .txt file if that setting is enabled
if output_to_txt == True:
    if len(data_format_step6) > 1:
        for i, thing in enumerate(data_format_step7):
            with open(f"output{i+1}.txt", "w", encoding="utf-8") as text_file:
                text_file.write(thing)
    else:
        with open("output.txt", "w", encoding="utf-8") as text_file:
            text_file.write(data)

# Output to a single program if the file is small enough
if len(data_format_step6) == 1:
    my_program = TIProgram(name=prgm_name)
    my_program.load_string(data)

    my_program.save(f"{prgm_name}.8xp")
    my_var = my_program.export()

# Output to multiple programs if file size is too big
if len(data_format_step6) > 1:
    i = 0
    for block in data_format_step7:
        # Edit program name to have a number at the end and export each program
        new_prgm_name = ""
        if len(prgm_name) == 8:
            for j, char in enumerate(prgm_name):
                if j != 7:
                    new_prgm_name += char
                if j == 7:
                    new_prgm_name += i+1
        elif len(prgm_name) < 8:
            new_prgm_name += prgm_name
            new_prgm_name += str(i+1)
        try:
            my_program = TIProgram(name=new_prgm_name)
            my_program.load_string(block)

            my_program.save(f"{new_prgm_name}.8xp")
            my_var = my_program.export()
        except:
            # Attempt to fix OverflowError if it happens
            print("An error occurred. The file was likely too large.")
            print("Attempting to fix error...")
            lines = block.splitlines()
            last_55 = "\n".join(lines[-55:])
            last_55 = header + "\n" + last_55
            block = "\n".join(lines[:-55])
            try:
                my_program = TIProgram(name=new_prgm_name)
                my_program.load_string(block)

                my_program.save(f"{new_prgm_name}.8xp")
                my_var = my_program.export()
            except Exception as ex:
                # OverflowError could not be fixed, or there was a different error
                print("Your file was exceptionally chonky and the tokenizer still couldn't handle it!")
                print("Or, there was a different error. The error is printed below:")
                print(ex)
                print("Please try using a different file.")
                sys.exit()
            else:
                try:
                    # Create second part of splitted block and continue fixing OverflowError
                    new_prgm_name2 = ""
                    i += 1
                    if len(prgm_name) == 8:
                        for j, char in enumerate(prgm_name):
                            if j != 7:
                                new_prgm_name2 += char
                            if j == 7:
                                new_prgm_name2 += i+2
                    elif len(prgm_name) < 8:
                        new_prgm_name2 += prgm_name
                        new_prgm_name2 += str(i+1)
                    my_program = TIProgram(name=new_prgm_name2)
                    my_program.load_string(last_55)

                    my_program.save(f"{new_prgm_name2}.8xp")
                    my_var = my_program.export()
                except Exception as ex:
                    # There was another error :(
                    print("There was an error splitting the file... It will be printed below.")
                    print(ex)
                    print("Please try using a different file.")
                    sys.exit()
                else:
                    # Error correction worked properly!
                    print(f"Our error correction worked! This block was split into two smaller blocks, {new_prgm_name} and {new_prgm_name2}.")
                    print("The program will now continue for all future blocks.")
        i += 1

# anything below is the tutorial for getting the file to the calculator
if len(data_format_step6) == 1:
    print("Step 6 completed.")
    print("Your file has been formatted into TI-BASIC.")
    print(f"It has been outputted under the file name '{prgm_name}.8xp'.")
    print("Would you like a tutorial on how to get the file onto your calculator?")
if len(data_format_step6) > 1:
    print("Step 6 completed.")
    print("Your file was too big to fit in a singular file.")
    print(f"It has been split into multiple files with names starting with {prgm_name}.")
    print("Please keep in mind that every program saves page numbers to the SAME VARIABLE. One program can override another.")
    print("Would you like a tutorial on how to get the files onto your calculator?")
while True:
    user_answer = input("(y/n) >")
    if user_answer.lower() == "y":
        tutorial = True
        break
    if user_answer.lower() == "n":
        break
    if user_answer.lower() not in "yn":
        print("Please choose yes (y) or no (n).")

while True:
    if tutorial == False:
        break
    if tutorial == True:
        print("Beginning tutorial.")
        print("Please keep in mind this tutorial is only useful if you have a CE or C calculator.")
        print("To do this tutorial, you will need a device running Windows or MacOS, any calculator with CE in its name (or a TI-84 Plus C Silver edition), and a cable to connect that calculator to the aforementioned device.")
        print("(you can press enter to continue to the next step, type q then hit enter to quit, or type r then enter to restart tutorial.)")
        user_choice = input("")
        if user_choice == "q":
            break
        if user_choice == "r":
            continue
        copy("https://education.ti.com/en/software/details/en/CA9C74CAD02440A69FDC7189D7E1B6C2/swticonnectcesoftware")
        print("Step 1: Visit the URL that has been copied to your clipboard in a web browser, then")
        print("download the TI Connect CE software for your operating system.")
        user_choice = input("")
        if user_choice == "q":
            break
        if user_choice == "r":
            continue
        print("Step 2: Once you have opened the program and reached the main menu, plug in your calculator to your device.")
        print("It should connect, and show up on the TI-Connect CE interface.")
        user_choice = input("")
        if user_choice == "q":
            break
        if user_choice == "r":
            continue
        print("Step 3: Open your file manager and drag the .8xp file onto your calculator in the interface.")
        user_choice = input("")
        if user_choice == "q":
            break
        if user_choice == "r":
            continue
        print("Congradumacations, you've gotten the file onto your calculator.")
        print("Give yourself a pat on the back, then go read whatever you put on there!")
        print("Press enter to quit, or type r and enter to restart.")
        user_choice = input("")
        if user_choice == "r":
            continue
        break



