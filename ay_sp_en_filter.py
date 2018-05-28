import os
import glob
import string

############################
# Reading in Spanish files #
############################
# Reading in the Spanish dictionary from subfolders
def extract_from_folders(folder):
    """
    Extracts lists of words from subfolders
    :param folder: folder in which documents are nested in subdirectories
    :return: a set of Spanish words (no frequency)
    """
    spanish_wordlist = []
    for dir in glob.glob(os.path.join(folder, '*/')):
        for filename in glob.glob(os.path.join(dir, '*.txt')):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    words = line.split(' ')
                    for word in words:
                        to_remove = string.punctuation
                        table = {ord(char): None for char in to_remove}
                        word = word.translate(table)
                        if word.isalpha():
                            spanish_wordlist.append(word)

    return spanish_wordlist


# Reading in the CMU file
def cmu_reader(filename):
    """
    Reads in the CMU file into a dictionary of spelling-to-pronunciation
    :param filename: name & path of the CMU file
    :return: a list of English words (no frequency)
    """
    cmu = []
    with open(filename, 'r') as cmu_f:
        for line in cmu_f:
            line = line.strip()
            bits = line.split(',')
            spelling = bits[0].strip('"')
            if spelling not in cmu:
                cmu.append(spelling)

    return cmu

# Reading in Aymara word list
def aymara_reader(filename):
    """
    Reads in an Aymara word list and returns a list with the words
    :param filename: name & path of the Aymara word list
    :return: a list of Aymara words (no frequency)
    """
    aym = []
    with open(filename, 'r', encoding='utf-8') as aym_f:
        for line in aym_f:
            line = line.strip()
            bits = line.split(' ')
            word = bits[1]
            to_remove = string.punctuation
            table = {ord(char): None for char in to_remove}
            word = word.translate(table)
            if word.isalpha() and word not in aym:
                aym.append(word)

    return aym


# Filtering lists with lists
def filter_lst(filter_from, stoplist):
    """
    Filters out words appearing in the stoplist from another list
    :param filter_from: the list that should be filtered
    :param stoplist: the list of words that should be filtered
                     from the other list
    :return: two lists: the list of words that were filtered out
             and the list of words that were not
    """
    pass_list = []
    discard_list = []

    for item in filter_from:
        if item in stoplist:
            discard_list.append(item.lower())
        else:
            pass_list.append(item.lower())

    return pass_list, discard_list


# Writing output lists to files
def write_list(lst, path):
    """
    Writes list of words to file.
    :param lst: list to be written to file
    :param path: path of new file
    :return: None
    """
    with open(path, 'w') as output_w:
        for item in lst:
            output_w.write(item + '\n')


def main():
    # Reading in files
    folder = os.getcwd()
    spanish_folder = os.path.join(folder, "Inputs\\CORLEC\\")
    sp = extract_from_folders(spanish_folder)
    cmu_path = "Inputs\\cmu_dictionary.txt"
    en = cmu_reader(cmu_path)
    aym_path = "Inputs\\ay-freq.txt"
    aym = aymara_reader(aym_path)

    # Filtering
    no_sp, sp_stop = filter_lst(aym, sp)
    write_list(sp_stop, "Outputs\\Spanish_loans.txt")
    no_sp_en, en_stop = filter_lst(no_sp, en)
    write_list(en_stop, "Outputs\\English_loans.txt")
    write_list(no_sp_en, "Outputs\\Aymara_words_no_sp_en.txt")


main()
