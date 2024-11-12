from task_executor.auto_api.api import ApiAutomation
from task_executor.automation_app.check_elements import AppElementsOperation
from task_executor.automation_web.web import WebAutomation


def app_automation_test(driver, params):
    AppElementsOperation().element_check_operation(driver, params)


def web_automation_test(driver, params):
    WebAutomation(driver).web_automation_test(params)

def api_automation_test(params):
    ApiAutomation().api_automation_test(params)
    pass

