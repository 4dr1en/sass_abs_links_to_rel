##
# Replace the absolutes links made with webpack (~)
# to relatives links in the sass files
##

import os
import re

# return all the sass files in the current directory and all its subdirectories
def find_sass_files(directory_name):
    files_found = []

    for path, subdirs, files in os.walk(directory_name):
        for name in files:
            if re.search(".scss$", name):
                file_path = os.path.join(path, name)
                files_found.append(file_path)

    return files_found


# get a clean path for the system
def get_sys_path(sass_path):
    path_called = "./"
    folders_path_called = sass_path.split("/")

    for i in range(1, len(folders_path_called)):
        if i == len(folders_path_called) - 1:
            path_called += "_" + folders_path_called[i] + ".scss"
        else:
            path_called += folders_path_called[i] + "/"

    return path_called


# take an array of lines
# make the replacements and return the number of replacement and an array of lines
def abs_paths_to_relatives(lines):
    replacements_in_file = 0
    i = -1
    for line in lines:
        i += 1

        if re.search("@(?:use|forward) ['\"]~/", line):
            sass_path = re.match("^@(?:use|forward) ['\"]~/(.+)['\"]", line).group(1)
            path_called = get_sys_path(sass_path)

            if os.path.exists(path_called):
                rel_path = os.path.relpath(path_called, os.path.dirname(path_scanned))
                txt_to_replace = re.match(
                    "^@(?:use|forward) ['\"](~/.+)['\"]", line
                ).group(1)
                lines[i] = line.replace(txt_to_replace, rel_path, 1)
                replacements_in_file += 1
            else:
                print(
                    "Error, link ignored: line "
                    + str(i + 1)
                    + " in "
                    + os.path.abspath(path_scanned)
                )
    return [replacements_in_file, lines]


replacements = 0
paths_scanned_scss = find_sass_files("./")

for path_scanned in paths_scanned_scss:
    file_scanned = open(path_scanned, "r")
    lines = file_scanned.readlines()

    replacements_in_file, new_content = abs_paths_to_relatives(lines)
    replacements += replacements_in_file

    if replacements_in_file > 0:
        file_to_overwrite = open(path_scanned, "w")
        file_to_overwrite.writelines(new_content)

print("Mission completed, " + str(replacements) + " replacements made.")
