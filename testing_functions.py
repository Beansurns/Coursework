plus_mag = {"name": "Bigger Mags",
            "power": 5,
            "mag": 1,
            "dmg": 0,
            "hlth": 0}
plus_dmg = {"name": "Plus Damage",
            "power": 8,
            "mag": 0,
            "dmg": 1,
            "hlth": 0}
plus_hlth = {"name": "Bigger Heart",
             "power": 7,
             "mag": 0,
             "dmg": 0,
             "hlth": 2}
plus_rad = {"name": "Bigger Bullets",
            "power": 4,
            "mag": 0,
            "dmg": 0.5,
            "hlth": 0}
plus_plus_dmg = {"name": "Super Damage",
                 "power": 10,
                 "mag": -1,
                 "dmg": 3,
                 "hlth": 0}
no_mag = {"name": "Infinitely Big Mags",
          "power": 8,
          "mag": 10,
          "dmg": -1,
          "hlth": 0}
plus_size = {"name": "Size Up",
             "power": 5,
             "mag": 0,
             "dmg": 0,
             "hlth": 1}
less_size = {"name": "Size Down",
             "power": 5,
             "mag": 0,
             "dmg": 0,
             "hlth": -1}
plus_life = {"name": "Extra Life",
             "power": 10,
             "mag": 0,
             "dmg": 0,
             "hlth": 5}

pwr_names = [plus_mag, plus_dmg, plus_hlth, plus_rad, plus_plus_dmg, no_mag, plus_size, less_size, plus_life]


def powerup_selection(shot, deaths, opp_deaths, opp_health, opp_shot):
    possible_powerups = pwr_names
    if deaths - opp_deaths >= 3:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["power"] < 7:
                possible_powerups.pop(i)
            else:
                i += 1
    if opp_health > 250:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["power"] < 7:
                possible_powerups.pop(i)
            else:
                i += 1
    if 10 < shot < 40:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["dmg"] < 0:
                possible_powerups.pop(i)
            else:
                i += 1
    if shot > 70:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["mag"] < 0:
                possible_powerups.pop(i)
            else:
                i += 1
    if opp_shot < 40:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["hlth"] < 0:
                possible_powerups.pop(i)
            else:
                i += 1
    return possible_powerups


def test_1():
    assert powerup_selection(50, 1, 0, 100, 100) == pwr_names, "Test 1 Failed"
    print("Test Passed")


def test_2():
    assert powerup_selection(50, 3, 0, 100, 100) == [plus_dmg, plus_hlth, plus_plus_dmg, no_mag, plus_life], "Test 2 Failed"
    print("Test Passed")


def test_3():
    assert powerup_selection(30, 3, 0, 300, 30) == [plus_dmg, plus_hlth, plus_plus_dmg, plus_life], "Test 3 Failed"
    print("Test Passed")


def test_4():
    assert powerup_selection(50, 1, 0, 100, 30) == [plus_mag, plus_dmg, plus_hlth, plus_rad, plus_plus_dmg, no_mag, plus_size, plus_life], "Test 4 Failed"
    print("Test Passed")


def test_5():
    assert powerup_selection(0, 0, 0, 0, 0) == [plus_mag, plus_dmg, plus_hlth, plus_rad, plus_plus_dmg, no_mag, plus_size, plus_life], "Test 5 Failed"
    print("Test Passed")




test_1()
test_2()
test_3()
test_4()
test_5()

