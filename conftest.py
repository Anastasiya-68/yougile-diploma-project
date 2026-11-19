import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import config
from page.AuthPage import AuthPage
from faker import Faker
from api.YougileApi import YougileApi


fake = Faker("ru_RU")


@pytest.fixture
def api_client() -> YougileApi:
    """Возвращает экземпляр API-клиента YouGile для работы с запросами."""
    return YougileApi()

@pytest.fixture
def browser() -> WebDriver:
    """
    Запускает браузер Chrome на весь экран для теста,
    а после его завершения корректно закрывает сессию браузера.
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def auth_browser(browser: WebDriver) -> WebDriver:
    """
    Открывает сайт YouGile и авторизуется в системе перед началом теста.
    Вход выполняется под учетными данными из конфигурационного файла `config.py`.
    """
    auth_page = AuthPage(browser)
    auth_page.open_main_page()
    auth_page.login_as(config.EMAIL, config.PASSWORD)
    return browser

@pytest.fixture
def project_name() -> str:
    """
    Генерирует название проекта перед тестом и удаляет этот проект
    после теста вместе с созданным чатом проекта.
    """
    name = f"Проект {fake.word()}"
    yield name
    api = YougileApi()
    api.delete_project_by_title(name)
    api.delete_chat_by_title(name)

@pytest.fixture
def new_project_name() -> str:
    """
    Генерирует новое название для переименования проекта
    и удаляет его после теста вместе с созданным чатом проекта.
    """
    name = f"Проект {fake.word()}"
    yield name
    api = YougileApi()
    api.delete_project_by_title(name)
    api.delete_chat_by_title(name)

@pytest.fixture
def current_user_id(api_client: YougileApi) -> str:
    """Возвращает ID текущего пользователя компании из API."""
    response = api_client.get_users()
    users = response.json().get("content", [])
    for user in users:
        if user.get("email") == config.EMAIL:
            return user["id"]
    return users["id"]

@pytest.fixture
def created_project(api_client: YougileApi) -> dict[str, str]:
    """
    Создает проект перед тестом и удаляет его после завершения.
    Возвращает словарь с id и title проекта.
    """
    title = f"API Проект {fake.word()}"
    response = api_client.create_project(title=title)
    project_id = response.json()["id"]

    yield {"id": project_id, "title": title}

    api_client.delete_project(project_id)

@pytest.fixture
def created_column(
    api_client: YougileApi, created_project: dict[str, str]
) -> dict[str, str]:
    """
    Создает доску и колонку внутри проекта.
    Очистка происходит автоматически при удалении проекта.
    """
    board_resp = api_client.create_board(
        title=f"Доска {fake.word()}", project_id=created_project["id"]
    )
    board_id = board_resp.json()["id"]

    column_resp = api_client.create_column(
        title=f"Колонка {fake.word()}", board_id=board_id
    )
    column_id = column_resp.json()["id"]

    return {"id": column_id, "board_id": board_id}

@pytest.fixture
def created_chat(
    api_client: YougileApi, current_user_id: str
) -> dict[str, str]:
    """
    Создает групповой чат перед тестом и удаляет его после.
    Возвращает словарь с id и title чата.
    """
    title = f"API Чат {fake.word()}"
    users = {current_user_id: {"notified": True}}
    user_role_map = {current_user_id: "owner"}
    role_config_map = {
        "owner": {
            "editProperties": True,
            "editAdmins": True,
            "editUsers": True,
            "sendMessages": True,
            "removeMessages": True,
        }
    }

    response = api_client.create_group_chat(
        title=title,
        users=users,
        user_role_map=user_role_map,
        role_config_map=role_config_map,
    )
    chat_id = response.json()["id"]

    yield {"id": chat_id, "title": title}

    api_client.delete_group_chat(chat_id)

@pytest.fixture
def new_chat_name() -> str:
    """
    Генерирует новое название для переименования чата
    и удаляет переименованный чат после завершения теста.
    """
    name = f"Чат {fake.word()}"
    yield name
    api = YougileApi()
    api.delete_chat_by_title(name)
