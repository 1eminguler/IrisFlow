"""Next-word / word-completion suggestions.

TODO:
    * Load a Turkish word-frequency list (e.g. ``assets/lang/tr_words.txt``).
    * Prefix lookup with a trie (or sorted list + bisect) -> top N by frequency.
    * Learn from what the user types (boost words they use often), saved per user.
    * Turkish-aware lowercasing: ``"I".lower()`` is "i" in Python, but Turkish
      needs "ı" (and "İ" -> "i").
"""

from __future__ import annotations


class WordPredictor:
    def suggest(self, prefix: str, limit: int = 4) -> list[str]:
        raise NotImplementedError

    def learn(self, word: str) -> None:
        raise NotImplementedError
