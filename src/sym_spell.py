"""
====== auto_correct Usage ======
import sym_spell
predictor = sym_spell.initialize()
predictor.auto_correct("perfct", verbose=1)

====== editDistance Usage ======
import sym_spell
distance = sym_spell.editDistance("fox", "focus")
print("Edit distance between fox and focus is:",distance)

"""

import pkg_resources

from symspellpy.symspellpy import SymSpell, Verbosity  # import the module


def editDistance(str1, str2):
    return __editDistance(str1.lower(), str2.lower(), len(str1), len(str2))

# A Naive recursive Python program to fin minimum number
# operations to convert str1 to str2


def __editDistance(str1, str2, m, n):

    # If first string is empty, the only option is to
    # insert all characters of second string into first
    if m == 0:
        return n

    # If second string is empty, the only option is to
    # remove all characters of first string
    if n == 0:
        return m

    # If last characters of two strings are same, nothing
    # much to do. Ignore last characters and get count for
    # remaining strings.
    if str1[m-1] == str2[n-1]:
        return __editDistance(str1, str2, m-1, n-1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all three operations and take
    # minimum of three values.
    return 1 + min(__editDistance(str1, str2, m, n-1),    # Insert
                   __editDistance(str1, str2, m-1, n),    # Remove
                   __editDistance(str1, str2, m-1, n-1)    # Replace
                   )


def initialize(max_edit_distance_dictionary=2, prefix_length=7):

    return AutoCorrect(max_edit_distance_dictionary, prefix_length)


class AutoCorrect():

    def __init__(self, max_edit_distance_dictionary=2, prefix_length=7):
        self.predictor = self.create_sym_spell(
            max_edit_distance_dictionary, prefix_length)

    def create_sym_spell(self, max_edit_distance_dictionary, prefix_length):
        '''
        create sym_spell object based on two hyperparameters

        @return sys_spell object
        '''
        sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
        dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt")
        bigram_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
        # term_index is the column of the term and count_index is the
        # column of the term frequency
        if not sym_spell.load_dictionary(dictionary_path, term_index=0,
                                         count_index=1):
            print("Dictionary file not found")
            return
        if not sym_spell.load_bigram_dictionary(bigram_path, term_index=0,
                                                count_index=2):
            print("Bigram dictionary file not found")
            return

        return sym_spell

    def auto_correct(self, input_term, max_edit_distance_lookup=2, max_edit_distance_dictionary=2, prefix_length=7, verbose=False):
        '''
        Input a word and return the auto corrected word

        @param input_term (str): the input word you want to correct
        @param max_edit_distance_lookup (int) : controls up to which edit distance words from the dictionary should be treated as suggestions. <= param3
        @param max_edit_distance_dictionary (int): hyperparameter for sysspell
        @param prefix_length (int):  Longer prefix length means higher search speed at the cost of higher index size.

        @return output_term (int): corrected word based on input_term
        '''

        suggestions = self.__auto_correct(input_term.lower(
        ), max_edit_distance_lookup, max_edit_distance_dictionary, prefix_length, verbose)

        if suggestions == []:
            if verbose:
                print("Word", input_term, "has no suggestion")
            return input_term.lower(), 100, 100

        return suggestions[0].term, suggestions[0].distance, suggestions[0].count
    def __auto_correct(self, input_term, max_edit_distance_lookup=2, max_edit_distance_dictionary=2, prefix_length=7, verbose=0):

        # get object
        sym_spell = self.predictor

        suggestion_verbosity = Verbosity.ALL  # TOP, CLOSEST, ALL

        suggestions = sym_spell.lookup(input_term, suggestion_verbosity,
                                       max_edit_distance_lookup)

        if verbose:
            print("There are {} suggestions. Ordered by edit_distance and frequency.".format(
                len(suggestions)))
            for suggestion in suggestions:
                print("{}, {}, {}".format(suggestion.term, suggestion.distance,
                                          suggestion.count))

        return suggestions


def test_editdistance():
    # Driver program to test the above function 
    str1 = "POSES"
    str2 = "posts"
    print (editDistance(str1, str2))
    
    # Driver program to test the above function
    str1 = "BENE"
    str2 = "bene"
    print(editDistance(str1, str2))

def main():
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 7
    # create object
    ao = AutoCorrect()
    sym_spell = ao.create_sym_spell(
        max_edit_distance_dictionary, prefix_length)

    # lookup suggestions for single-word input strings
    input_term = "memebers"  # misspelling of "members"
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_edit_distance_dictionary)
    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.TOP  # TOP, CLOSEST, ALL
    suggestions = sym_spell.lookup(input_term, suggestion_verbosity,
                                   max_edit_distance_lookup)
    # display suggestion term, term frequency, and edit distance
    for suggestion in suggestions:
        print("{}, {}, {}".format(suggestion.term, suggestion.distance,
                                  suggestion.count))

    # lookup suggestions for multi-word input strings (supports compound
    # splitting & merging)
    input_term = ("whereis th elove hehad dated forImuch of thepast who "
                  "couqdn'tread in sixtgrade and ins pired him")
    # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 2
    suggestions = sym_spell.lookup_compound(input_term,
                                            max_edit_distance_lookup)
    # display suggestion term, edit distance, and term frequency
    for suggestion in suggestions:
        print("{}, {}, {}".format(suggestion.term, suggestion.distance,
                                  suggestion.count))


if __name__ == "__main__":

    # main()
    test_editdistance()
