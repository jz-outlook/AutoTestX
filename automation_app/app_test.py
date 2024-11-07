from automation_app.checkelementsandactions import CheckElementsAndActions


def app_automation_test(driver, params):
    CheckElementsAndActions().check_element(driver, params)
