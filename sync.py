import os
import sys
import hashlib
import datetime
import subprocess
from filecmp import dircmp

######
## Class "File":

class File:

    def __init__ (self, name, location, hash_md5='', location2=''):
        self.name = name
        self.location = location
        self.hash_md5 = hash_md5
        self.location2 = location2

##########################

######
## Print Headers:

def print_color(text):
    print ('\033[1;35m' + text + '\033[1;m')

##########################

######
## Remove last Slash If Found:

def trim_slash(input_location):
    
    if input_location[-1] == '/':
        input_location = input_location[:-1]
        
    return input_location
    

##########################

######
## Replace the source with the target:

def replace_source_target(target, location):

    location_with_target = location[location.find('/')+1:]
    location_with_target = target + '/' + location_with_target
    
    return location_with_target
    
##########################

######
## MD5 Hash Calculator:

deleted_dirs = []

def md5(fname):

    hash_md5 = hashlib.md5()

    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except:
        deleted_dirs.append(fname)

    return hash_md5.hexdigest()

##########################

######
## Comparator Function:

files_on_source  = []
dirs_on_source   = []
files_on_target  = []
dirs_on_target   = []
modified_files   = []

def compare_files_dirs(dcmp):

    # Modified Files:
    for name_filename in dcmp.diff_files:
        location = dcmp.left + '/' + name_filename
        location2 = dcmp.right + '/' + name_filename
        the_file = File(name_filename, location, md5(location), location2)
        modified_files.append(the_file)

    for sub_dcmp in dcmp.subdirs.values():
        compare_files_dirs(sub_dcmp)

    # Files/Directories on Source Only:
    for name_filename in dcmp.left_only:
        location = dcmp.left  + '/' +  name_filename
        if os.path.isfile(location):
            the_file = File(name_filename, location, md5(location))
            files_on_source.append(the_file)
        else: dirs_on_source.append(location)

    # Files/Directories on Target Only:
    for name_filename in dcmp.right_only:
        location = dcmp.right + '/' + name_filename
        if os.path.isfile(location):
            the_file = File(name_filename, location, md5(location))
            files_on_target.append(the_file)
        else: dirs_on_target.append(location)

##########################

######
## User Inputs:

source = sys.argv[1]
target = sys.argv[2]

source = trim_slash(source)
target = trim_slash(target)

dcmp = dircmp(source, target)
compare_files_dirs(dcmp)

##########################

######
## Print Modified Files Names:

counter = 1
print_color("Modified Files: ")
print("Modified Files Found: ", len(modified_files), '\n')
for modified_file in modified_files:
    print("[", counter, "]", sep='')
    print("Filename     : ", modified_file.name)
    print("Source       : ", modified_file.location)
    print("Destination  : ", modified_file.location2)
    print("MD5          : ", modified_file.hash_md5)
    print()
    counter += 1

##########################

######
## Print Files Found on Source ONLY:

counter = 1
print_color("Files that has been Found on Source ONLY: ")
print("Files Found: ", len(files_on_source), '\n')
for file_on_source in files_on_source:
    print("[", counter, "]", sep='')
    print("Filename     : ", file_on_source.name)
    print("Location     : ", file_on_source.location)
    print("MD5          : ", file_on_source.hash_md5)
    print()
    counter += 1

##########################

######
## Print Directories Found on Source ONLY:

counter = 1
print_color("Directories that has been Found on Source ONLY: ")
print("Directories Found: ", len(dirs_on_source), '\n')
for dir_on_source in dirs_on_source:
    print("[", counter, "]", sep='')
    print("Location     : ", dir_on_source)
    print()
    counter += 1

##########################

######
## Print Files Found on Target ONLY:

counter = 1
print_color("Files that has been Found on Destination ONLY: ")
print("Files Found: ", len(files_on_target), '\n')
for file_on_target in files_on_target:
    print("[", counter, "]", sep='')
    print("Filename     : ", file_on_target.name)
    print("Location     : ", file_on_target.location)
    print("MD5          : ", file_on_target.hash_md5)
    print()
    counter += 1

##########################

######
## Print Directories Found on Target ONLY:

counter = 1
print_color("Directories that has been Found on Target ONLY: ")
print("Directories Found: ", len(dirs_on_target), '\n')
for dir_on_target in dirs_on_target:
    print("[", counter, "]", sep='')
    print("Location     : ", dir_on_target)
    print()
    counter += 1

##########################

######
## Output to Text Files:

# Get Current Date and Time
now = datetime.datetime.now()
now = now.strftime("%y%m%d")

###

filename = "sync_log [" + str(now) + "].txt"
print_color("Writing sync_log.txt")
sync_log_output = open(filename, "w")

######
## Writing Modified Files Names:

counter = 1
sync_log_output.write("Modified Files: " + '\n')
sync_log_output.write("Modified Files Found: " + str(len(modified_files)) + '\n\n')
for modified_file in modified_files:
    sync_log_output.write("[" + str(counter) + "]" + '\n')
    sync_log_output.write("Filename     : " + modified_file.name + '\n')
    sync_log_output.write("Source       : " + modified_file.location + '\n')
    sync_log_output.write("Destination  : " + modified_file.location2 + '\n')
    sync_log_output.write("MD5          : " + modified_file.hash_md5 + '\n\n')
    counter += 1

sync_log_output.write("################################################################################" + '\n\n')

##########################

######
## Writing Files Found on Source ONLY:

counter = 1
sync_log_output.write("Files that has been Found on Source ONLY: " + '\n')
sync_log_output.write("Files Found: " + str(len(files_on_source)) + '\n\n')
for file_on_source in files_on_source:
    sync_log_output.write("[" + str(counter) + "]" + '\n')
    sync_log_output.write("Filename     : " + file_on_source.name + '\n')
    sync_log_output.write("Location     : " + file_on_source.location + '\n')
    sync_log_output.write("MD5          : " + file_on_source.hash_md5 + '\n\n')
    counter += 1

sync_log_output.write("################################################################################" + '\n\n')

##########################

######
## Writing Directories Found on Source ONLY:

counter = 1
sync_log_output.write("Directories that has been Found on Source ONLY: " + '\n')
sync_log_output.write("Directories Found: " + str(len(dirs_on_source)) + '\n\n')
for dir_on_source in dirs_on_source:
    sync_log_output.write("[" + str(counter) + "]" + '\n')
    sync_log_output.write("Location     : " + dir_on_source + '\n\n')
    counter += 1
    
sync_log_output.write("################################################################################" + '\n\n')

##########################

######
## Writing Files Found on Target ONLY:

counter = 1
sync_log_output.write("Files that has been Found on Destination ONLY: " + '\n')
sync_log_output.write("Files Found: " + str(len(files_on_target)) + '\n\n')
for file_on_target in files_on_target:
    sync_log_output.write("[" + str(counter) + "]" + '\n')
    sync_log_output.write("Filename     : " + file_on_target.name + '\n')
    sync_log_output.write("Location     : " + file_on_target.location + '\n')
    sync_log_output.write("MD5          : " + file_on_target.hash_md5 + '\n\n')
    counter += 1

sync_log_output.write("################################################################################" + '\n\n')

##########################

######
## Writing Directories Found on Target ONLY:

counter = 1
sync_log_output.write("Directories that has been Found on Target ONLY: " + '\n')
sync_log_output.write("Directories Found: " + str(len(dirs_on_target)) + '\n\n')
for dir_on_target in dirs_on_target:
    sync_log_output.write("[" + str(counter) + "]" + '\n')
    sync_log_output.write("Location     : " + dir_on_target + '\n\n')
    counter += 1

sync_log_output.write("################################################################################" + '\n\n')

##########################

sync_log_output.close()
print_color("Finished writing sync_log.txt")
print("\n")


##########################

######
## Copy Files from Source not Found in Target:

if len(files_on_source) > 0 or len(dirs_on_source) > 0:

    user_input = input("Copy missing files from source to target? Y/n : ").upper()

    if user_input == 'Y':
        
        print_color("Copying files:")
        
        for file_on_source in files_on_source:
            location1 = file_on_source.location
            location2 = replace_source_target(target, location1)
            
            subprocess.run(['cp', location1, location2])
            
        print("Files copied successfully.\n")
        
    ###
        
        print_color("Copying Directories:")
        
        for dir_on_source in dirs_on_source:
            location1 = dir_on_source
            location2 = replace_source_target(target, location1)
            
            copy_command = 'cp -a "' + location1 + '" "' + location2 + '"'
            subprocess.call(copy_command, shell=True)
            
        print("Directories copied successfully.\n\n")

##########################
