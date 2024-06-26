import unittest

from grammar.grammar import Grammar, LL1Table, TableCell, ParseTree, SyntaxError
from grammar.utils import GrammarFormat
from typing import Optional, Type

class TestAnalyze(unittest.TestCase):
    def _check_analyze(
            self,
            table: LL1Table,
            input_string: str,
            start: str,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            if exception is None:
                self.assertTrue(table.analyze(input_string, start) is not None)
            else:
                with self.assertRaises(exception):
                    table.analyze(input_string, start)

    def _check_analyze_from_grammar(
            self,
            grammar: Grammar,
            input_string: str,
            start: str,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            table = grammar.get_ll1_table()
            self.assertTrue(table is not None)
            if table is not None:
                if exception is None:
                    self.assertTrue(table.analyze(input_string, start) is not None)
                else:
                    with self.assertRaises(exception):
                        table.analyze(input_string, start)

    def _check_parse_tree(
            self,
            table: LL1Table,
            input_string: str,
            start: str,
            tree: ParseTree,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            if exception is None:
                self.assertEqual(table.analyze(input_string, start), tree)
            else:
                with self.assertRaises(exception):
                    table.analyze(input_string, start)

    def test_case1(self) -> None:
        """Test for syntax analysis from table."""
        terminals = {"(", ")", "i", "+", "*", "$"}
        non_terminals = {"E", "T", "X", "Y"}
        cells = [TableCell('E', '(', 'TX'),
                 TableCell('E', 'i', 'TX'),
                 TableCell('T', '(', '(E)'),
                 TableCell('T', 'i', 'iY'),
                 TableCell('X', '+', '+E'),
                 TableCell('X', ')', ''),
                 TableCell('X', '$', ''),
                 TableCell('Y', '*', '*T'),
                 TableCell('Y', '+', ''),
                 TableCell('Y', ')', ''),
                 TableCell('Y', '$', '')]
        table = LL1Table(non_terminals, terminals, cells)

        self._check_analyze(table, "i*i$", "E")
        self._check_analyze(table, "i*i+i$", "E")
        self._check_analyze(table, "i*i+i+(i*i)$", "E")
        self._check_analyze(table, "a", "E", exception=SyntaxError)
        self._check_analyze(table, "(i$", "E", exception=SyntaxError)
        self._check_analyze(table, "i*i$i", "E", exception=SyntaxError)
        self._check_analyze(table, "i*i", "E", exception=SyntaxError)
        self._check_analyze(table, "+i*i", "E", exception=SyntaxError)

    def test_case2(self) -> None:
        """Test for syntax analysis from grammar."""
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

        self._check_analyze_from_grammar(grammar, "i*i$", "E")
        self._check_analyze_from_grammar(grammar, "i*i+i$", "E")
        self._check_analyze_from_grammar(grammar, "i*i+i+(i*i)$", "E")
        self._check_analyze_from_grammar(grammar, "a", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "(i$", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i$i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "+i*i", "E", exception=SyntaxError)


        terminals = {"(", ")", "i", "+", "*", "$"}
        non_terminals = {"E", "T", "X", "Y"}
        cells = [TableCell('E', '(', 'TX'),
                 TableCell('E', 'i', 'TX'),
                 TableCell('T', '(', '(E)'),
                 TableCell('T', 'i', 'iY'),
                 TableCell('X', '+', '+E'),
                 TableCell('X', ')', ''),
                 TableCell('X', '$', ''),
                 TableCell('Y', '*', '*T'),
                 TableCell('Y', '+', ''),
                 TableCell('Y', ')', ''),
                 TableCell('Y', '$', '')]
        table = LL1Table(non_terminals, terminals, cells)
        self.assertEqual(grammar.get_ll1_table().terminals, table.terminals)
        self.assertEqual(grammar.get_ll1_table().non_terminals, table.non_terminals)
        self.assertDictEqual(grammar.get_ll1_table().cells, table.cells)

    def test_case4(self) -> None:
        """Test for syntax analysis from grammar."""
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

        terminals = {'<', '0', '1', '>', '$'}
        non_terminals = {'A', 'B', 'C', 'D'}
        cells = [TableCell('A', '0', 'BCD'),
                 TableCell('A', '1', 'BCD'),
                 TableCell('A', '<', 'BCD'),
                 TableCell('B', '0', ''),
                 TableCell('B', '1', ''),
                 TableCell('B', '<', '<'),
                 TableCell('C', '0', '0C'),
                 TableCell('C', '1', '1C'),
                 TableCell('D', '0', '0>'),
                 TableCell('D', '1', '1>')]
        table = LL1Table(non_terminals, terminals, cells)
        self.assertEqual(grammar.get_ll1_table().terminals, table.terminals)
        self.assertEqual(grammar.get_ll1_table().non_terminals, table.non_terminals)
        self.assertDictEqual(grammar.get_ll1_table().cells, table.cells)

        self._check_analyze_from_grammar(grammar, "0", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "<0101;;;;1>", "E", exception=SyntaxError)
    
    def test_case5(self) -> None:
        """Test non LL1 grammar"""
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
        self.assertEqual(grammar.get_ll1_table(), None)

    def test_case6(self) -> None:
        """Test non LL1 grammar"""
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
        self.assertEqual(grammar.get_ll1_table(), None)

'''
    def test_case3(self) -> None:
        """Test for parse tree construction."""
        terminals = {"(", ")", "i", "+", "*", "$"}
        non_terminals = {"E", "T", "X", "Y"}
        cells = [TableCell('E', '(', 'TX'),
                 TableCell('E', 'i', 'TX'),
                 TableCell('T', '(', '(E)'),
                 TableCell('T', 'i', 'iY'),
                 TableCell('X', '+', '+E'),
                 TableCell('X', ')', ''),
                 TableCell('X', '$', ''),
                 TableCell('Y', '*', '*T'),
                 TableCell('Y', '+', ''),
                 TableCell('Y', ')', ''),
                 TableCell('Y', '$', '')]
        table = LL1Table(non_terminals, terminals, cells)

        t01 = ParseTree("λ")
        t02 = ParseTree("X", [t01])
        t03 = ParseTree("λ")
        t04 = ParseTree("Y", [t03])
        t05 = ParseTree("i")
        t06 = ParseTree("T", [t05, t04])
        t07 = ParseTree("*")
        t08 = ParseTree("Y", [t07, t06])
        t09 = ParseTree("i")
        t10 = ParseTree("T", [t09, t08])
        tree = ParseTree("E", [t10, t02])
        
        self._check_parse_tree(table, "i*i$", "E", tree)
'''
if __name__ == '__main__':
    unittest.main()


