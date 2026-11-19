import allure
from faker import Faker
from selenium.webdriver.remote.webdriver import WebDriver
from page.ProjectPage import ProjectPage
from page.ChatPage import ChatPage


fake = Faker("ru_RU")


@allure.epic("YouGile")
@allure.suite("UI Тесты")
@allure.feature("Управление проектами")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title(
    "UI-1: Создание нового проекта с задачами через кнопку '+ Добавить проект'"
)
def test_create_project_with_tasks(
    auth_browser: WebDriver, project_name: str
) -> None:
    """Проверка создания нового проекта с задачами через UI."""
    project_page = ProjectPage(auth_browser)

    with allure.step("Открыть раздел 'Моя компания' и создать новый проект"):
        project_page.open_my_company()
        project_page.create_project_with_tasks(project_name)

    with allure.step("Проверить, что проект открылся и его название отображается"):
        assert project_name in project_page.get_project_title()


@allure.epic("YouGile")
@allure.suite("UI Тесты")
@allure.feature("Управление проектами")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title(
    "UI-2: Изменение названия существующего проекта через верхнюю панель управления"
)
def test_rename_project(
    auth_browser: WebDriver, project_name: str, new_project_name: str
) -> None:
    """Проверка переименования проекта через верхнюю панель управления."""
    project_page = ProjectPage(auth_browser)

    with allure.step("Подготовка: создать новый проект"):
        project_page.open_my_company()
        project_page.create_project_with_tasks(project_name)

    with allure.step("Переименовать проект через верхнюю панель"):
        project_page.rename_project(new_project_name)

    with allure.step("Проверить обновление названия проекта в заголовке"):
        assert new_project_name in project_page.get_project_title()


@allure.epic("YouGile")
@allure.suite("UI Тесты")
@allure.feature("Управление задачами")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("UI-3: Удаление существующей задачи из колонки проекта")
def test_delete_task_from_column(
    auth_browser: WebDriver, project_name: str
) -> None:
    """Проверка удаления задачи из колонки на доске проекта."""
    task_name = f"Задача {fake.word()}"
    project_page = ProjectPage(auth_browser)

    with allure.step("Подготовка: создать проект и добавить в него задачу"):
        project_page.open_my_company()
        project_page.create_project_with_tasks(project_name)
        project_page.create_task(task_name)

    with allure.step("Удалить задачу и убедиться, что она исчезла из колонки"):
        assert project_page.delete_task(task_name) is True


@allure.epic("YouGile")
@allure.suite("UI Тесты")
@allure.feature("Мессенджер и чаты")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("UI-4: Изменение названия группового чата проекта в разделе 'Мессенджер'")
def test_rename_project_chat(
    auth_browser: WebDriver, project_name: str, new_chat_name: str
) -> None:
    """Проверка переименования чата проекта в разделе 'Мессенджер'."""
    project_page = ProjectPage(auth_browser)
    chat_page = ChatPage(auth_browser)

    with allure.step("Подготовка: создать проект с привязанным чатом"):
        project_page.open_my_company()
        project_page.create_project_with_tasks(project_name)

    with allure.step("Перейти в Мессенджер и открыть чат проекта"):
        chat_page.open_messenger()
        chat_page.open_chat(project_name)

    with allure.step("Переименовать чат и проверить новое название в списке"):
        assert chat_page.rename_chat(new_chat_name) is True

@allure.epic("YouGile")
@allure.suite("UI Тесты")
@allure.feature("Мессенджер и чаты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("UI-5: Отправка текстового сообщения в чат существующего проекта")
def test_send_message_to_project_chat(
    auth_browser: WebDriver, project_name: str
) -> None:
    """Проверка отправки текстового сообщения в чат проекта."""
    message_text = fake.sentence(nb_words=4)
    project_page = ProjectPage(auth_browser)
    chat_page = ChatPage(auth_browser)

    with allure.step("Подготовка: создать проект с привязанным чатом"):
        project_page.open_my_company()
        project_page.create_project_with_tasks(project_name)

    with allure.step("Перейти в Мессенджер и открыть чат проекта"):
        chat_page.open_messenger()
        chat_page.open_chat(project_name)

    with allure.step("Отправить сообщение и проверить его отображение в переписке"):
        assert chat_page.send_message(message_text) is True
