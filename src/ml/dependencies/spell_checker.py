from pathlib import Path

from symspellpy import SymSpell

from src.ml.services.spell_checker import SpellCheckerService
from ..conf import ml_config


def get_spell_checker_service(spellchecker):
    return SpellCheckerService(spellchecker)


def get_spell_checker_instance():
    DICTIONARY_PATH = Path(ml_config.dictionary_path)

    symspell = SymSpell(max_dictionary_edit_distance=2)
    symspell.load_dictionary(
        DICTIONARY_PATH, term_index=0, count_index=1, encoding="utf-8"
    )

    return symspell
