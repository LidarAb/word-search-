########################################################################
# FILE : wordsearch.py
# WRITER : Lidar Abukarat , lidarabu1 , 318929742
# EXERCISE : intro2cs1 ex4 2021
# DESCRIPTION: A program that simulates a word search game and
# searches for words in a matrix.
########################################################################

import os
import sys
DIRECTIONS = 'udrlwxyz'
STRAIGHT = 1
DIAGONAL = 2


def read_wordlist(filename):
    """
    receives file path, which contains a words list and
    returns a list contains the words, by them original order."
    :param filename: file path which contains a words list
    :return: list contains the words from the file.
    """
    with open(filename) as words_file:
        words_list = words_file.readlines()
    words_list = [i.strip() for i in words_list]
    return words_list


def read_matrix(filename):
    """
    receives file path, which contains a matrix. Every line of the matrix
    contains letters, separated by ',' and all lines in same length.
    returns a matrix which is list of lists. each sub-list contains
    the letters from the original relevant line, by them original order.
    :param filename: file path which contains a matrix of letters.
    :return: matrix- list of lists contains letters.
    """
    with open(filename) as letters_file:
        lines_list = letters_file.readlines()
    letters_str_list = [i.strip() for i in lines_list]
    final_matrix = [letters.split(',') for letters in letters_str_list]
    return final_matrix


def transpose_matrix_left_right(matrix):
    """
    transpose the order of the matrix columns from the right
    to the left.
    :param matrix: list of lists represents a matrix
    :return: transposed matrix
    """
    new_matrix = []
    for line in matrix:
        new_matrix.append(line[::-1])
    return new_matrix


def transpose_matrix_row_to_column(matrix):
    """
    replaces the columns of the matrix in its rows.
    :param matrix: list of lists represents a matrix
    :return: transposed matrix
    """
    new_matrix = []
    for j in range(len(matrix[0])):
        line_list = []
        for i in range(len(matrix)):
            line_list.append(matrix[i][j])
        new_matrix.append(line_list)
    return new_matrix


def transpose_matrix_up_down(matrix):
    """
    Replaces between the order of the rows of the matrix from end to beginning.
    :param matrix: list of lists represents a matrix
    :return: transposed matrix
    """
    new_matrix = []
    for i in range(1, len(matrix) + 1):
        new_matrix.append(matrix[-i])
    return new_matrix


def row_str(matrix):
    """
    Turns each row of the matrix (form up to down) into a string that
    contains the letters in the row. returns a list contains the strings.
    :param matrix: list of lists represents a matrix
    :return: list of the rows represented as strings.
    """
    lines_list = []
    for line in matrix:
        new_line = ''.join(line)
        lines_list.append(new_line)
    return lines_list


def diagonals_str(matrix):
    """
    Turns each diagonal of the matrix (in up-right direction) into a string.
    returns a list contains all the diagonals strings.
    :param matrix: matrix of letters
    :return: list of strings
    """
    diags_list = []
    for i in range(len(matrix)):
        j = 0
        str = ''
        while i in range(len(matrix)) and j in range(len(matrix[0])):
            str += matrix[i][j]
            i -= 1
            j += 1
        diags_list.append(str)
    for j in range(1, len(matrix[0])):
        i = -1
        str = ''
        while i in range(-1, -len(matrix) - 1, -1) and j in \
                range(len(matrix[0])):
            str += matrix[i][j]
            i -= 1
            j += 1
        diags_list.append(str)
    return diags_list


def add_to_dict(word, counter, words_in_matrix):
    """
    This function adds the word as a key and, the counter as a value to the
    dictionary.
    if the word is already in the dict, it adds the counter to word's
    value. and if not, creates a new item.
    :param word: the word we want to add to the dictionary
    :param counter: The number of times the word appears in the matrix
    :param words_in_matrix: the dictionary contains the words in the matrix
    :return: None
    """
    if counter != 0:
        if word in words_in_matrix.keys():
            words_in_matrix[word] += counter
        else:
            words_in_matrix[word] = counter


def word_in_string(word, string):
    """
    This functions counts how many times the word appears in the string and
    returns the result.
    :param word: the word we search
    :param string: the string we search in
    :return: the numbers of times the word appears in the string
    """
    counter = 0
    new_str = string
    while word in new_str:
        counter += 1
        n = new_str.index(word)
        if len(word) == 1:
            next_index = n + len(word)
            new_str = new_str[next_index:]
        else:
            next_index = n + len(word) - 1
            new_str = new_str[next_index:]
    return counter


def search_word(matrix, words, words_in_matrix, direction):
    """
    Checks every word in the words list if the word is in the matrix in the
    search direction it received and changed the dictionary according to the
    result.
    :param matrix: list of lists contains letters
    :param words: list of words we search in the matrix
    :param words_in_matrix: dictionary contains the words in the matrix
    :param direction: one search direction - straight or diagonal.
    :return: None
    """
    if direction == STRAIGHT:
        str_list = row_str(matrix)
    else:
        str_list = diagonals_str(matrix)
    for word in words:
        counter = 0
        for str in str_list:
            counter += word_in_string(word, str)
        add_to_dict(word, counter, words_in_matrix)


def arguments_validity(arguments):
    """
    checks if the sys.argv list contains 5 arguments as it should, and if not,
    prints an error message to the screen.
    :param arguments: the sys.argv list
    :return: True or False according to the the validity.
    """
    if len(arguments) != 5:
        print('The number of system arguments is invalid.')
        return False
    return True


def directions_validity(directions):
    """
    checks the validity of the directions. if there is a letter that is not one
    of the directions, or is in capital letter - the directions are invalid.
    :param directions: string of letters represents the search directions.
    :return: True or False according the directions validity.
    """
    for char in directions:
        if char not in DIRECTIONS:
            return False
    return True


def files_validity(words_file, matrix_file):
    """
    checks if the files paths are exists. return 1/2/0 according to the result.
    if both are not exist, returns only about the words file.
    :param words_file: the path to the word file
    :param matrix_file: the path to the matrix file
    :return: int represents the file that does not exist, if any
    """
    if not os.path.isfile(words_file):
        return 1
    if not os.path.isfile(matrix_file):
        return 2
    return 0


def errors_msg(directions, words_file, matrix_file):
    """
    prints to the screen an errors message according the invalid situation.
    if there are more than one problem, print only one message.
    :return: True or False if there is a problem or not
    """
    if not directions_validity(directions):
        print("The directions are invalid.")
        return False
    elif files_validity(words_file, matrix_file) != 0:
        if files_validity(words_file, matrix_file) == 1:
            print('The words file is not exist.')
            return False
        if files_validity(words_file, matrix_file) == 2:
            print('The matrix file is not exist.')
            return False
    return True


def filtered_directions(directions):
    """
    receives a string contains the letters represents the search directions
    and returns a new list without duplicates.
    :param directions:  string of letters represents the search directions
    :return: filtered string
    """
    new_directions = ''
    for char in directions:
        if char not in new_directions:
            new_directions += char
    return new_directions


def u_d_r_l(char, matrix, word_list, words_in_matrix):
    """
    this functions checks for every word in the list if it is in the matrix,
    and how many times it is appears, according to the search direction (char).
    the function updates the dictionary if the word is in the matrix.
    every key is the word and the value is the amount of times it in the matrix
    :param char: letter represents the diagonal search direction
    :param matrix: a matrix of letters - list of lists
    :param word_list: words list contains the word we search
    :param words_in_matrix: dictionary
    :return: None
    """
    if char == 'd':
        new_matrix = transpose_matrix_row_to_column(matrix)
        search_word(new_matrix, word_list, words_in_matrix, STRAIGHT)
    elif char == 'u':
        new_matrix_1 = transpose_matrix_row_to_column(matrix)
        new_matrix = transpose_matrix_left_right(new_matrix_1)
        search_word(new_matrix, word_list, words_in_matrix, STRAIGHT)
    elif char == 'r':
        search_word(matrix, word_list, words_in_matrix, STRAIGHT)
    elif char == 'l':
        new_matrix = transpose_matrix_left_right(matrix)
        search_word(new_matrix, word_list, words_in_matrix, STRAIGHT)


def w_x_y_z(char, matrix, word_list, words_in_matrix):
    """
    this functions checks for every word in the list if it is in the matrix,
    and how many times it is appears, according to the search direction (char).
    the function updates the dictionary if the word is in the matrix.
    every key is the word and the value is the amount of times it in the matrix
    :param char: letter represents the straight search direction
    :param matrix: matrix of letters
    :param word_list: the list of words we search in the matrix
    :param words_in_matrix: dictionary.
    :return: None
    """
    if char == 'w':
        search_word(matrix, word_list, words_in_matrix, DIAGONAL)
    elif char == 'x':
        new_matrix = transpose_matrix_left_right(matrix)
        search_word(new_matrix, word_list, words_in_matrix, DIAGONAL)
    elif char == 'y':
        new_matrix = transpose_matrix_up_down(matrix)
        search_word(new_matrix, word_list, words_in_matrix, DIAGONAL)
    elif char == 'z':
        new_matrix = transpose_matrix_row_to_column(matrix)
        search_word(new_matrix, word_list, words_in_matrix, DIAGONAL)


def find_words(word_list, matrix, directions):
    """
    This function searches for all words in the words list in all the
    directions it receives. returns a list of tuples of the word, if in the
    matrix, and the numbers of times it appears.
    :param word_list: the list of words we search in the matrix
    :param matrix: matrix of letters
    :param directions: search directions
    :return: list of tuples
    """
    new_directions = filtered_directions(directions)
    words_in_matrix = {}
    for char in new_directions:
        if char in 'udrl':
            u_d_r_l(char, matrix, word_list, words_in_matrix)
        if char in 'wxyz':
            w_x_y_z(char, matrix, word_list, words_in_matrix)
    results = [(word, counter) for word, counter in words_in_matrix.items()]
    return results


def write_output(results, filename):
    """
    opened new file and write there the search result. each word that appears
    in the matrix is in different line with ',' and the numbers of appearance
    in the matrix.
    :param results: a list of tuples
    :param filename: the path to the new file
    return: None
    """
    with open(filename, 'w') as result_file:
        for pair in results:
            result_file.write(pair[0] + ',' + str(pair[1]) + '\n')


def main():
    """
    This function searches for words in a matrix according to given search
    directions. all arguments received as system arguments.
    If there is something invalid with the system arguments the function stop
    running the program.
    If all arguments are valid ,the functions opens new file with the search
    result.
    :return: None
    """
    if not arguments_validity(sys.argv):
        exit()
    word_file, matrix_file, output_file, directions = sys.argv[1:]
    if not errors_msg(directions, word_file, matrix_file):
        exit()
    else:
        if os.stat(word_file).st_size == 0 or os.stat(matrix_file).st_size\
                == 0:
            results = []
        else:
            words_list = read_wordlist(word_file)
            matrix = read_matrix(matrix_file)
            results = find_words(words_list, matrix, directions)
        write_output(results, output_file)


if __name__ == '__main__':
    main()

