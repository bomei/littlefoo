import os
import threading
import time
import platform
import arrow
import yaml
from selenium import webdriver

from pyvirtualdisplay import Display

class Member:
    def __init__(self, name, banji, danwei):
        self.name = name
        self.banji = banji
        self.danwei = danwei

    def __str__(self):
        return 'name:{} | banji:{} | danwei:{}'.format(self.name, self.banji, self.danwei)


class Group:
    def __init__(self, yaml_file):
        buddy_info = yaml.load(open(yaml_file, 'r', encoding='utf-8'))
        # print('raw yaml rendered..',buddy_info)
        buddy_info = buddy_info['members']
        self.members = list()
        for each in buddy_info:
            self.members.append(Member(each['name'], each['banji'], each['danwei']))


class Pingjiao:
    def __init__(self, url, dry_run=True):
        print('in pingjiao init')
        self.dry_run = dry_run
        self.group = Group('pingjiao/members.yml').members
        # print(self.group)
        self.url = url
        self.log_info_dict = dict()
        self.log_file = 'log/pingjiao.log'
        self.today = arrow.now().format('YYYY-MM-DD')
        if os.path.exists('log/used_url.log.yml'):
            self.used_url = yaml.load(open('log/used_url.log.yml', 'r', encoding='utf-8'))
            if not isinstance(self.used_url, dict):
                self.used_url = dict()
        else:
            self.used_url = dict()

    def log_once(self, name, title):
        self.log_info_dict[arrow.now().isoformat()] = [name, title]

    def log_to_file(self):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            log = self.today + '\n'
            for k, v in self.log_info_dict.items():
                this_log = '{time} {name}\n{title}\n'.format(time=k, name=v[0], title=v[1])
                print(this_log)
                log += this_log
            f.write(log)

    def pingjiao(self):

        print(self.url, 'in pingjiao func...before')
        if self.url in self.used_url.values():
            return 'used url'

        print(self.url, ' this is in pingjiao func...')
        with open('pingjiao/pingjiao_template.js', 'r', encoding='utf-8') as f:
            js = f.read()
        try:
            if platform.system() != 'Windows':
                display = Display(visible=0, size=(800, 600))
                display.start()
            browser = webdriver.Firefox()
            for each in self.group:  # type: Member

                browser.get(self.url)
                js += '\ngogogo("{name}","{danwei}","{banji}");'.format(name=each.name, danwei=each.danwei,
                                                                        banji=each.banji)
                browser.execute_script(js)
                inserted_name = browser.find_elements_by_css_selector('.question-answer.format1')[0].find_elements_by_css_selector(
                    'input')[
                    0].get_attribute('value')
                web_title = browser.find_element_by_tag_name('title').get_attribute('text')
                if not self.dry_run:
                    # ActionChains(browser).move_to_element(submit_btn).click().perform()
                    submit_js = '$("#page-next").click();'
                    browser.execute_script(submit_js)
                    self.log_once(inserted_name, web_title)
                time.sleep(0.5)
            browser.quit()
            if platform.system() != 'Windows':
                display.stop()
            self.log_to_file()
            self.used_url[self.today] = self.url
            yaml.dump(self.used_url, open('log/used_url.log.yml', 'w', encoding='utf-8'))
            return 'pingjiao finish'
        except:
            print('error in pingjiao')
            return 'error in pinjiao'

    def run(self):
        t = threading.Thread(target=self.pingjiao)
        t.start()
