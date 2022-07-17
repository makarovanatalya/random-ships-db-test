import allure
from hamcrest import assert_that, equal_to


@allure.story('Hull')
@allure.description('Check hull for ship')
def test_hull(make_test_db_and_get_data_for_cases, ships_name):
    original_data = make_test_db_and_get_data_for_cases[0][ships_name]
    tested_data = make_test_db_and_get_data_for_cases[1][ships_name]

    assert_text = f'{ships_name} {tested_data["components"]["hull"]}'

    assert_that(tested_data["components"]["hull"],
                equal_to(original_data["components"]["hull"]),
                f'{assert_text}: wrong component')

    assert_that(tested_data["hull"],
                equal_to(original_data["hull"]),
                f'{assert_text}: wrong component\'s parameters')
