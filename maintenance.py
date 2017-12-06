"""
    Counts the number of records each subfolder and updates the overview. Sorts the entries in the contents files of
    each subfolder alphabetically.

    TODO check for external dead links (if desired, only now and then)
"""

import os
import re

def read_first_line_from_file(file):
    with open(file, 'r') as f:
        line = f.readline()
    return line

def update_readme():
    """
    Recounts entries in subcategories and writes them to the readme
    """
    print('update readme file')

    # load readme
    readme_path = os.path.join(base_path, 'README.md')

    # read readme
    with open(readme_path) as f:
        readme_text = f.read()

    # compile regex for identifying the building blocks
    regex = re.compile(r"(.*## Contents\n\n)(.*)(\n## Contributing.*)", re.DOTALL)

    # apply regex
    matches = regex.findall(readme_text)
    matches = matches[0]
    start = matches[0]
    middle = matches[1]
    end = matches[2]

    # get sub folders
    subfolders = [x for x in os.listdir(base_path) if x != '.git' and os.path.isdir(os.path.join(base_path, x))]

    # get number of files (minus 1) in each sub folder
    n = [len(os.listdir(os.path.join(base_path, folder))) - 1 for folder in subfolders]

    # assemble paths
    paths = [os.path.join(base_path, folder, '_toc.md') for folder in subfolders]

    # get titles (discarding first two ("# ") and last ("\n") characters)
    titles = [read_first_line_from_file(path)[2:-1] for path in paths]

    # combine folder name, number, titles in one list
    info = zip(titles, subfolders, n)

    # sort according to title
    info.sort(key=lambda x:x[0])

    # assemble output
    update = ['- [{}]({}/_toc.md) ({})\n'.format(*entry) for entry in info]
    update = "".join(update)

    # insert new text in the middle
    text = start + update + end

    # write to readme
    with open(readme_path, 'w') as f:
        f.write(text)

def update_category_tocs():
    """
    Lists all entries in all sub folders and generates the list in the toc file
    """
    # get sub folders
    subfolders = [x for x in os.listdir(base_path) if x != '.git' and os.path.isdir(os.path.join(base_path, x))]

    # for each subfolder
    for folder in subfolders:
        print('generate toc for {}'.format(folder))

        # read toc header line
        toc_folder = os.path.join(base_path, folder)
        toc_file = os.path.join(toc_folder, '_toc.md')
        toc_header = read_first_line_from_file(toc_file)

        # get all files
        files = [x for x in os.listdir(toc_folder) if x != '_toc.md' and os.path.isfile(os.path.join(toc_folder, x))]
        paths = [os.path.join(toc_folder, file) for file in files]

        # get titles (discarding first two ("# ") and last ("\n") characters)
        titles = [read_first_line_from_file(path)[2:-1] for path in paths]

        # combine name and file name
        info = zip(titles, files)

        # sort according to title
        info.sort(key=lambda x:x[0])

        # assemble output
        update = ['- [{}]({})\n'.format(*entry) for entry in info]
        update = "".join(update)

        # combine toc header
        text = toc_header + '\n' + update

        # write to toc file
        with open(toc_file, 'w') as f:
            f.write(text)

if __name__ == "__main__":

    # base path
    base_path = os.path.abspath(os.path.dirname(__file__))

    # recount and write to readme
    update_readme()

    # generate list in toc files
    update_category_tocs()

