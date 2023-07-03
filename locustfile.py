from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        response = self.client.get("/index")

