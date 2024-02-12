from cdprecorder.str_evaluator import randomness_score


def test_randomness_score():
    assert randomness_score("AAAAAAAAAAA") > 100
    assert randomness_score("ghfdsa7GADSUY8") < 50
