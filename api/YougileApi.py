import requests
import config
import allure


class YougileApi:
    def __init__(self) -> None:
        """Класс для взаимодействия с REST API сервиса YouGile v2.0."""

        self.url = config.API_URL
        self.headers = {
            "Authorization": f"Bearer {config.API_KEY}",
            "Content-Type": "application/json",
        }

    @allure.step("Удалить проект по названию '{project_name}'")
    def delete_project_by_title(self, project_name: str) -> None:
        for _ in range(3):
            response = requests.get(
                f"{self.url}/projects",
                headers=self.headers,
                params={"limit": 1000},
            )
            if response.status_code == 200:
                projects = response.json()["content"]
                for project in projects:
                    if project["title"] == project_name:
                        project_id = project["id"]
                        requests.put(
                            f"{self.url}/projects/{project_id}",
                            headers=self.headers,
                            json={"deleted": True},
                        )
                        return

    @allure.step("Удалить групповой чат по названию '{chat_name}'")
    def delete_chat_by_title(self, chat_name: str) -> None:
        response = requests.get(
            f"{self.url}/group-chats",
            headers=self.headers,
            params={"title": chat_name},
        )
        if response.status_code == 200:
            chats = response.json()["content"]

            for chat in chats:
                if chat_name in chat["title"]:
                    chat_id = chat["id"]
                    requests.put(
                        f"{self.url}/group-chats/{chat_id}",
                        headers=self.headers,
                        json={"deleted": True},
                    )

    @allure.step("Создать проект '{title}'")
    def create_project(
        self, title: str, users: dict[str, str] | None = None
    ) -> requests.Response:
        body: dict = {"title": title}
        if users:
            body["users"] = users
        return requests.post(
            f"{self.url}/projects", headers=self.headers, json=body
        )

    @allure.step("Получить проект по ID '{project_id}'")
    def get_project_by_id(self, project_id: str) -> requests.Response:
        return requests.get(
            f"{self.url}/projects/{project_id}", headers=self.headers
        )

    @allure.step("Удалить проект по ID '{project_id}'")
    def delete_project(self, project_id: str) -> requests.Response:
        return requests.put(
            f"{self.url}/projects/{project_id}",
            headers=self.headers,
            json={"deleted": True},
        )

    @allure.step("Создать доску '{title}' в проекте '{project_id}'")
    def create_board(self, title: str, project_id: str) -> requests.Response:
        body = {"title": title, "projectId": project_id}
        return requests.post(
            f"{self.url}/boards", headers=self.headers, json=body
        )

    @allure.step("Создать колонку '{title}' на доске '{board_id}'")
    def create_column(
        self, title: str, board_id: str, color: int = 1
    ) -> requests.Response:
        body = {"title": title, "boardId": board_id, "color": color}
        return requests.post(
            f"{self.url}/columns", headers=self.headers, json=body
        )

    @allure.step("Создать задачу '{title}' в колонке '{column_id}'")
    def create_task(
        self,
        title: str,
        column_id: str,
        description: str | None = None,
    ) -> requests.Response:
        body: dict = {"title": title, "columnId": column_id}
        if description:
            body["description"] = description
        return requests.post(
            f"{self.url}/tasks", headers=self.headers, json=body
        )

    @allure.step("Получить список задач")
    def get_tasks(
        self, column_id: str | None = None, title: str | None = None
    ) -> requests.Response:
        params: dict = {}
        if column_id:
            params["columnId"] = column_id
        if title:
            params["title"] = title
        return requests.get(
            f"{self.url}/task-list", headers=self.headers, params=params
        )

    @allure.step("Удалить задачу по ID '{task_id}'")
    def delete_task(self, task_id: str) -> requests.Response:
        return requests.put(
            f"{self.url}/tasks/{task_id}",
            headers=self.headers,
            json={"deleted": True},
        )

    @allure.step("Получить список сотрудников компании")
    def get_users(self) -> requests.Response:
        return requests.get(f"{self.url}/users", headers=self.headers)

    @allure.step("Создать групповой чат '{title}'")
    def create_group_chat(
        self,
        title: str,
        users: dict,
        user_role_map: dict,
        role_config_map: dict,
    ) -> requests.Response:
        body = {
            "title": title,
            "users": users,
            "userRoleMap": user_role_map,
            "roleConfigMap": role_config_map,
        }
        return requests.post(
            f"{self.url}/group-chats", headers=self.headers, json=body
        )

    @allure.step("Удалить групповой чат по ID '{chat_id}'")
    def delete_group_chat(self, chat_id: str) -> requests.Response:
        return requests.put(
            f"{self.url}/group-chats/{chat_id}",
            headers=self.headers,
            json={"deleted": True},
        )

    @allure.step("Отправить сообщение в чат '{chat_id}'")
    def send_chat_message(
        self, chat_id: str, text: str, label: str | None = None
    ) -> requests.Response:
        body: dict = {"text": text}
        if label:
            body["label"] = label
        return requests.post(
            f"{self.url}/chats/{chat_id}/messages",
            headers=self.headers,
            json=body,
        )
