from selenium.webdriver import ChromeOptions

class MetaMaskConnector:
    def __init__(self):
        options = ChromeOptions()
        options.add_extension('metamask.crx')