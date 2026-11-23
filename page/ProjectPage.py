import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ProjectPage:
    """Page Object для работы с проектами и задачами в YouGile."""

    MY_COMPANY_MENU_BTN = (
        By.XPATH,
        "(//div[contains(text(),'Моя компания')])[1]",
    )
    ADD_PROJECT_BTN = (
        By.XPATH,
        "//span[contains(text(),'Добавить проект')]",
    )
    PROJECT_WITH_TASKS_OPTION = (
        By.XPATH,
        "//div[contains(text(),'Проект с задачами')]",
    )
    PROJECT_NAME_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Введите название проекта…']",
    )
    CONFIRM_CREATE_BTN = (
        By.XPATH,
        "//div[contains(text(),'Добавить проект с задачами')]",
    )
    HEADER_PROJECT_TITLE = (
        By.CSS_SELECTOR,
        "div[data-testid='project-name-upper-panel']",
    )
    PROJECT_OPTIONS_BTN = (
        By.CSS_SELECTOR,
        "button[data-testid='project-header-menu-button']",
    )
    RENAME_PROJECT_BTN = (
        By.CSS_SELECTOR, "div[data-testid='menu-item-edit']",
    )
    RENAME_PROJECT_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Название проекта']",
    )
    SAVE_PROJECT_NAME_BTN = (
        By.XPATH,
        "//span[contains(text(),'Сохранить')]",
    )

    # Локаторы для работы с задачами
    ADD_TASK_BTN = (
        By.XPATH,
        "//span[contains(text(),'Добавить задачу')]",
    )

    TASK_NAME_INPUT = (
        By.CSS_SELECTOR,
        "textarea[data-testid='board-task-input-name']",
    )

    TASK_MENU_BTN = (
        By.CSS_SELECTOR,
        "div[data-testid='board-task-menu']",
    )

    DELETE_TASK_BTN = (
        By.CSS_SELECTOR,
        "div[data-testid='menu-item-delete']",
    )

    CONFIRM_DELETE_TASK_BTN = (
        By.XPATH,
        "//div[@role='button'][normalize-space()='Удалить']",
    )

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу работы с проектами.

        :param driver: экземпляр веб-драйвера Selenium
        """
        self.__driver = driver
        self.__wait = WebDriverWait(driver, 25)

    @allure.step("Нажать на раздел 'Моя компания' в левом боковом меню")
    def open_my_company(self) -> None:
        """Открывает раздел 'Моя компания' в левой панели навигации."""
        company_btn = self.__wait.until(
            EC.element_to_be_clickable(self.MY_COMPANY_MENU_BTN)
        )
        company_btn.click()

    @allure.step("Создать новый проект с названием '{project_name}'")
    def create_project_with_tasks(self, project_name: str) -> None:
        """
        Создает новый проект с задачами через кнопку '+ Добавить проект'.

        :param project_name: название создаваемого проекта
        """
        add_btn = self.__wait.until(
            EC.element_to_be_clickable(self.ADD_PROJECT_BTN)
        )
        add_btn.click()

        option_btn = self.__wait.until(
            EC.element_to_be_clickable(self.PROJECT_WITH_TASKS_OPTION)
        )
        option_btn.click()

        name_input = self.__wait.until(
            EC.visibility_of_element_located(self.PROJECT_NAME_INPUT)
        )
        name_input.send_keys(project_name)

        confirm_btn = self.__wait.until(
            EC.element_to_be_clickable(self.CONFIRM_CREATE_BTN)
        )
        confirm_btn.click()

    @allure.step("Получить название открытого проекта из верхней панели")
    def get_project_title(self) -> str:
        """
        Возвращает текущее название открытого проекта из верхней панели.

        :return: строка с названием проекта
        """
        element = self.__wait.until(
            EC.visibility_of_element_located(self.HEADER_PROJECT_TITLE)
        )
        return element.text

    @allure.step("Переименовать проект на '{new_name}'")
    def rename_project(self, new_name: str) -> None:
        """
        Изменяет название проекта через меню в верхней панели управления.

        :param new_name: новое название проекта
        """
        menu_btn = self.__wait.until(
            EC.element_to_be_clickable(self.PROJECT_OPTIONS_BTN)
        )
        menu_btn.click()

        rename_option = self.__wait.until(
            EC.element_to_be_clickable(self.RENAME_PROJECT_BTN)
        )
        rename_option.click()

        name_input = self.__wait.until(
            EC.visibility_of_element_located(self.RENAME_PROJECT_INPUT)
        )
        name_input.send_keys(Keys.CONTROL + "a")
        name_input.send_keys(Keys.BACKSPACE)
        name_input.send_keys(new_name)

        save_btn = self.__wait.until(
            EC.element_to_be_clickable(self.SAVE_PROJECT_NAME_BTN)
        )
        save_btn.click()

        self.__wait.until(
            EC.text_to_be_present_in_element(
                self.HEADER_PROJECT_TITLE, new_name
            )
        )

    @allure.step("Создать новую задачу '{task_name}' в колонке")
    def create_task(self, task_name: str) -> None:
        """
        Добавляет новую задачу в колонку открытого проекта.

        :param task_name: название создаваемой задачи
        """
        add_btn = self.__wait.until(
            EC.element_to_be_clickable(self.ADD_TASK_BTN)
        )
        add_btn.click()

        task_input = self.__wait.until(
            EC.visibility_of_element_located(self.TASK_NAME_INPUT)
        )
        task_input.send_keys(task_name)
        task_input.send_keys(Keys.ENTER)

        # Ждем, пока карточка с новой задачей появится в колонке
        task_locator = (By.XPATH, f"//div[normalize-space()='{task_name}']")
        self.__wait.until(EC.visibility_of_element_located(task_locator))

    @allure.step("Удалить задачу '{task_name}' из колонки")
    def delete_task(self, task_name: str) -> bool:
        """
        Удаляет существующую задачу из колонки и проверяет её исчезновение.

        :param task_name: название удаляемой задачи
        :return: True, если карточка задачи успешно удалена со страницы
        """
        menu_btn = self.__wait.until(
            EC.element_to_be_clickable(self.TASK_MENU_BTN)
        )
        menu_btn.click()

        delete_option = self.__wait.until(
            EC.element_to_be_clickable(self.DELETE_TASK_BTN)
        )
        delete_option.click()

        confirm_btn = self.__wait.until(
            EC.element_to_be_clickable(self.CONFIRM_DELETE_TASK_BTN)
        )
        confirm_btn.click()

        task_locator = (By.XPATH, f"//div[normalize-space()='{task_name}']")
        self.__wait.until(EC.invisibility_of_element_located(task_locator))
        return True
