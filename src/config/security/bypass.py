import cv2
import pytesseract
from selenium.webdriver.support.ui import WebDriverWait

class CaptchaHandler:
    def solve_captcha(self, driver):
        """Only works with simple CAPTCHAs when permitted"""
        try:
            img = driver.find_element('xpath', '//captcha/img')
            img.screenshot('captcha.png')
            
            # Simple image processing
            image = cv2.imread('captcha.png')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            
            input_field = driver.find_element('id', 'captcha-input')
            input_field.send_keys(text)
            return True
        except:
            return False  # Fallback to manual

class TwoFactorAuth:
    def handle_2fa(self, method='sms'):
        """Pauses for manual 2FA input when required"""
        if method == 'sms':
            input("Enter SMS code and press Enter: ")
        return True