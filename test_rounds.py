import pytest
import rounds

#(shot, deaths, opp_deaths, opp_health, opp_shot, player_num)

def test_powerup_selection():
    assert rounds.powerup_selection(50, 1, 0, 100, 100, 1) == [rounds.plus_mag, rounds.plus_dmg, rounds.plus_hlth,
                                                               rounds.plus_rad, rounds.plus_plus_dmg, rounds.no_mag,
                                                               rounds.plus_size, rounds.less_size, rounds.plus_life]