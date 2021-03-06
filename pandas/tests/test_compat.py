# -*- coding: utf-8 -*-
"""
Testing that functions from compat work as expected
"""

import re

import pytest

from pandas.compat import (
    builtins, get_range_parameters, iteritems, iterkeys, itervalues, lfilter,
    lmap, lrange, lzip, re_type)


class TestBuiltinIterators(object):

    @classmethod
    def check_results(cls, results, expecteds, lengths):
        for result, expected, length in zip(results, expecteds, lengths):
            assert isinstance(result, list)
            assert len(result) == length
            assert result == expected

    def test_lrange(self):
        results = lrange(10),
        expecteds = list(builtins.range(10)),
        lengths = 10,

        results += lrange(1, 10, 2),
        lengths += 5,
        expecteds += list(builtins.range(1, 10, 2)),
        self.check_results(results, expecteds, lengths)

    def test_lmap(self):
        func = lambda x, y, z: x + y + z
        lst = [builtins.range(10), builtins.range(10), builtins.range(10)]
        results = lmap(func, *lst),
        expecteds = list(builtins.map(func, *lst)),
        lengths = 10,
        self.check_results(results, expecteds, lengths)

    def test_lfilter(self):
        func = lambda x: x
        lst = list(builtins.range(10))
        results = lfilter(lambda x: x, lst),
        lengths = 9,
        expecteds = list(builtins.filter(func, lst)),
        self.check_results(results, expecteds, lengths)

    def test_lzip(self):
        lst = [builtins.range(10), builtins.range(10), builtins.range(10)]
        results = lzip(*lst),
        expecteds = list(builtins.zip(*lst)),
        lengths = 10,
        self.check_results(results, expecteds, lengths)

    def test_dict_iterators(self):
        assert next(itervalues({1: 2})) == 2
        assert next(iterkeys({1: 2})) == 1
        assert next(iteritems({1: 2})) == (1, 2)


class TestCompatFunctions(object):

    @pytest.mark.parametrize(
        'start,stop,step', [(0, 10, 2), (11, -2, -1), (0, -5, 1), (2, 4, 8)])
    def test_get_range_parameters(self, start, stop, step):
        rng = range(start, stop, step)
        start_expected, stop_expected, step_expected = start, stop, step

        start_result, stop_result, step_result = get_range_parameters(rng)
        assert start_result == start_expected
        assert stop_result == stop_expected
        assert step_result == step_expected


def test_re_type():
    assert isinstance(re.compile(''), re_type)
