from symspellpy import Verbosity, SymSpell


class SpellCheckerService:
    def __init__(self,spellchecker):
        self.spell_checker = spellchecker

    def lookup_word(self,word, verbosity, max_edit_distance):
        """Find closest or frequent words to input word
        Args:
            word (str): Input word to lookup
            verbosity (Verbosity): Verbosity mode (Verbosity.TOP, Verbosity.CLOSEST, Verbosity.ALL)
            max_edit_distance (int): Max edit distance

        Returns:
            Union[str, List, None]:
                Either string or list or none.

                Returns str
                    If verbosity is set to Verbosity.TOP and input word has
                    most frequent word within max_edit_distance. It outputs
                    the most frequent word.

                Returns None
                    If input word doesn't have any words in dictionary within max_edit_distance.
                    For example, this can happen when you pass word in different language

                Returns List
                    If verbosity is set to Verbosity.CLOSEST.
                    List is empty if input word doesn't have any
                    closest words within max_edit_distance.
        """
        suggestions = self.spell_checker.lookup(word.lower(), verbosity, max_edit_distance)
        words_list = [item.term for item in suggestions]

        correct = None

        if len(words_list) > 0:
            top_word = words_list[0]
            correct = False

            if top_word==word:
                correct = True
                return {'word':top_word,
                        'correct':correct}

            if verbosity == Verbosity.CLOSEST.value:
                return {'word':word,
                    'correct':correct,
                    'variants':words_list}

            return {'word':word,
                    'correct':correct,
                    'correction':top_word}

        return {'word':word,
                'correct':correct}


