import pytest
from selenium import webdriver
from app.main import app
from flask_testing import LiveServerTestCase

class MyTest(LiveServerTestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()

    def test_index_page(self):
        self.driver.get(self.get_server_url())
        assert "Your Page Title" in self.driver.title

    def test_get_players(self):
        self.driver.get(f"{self.get_server_url()}/api/v1/players")
        response = self.driver.find_element_by_tag_name('body').text
        assert 'names' in response

if __name__ == "__main__":
    pytest.main(["-s", "test_ui.py"])