class SessionHelper:

    def __init__(self, application):
        self.application = application

    def login(self, username, password):
        wd = self.application.wd
        self.application.open_home_page()
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_css_selector("input[value='Login']").click()
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_css_selector("input[value='Login']").click()

    def logout(self):
        wd = self.application.wd
        wd.find_element_by_css_selector("span.user-info").click()
        wd.find_element_by_link_text("Logout").click()
