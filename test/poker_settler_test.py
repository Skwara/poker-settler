import pytest

from src.poker_settler import PokerSettler


@pytest.fixture()
def settler():
    return PokerSettler()


def settlement(transfers, unmatched):
    return PokerSettler.Settlement(transfers, unmatched)


def test_empty_result(settler):
    assert settler.settlement() == settlement([], [])


def test_reset(settler):
    settler.add_result('First', 5000, 3000)
    settler.add_result('Second', 2000, 4000)
    settler.reset()
    assert settler._results == []
    assert settler.settlement() == settlement([], [])



def test_single_player(settler):
    settler.add_result('First', 5000, 5000)
    assert settler.settlement() == settlement([], [])


def test_two_equal_players(settler):
    settler.add_result('First', 5000, 5000)
    settler.add_result('Second', 5000, 5000)
    assert settler.settlement() == settlement([], [])


def test_two_players_break_even(settler):
    settler.add_result('First', 5000, 5000)
    settler.add_result('Second', 2000, 2000)
    assert settler.settlement() == settlement([], [])


def test_two_players_not_even(settler):
    settler.add_result('First', 5000, 3000)
    settler.add_result('Second', 2000, 4000)
    assert settler.settlement() == settlement([PokerSettler.Transfer('First', 'Second', 2000)], [])


def test_same_diff_matched_first(settler):
    settler.add_result('First', 5000, 12000)
    settler.add_result('Second', 5000, 10000)
    settler.add_result('Third', 5000, 0)
    settler.add_result('Fourth', 5000, 1000)
    settler.add_result('Fifth', 5000, 2000)
    assert settler.settlement() == settlement([PokerSettler.Transfer('Third', 'Second', 5000),
                                               PokerSettler.Transfer('Fourth', 'First', 4000),
                                               PokerSettler.Transfer('Fifth', 'First', 3000)], [])


def test_two_players_wrong_input_too_much(settler):
    settler.add_result('First', 5000, 3000)
    settler.add_result('Second', 2000, 4100)
    assert settler.settlement() == settlement([], [PokerSettler.Result('Second', 2000, 4100, 100)])


def test_two_players_wrong_input_too_little(settler):
    settler.add_result('First', 5000, 3000)
    settler.add_result('Second', 2000, 3900)
    assert settler.settlement() == settlement([], [PokerSettler.Result('First', 5000, 3000, -100)])
