from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec 
import pytest

class TestSaucePyTest:
    def setup_method(self): 
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com")
        self.driver.maximize_window() 

    def teardown_method(self): 
        self.driver.quit()
    

    @pytest.mark.parametrize("username,password",[("","")])
    def test_invalid_user(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name"))).send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password"))).send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()
        error_message_user = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        assert error_message_user.text == "Epic sadface: Username is required"

    
    @pytest.mark.parametrize("username,password",[("locked_out_user","")])
    def test_invalid_password(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name"))).send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password"))).send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()
        error_message_password = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        assert error_message_password.text == "Epic sadface: Password is required"
    
    
    @pytest.mark.parametrize("username,password",[("locked_out_user","secret_sauce")])
    def test_invalid_lock(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name"))).send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password"))).send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()
        error_message_lock = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        assert error_message_lock.text == "Epic sadface: Sorry, this user has been locked out."
    
    
    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")])
    def test_valid_item(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name"))).send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password"))).send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()
        inventory_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(inventory_items) == 6
   

    @pytest.mark.parametrize("username,password",[("1","secret_sauce"),("problem_user","1"),("1","1")])
    def test_invalid_match(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name"))).send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password"))).send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()
        error_message_match = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        assert error_message_match.text == "Epic sadface: Username and password do not match any user in this service"


    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")]) 
    def test_add_product(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name"))).send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password"))).send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='add-to-cart-sauce-labs-backpack']"))).click()
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='shopping_cart_container']/a"))).click()
        product = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='item_4_title_link']")))
        assert product.text == "Sauce Labs Backpack"
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='continue-shopping']"))).click()
        remove = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*//*[@id='remove-sauce-labs-backpack']")))
        assert remove.text == "Remove"

    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")]) 
    def test_product_review(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name"))).send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password"))).send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()
        self.driver.execute_script("window.scrollTo(0,500)")
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH, "//*[@id='item_2_title_link']/div"))).click()
        product_title = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='inventory_item_container']/div/div/div[2]/div[1]")))
        assert product_title.text == "Sauce Labs Onesie"
        self.driver.find_element(By.XPATH,"//*[@id='back-to-products']").click()
        