from __future__ import absolute_import, print_function

import ast
from collections import namedtuple
from contextlib import suppress

import pycodestyle


Error = namedtuple('Error', ['lineno', 'message'])


class NetworkCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def compose_call_path(self, node):
        if isinstance(node, ast.Attribute):
            yield from self.compose_call_path(node.value)
            yield node.attr
        elif isinstance(node, ast.Name):
            yield node.id

    def visit_Call(self, node):  # noqa
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ('from_url'):
                call_path = '.'.join(self.compose_call_path(node.func.value))
                if call_path not in {'Redis', 'StrictRedis'}:
                    return

                for arg in node.keywords:
                    if arg.arg == 'socket_timeout':
                        return

                for index, arg in enumerate(node.args):
                    if index == 0 and isinstance(arg, ast.Str):
                        if 'socket_timeout' in arg.s:
                            return

                self.errors.append(Error(
                    lineno=node.lineno,
                    message='T601 You should set `socket_timeout` when calling `{}.{}`'.format(
                        call_path, node.func.attr)
                ))
        else:
            with suppress(AttributeError):
                if node.func.id not in {'Redis', 'StrictRedis'}:
                    return

                for arg in node.keywords:
                    if arg.arg == 'socket_timeout':
                        return

                for index, arg in enumerate(node.args):
                    if index == 0 and isinstance(arg, ast.Str):
                        if 'socket_timeout' in arg.s:
                            return

                self.errors.append(Error(
                    lineno=node.lineno,
                    message='T601 You should set `socket_timeout` when calling `{}`'.format(node.func.id)
                ))

        self.generic_visit(node)


class NetworkTimeoutLinter(object):
    name = 'network-timeout'
    version = '0.2.0'
    visitor_class = NetworkCallVisitor

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.lines = None

    def load_file(self):
        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pycodestyle.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        if not self.tree:
            self.tree = ast.parse("".join(self.lines))

    def error(self, error):
        return (
            error.lineno,
            0,
            error.message,
            NetworkTimeoutLinter,
        )

    def check_network_timeout(self):
        if not self.tree or not self.lines:
            self.load_file()

        visitor = self.visitor_class()
        visitor.visit(self.tree)
        return visitor.errors

    def run(self):
        for error in self.check_network_timeout():
            yield self.error(error)
