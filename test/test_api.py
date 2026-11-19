import allure
import pytest
from faker import Faker
from api.YougileApi import YougileApi

fake = Faker("ru_RU")


@allure.epic("YouGile")
@allure.suite("API Тесты")
@allure.feature("Управление проектами")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("API-1: Получение проекта по его ID")
def test_get_project_by_id(
    api_client: YougileApi, created_project: dict[str, str]
) -> None:
    """Проверка получения данных проекта по его уникальному ID."""
    project_id = created_project["id"]
    expected_title = created_project["title"]

    with allure.step("Отправить GET-запрос на получение проекта по ID"):
        response = api_client.get_project_by_id(project_id)

    with allure.step("Проверить статус-код 200 и соответствие ID и названия"):
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == project_id
        assert body["title"] == expected_title


@allure.epic("YouGile")
@allure.suite("API Тесты")
@allure.feature("Управление задачами")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("API-2: Создание новой задачи в проекте")
def test_create_task(
    api_client: YougileApi, created_column: dict[str, str]
) -> None:
    """Проверка создания новой задачи в колонке проекта через API."""
    task_title = f"Тестовая задача {fake.word()}"
    task_description = fake.sentence()
    column_id = created_column["id"]

    with allure.step("Отправить POST-запрос на создание задачи"):
        response = api_client.create_task(
            title=task_title,
            column_id=column_id,
            description=task_description,
        )

    with allure.step("Проверить статус-код 201 и наличие ID созданной задачи"):
        assert response.status_code == 201
        body = response.json()
        assert "id" in body
        assert isinstance(body["id"], str)

    with allure.step("Очистка: удалить созданную задачу"):
        api_client.delete_task(body["id"])


@allure.epic("YouGile")
@allure.suite("API Тесты")
@allure.feature("Управление задачами")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("API-3: Получение списка задач")
def test_get_tasks_list(
    api_client: YougileApi, created_column: dict[str, str]
) -> None:
    """Проверка получения списка задач в колонке проекта."""
    column_id = created_column["id"]
    task_title = f"Задача для списка {fake.word()}"

    with allure.step("Подготовка: создать тестовую задачу в колонке"):
        create_resp = api_client.create_task(
            title=task_title, column_id=column_id
        )
        created_task_id = create_resp.json()["id"]

    with allure.step("Отправить GET-запрос на получение списка задач"):
        response = api_client.get_tasks(column_id=column_id)

    with allure.step("Проверить статус-код 200 и наличие созданной задачи в списке"):
        assert response.status_code == 200
        body = response.json()
        assert "content" in body
        assert isinstance(body["content"], list)
        task_ids = [task["id"] for task in body["content"]]
        assert created_task_id in task_ids

    with allure.step("Очистка: удалить созданную задачу"):
        api_client.delete_task(created_task_id)


@allure.epic("YouGile")
@allure.suite("API Тесты")
@allure.feature("Мессенджер и чаты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("API-4: Создание нового чата")
def test_create_group_chat(
    api_client: YougileApi, current_user_id: str
) -> None:
    """Проверка создания нового группового чата через API."""
    chat_title = f"Новый чат {fake.word()}"
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

    with allure.step("Отправить POST-запрос на создание группового чата"):
        response = api_client.create_group_chat(
            title=chat_title,
            users=users,
            user_role_map=user_role_map,
            role_config_map=role_config_map,
        )

    with allure.step("Проверить статус-код 201 и получение ID нового чата"):
        assert response.status_code == 201
        body = response.json()
        assert "id" in body
        assert isinstance(body["id"], str)

    with allure.step("Очистка: удалить созданный чат"):
        api_client.delete_group_chat(body["id"])



@allure.epic("YouGile")
@allure.suite("API Тесты")
@allure.feature("Мессенджер и чаты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("API-5: Отправка текстового сообщения в чат существующего проекта")
@pytest.mark.parametrize(
    "message_text",
    [
        "Тестирование отправки сообщения.",
        "1234567890 !@#$%^&*()_+",
    ],
)
def test_send_message_to_chat(
    api_client: YougileApi,
    created_chat: dict[str, str],
    message_text: str,
) -> None:
    """Проверка отправки текстового сообщения в групповой чат."""
    chat_id = created_chat["id"]

    with allure.step("Отправить POST-запрос с текстом сообщения в чат"):
        response = api_client.send_chat_message(
            chat_id=chat_id, text=message_text
        )

    with allure.step("Проверить статус-код 201 и возврат ID отправленного сообщения"):
        assert response.status_code == 201
        body = response.json()
        assert "id" in body
