import os
from selenium import webdriver
from PIL import Image
from io import BytesIO
import numpy as np
import subprocess

class Highlighter():

    def __init__(self):
        os.environ['MOZ_HEADLESS'] = '1'
        self.load_local_files()

    def store_snapshot(self, img_target, grayscale=False):
        data = self.driver.get_screenshot_as_png()

        if grayscale:
            img = Image.open(BytesIO(data)).convert('LA')
        else:
            img = Image.open(BytesIO(data)).convert()

        img = img.crop((0, 0, 1366, 1366))

        img.save(img_target)
        numpy_array = np.asarray(img)

    """
    source: wayback
    """
    def prepare(self, webpage, wayback=False):
        # self.driver = webdriver.Chrome("./libraries/chromedriver")

        # caps = webdriver.DesiredCapabilities.FIREFOX
        # caps["marionette"] = False
        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.set_preference('permissions.default.stylesheet', 1)
        firefoxProfile.set_preference('permissions.default.image', 1)
        firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
        firefoxProfile.set_preference("http.response.timeout", 90)
        firefoxProfile.set_preference("dom.max_script_run_time", 90)

        # # now create browser instance and APPLY the FirefoxProfile
        self.driver = webdriver.Firefox(firefox_profile=firefoxProfile)
        #self.driver = webdriver.PhantomJS();
        # self.driver.set_window_position(0, 0)
        # we remove 74 pixels at the top.
        height = 1366
        if wayback:
            height += 74
        self.driver.set_window_size(1366, height) 
        print(self.driver.get_window_size(windowHandle='current'))
        self.driver.get(webpage)

        self.driver.execute_script(self.injectJquery)
        self.driver.execute_script(self.injectHighlighter)
        self.driver.execute_script(self.injectCSS)

        if wayback:
            self.driver.execute_script('$("#wm-ipp").remove();')

    def set_highlights(self, query):
        for word in query.split(" "):
            self.driver.execute_script(self.search.format(word))

    def remove_content(self):
        self.driver.execute_script(self.coverAll)

    def load_local_files(self):
        with open('libraries/jquery-3.2.1.min.js', 'r') as file:
            self.injectJquery = file.read().replace('\n', '')

        with open('libraries/jquery.highlight-5.js', 'r') as file:
            self.injectHighlighter = file.read().replace('\n', '')

        with open('libraries/style.css', 'r') as file:
            self.injectCSS = 'addStyleString("{}");'.format(file.read().replace('\n', ''))

    def close(self, driver=True):
        if driver:
            self.driver.close()
        subprocess.Popen(["killall", "firefox"])
        subprocess.Popen(["killall", "geckodriver"])
        subprocess.Popen(["pkill", "-f", "firefox"])
        subprocess.Popen(["pkill", "-f", "geckodriver"])

    def get_final_url(self):
        return self.driver.current_url

    search = "$('html').highlight('{}');"
    
    coverAll = """addStyleString('.highlight { color: black !important; background-color: black !important; }'); $("<html>").addClass("cover").appendTo("body").animate({opacity : 1},0).delay(0);"""

    
