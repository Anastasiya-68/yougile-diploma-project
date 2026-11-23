import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthPage:
    """Page Object для страницы авторизации YouGile."""

    URL = "https://ru.yougile.com/"
    HEADER_LOGIN_BUTTON = (By.CSS_SELECTOR, "a[role='button']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='example@mail.ru']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Введите пароль']")
    FORM_LOGIN_BUTTON = (
        By.XPATH,
        "//div[@role='button' and contains(., 'Войти')]"
    )

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу входа.

        :param driver: экземпляр веб-драйвера Selenium
        """
        self.__url = self.URL
        self.__driver = driver
        self.__wait = WebDriverWait(driver, 10)

    @allure.step("Открыть главную страницу YouGile")
    def open_main_page(self) -> None:
        """Открывает главную страницу сервиса YouGile."""
        self.__driver.get(self.__url)

    @allure.step("Авторизоваться под пользователем {email}")
    def login_as(self, email: str, password: str) -> None:
        """
        Выполняет вход в систему с указанными учетными данными.

        :param email: адрес электронной почты пользователя
        :param password: пароль от учетной записи
        """
        header_login_btn = self.__wait.until(
            EC.element_to_be_clickable(self.HEADER_LOGIN_BUTTON)
        )
        header_login_btn.click()

        email_input = self.__wait.until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )
        email_input.send_keys(email)

        password_input = self.__wait.until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )
        password_input.send_keys(password)

        form_login_btn = self.__wait.until(
            EC.element_to_be_clickable(self.FORM_LOGIN_BUTTON)
        )
        form_login_btn.click()

    @allure.step("Получить текущий URL страницы")
    def get_current_url(self) -> str:
        """
        Возвращает текущий URL открытой страницы в браузере.

        :return: строка с текущим URL
        """
        return self.__driver.current_url
