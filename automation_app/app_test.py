from automation_app.check_elements import CheckAndOperationElements


def app_automation_test(driver, params):
    CheckAndOperationElements().element_check_operation(driver, params)
