from unittest import TestCase

from rxtender.rxtender import parse_idl

class ParserTestCase(TestCase):

    def test_no_arg_stream(self):
        rxt = 'stream Foo() -> BarItem;'
        expected_ast = [   {   'item': None,
        'stream': {   'arg': [],
                      'identifier': 'Foo',
                      'result_identifier': 'BarItem'}}]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)

    def test_single_arg_stream(self):
        rxt = 'stream Foo(one: i32) -> BarItem;'
        expected_ast = [   {   'item': None,
        'stream': {   'arg': [   {   'identifier': 'one',
                                     'type': 'i32'}],
                      'identifier': 'Foo',
                      'result_identifier': 'BarItem'}}]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)

    def test_multi_arg_stream(self):
        rxt = 'stream Foo(one: i32, two: i32, three: i32) -> BarItem;'
        expected_ast = [   {   'item': None,
        'stream': {   'arg': [   {   'identifier': 'one',
                                     'type': 'i32'},
                                 {   'identifier': 'two',
                                     'type': 'i32'},
                                 {   'identifier': 'three',
                                     'type': 'i32'}],
                      'identifier': 'Foo',
                      'result_identifier': 'BarItem'}}]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)
