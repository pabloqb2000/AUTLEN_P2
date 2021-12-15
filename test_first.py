import unittest
from typing import AbstractSet

from grammar.grammar import Grammar
from grammar.utils import GrammarFormat

class TestFirst(unittest.TestCase):
    def _check_first(
        self,
        grammar: Grammar,
        input_string: str,
        first_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"First({input_string}), expected {first_set}",
        ):
            computed_first = grammar.compute_first(input_string)
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "Y+i", {'+', '*'})
        self._check_first(grammar, "YX", {'+', '*', ''})
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})

    def test_case2(self) -> None:
        """Test Case 2."""
        grammar_str = """
        X->I*AD
        I->A*I
        I->a
        I->
        A->aa*A
        A->a
        A->
        D->*
        D->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "A", {'', 'a'})
        self._check_first(grammar, "D", {'', '*'})
        self._check_first(grammar, "I", {'', 'a', '*'})
        self._check_first(grammar, "X", {'a', '*'})
        self._check_first(grammar, "a", {'a'})
        self._check_first(grammar, "*", {'*'})

        with self.subTest(
            string=f"First(w), ValueError should be raised since w is not a symbol of the grammar",
        ):
            with self.assertRaises(ValueError):
                grammar.compute_first("w")

        
    def test_case3(self) -> None:
        """Test Case 3."""
        grammar_str = """
        A->BCD
        B-><
        B->
        C->0C
        C->1C
        D->0>
        D->1>
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "A", {'1', '0', '<'})
        self._check_first(grammar, "B", {'', '<'})
        self._check_first(grammar, "C", {'1', '0'})
        self._check_first(grammar, "D", {'1', '0'})
        self._check_first(grammar, "1", {'1'})
        self._check_first(grammar, "0", {'0'})
        self._check_first(grammar, "<", {'<'})
        self._check_first(grammar, ">", {'>'})


    def test_case4(self) -> None:
        """Test Case 4."""
        grammar_str = """
        T->FGH
        F->Gb
        F->
        G->Nd
        G->
        H->aA
        H->
        N->0N
        N->1N
        N->
        A->a
        A->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "A", {'a', ''})
        self._check_first(grammar, "F", {'', '1', 'd', '0', 'b'})
        self._check_first(grammar, "G", {'', '1', 'd', '0'})
        self._check_first(grammar, "H", {'a', ''})
        self._check_first(grammar, "N", {'', '1', '0'})
        self._check_first(grammar, "T", {'', '1', 'd', '0', 'b', 'a'})
        self._check_first(grammar, "1", {'1'})
        self._check_first(grammar, "0", {'0'})
        self._check_first(grammar, "a", {'a'})
        self._check_first(grammar, "b", {'b'})
        self._check_first(grammar, "d", {'d'})
        

if __name__ == '__main__':
    unittest.main()
