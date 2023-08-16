from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        response = self.client.get("/")

    @task
    def showSummary(self):
        self.client.post('/showSummary', data={"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get('/book/Spring Festival/Simply Lift')

    @task
    def purchasePlaces(self):
        self.client.post('/purchasePlaces', data={'competition': 'HollyDays', 'club': 'Simply_Lift', 'places': '3'})

    @task
    def pointsDisplay(self):
        response = self.client.get("/pointsDisplay")

    @task
    def logout(self):
        response = self.client.get("/logout")


