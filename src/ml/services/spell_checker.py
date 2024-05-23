from symspellpy import Verbosity, SymSpell


class SpellCheckerService:
    def __init__(self, spellchecker):
        self.spell_checker = spellchecker

    def apply_case_from_original(self, original: str, corrected: str):
        # Preserve original case by applying it to the corrected word character by character
        if original.istitle():
            corrected = corrected[0].upper() + corrected[1:]

        return corrected

    def lookup_word(self, word, verbosity, max_edit_distance):
        correct = None

        if word in "'.,!?;:":
            return {"word": word, "correct": correct}

        suggestions = self.spell_checker.lookup(
            word.lower(), verbosity, max_edit_distance
        )
        words_list = [item.term for item in suggestions]

        if len(words_list) > 0:
            top_word = words_list[0]
            correct = False

            if top_word == word.lower():
                correct = True
                return {"word": word, "correct": correct}

            if verbosity == Verbosity.CLOSEST.value:
                corrected_word = self.apply_case_from_original(word, top_word)
                return {
                    "word": word,
                    "correct": correct,
                    "variants": [corrected_word] + words_list[1:],
                }

            corrected_word = self.apply_case_from_original(word, top_word)
            return {"word": word, "correct": correct, "correction": corrected_word}

        return {"word": word, "correct": correct}
