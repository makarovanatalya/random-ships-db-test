import allure
from hamcrest import assert_that, equal_to


@allure.story('Engine')
@allure.description('Check engine for ship')
def test_engine(make_test_db_and_get_data_for_cases, ships_name):
    original_data = make_test_db_and_get_data_for_cases[0][ships_name]
    tested_data = make_test_db_and_get_data_for_cases[1][ships_name]

    assert_text = f'{ships_name} {tested_data["components"]["engine"]}'

    assert_that(tested_data["components"]["engine"],
                equal_to(original_data["components"]["engine"]),
                f'{assert_text}: wrong component')

    assert_that(tested_data["engine"],
                equal_to(original_data["engine"]),
                f'{assert_text}: wrong component\'s parameters')
