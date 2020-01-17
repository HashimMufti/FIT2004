"""
Name of File: trie.py
Author: Hashim Talal Mufti
Language: Python 3.7
Date of Creation: 01/05/2019
Last Edited: 10/05/2019
Description: This file contains two tasks, Task 1 is responsible for creating a Trie of ID's and Last Names from a file
and searching through it with Prefixes, Task 2 is responsible for finding all palindromic substrings inside of the
first line of a file.
List of Functions for Task 1:
CharToVal(Char)
CharPos(Char)
builder(array, index, id, name)
valuefinder(array, solutions)
finder(array, id, name, solutions)
query(filename, id_prefix, last_name_prefix)
List of Functions for Task 2:
get_all_substrings(input_string)
reverseSubstrings(filename)
"""


"""
TASK 1 -> Building a Trie and finding all matching results of a query.
"""


def CharToVal(Char):
    '''
    Description:        This function is responsible for taking a character, finding it's ordinance value and returning
                        it to the caller.
    Time Complexity:    Best:   O(1)
                        Worst:  O(1)
    Space Complexity:   Best    O(1)
                        Worst:  O(1)
    Error Handle:       Not required, is handled by the caller function.
    Return:             Returns the ordinance value of the character it is passed
    Precondition:       A character is passed to this function
    '''
    Val = ord(Char)
    return Val


def CharPos(Char):
    '''
    Description:        This function is responsible for taking a character, converting it into an integer value within
                        the range 0 - 62.
    Time Complexity:    Best:   O(1)
                        Worst:  O(1)
    Space Complexity:   Best    O(1)
                        Worst:  O(1)
    Error Handle:       Not required, is handled by the caller function.
    Return:             Returns the value of the character it was passed, ranging from 0 - 62
    Precondition:       The character it is passed, must be either 0 - 9, a - z or A - Z, any other character will
                        result in erratic behaviour and errors.
    '''
    val = CharToVal(Char)
    if val < 58:
        val = val - 48
        return val
    if val < 91:
        val = val - 55
        return val
    else:
        val = val - 61
        return val


def builder(array, index, id, name):
    '''
    Description:        This function is recursive in nature, it creates a Trie using each character of id, followed by
                        name, followed by finally placed the index value in the array which is used to make the Trie.
    Time Complexity:    Best:   O(T), where T is the number oc characters in ID and Last names
                        Worst:  O(T), where T is the number oc characters in ID and Last names
    Space Complexity:   Best    O(T + NM)
                        Worst:  O(T + NM)
    Error Handle:       Not required, is handled by the caller function.
    Return:             Returns the value of the character it was passed, ranging from 0 - 62
    Precondition:       It must be given an array, index, id and name
    '''
    if len(id) == 0:
        if len(name) == 0:
            if len(index) == 0:
                return array
            else:
                array[0] = index
                index = ""
                builder(array, index, id, name)
                return array
        else:
            char = name[0]
            pos = CharPos(char)
            count = 0
            tmp = ""
            while count < len(name):
                if count == 0:
                    pass
                else:
                    tmp = tmp + name[count]
                count = count + 1
            name = tmp
            if len(array[pos]) == 0:
                array[pos] = [[]] * 62
                array = array[pos]
                builder(array, index, id, name)
                return array
            else:
                array = array[pos]
                builder(array, index, id, name)
                return array
    else:
        char = id[0]
        pos = CharPos(char)
        count = 0
        tmp = ""
        while count < len(id):
            if count == 0:
                pass
            else:
                tmp = tmp + id[count]
            count = count + 1
        id = tmp
        if len(array[pos]) == 0:
            array[pos] = [[]]*62
            array = array[pos]
            builder(array, index, id, name)
            return array
        else:
            array = array[pos]
            builder(array, index, id, name)
            return array


def valuefinder(array, solutions):
    '''
    Description:        This function checks whether there is a node in the Trie
    Time Complexity:    Best:   O(N) where N is the size of the array
                        Worst:  O(N) where N is the size of the array
    Space Complexity:   Best    O(N) going to each node
                        Worst:  O(N) going to each node
    Error Handle:       If a value is not an integer, it repeats the search in the index (which must be a list)
    Return:             Nothing
    Precondition:       It is given both an array and an array for solutions
    '''
    count = 0
    for values in array:
        if len(values) > 0:
            try:
                int(values) + 1
                solutions.append(array[count])
            except:
                valuefinder(array[count], solutions)
        count = count + 1


def finder(array, id, name, solutions):
    '''
    Description:        This function calls the valuefinder function which then calls itself recursively. It is
                        responsible for finding all possible solutions to the query
    Time Complexity:    Best:   O(k + l + n(k), + n(i)), where k is the length of the id, l is the length of the name,
                                n(k) is the number of records matching the id_prefix and n(l) is the number of records
                                matching the last_name_prefix
                        Worst:  O(k + l + n(k), + n(i)), where k is the length of the id, l is the length of the name,
                                n(k) is the number of records matching the id_prefix and n(l) is the number of records
                                matching the last_name_prefix
    Space Complexity:   Best    O(N), where N is the size of solutions
                        Worst:  O(N), where N is the size of solutions
    Error Handle:       Not required, handled by caller
    Return:             Returns solutions
    Precondition:       It is given an array, id, name and solutions.
    '''
    if len(id) == 0:
        if len(name) == 0:
            valuefinder(array, solutions)
        else:
            char = name[0]
            pos = CharPos(char)
            check = 0
            for x in array:
                if len(x) != 0:
                    if check == pos:
                        passer = name
                        count = 0
                        tmp = ""
                        while count < len(passer):
                            if count == 0:
                                pass
                            else:
                                tmp = tmp + passer[count]
                            count = count + 1
                        passer = tmp
                        finder(array[check], id, passer, solutions)
                    else:
                        if check < 11:
                            if len(array) == 62:
                                finder(array[check], id, name, solutions)
                check = check + 1
    else:
        char = id[0]
        pos = CharPos(char)
        count = 0
        tmp = ""
        while count < len(id):
            if count == 0:
                pass
            else:
                tmp = tmp + id[count]
            count = count + 1
        id = tmp
        if len(array[pos]) == 62:
            finder(array[pos],id,name, solutions)
        else:
            print("Does not exist.")
    return solutions


def query(filename, id_prefix, last_name_prefix):
    '''
    Description:        This function calls the queries through the data to find all results that match id_prefix and
                        last_name_prefix.
    Time Complexity:    Best:   O(k + l + n(k), + n(i)), where k is the length of the id, l is the length of the name,
                                n(k) is the number of records matching the id_prefix and n(l) is the number of records
                                matching the last_name_prefix
                        Worst:  O(k + l + n(k), + n(i)), where k is the length of the id, l is the length of the name,
                                n(k) is the number of records matching the id_prefix and n(l) is the number of records
                                matching the last_name_prefix
    Space Complexity:   Best    O(N), where N is the size of solutions
                        Worst:  O(N), where N is the size of solutions
    Error Handle:       Not required, handled by caller
    Return:             Returns FinalSolutions
    Precondition:       It is given a filename, id_prefix and a last_name_prefix.
    '''
    try:
        Array = [[]] * 62
        file = open(filename, "r")
        for x in file:
            Str = ""
            count = 0
            for y in x:
                if y == " ":
                    if count == 0:
                        index = Str
                    if count == 1:
                        id = Str
                    if count == 3:
                        last_name = Str
                        builder(Array, index, id, last_name)
                        count = 0
                    count = count + 1
                    Str = ""
                else:
                    Str = Str + y
        FinalSolutions = finder(Array, id_prefix, last_name_prefix, solutions = [])
        print(len(FinalSolutions), "record found")
        for x in FinalSolutions:
            print("Index Number :", x)
        return FinalSolutions
    except:
        print("E R R O R")
        print("P R O G R A M   H A S   C R A S H E D")
        print("File that caused crash:", filename)
        print("ID that was provided:", id_prefix)
        print("Last name that was provided:", last_name_prefix)


"""
TASK 2 -> Finding all palindromic substrings of the first line of a file.
"""


def get_all_substrings(input_string):
    '''
    Description:        Generates all the unique substrings of the input_string
    Time Complexity:    Best:   O(N^2)
                        Worst:  O(N^2)
    Space Complexity:   Best    O(N) where N is the number of possible substrings
                        Worst:  O(N) where N is the number of possible substrings
    Error Handle:       Not required, is handled by the caller function.
    Return:             Returns the array of all possible substrings
    Precondition:       A string is passed to this function
    '''
    array = []
    for x in range(len(input_string)):
        for y in range(x, len(input_string)):
            array.append(input_string[x:y+1])
    return array


def reverseSubstrings(filename):
    '''
    Description:        Finds all palindromic substrings of the first line of a file.
    Time Complexity:    Best:   O(N^2 + P), where N is the number of characters in the input string and P is the total
                        length of all substrings whose reverse appears in the string
                        Worst:  O(N^2 + P), where N is the number of characters in the input string and P is the total
                        length of all substrings whose reverse appears in the string
    Space Complexity:   Best    O(N^2 + P), where N is the number of characters in the input string and P is the total
                        length of all substrings whose reverse appears in the string
                        Worst:  O(N^2 + P), where N is the number of characters in the input string and P is the total
                        length of all substrings whose reverse appears in the string
    Error Handle:       If a crash is caused, will name the file that caused the crash for debugging
    Return:             Returns the 2D array of all palindromic substrings
    Precondition:       A filename is passed to the function
    '''
    try:
        file = open(filename)
        count = 0
        for line in file:
            if count == 0:
                word = line
        word2 = word[::-1]
        array = get_all_substrings(word)
        list_array = []
        for x in array:
            if x in word2:
                if len(x) > 1:
                    position = word.find(x)
                    tuple = [x,position]
                    if tuple not in list_array:
                        list_array.append(tuple)
                    else:
                        while tuple in list_array:
                            position2= word[position + 1:].find(x)
                            if position2 == 0:
                                position = position + 1
                            else:
                                position = position + 1 + position2
                            tuple = [x,position]
                        list_array.append(tuple)
        return list_array
    except:
        print("E R R O R")
        print("P R O G R A M   H A S   C R A S H E D")
        print("File that caused crash:", filename)

if __name__ == "main":
    try:
        filename = input("Please Enter Filename: ")
        id_prefix = input("Please Enter ID Prefix")
        last_name_prefix = input("Please Enter Last Name Prefix")
        query(filename, id_prefix, last_name_prefix)
        filename = input("Please Enter a Filename for Task 2: ")
        reverseSubstrings(filename)
    except:
        print("An Error has occured.")