#!/usr/bin/python
"""
Copyright (C) 2018 Ildiko Emese Szabo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import os
import glob
import string
import tct_utility as uti

########################
# Reading in wordlists #
########################
## Reading in the Spanish dictionary from subfolders
def extract_from_folders(folder):
    """
    Extracts a set of words from files in subfolders, removes punctuation
    :param folder: folder in which documents are nested in subdirectories
    :return: a set of Spanish words (no frequency)
    """
    spanish_wordlist = set()
    to_remove = string.punctuation
    table = {ord(char): None for char in to_remove}

    for dir in glob.glob(os.path.join(folder, '*/')):
        for filename in glob.glob(os.path.join(dir, '*.txt')):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    words = line.split(' ')
                    for word in words:
                        word = word.translate(table)
                        word = word.lower()
                        if word.isalpha():
                            spanish_wordlist.add(word)

    return spanish_wordlist


## Reading in the CMU file
def cmu_reader(filename):
    """
    Reads in the CMU file into a set of English words
    :param filename: name & path of the CMU file
    :return: a set of English words (no frequency)
    """
    with open(filename, 'r') as cmu_f:
        cmu = {line.strip().split(',')[0].strip('"').lower() for line in cmu_f}

    return cmu


## Reading in Aymara word list
def aymara_reader(filename):
    """
    Reads in an Aymara word list and returns a list with the words,
    removes punctuation, except for "'"
    :param filename: name & path of the Aymara word list
    :return: a list of Aymara words (no frequency)
    """
    to_remove = '"():;.,?!^'
    table = {ord(char): '' for char in to_remove}
    table[ord("’")] = "'"
    with open(filename, 'r', encoding='utf-8') as aym_f:
        interim_aym = {line.split(' ')[-1].strip().lower().translate(table) for line in aym_f}
        aym = {word for word in interim_aym if
               not any(char.isdigit() for char in word) and \
               '@' not in word and '-' not in word and
               len(word) > 2}
    return aym



def main():
    # Reading in files
    spanish_folder = os.path.join(*[os.pardir, 'Aymara', 'Inputs', 'CORLEC'])
    sp = extract_from_folders(spanish_folder)
    cmu_path = os.path.join(*[os.pardir, 'Aymara', 'Inputs',
                              'cmu_dictionary.txt'])
    en = cmu_reader(cmu_path)

    ay_path = os.path.join(*[os.pardir, 'Aymara', 'Inputs', 'ay_freq.txt'])
    ay = aymara_reader(ay_path)

    # Filtering and writing
    sp_disc = ay - (ay - sp)
    uti.write_iter(sp_disc, os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Spanish_loans.txt']))
    en_disc = ay - (ay - en)
    uti.write_iter(en_disc, os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'English_loans.txt']))
    no_sp_en = ay - sp - en
    uti.write_iter(no_sp_en, os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Aymara_words_no_sp_en.txt']))


if __name__ == '__main__':
    main()