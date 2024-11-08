from automation_app.check_action import CheckAction
from automation_app.check_elements import CheckElements


def app_automation_test(driver, params):
    CheckElements().check_element(driver, params)
