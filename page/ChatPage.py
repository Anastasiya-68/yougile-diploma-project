import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChatPage:
    """Page Object для работы с разделом 'Мессенджер' и чатами в YouGile."""

    MESSENGER_BTN = (
        By.CSS_SELECTOR,
        "div[data-testid='messenger-menu-item']",
    )
    EDIT_CHAT_BTN = (
        By.CSS_SELECTOR,
        "div[data-testid='edit-group-chat']",
    )
    CHAT_NAME_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Введите название группового чата']",
    )
    SAVE_CHAT_NAME_BTN = (
        By.XPATH,
        "//span[contains(text(),'Сохранить')]",
    )
    MESSAGE_INPUT = (
        By.CSS_SELECTOR,
        "p[data-placeholder='Напишите сообщение в чат']",
    )
    SEND_MESSAGE_BTN = (
        By.CSS_SELECTOR,
        "svg[data-icon='IconSend']",
    )

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу мессенджера.

        :param driver: экземпляр веб-драйвера Selenium
        """
        self.__driver = driver
        self.__wait = WebDriverWait(driver, 25)

    @allure.step("Перейти в раздел 'Мессенджер'")
    def open_messenger(self) -> None:
        """Открывает раздел 'Мессенджер' через боковое меню."""
        messenger_btn = self.__wait.until(
            EC.element_to_be_clickable(self.MESSENGER_BTN)
        )
        messenger_btn.click()

    @allure.step("Открыть чат '{chat_name}' в списке чатов")
    def open_chat(self, chat_name: str) -> None:
        """
        Выбирает и открывает чат из списка по его названию.

        :param chat_name: название искомого чата
        """
        chat_locator = (
            By.XPATH,
            f"//ul[contains(@class, 'chat-list')]//div[contains(., '{chat_name}')]",
        )
        chat_item = self.__wait.until(
            EC.element_to_be_clickable(chat_locator)
        )
        chat_item.click()

    @allure.step("Переименовать открытый чат на '{new_chat_name}'")
    def rename_chat(self, new_chat_name: str) -> bool:
        """
        Изменяет название текущего группового чата и проверяет обновление в списке.

        :param new_chat_name: новое название для чата
        :return: True, если чат с новым названием отображается в списке
        """
        edit_btn = self.__wait.until(
            EC.element_to_be_clickable(self.EDIT_CHAT_BTN)
        )
        edit_btn.click()

        name_input = self.__wait.until(
            EC.visibility_of_element_located(self.CHAT_NAME_INPUT)
        )
        name_input.send_keys(Keys.CONTROL + "a")
        name_input.send_keys(Keys.BACKSPACE)
        name_input.send_keys(new_chat_name)

        save_btn = self.__wait.until(
            EC.element_to_be_clickable(self.SAVE_CHAT_NAME_BTN)
        )
        save_btn.click()

        new_chat_locator = (
            By.XPATH,
            f"//ul[contains(@class, 'chat-list')]//div[normalize-space()='{new_chat_name}']",
        )
        element = self.__wait.until(
            EC.visibility_of_element_located(new_chat_locator)
        )
        return element.is_displayed()

    @allure.step("Отправить сообщение '{message_text}' в открытый чат")
    def send_message(self, message_text: str) -> bool:
        """
        Вводит и отправляет текстовое сообщение в открытый чат.

        :param message_text: текст отправляемого сообщения
        :return: True, если отправленное сообщение появилось в окне переписки
        """
        msg_input = self.__wait.until(
            EC.element_to_be_clickable(self.MESSAGE_INPUT)
        )
        msg_input.click()
        msg_input.send_keys(message_text)

        send_btn = self.__wait.until(
            EC.element_to_be_clickable(self.SEND_MESSAGE_BTN)
        )
        send_btn.click()

        sent_message_locator = (
            By.XPATH,
            f"//div[normalize-space()='{message_text}']",
        )
        element = self.__wait.until(
            EC.visibility_of_element_located(sent_message_locator)
        )
        return element.is_displayed()
