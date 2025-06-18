import unittest
import os
import time
import tempfile
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pytest

with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)
BASE_URL = CONFIG["base_url"]
VALIDATION_RULES = CONFIG["validation_rules"]

class Locators:
    LOGIN_EMAIL = (By.ID, "email")
    LOGIN_PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.TAG_NAME, "button")
    POPUP_CONTENT = (By.CLASS_NAME, "popup-content")
    NOTIFICATION = (By.CLASS_NAME, "notification")
    COMPANY_NAME = (By.ID, "companyName")
    COMPANY_LOCATION = (By.ID, "location")
    COMPANY_CREATE_BUTTON = (By.XPATH, "//button[contains(text(),'Create Company')]")
    COMPANY_SELECT = (By.ID, "companySelect")
    PROJECT_SELECT = (By.ID, "projectSelect")
    ASSIGN_PROJECT_BUTTON = (By.XPATH, "//button[contains(text(),'Assign Project')]")
    VIEW_METRICS_BUTTON = (By.XPATH, "//button[contains(text(),'View Metrics')]")
    COMPANY_DASHBOARD = (By.ID, "companyDashboard")
    UPDATE_COMPANY_BUTTON = (By.XPATH, "//button[contains(text(),'Update Company')]")
    TEAM_NAME = (By.ID, "teamName")
    ADD_MEMBER = (By.ID, "addMember")
    TEAM_CREATE_BUTTON = (By.XPATH, "//button[contains(text(),'Create Team')]")
    TEAM_SELECT = (By.ID, "teamSelect")
    ASSIGN_PROJECT_TO_TEAM_BUTTON = (By.XPATH, "//button[contains(text(),'Assign Project')]")
    EDIT_TEAM_BUTTON = (By.XPATH, "//button[contains(text(),'Edit Team')]")
    CLIENT_NAME = (By.ID, "clientName")
    CLIENT_EMAIL = (By.ID, "clientEmail")
    ADD_CLIENT_BUTTON = (By.XPATH, "//button[contains(text(),'Add Client')]")
    ASSIGN_TEAM_TO_CLIENT_BUTTON = (By.XPATH, "//button[contains(text(),'Assign Team')]")
    UPDATE_CLIENT_BUTTON = (By.XPATH, "//button[contains(text(),'Update Client')]")
    SEARCH_CLIENT = (By.ID, "searchClient")
    SEARCH_CLIENT_BUTTON = (By.XPATH, "//button[contains(text(),'Search')]")
    CLIENT_RESULTS = (By.ID, "clientResults")
    TEMPLATE_NAME = (By.ID, "templateName")
    TEMPLATE_DESCRIPTION = (By.ID, "description")
    CREATE_TEMPLATE_BUTTON = (By.XPATH, "//button[contains(text(),'Create Template')]")
    TEMPLATE_SELECT = (By.ID, "templateSelect")
    UPDATE_TEMPLATE_BUTTON = (By.XPATH, "//button[contains(text(),'Update Template')]")
    VIEW_VERSIONS_BUTTON = (By.XPATH, "//button[contains(text(),'View Versions')]")
    VERSION_HISTORY = (By.ID, "versionHistory")
    EDIT_TEMPLATE_BUTTON = (By.XPATH, "//button[contains(text(),'Edit Template')]")
    PROJECT_NAME = (By.ID, "projectName")
    BUDGET = (By.ID, "budget")
    DEADLINE = (By.ID, "deadline")
    CREATE_PROJECT_BUTTON = (By.XPATH, "//button[contains(text(),'Create Project')]")
    ASSIGN_TEAM_BUTTON = (By.XPATH, "//button[contains(text(),'Assign Team')]")
    TASK_NAME = (By.ID, "taskName")
    DUE_DATE = (By.ID, "dueDate")
    ADD_TASK_BUTTON = (By.XPATH, "//button[contains(text(),'Add Task')]")
    VIEW_GANTT_BUTTON = (By.XPATH, "//button[contains(text(),'View Gantt')]")
    GANTT_CHART = (By.ID, "ganttChart")
    EDIT_PROJECT_BUTTON = (By.XPATH, "//button[contains(text(),'Edit Project')]")
    PROJECT_DESCRIPTION = (By.ID, "description")
    UPDATE_PROJECT_BUTTON = (By.XPATH, "//button[contains(text(),'Update Project')]")
    PROPERTY_TYPE = (By.ID, "propertyType")
    PROPERTY_NAME = (By.ID, "name")
    PROPERTY_LOCATION = (By.ID, "location")
    TENANT = (By.ID, "tenant")
    ADD_PROPERTY_BUTTON = (By.XPATH, "//button[contains(text(),'Add')]")
    CLOSE_BUTTON = (By.XPATH, "//button[contains(text(),'Close')]")
    CHAT_INPUT = (By.ID, "chatInput")
    SEND_BUTTON = (By.XPATH, "//button[contains(text(),'Send')]")
    CHAT_HISTORY = (By.ID, "chatHistory")
    COMMENT = (By.ID, "comment")
    ADD_COMMENT_BUTTON = (By.XPATH, "//button[contains(text(),'Add Comment')]")
    TASK_SELECT = (By.ID, "taskSelect")
    ACCESS_CHAT_BUTTON = (By.XPATH, "//button[contains(text(),'Access Chat')]")
    CHAT_INTERFACE = (By.ID, "chatInterface")
    FILE_UPLOAD = (By.ID, "fileUpload")
    UPLOAD_FILE_BUTTON = (By.XPATH, "//button[contains(text(),'Upload File')]")
    FOLDER_NAME = (By.ID, "folderName")
    CREATE_FOLDER_BUTTON = (By.XPATH, "//button[contains(text(),'Create Folder')]")
    FILE_SELECT = (By.ID, "fileSelect")
    SHARE_FILE_BUTTON = (By.XPATH, "//button[contains(text(),'Share File')]")
    ACCESS_FILE_BUTTON = (By.XPATH, "//button[contains(text(),'Access File')]")
    DESIGN_UPLOAD = (By.ID, "designUpload")
    UPLOAD_DESIGN_BUTTON = (By.XPATH, "//button[contains(text(),'Upload Design')]")
    ANNOTATION = (By.ID, "annotation")
    ADD_ANNOTATION_BUTTON = (By.XPATH, "//button[contains(text(),'Add Annotation')]")
    APPROVE_DESIGN_BUTTON = (By.XPATH, "//button[contains(text(),'Approve Design')]")
    DESIGN_SELECT = (By.ID, "designSelect")
    PREVIEW_DESIGN_BUTTON = (By.XPATH, "//button[contains(text(),'Preview Design')]")
    DESIGN_PREVIEW = (By.ID, "designPreview")
    VIEW_DASHBOARD_BUTTON = (By.XPATH, "//button[contains(text(),'View Dashboard')]")
    PROGRESS_DASHBOARD = (By.ID, "progressDashboard")
    GENERATE_REPORT_BUTTON = (By.XPATH, "//button[contains(text(),'Generate Report')]")
    EXPORT_REPORT_BUTTON = (By.XPATH, "//button[contains(text(),'Export Report')]")
    EXPENSE_AMOUNT = (By.ID, "expenseAmount")
    ADD_EXPENSE_BUTTON = (By.XPATH, "//button[contains(text(),'Add Expense')]")
    REVENUE_AMOUNT = (By.ID, "revenueAmount")
    ADD_REVENUE_BUTTON = (By.XPATH, "//button[contains(text(),'Add Revenue')]")
    VIEW_RECORDS_BUTTON = (By.XPATH, "//button[contains(text(),'View Records')]")
    EVENT_NAME = (By.ID, "eventName")
    EVENT_DATE = (By.ID, "eventDate")
    CREATE_EVENT_BUTTON = (By.XPATH, "//button[contains(text(),'Create Event')]")
    EVENT_SELECT = (By.ID, "eventSelect")
    REMINDER = (By.ID, "reminder")
    SET_REMINDER_BUTTON = (By.XPATH, "//button[contains(text(),'Set Reminder')]")
    SYNC_CALENDAR_BUTTON = (By.XPATH, "//button[contains(text(),'Sync with Google Calendar')]")
    FINANCIALS_DISPLAY = (By.ID, "financialsDisplay")
    ACTION_FILTER = (By.ID, "actionFilter")
    VIEW_LOG_BUTTON = (By.XPATH, "//button[contains(text(),'View Log')]")
    AUDIT_LOG = (By.ID, "auditLog")
    INTEGRATION_SELECT = (By.ID, "integrationSelect")
    API_KEY = (By.ID, "apiKey")
    CONNECT_BUTTON = (By.XPATH, "//button[contains(text(),'Connect')]")
    EMAIL_CONFIG = (By.ID, "emailConfig")
    API_ENDPOINT = (By.ID, "apiEndpoint")
    API_PAYLOAD = (By.ID, "apiPayload")
    SEND_REQUEST_BUTTON = (By.XPATH, "//button[contains(text(),'Send Request')]")

class TestUtils:
    @staticmethod
    def click_button(driver, locator):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()

    @staticmethod
    def verify_popup(driver, expected_message):
        popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located(Locators.POPUP_CONTENT))
        assert expected_message in popup.text

    @staticmethod
    def verify_notification(driver, expected_message):
        notification = WebDriverWait(driver, 10).until(EC.presence_of_element_located(Locators.NOTIFICATION))
        assert expected_message in notification.text

    @staticmethod
    def fill_input(driver, locator, value):
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(value)

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, email, password):
        TestUtils.fill_input(self.driver, Locators.LOGIN_EMAIL, email)
        TestUtils.fill_input(self.driver, Locators.LOGIN_PASSWORD, password)
        TestUtils.click_button(self.driver, Locators.LOGIN_BUTTON)

class CompanyManagementPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def create_company(self, name, location):
        TestUtils.fill_input(self.driver, Locators.COMPANY_NAME, name)
        TestUtils.fill_input(self.driver, Locators.COMPANY_LOCATION, location)
        TestUtils.click_button(self.driver, Locators.COMPANY_CREATE_BUTTON)

class TeamManagementPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def create_team(self, name, member_email):
        TestUtils.fill_input(self.driver, Locators.TEAM_NAME, name)
        TestUtils.fill_input(self.driver, Locators.ADD_MEMBER, member_email)
        TestUtils.click_button(self.driver, Locators.TEAM_CREATE_BUTTON)

class ClientManagementPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_client(self, name, email):
        TestUtils.fill_input(self.driver, Locators.CLIENT_NAME, name)
        TestUtils.fill_input(self.driver, Locators.CLIENT_EMAIL, email)
        TestUtils.click_button(self.driver, Locators.ADD_CLIENT_BUTTON)

class RequirementGatheringPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def create_template(self, name, description):
        TestUtils.fill_input(self.driver, Locators.TEMPLATE_NAME, name)
        TestUtils.fill_input(self.driver, Locators.TEMPLATE_DESCRIPTION, description)
        TestUtils.click_button(self.driver, Locators.CREATE_TEMPLATE_BUTTON)

class ProjectManagementPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def create_project(self, name, budget, deadline):
        TestUtils.fill_input(self.driver, Locators.PROJECT_NAME, name)
        TestUtils.fill_input(self.driver, Locators.BUDGET, budget)
        TestUtils.fill_input(self.driver, Locators.DEADLINE, deadline)
        TestUtils.click_button(self.driver, Locators.CREATE_PROJECT_BUTTON)

    def assign_team(self, project_name, team_name):
        TestUtils.fill_input(self.driver, Locators.PROJECT_SELECT, project_name)
        TestUtils.fill_input(self.driver, Locators.TEAM_SELECT, team_name)
        TestUtils.click_button(self.driver, Locators.ASSIGN_TEAM_BUTTON)

class AddPropertyPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_property(self, property_type, name, location, tenant):
        select = self.wait.until(EC.presence_of_element_located(Locators.PROPERTY_TYPE))
        select.click()
        select.find_element(By.XPATH, f"//option[@value='{property_type}']").click()
        TestUtils.fill_input(self.driver, Locators.PROPERTY_NAME, name)
        TestUtils.fill_input(self.driver, Locators.PROPERTY_LOCATION, location)
        TestUtils.fill_input(self.driver, Locators.TENANT, tenant)
        TestUtils.click_button(self.driver, Locators.ADD_PROPERTY_BUTTON)

class CommunicationToolsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def send_chat_message(self, message):
        TestUtils.fill_input(self.driver, Locators.CHAT_INPUT, message)
        TestUtils.click_button(self.driver, Locators.SEND_BUTTON)

class FileSharingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def upload_file(self, file_path):
        TestUtils.fill_input(self.driver, Locators.FILE_UPLOAD, file_path)
        TestUtils.click_button(self.driver, Locators.UPLOAD_FILE_BUTTON)

class DesignPreviewPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def upload_design(self, file_path):
        TestUtils.fill_input(self.driver, Locators.DESIGN_UPLOAD, file_path)
        TestUtils.click_button(self.driver, Locators.UPLOAD_DESIGN_BUTTON)

class ProgressSharingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def generate_dashboard(self, project_name):
        TestUtils.fill_input(self.driver, Locators.PROJECT_SELECT, project_name)
        TestUtils.click_button(self.driver, Locators.VIEW_DASHBOARD_BUTTON)

class RecordTrackingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_expense(self, project_name, amount):
        TestUtils.fill_input(self.driver, Locators.PROJECT_SELECT, project_name)
        TestUtils.fill_input(self.driver, Locators.EXPENSE_AMOUNT, amount)
        TestUtils.click_button(self.driver, Locators.ADD_EXPENSE_BUTTON)

class CalendarSchedulingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def create_event(self, name, date):
        TestUtils.fill_input(self.driver, Locators.EVENT_NAME, name)
        TestUtils.fill_input(self.driver, Locators.EVENT_DATE, date)
        TestUtils.click_button(self.driver, Locators.CREATE_EVENT_BUTTON)

class IntegrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def connect_slack(self, api_key):
        TestUtils.fill_input(self.driver, Locators.INTEGRATION_SELECT, "Slack")
        TestUtils.fill_input(self.driver, Locators.API_KEY, api_key)
        TestUtils.click_button(self.driver, Locators.CONNECT_BUTTON)

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs("screenshots", exist_ok=True)

    def setUp(self):
        browser = os.getenv("BROWSER", "chrome").lower()
        if browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=options)
        else:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.utils = TestUtils()

    def tearDown(self):
        if self._outcome.errors or self._outcome.failures:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{self._testMethodName}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            logs = self.driver.get_log("browser")
            if logs:
                print(f"Browser logs: {logs}")
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        pass

@pytest.fixture(scope="class")
def test_data(request):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    data = {
        "company_name": f"TestCompany_{timestamp}",
        "team_name": f"TestTeam_{timestamp}",
        "project_name": f"TestProject_{timestamp}",
        "client_name": f"TestClient_{timestamp}",
    }
    request.cls.test_data = data
    yield
    pass

@pytest.mark.usefixtures("test_data")
class SignInTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL)
        self.page = LoginPage(self.driver)

    @pytest.mark.smoke
    def test_valid_login(self):
        self.page.login("admin@gmail.com", "123")
        self.utils.verify_popup(self.driver, "Sign in successful")

    def test_invalid_email_and_password(self):
        self.page.login("wrong@gmail.com", "wrongpass")
        self.utils.verify_popup(self.driver, "Owner not found")

    def test_valid_email_wrong_password(self):
        self.page.login("admin@gmail.com", "wrongpass")
        self.utils.verify_popup(self.driver, "Invalid credentials")

    def test_empty_credentials(self):
        self.page.login("", "")
        self.utils.verify_popup(self.driver, "Owner not found")

    def test_special_characters_email(self):
        self.page.login("test@<script>.com", "123")
        self.utils.verify_popup(self.driver, "Invalid email format")

    @pytest.mark.regression
    def test_multiple_failed_logins(self):
        for _ in range(5):
            self.page.login("admin@gmail.com", "wrongpass")
        self.utils.verify_popup(self.driver, "Too many failed attempts")

@pytest.mark.usefixtures("test_data")
class SecurityAndPermissionsTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard")

    @pytest.mark.smoke
    def test_admin_access_financials(self):
        self.driver.get(BASE_URL + "/dashboard/financials?user=admin")
        financials = self.wait.until(EC.presence_of_element_located(Locators.FINANCIALS_DISPLAY))
        assert "Financial Overview" in financials.text

    def test_non_admin_access_restriction(self):
        self.driver.get(BASE_URL + "/dashboard/financials?user=nonadmin")
        self.utils.verify_popup(self.driver, "Unauthorized action")

    def test_https_encryption(self):
        self.driver.get(BASE_URL)
        assert self.driver.current_url.startswith("https://")

    def test_manager_role_permissions(self):
        self.driver.get(BASE_URL + "/dashboard/team-management?user=manager")
        self.utils.fill_input(self.driver, Locators.TEAM_SELECT, self.test_data["team_name"])
        self.utils.click_button(self.driver, Locators.EDIT_TEAM_BUTTON)
        self.utils.verify_popup(self.driver, "Team updated successfully")

    def test_session_timeout(self):
        self.driver.get(BASE_URL + "?simulate_timeout=true")
        self.wait.until(EC.url_contains("/login"))
        assert "/login" in self.driver.current_url

    def test_xss_prevention(self):
        self.driver.get(BASE_URL)
        self.page = LoginPage(self.driver)
        self.page.login("<script>alert('xss')</script>", "123")
        self.utils.verify_popup(self.driver, "Invalid email format")

    @pytest.mark.regression
    def test_audit_log(self):
        self.driver.get(BASE_URL + "/dashboard/audit-log?user=admin")
        self.utils.fill_input(self.driver, Locators.ACTION_FILTER, "Project Creation")
        self.utils.click_button(self.driver, Locators.VIEW_LOG_BUTTON)
        log = self.wait.until(EC.presence_of_element_located(Locators.AUDIT_LOG))
        assert "Project created" in log.text

@pytest.mark.usefixtures("test_data")
class MultiCompanyManagementTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/company-management")
        self.page = CompanyManagementPage(self.driver)

    @pytest.mark.smoke
    def test_create_company(self):
        self.page.create_company(self.test_data["company_name"], "Test Location")
        self.utils.verify_popup(self.driver, "Company created successfully")

    def test_assign_project_to_company(self):
        self.utils.fill_input(self.driver, Locators.COMPANY_SELECT, self.test_data["company_name"])
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.ASSIGN_PROJECT_BUTTON)
        self.utils.verify_popup(self.driver, "Project assigned successfully")

    def test_company_metrics_dashboard(self):
        self.utils.fill_input(self.driver, Locators.COMPANY_SELECT, self.test_data["company_name"])
        self.utils.click_button(self.driver, Locators.VIEW_METRICS_BUTTON)
        dashboard = self.wait.until(EC.presence_of_element_located(Locators.COMPANY_DASHBOARD))
        assert "Performance Metrics" in dashboard.text

    def test_data_isolation(self):
        self.driver.get(BASE_URL + "/dashboard/company-management?user=companyA")
        self.utils.fill_input(self.driver, Locators.COMPANY_SELECT, "Company B")
        self.utils.click_button(self.driver, (By.XPATH, "//button[contains(text(),'View Data')]"))
        self.utils.verify_popup(self.driver, "Unauthorized access")

    def test_update_company_details(self):
        self.utils.fill_input(self.driver, Locators.COMPANY_SELECT, self.test_data["company_name"])
        self.utils.fill_input(self.driver, Locators.COMPANY_LOCATION, "Updated Location")
        self.utils.click_button(self.driver, Locators.UPDATE_COMPANY_BUTTON)
        self.utils.verify_popup(self.driver, "Company updated successfully")

    def test_invalid_company_name(self):
        self.page.create_company("", "Test Location")
        self.utils.verify_popup(self.driver, VALIDATION_RULES["company_name"]["error"])

    @pytest.mark.regression
    def test_large_company_description(self):
        self.page.create_company(self.test_data["company_name"], "A" * 1000)
        self.utils.verify_popup(self.driver, "Company created successfully")

@pytest.mark.usefixtures("test_data")
class TeamManagementTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/team-management")
        self.page = TeamManagementPage(self.driver)

    @pytest.mark.smoke
    def test_create_team(self):
        self.page.create_team(self.test_data["team_name"], "member@gmail.com")
        self.utils.verify_popup(self.driver, "Team created successfully")

    def test_add_team_member(self):
        self.utils.fill_input(self.driver, Locators.TEAM_SELECT, self.test_data["team_name"])
        self.utils.fill_input(self.driver, Locators.ADD_MEMBER, "newmember@gmail.com")
        self.utils.click_button(self.driver, (By.XPATH, "//button[contains(text(),'Add Member')]"))
        self.utils.verify_popup(self.driver, "Member added successfully")

    def test_assign_team_to_project(self):
        self.utils.fill_input(self.driver, Locators.TEAM_SELECT, self.test_data["team_name"])
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.ASSIGN_PROJECT_TO_TEAM_BUTTON)
        self.utils.verify_popup(self.driver, "Project assigned successfully")

    def test_team_creation_notification(self):
        self.page.create_team(self.test_data["team_name"], "member@gmail.com")
        self.utils.verify_notification(self.driver, "Team created")

    def test_invalid_team_name(self):
        self.page.create_team("", "member@gmail.com")
        self.utils.verify_popup(self.driver, VALIDATION_RULES["team_name"]["error"])

    def test_non_admin_cannot_modify_team(self):
        self.driver.get(BASE_URL + "/dashboard/team-management?user=nonadmin")
        self.utils.fill_input(self.driver, Locators.TEAM_SELECT, self.test_data["team_name"])
        self.utils.click_button(self.driver, Locators.EDIT_TEAM_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class ClientManagementTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/client-management")
        self.page = ClientManagementPage(self.driver)

    @pytest.mark.smoke
    def test_add_client(self):
        self.page.add_client(self.test_data["client_name"], "client@gmail.com")
        self.utils.verify_popup(self.driver, "Client added successfully")

    def test_assign_client_to_team(self):
        self.utils.fill_input(self.driver, (By.ID, "clientSelect"), self.test_data["client_name"])
        self.utils.fill_input(self.driver, Locators.TEAM_SELECT, self.test_data["team_name"])
        self.utils.click_button(self.driver, Locators.ASSIGN_TEAM_TO_CLIENT_BUTTON)
        self.utils.verify_popup(self.driver, "Team assigned successfully")

    def test_update_client_details(self):
        self.utils.fill_input(self.driver, (By.ID, "clientSelect"), self.test_data["client_name"])
        self.utils.fill_input(self.driver, Locators.CLIENT_EMAIL, "updated@gmail.com")
        self.utils.click_button(self.driver, Locators.UPDATE_CLIENT_BUTTON)
        self.utils.verify_popup(self.driver, "Client updated successfully")

    def test_client_search(self):
        self.utils.fill_input(self.driver, Locators.SEARCH_CLIENT, self.test_data["client_name"])
        self.utils.click_button(self.driver, Locators.SEARCH_CLIENT_BUTTON)
        result = self.wait.until(EC.presence_of_element_located(Locators.CLIENT_RESULTS))
        assert self.test_data["client_name"] in result.text

    def test_invalid_client_email(self):
        self.page.add_client(self.test_data["client_name"], "invalid-email")
        self.utils.verify_popup(self.driver, "Invalid email format")

    def test_non_authorized_cannot_view(self):
        self.driver.get(BASE_URL + "/dashboard/client-management?user=nonadmin")
        self.utils.fill_input(self.driver, (By.ID, "clientSelect"), self.test_data["client_name"])
        self.utils.click_button(self.driver, (By.XPATH, "//button[contains(text(),'View Client')]"))
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class RequirementGatheringTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/requirements")
        self.page = RequirementGatheringPage(self.driver)

    @pytest.mark.smoke
    def test_create_requirement_template(self):
        self.page.create_template("Test Template", "Test Requirements")
        self.utils.verify_popup(self.driver, "Template created successfully")

    def test_edit_template(self):
        self.utils.fill_input(self.driver, Locators.TEMPLATE_SELECT, "Test Template")
        self.utils.fill_input(self.driver, Locators.TEMPLATE_DESCRIPTION, "Updated Requirements")
        self.utils.click_button(self.driver, Locators.UPDATE_TEMPLATE_BUTTON)
        self.utils.verify_popup(self.driver, "Template updated successfully")

    def test_version_control(self):
        self.utils.fill_input(self.driver, Locators.TEMPLATE_SELECT, "Test Template")
        self.utils.click_button(self.driver, Locators.VIEW_VERSIONS_BUTTON)
        versions = self.wait.until(EC.presence_of_element_located(Locators.VERSION_HISTORY))
        assert "Version 1" in versions.text

    def test_template_creation_notification(self):
        self.page.create_template("New Template", "Test Requirements")
        self.utils.verify_notification(self.driver, "Template created")

    def test_invalid_template_name(self):
        self.page.create_template("", "Test Requirements")
        self.utils.verify_popup(self.driver, "Template name is required")

    def test_client_cannot_edit(self):
        self.driver.get(BASE_URL + "/dashboard/requirements?user=client")
        self.utils.fill_input(self.driver, Locators.TEMPLATE_SELECT, "Test Template")
        self.utils.click_button(self.driver, Locators.EDIT_TEMPLATE_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class ProjectManagementTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/project-management")
        self.page = ProjectManagementPage(self.driver)

    @pytest.mark.smoke
    def test_create_project(self):
        self.page.create_project(self.test_data["project_name"], "10000", "2025-12-31")
        self.utils.verify_popup(self.driver, "Project created successfully")

    def test_assign_project_to_team(self):
        self.page.assign_team(self.test_data["project_name"], self.test_data["team_name"])
        self.utils.verify_popup(self.driver, "Team assigned successfully")

    def test_add_task(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.fill_input(self.driver, Locators.TASK_NAME, "Task 1")
        self.utils.fill_input(self.driver, Locators.DUE_DATE, "2025-12-15")
        self.utils.click_button(self.driver, Locators.ADD_TASK_BUTTON)
        self.utils.verify_popup(self.driver, "Task added successfully")

    def test_gantt_chart_rendering(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.VIEW_GANTT_BUTTON)
        chart = self.wait.until(EC.presence_of_element_located(Locators.GANTT_CHART))
        assert chart.is_displayed()

    def test_project_update_notification(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.fill_input(self.driver, Locators.PROJECT_DESCRIPTION, "Updated Description")
        self.utils.click_button(self.driver, Locators.UPDATE_PROJECT_BUTTON)
        self.utils.verify_notification(self.driver, "Project updated")

    def test_invalid_budget(self):
        self.page.create_project(self.test_data["project_name"], "-100", "2025-12-31")
        self.utils.verify_popup(self.driver, "Invalid budget")

    @pytest.mark.regression
    def test_non_manager_cannot_edit(self):
        self.driver.get(BASE_URL + "/dashboard/project-management?user=nonmanager")
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.EDIT_PROJECT_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class AddPropertyTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/add-property")
        self.page = AddPropertyPage(self.driver)

    @pytest.mark.smoke
    def test_add_apartment_successfully(self):
        self.page.add_property("apartment", "Test Property", "Test Location", "Test Tenant")
        self.utils.verify_popup(self.driver, "Property added successfully")

    def test_add_shop_successfully(self):
        self.page.add_property("shop", "Test Shop", "Test Location", "Test Tenant")
        self.utils.verify_popup(self.driver, "Property added successfully")

    def test_property_notification(self):
        self.page.add_property("apartment", "Test Property", "Test Location", "Test Tenant")
        self.utils.verify_notification(self.driver, "Property added")

    def test_close_button_redirect(self):
        self.utils.click_button(self.driver, Locators.CLOSE_BUTTON)
        self.wait.until(EC.url_contains("/dashboard"))
        assert "/dashboard" in self.driver.current_url

    def test_missing_name(self):
        self.page.add_property("apartment", "", "Test Location", "Test Tenant")
        self.utils.verify_popup(self.driver, "Name is required")

    def test_invalid_tenant_email(self):
        self.page.add_property("apartment", "Test Property", "Test Location", "invalid-email")
        self.utils.verify_popup(self.driver, "Invalid tenant email")

@pytest.mark.usefixtures("test_data")
class CommunicationToolsTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/communication")
        self.page = CommunicationToolsPage(self.driver)

    @pytest.mark.smoke
    def test_send_chat_message(self):
        self.page.send_chat_message("Hello team")
        message = self.wait.until(EC.presence_of_element_located(Locators.CHAT_HISTORY))
        assert "Hello team" in message.text

    def test_add_project_comment(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.fill_input(self.driver, Locators.COMMENT, "Progress update")
        self.utils.click_button(self.driver, Locators.ADD_COMMENT_BUTTON)
        self.utils.verify_popup(self.driver, "Comment added successfully")

    def test_chat_ui_rendering(self):
        chat = self.wait.until(EC.presence_of_element_located(Locators.CHAT_INTERFACE))
        assert chat.is_displayed()

    def test_empty_message(self):
        self.page.send_chat_message("")
        self.utils.verify_popup(self.driver, "Message cannot be empty")

    def test_non_team_chat_access(self):
        self.driver.get(BASE_URL + "/dashboard/communication?user=nonmember")
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.ACCESS_CHAT_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized access")

@pytest.mark.usefixtures("test_data")
class FileSharingTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/file-sharing")
        self.page = FileSharingPage(self.driver)

    @pytest.mark.smoke
    def test_upload_file(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            self.page.upload_file(f.name)
        self.utils.verify_popup(self.driver, "File uploaded successfully")

    def test_create_folder(self):
        self.utils.fill_input(self.driver, Locators.FOLDER_NAME, "Test Folder")
        self.utils.click_button(self.driver, Locators.CREATE_FOLDER_BUTTON)
        self.utils.verify_popup(self.driver, "Folder created successfully")

    def test_share_file(self):
        self.utils.fill_input(self.driver, Locators.FILE_SELECT, "test.pdf")
        self.utils.fill_input(self.driver, Locators.TEAM_SELECT, self.test_data["team_name"])
        self.utils.click_button(self.driver, Locators.SHARE_FILE_BUTTON)
        self.utils.verify_popup(self.driver, "File shared successfully")

    def test_invalid_file_upload(self):
        with tempfile.NamedTemporaryFile(suffix=".exe") as f:
            self.page.upload_file(f.name)
        self.utils.verify_popup(self.driver, "Invalid file format")

    def test_restricted_file_access(self):
        self.driver.get(BASE_URL + "/dashboard/file-sharing?user=nonmember")
        self.utils.fill_input(self.driver, Locators.FILE_SELECT, "restricted.pdf")
        self.utils.click_button(self.driver, Locators.ACCESS_FILE_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized access")

@pytest.mark.usefixtures("test_data")
class DesignPreviewAndEditingTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/designs")
        self.page = DesignPreviewPage(self.driver)

    @pytest.mark.smoke
    def test_upload_design(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            self.page.upload_design(f.name)
        self.utils.verify_popup(self.driver, "Design uploaded successfully")

    def test_add_annotation(self):
        self.utils.fill_input(self.driver, Locators.DESIGN_SELECT, "wireframe.png")
        self.utils.fill_input(self.driver, Locators.ANNOTATION, "Add button here")
        self.utils.click_button(self.driver, Locators.ADD_ANNOTATION_BUTTON)
        self.utils.verify_popup(self.driver, "Annotation added successfully")

    def test_approve_design(self):
        self.utils.fill_input(self.driver, Locators.DESIGN_SELECT, "wireframe.png")
        self.utils.click_button(self.driver, Locators.APPROVE_DESIGN_BUTTON)
        self.utils.verify_popup(self.driver, "Design approved successfully")

    def test_design_preview_rendering(self):
        self.utils.fill_input(self.driver, Locators.DESIGN_SELECT, "wireframe.png")
        self.utils.click_button(self.driver, Locators.PREVIEW_DESIGN_BUTTON)
        preview = self.wait.until(EC.presence_of_element_located(Locators.DESIGN_PREVIEW))
        assert preview.is_displayed()

    def test_invalid_design_upload(self):
        with tempfile.NamedTemporaryFile(suffix=".exe") as f:
            self.page.upload_design(f.name)
        self.utils.verify_popup(self.driver, "Invalid file format")

    def test_non_authorized_cannot_annotate(self):
        self.driver.get(BASE_URL + "/dashboard/designs?user=nonmember")
        self.utils.fill_input(self.driver, Locators.DESIGN_SELECT, "wireframe.png")
        self.utils.click_button(self.driver, Locators.ADD_ANNOTATION_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class ProgressSharingTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/progress")
        self.page = ProgressSharingPage(self.driver)

    @pytest.mark.smoke
    def test_generate_progress_dashboard(self):
        self.page.generate_dashboard(self.test_data["project_name"])
        dashboard = self.wait.until(EC.presence_of_element_located(Locators.PROGRESS_DASHBOARD))
        assert "Completion Percentage" in dashboard.text

    def test_generate_report(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.GENERATE_REPORT_BUTTON)
        self.utils.verify_popup(self.driver, "Report generated successfully")

    def test_export_report(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.EXPORT_REPORT_BUTTON)
        self.utils.verify_popup(self.driver, "Report exported successfully")

    def test_invalid_dashboard_config(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, "")
        self.utils.click_button(self.driver, Locators.VIEW_DASHBOARD_BUTTON)
        self.utils.verify_popup(self.driver, "Project selection required")

    def test_non_authorized_cannot_view(self):
        self.driver.get(BASE_URL + "/dashboard/progress?user=nonadmin")
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.VIEW_DASHBOARD_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class RecordTrackingTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/records")
        self.page = RecordTrackingPage(self.driver)

    @pytest.mark.smoke
    def test_track_expenses(self):
        self.page.add_expense(self.test_data["project_name"], "5000")
        self.utils.verify_popup(self.driver, "Expense added successfully")

    def test_track_revenue(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.fill_input(self.driver, Locators.REVENUE_AMOUNT, "10000")
        self.utils.click_button(self.driver, Locators.ADD_REVENUE_BUTTON)
        self.utils.verify_popup(self.driver, "Revenue added successfully")

    def test_generate_financial_report(self):
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.GENERATE_REPORT_BUTTON)
        self.utils.verify_popup(self.driver, "Report generated successfully")

    def test_expense_notification(self):
        self.page.add_expense(self.test_data["project_name"], "5000")
        self.utils.verify_notification(self.driver, "Expense added")

    def test_invalid_expense(self):
        self.page.add_expense(self.test_data["project_name"], "-500")
        self.utils.verify_popup(self.driver, "Invalid expense amount")

    def test_non_admin_cannot_view(self):
        self.driver.get(BASE_URL + "/dashboard/records?user=nonadmin")
        self.utils.fill_input(self.driver, Locators.PROJECT_SELECT, self.test_data["project_name"])
        self.utils.click_button(self.driver, Locators.VIEW_RECORDS_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class CalendarAndSchedulingTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/calendar")
        self.page = CalendarSchedulingPage(self.driver)

    @pytest.mark.smoke
    def test_create_event(self):
        self.page.create_event("Team Meeting", "2025-12-01")
        self.utils.verify_popup(self.driver, "Event created successfully")

    def test_set_reminder(self):
        self.utils.fill_input(self.driver, Locators.EVENT_SELECT, "Team Meeting")
        self.utils.fill_input(self.driver, Locators.REMINDER, "1 day before")
        self.utils.click_button(self.driver, Locators.SET_REMINDER_BUTTON)
        self.utils.verify_popup(self.driver, "Reminder set successfully")

    def test_sync_calendar(self):
        self.utils.fill_input(self.driver, Locators.EVENT_SELECT, "Team Meeting")
        self.utils.click_button(self.driver, Locators.SYNC_CALENDAR_BUTTON)
        self.utils.verify_popup(self.driver, "Calendar synced successfully")

    def test_event_notification(self):
        self.page.create_event("New Meeting", "2025-12-01")
        self.utils.verify_notification(self.driver, "Event created")

    def test_invalid_event_date(self):
        self.page.create_event("Team Meeting", "2020-01-01")
        self.utils.verify_popup(self.driver, "Invalid date")

    def test_non_admin_cannot_create_event(self):
        self.driver.get(BASE_URL + "/dashboard/calendar?user=nonadmin")
        self.utils.fill_input(self.driver, Locators.EVENT_NAME, "Team Meeting")
        self.utils.click_button(self.driver, Locators.CREATE_EVENT_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class IntegrationTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL + "/dashboard/integrations")
        self.page = IntegrationPage(self.driver)

    @pytest.mark.smoke
    def test_slack_integration(self):
        self.page.connect_slack("valid-key")
        self.utils.verify_popup(self.driver, "Slack connected successfully")

    def test_email_integration(self):
        self.utils.fill_input(self.driver, Locators.INTEGRATION_SELECT, "Email")
        self.utils.fill_input(self.driver, Locators.EMAIL_CONFIG, "test@example.com")
        self.utils.click_button(self.driver, Locators.CONNECT_BUTTON)
        self.utils.verify_popup(self.driver, "Email connected successfully")

    def test_api_project_creation(self):
        self.utils.fill_input(self.driver, Locators.API_ENDPOINT, "/api/projects")
        self.utils.fill_input(self.driver, Locators.API_PAYLOAD, f'{{"name":"{self.test_data["project_name"]}"}}')
        self.utils.click_button(self.driver, Locators.SEND_REQUEST_BUTTON)
        self.utils.verify_popup(self.driver, "Project created successfully")

    def test_slack_notification_content(self):
        self.utils.fill_input(self.driver, Locators.INTEGRATION_SELECT, "Slack")
        self.utils.fill_input(self.driver, Locators.API_KEY, "valid-key")
        self.utils.click_button(self.driver, (By.XPATH, "//button[contains(text(),'Test Notification')]"))
        notification = self.wait.until(EC.presence_of_element_located((By.ID, "slackNotification")))
        assert "Project update" in notification.text

    def test_invalid_api_key(self):
        self.page.connect_slack("invalid-key")
        self.utils.verify_popup(self.driver, "Invalid API key")

    def test_non_admin_cannot_integrate(self):
        self.driver.get(BASE_URL + "/dashboard/integrations?user=nonadmin")
        self.utils.fill_input(self.driver, Locators.INTEGRATION_SELECT, "Slack")
        self.utils.click_button(self.driver, Locators.CONNECT_BUTTON)
        self.utils.verify_popup(self.driver, "Unauthorized action")

@pytest.mark.usefixtures("test_data")
class EndToEndTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(BASE_URL)
        self.login_page = LoginPage(self.driver)
        self.company_page = CompanyManagementPage(self.driver)
        self.team_page = TeamManagementPage(self.driver)
        self.project_page = ProjectManagementPage(self.driver)
        self.comm_page = CommunicationToolsPage(self.driver)
        self.progress_page = ProgressSharingPage(self.driver)

    @pytest.mark.smoke
    def test_create_company_to_project_workflow(self):
        self.login_page.login("admin@gmail.com", "123")
        self.utils.verify_popup(self.driver, "Sign in successful")
        self.driver.get(BASE_URL + "/dashboard/company-management")
        self.company_page.create_company(self.test_data["company_name"], "Test Location")
        self.utils.verify_popup(self.driver, "Company created successfully")
        self.driver.get(BASE_URL + "/dashboard/team-management")
        self.team_page.create_team(self.test_data["team_name"], "member@gmail.com")
        self.utils.verify_popup(self.driver, "Team created successfully")
        self.driver.get(BASE_URL + "/dashboard/project-management")
        self.project_page.create_project(self.test_data["project_name"], "10000", "2025-12-31")
        self.utils.verify_popup(self.driver, "Project created successfully")

    def test_project_collaboration_workflow(self):
        self.login_page.login("admin@gmail.com", "123")
        self.utils.verify_popup(self.driver, "Sign in successful")
        self.driver.get(BASE_URL + "/dashboard/project-management")
        self.project_page.assign_team(self.test_data["project_name"], self.test_data["team_name"])
        self.utils.verify_popup(self.driver, "Team assigned successfully")
        self.driver.get(BASE_URL + "/dashboard/communication")
        self.comm_page.send_chat_message("Project update")
        chat = self.wait.until(EC.presence_of_element_located(Locators.CHAT_HISTORY))
        assert "Project update" in chat.text

    @pytest.mark.regression
    def test_full_workflow_with_progress(self):
        self.login_page.login("admin@gmail.com", "123")
        self.utils.verify_popup(self.driver, "Sign in successful")
        self.driver.get(BASE_URL + "/dashboard/project-management")
        self.project_page.create_project(self.test_data["project_name"], "10000", "2025-12-31")
        self.utils.verify_popup(self.driver, "Project created successfully")
        self.driver.get(BASE_URL + "/dashboard/progress")
        self.progress_page.generate_dashboard(self.test_data["project_name"])
        dashboard = self.wait.until(EC.presence_of_element_located(Locators.PROGRESS_DASHBOARD))
        assert "Completion Percentage" in dashboard.text

if __name__ == "__main__":
    pytest.main(["-v", "--disable-warnings", "test_suite.py"])