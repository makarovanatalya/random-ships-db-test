import allure
from hamcrest import assert_that, equal_to


@allure.story('Weapon')
@allure.description('Check weapon for ship')
def test_weapon(make_test_db_and_get_data_for_cases, ships_name):

    original_data = make_test_db_and_get_data_for_cases[0][ships_name]
    tested_data = make_test_db_and_get_data_for_cases[1][ships_name]

    assert_text = f'{ships_name} {tested_data["components"]["weapon"]}'

    # в первую очередь проверяем название компонента, потому что если он неправильный - параметры смотреть нет смысла
    assert_that(tested_data["components"]["weapon"],
                equal_to(original_data["components"]["weapon"]),
                f'{assert_text}: wrong component')

    assert_that(tested_data["weapon"],
                equal_to(original_data["weapon"]),
                f'{assert_text}: wrong component\'s parameters')
