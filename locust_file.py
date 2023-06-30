import sys
from locust import HttpUser, task, between
from test_integration import *

class MyLocustUser(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente entre les requêtes

    @task
    def run_integration_tests(self):
        test_show_summary_with_existing_email(self.client)
        test_show_summary_with_non_existing_email(self.client)
        test_purchase_places_with_enough_points_available(self.client)
        test_purchase_places_with_not_enough_points_available(self.client)
        test_purchase_places_exceed_max_limit(self.client)
        test_purchase_valid_places(self.client)
        test_book_route(self.client)

if __name__ == "__main__":
    sys.argv = ['locust', '-f', __file__, '--host=http://localhost:5000']
    from locust.main import main
    main()
