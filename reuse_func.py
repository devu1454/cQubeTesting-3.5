import configparser
import datetime
import json
import os
import subprocess
import time
from datetime import date
from PIL import ImageColor
from selenium.webdriver.firefox.options import Options

#import psycopg2
import psycopg2
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from Locators.parameters import Data
from get_dir import pwd


class GetData():

    def __init__(self):
        self.p = pwd()

    def get_domain_name(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['domain']

    def get_username(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['username']

    def get_password(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['password']

    def get_admin_username(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['username']

    def get_admin_password(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['password']

    def get_current_date(self):
        today = date.today()
        dates = today.strftime('%d-%m-%Y')
        return dates

    def get_driver(self):
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': self.p.get_download_dir()}
        options.add_experimental_option('prefs', prefs)
        options.add_argument("--window-size=3860,2160")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options, executable_path=self.p.get_driver_path())
        self.driver.set_window_size(3860, 2160)
        print('window size :',self.driver.get_window_size())
        print("Current session is {}".format(self.driver.session_id))
        return self.driver

    def get_firefox_driver(self):
        p = pwd()
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(firefox_options=options, executable_path=p.get_firefox_driver_path())
        driver.set_window_size(3860, 2160)
        print('Screen Resolutions : ', driver.get_window_size())
        prefs = {'download.default_directory': self.p.get_download_dir()}
        options.add_argument(prefs)
        return driver


    def open_cqube_appln(self, driver):
        self.driver = driver
        # self.driver.maximize_window()
        self.driver.set_window_size(3860,2160)
        try:
            self.driver.get(self.get_domain_name())
        except WebDriverException:
                print("page down")
        self.driver.implicitly_wait(60)

    def login_cqube(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(60)
        self.driver.find_element_by_name(Data.email).send_keys(self.get_username())
        time.sleep(1)
        self.driver.find_element_by_name(Data.passwd).send_keys(self.get_password())
        time.sleep(1)
        self.driver.find_element_by_id(Data.login).click()
        self.page_loading(self.driver)
        time.sleep(1)
        self.driver.find_element_by_id('cQb_dhsbrd').click()
        time.sleep(3)
        self.page_loading(self.driver)

    def login_to_adminconsole(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(60)
        self.driver.find_element_by_name(Data.email).send_keys(self.get_username())
        self.driver.find_element_by_name(Data.passwd).send_keys(self.get_password())
        self.driver.find_element_by_id(Data.login).click()
        self.page_loading(self.driver)
        self.driver.find_element_by_id('admin_console').click()
        time.sleep(3)
        self.page_loading(self.driver)

    def navigate_to_telemetry(self):
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.Telemetry).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.tele_report).click()
        self.page_loading(self.driver)

    def navigate_to_periodic_report(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.std_performance).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.patmap).click()
        time.sleep(4)

    def navigate_to_heatchart_report(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.std_performance).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.patheatchart).click()
        time.sleep(4)

    def navigate_to_lo_table_report(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.std_performance).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.patlotable).click()
        time.sleep(3)

    def navigate_to_sat_heatchart_report(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.std_performance).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.sat_heatchart).click()
        time.sleep(3)

    def navigate_to_composite_report(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.composite_metrics).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.composite_metric).click()
        time.sleep(3)

    def logs_page(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.Dashboard).click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[@id='logs']").click()
        time.sleep(3)

    def page_loading(self, driver):
        try:
            driver.implicitly_wait(20)
            self.driver = driver
            for x in range(1, 10):
                elem = self.driver.find_element_by_id('loader').text
                if str(elem) == "Loading…":
                    time.sleep(5)
                if str(elem) != "Loading…":
                    time.sleep(5)
                    break
        except NoSuchElementException:
            pass

    def click_on_state(self, driver):
        self.driver = driver
        self.driver.find_element_by_xpath(Data.hyper_link).click()
        time.sleep(4)

    def get_data_status(self):
        errMsg = self.driver.find_element_by_css_selector('p#errMsg')
        return errMsg

    def navigate_passwordchange(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(Data.user_options).click()
        time.sleep(2)

    def get_management_selected_option(self):
        self.driver.implicitly_wait(10)
        management_name = self.driver.find_element_by_id('name').text
        management_name = management_name[16:].strip().lower()
        return management_name

    def get_month_and_year_values(self):
        year = self.driver.find_element_by_id('year').text
        month = self.driver.find_element_by_id('month').text
        return year , month

    def pat_year_month_firstselected(self):
        year = Select(self.driver.find_element_by_id('year'))
        month = Select(self.driver.find_element_by_id('month'))
        year = year.first_selected_option.text
        month = month.first_selected_option.text
        return year , month

    def get_student_month_and_year_values(self):
        times = Select(self.driver.find_element_by_id('period'))
        # times.select_by_visible_text(' Year and Month ')
        times.select_by_index(5)
        year = Select(self.driver.find_element_by_id(Data.sar_year))
        month = Select(self.driver.find_element_by_id(Data.sar_month))
        self.year = (year.first_selected_option.text).strip()
        self.month = (month.first_selected_option.text).strip()
        return self.year,self.month

    def get_crc_month_and_year_values(self):
        times = Select(self.driver.find_element_by_id('period'))
        times.select_by_index(5)
        year = Select(self.driver.find_element_by_id(Data.sar_year))
        month = Select(self.driver.find_element_by_id(Data.sar_month))
        self.year = (year.first_selected_option.text).strip()
        self.month = (month.first_selected_option.text).strip()
        datetime_object = datetime.datetime.strptime(self.month, "%B")
        month_number = datetime_object.month
        return self.year,month_number

    def get_pat_month_and_year_values(self):
        year = Select(self.driver.find_element_by_id(Data.sar_year))
        month = Select(self.driver.find_element_by_id(Data.sar_month))
        self.year = (year.first_selected_option.text).strip()
        self.month = (month.first_selected_option.text).strip()
        return self.year, self.month

    def pat_month_and_year_values(self):
        year = Select(self.driver.find_element_by_id('year'))
        month = Select(self.driver.find_element_by_id('month'))
        self.year = (year.first_selected_option.text).strip()
        self.month = (month.first_selected_option.text).strip()
        return self.year,self.month

    def navigate_to_student_report(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.attendance).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.studentattendance).click()
        time.sleep(3)

    def navigate_to_teacher_attendance_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.attendance).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.teacherattendance).click()
        time.sleep(3)

    def navigate_to_composite_infrastructure(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.sch_infra).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.composite).click()
        time.sleep(3)

    def navigate_to_school_infrastructure_map(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.sch_infra).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.inframap).click()
        time.sleep(5)

    def select_month_year(self, y, m):
        year = Select(self.driver.find_element_by_id(Data.sar_year))
        month = Select(self.driver.find_element_by_id(Data.sar_month))
        time.sleep(2)
        year.select_by_visible_text(y)
        time.sleep(2)
        month.select_by_visible_text(m)
        time.sleep(2)

    def navigate_to_semester_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(3)
        self.driver.find_element_by_id(Data.std_performance).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.satmap).click()
        time.sleep(5)

    def navigate_to_udise_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.sch_infra).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.udise).click()
        time.sleep(3)

    def navigate_to_crc_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.crc_visit).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.crcreport).click()
        time.sleep(3)

    def navigate_to_diksha_graph(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.diksha_graph).click()
        time.sleep(3)

    def navigate_to_diksha_content_course(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.content_course).click()
        time.sleep(3)

    def navigate_to_tpd_content_progress(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.course_progress).click()
        time.sleep(3)

    def navigate_to_tpd_enrollment_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.tpd_enrollment).click()
        time.sleep(3)

    def navigate_to_gps_of_learning_tpd(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.gps_tpd_map).click()
        time.sleep(3)

    def navigate_to_tpd_content_usage_piechart_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.other_diksha).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.tpd_content_preference).click()
        time.sleep(5)

    def navigate_to_etb_content_plays_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.diksha_ETB).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.gps_etb_map).click()
        time.sleep(3)

    def navigate_to_etb_usage_per_capita_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.diksha_ETB).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.usage_capita).click()
        time.sleep(3)

    def navigate_to_tpd_user_engagement_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.user_engage).click()
        time.sleep(3)


    def navigate_to_tpd_user_on_boarding_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.on_boarding).click()
        time.sleep(3)

    def navigate_to_tpd_completion_percentage(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.completion_percentage).click()
        time.sleep(3)

    def navigate_to_health_card_index(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.progress_card).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.Progresscard).click()
        time.sleep(3)

    def navigate_to_tpd_percentage_progress(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.tpd_percentage).click()
        time.sleep(3)

    def navigate_to_diksha_content_textbook(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.diksha_ETB).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.content_textbook).click()
        time.sleep(3)

    def navigate_to_column_course(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.usage_course).click()
        time.sleep(3)

    def navigate_to_column_textbook(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.diksha_ETB).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.usage_textbook).click()
        time.sleep(3)

    def navigate_to_etb_nation_learning_report(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.diksha_ETB).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.nation_learning).click()
        time.sleep(3)

    def navigate_to_completion_error(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.tpd_opts).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.completion).click()
        time.sleep(3)

    def navigate_to_semester_exception(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.Exception_Reports).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.semesterexception).click()
        time.sleep(3)

    def navigate_to_pat_exception(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.Exception_Reports).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.patexception).click()
        time.sleep(3)

    def navigate_to_teacher_exception(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.Exception_Reports).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.teacherexception).click()
        time.sleep(3)

    def navigate_to_student_exception(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_id(Data.menu_icon).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.Exception_Reports).click()
        time.sleep(2)
        self.driver.find_element_by_id(Data.studentexception).click()
        time.sleep(3)

    def Details_text(self):
        Details = self.driver.find_elements_by_xpath(Data.details)
        time.sleep(5)
        for i in range(len(Details)):
            print(Details[i].text)

    def Click_HomeButton(self):
        self.driver.find_element_by_id(Data.homeicon).click()
        time.sleep(3)

    def CRC_footers(self):
        footer = self.driver.find_elements_by_xpath(Data.footer)
        for i in range(len(footer)):
            print(footer[i].text)
            time.sleep(5)

    def test_Distnames(self):
        dnames = self.driver.find_elements_by_xpath(Data.SAR_Dnames)
        for i in range(len(dnames)):
            print(dnames[i].text)
            time.sleep(2)

    def dots_dist(self):
        distnames = self.driver.find_elements_by_xpath(Data.SAR_Dnames)
        for i in range(len(distnames)):
            distnames[i].click()
            time.sleep(3)
            lists = self.driver.find_elements_by_class_name(Data.dots)
            time.sleep(2)
            count = len(lists) - 1
            print(distnames[i].text, ":", count)

    def crcclusters_click(self):
        clu = self.driver.find_elements_by_xpath(Data.clusterlist)
        for i in range(len(clu)):
            clu[i].click()
            time.sleep(3)

    def clusters_text(self):
        cluster = self.driver.find_elements_by_xpath(Data.clusterlist)
        for i in range(len(cluster)):
            cluster[i].click()
            print(cluster[i].text)
            time.sleep(5)

    def get_driver_path(self):
        os.chdir('../cQube_Components/')
        executable_path = os.path.join(os.getcwd(), 'Driver/chromedriver1')
        return executable_path

    def crc_downloadwise(self):
        self.driver.find_element_by_xpath(Data.crc_sel2).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(Data.crc_sel3).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(Data.crc_sel4).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(Data.crc_sel5).click()
        time.sleep(3)

    def crc_table_value(self):
        rows = self.driver.find_elements_by_xpath(Data.distrows)
        for j in range(len(rows)):
            print(rows[j].text)
            time.sleep(2)

    # SAR_2
    def blocks_names(self):
        self.driver.find_element_by_xpath(Data.SAR_Bnames).click()
        time.sleep(15)
        print("Block details..")
        infob = self.driver.find_elements_by_xpath(Data.details)
        for i in range(len(infob)):
            print(infob[i].text)

    def clusters_names(self):
        self.driver.find_element_by_xpath(Data.SAR_cnames).click()
        time.sleep(15)
        print("Cluster details..")
        infoc = self.driver.find_elements_by_xpath(Data.details)
        for i in range(len(infoc)):
            print(infoc[i].text)

    def schools_test(self):
        self.driver.find_element_by_xpath(Data.SAR_Schools_btn).click()
        print("for schools details...")
        time.sleep(15)
        infos = self.driver.find_elements_by_xpath(Data.details)
        for i in range(len(infos)):
            print(infos[i].text)

    def Total_details(self):
        details = self.driver.find_elements_by_xpath(Data.SAR_Details)
        for i in range(len(details)):
            print(details[i].text)
            time.sleep(3)

    def test_mouse_over(self):
        self.driver.implicitly_wait(20)
        lists = self.driver.find_elements_by_class_name(Data.dots)
        count = len(lists) - 1
        time.sleep(5)

        def mouseover(i):
            action = ActionChains(self.driver)
            action.move_to_element(lists[i]).perform()
            time.sleep(3)
            del action

        i = 0
        while i < len(lists):
            mouseover(i)
            i = i + 1
        return count

    def Table_data(self):
        tabledata = self.driver.find_elements_by_xpath(Data.distrows)
        for i in range(len(tabledata)):
            print(tabledata[i].text)
        footer = self.driver.find_elements_by_xpath(Data.footer)
        for i in range(len(footer)):
            print(footer[i].text)
            time.sleep(5)

    def CRC_dist_Clicks(self):
        dist = self.driver.find_elements_by_xpath(Data.CRC_Districts)
        for i in range(len(dist)):
            dist[i].click()
            time.sleep(3)

    # Admin login separation
    def get_admin_domain_name(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['admin_domain']

    def open_admin_appln(self, driver):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.get(self.get_admin_domain_name())
        self.driver.implicitly_wait(60)

    def login_admin(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(60)
        self.driver.find_element_by_id(Data.email).send_keys(self.get_admin_username())
        self.driver.find_element_by_id(Data.passwd).send_keys(self.get_admin_password())
        self.driver.find_element_by_id(Data.login).click()
        time.sleep(3)

    def get_demoadmin_name(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['createadmin']

    def get_demoreport_name(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['createviewer']

    def get_demoemission_name(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['createemission']

    def get_demoadmin_password(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['adminpassword']

    def get_demoreport_password(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['viewerpassword']

    def get_demoemission_password(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['emissionpassword']

    def get_nifi_status(self):
        cal = GetData()
        nifi_domain = cal.get_domain_name()
        url = nifi_domain + "/nifi-api/process-groups/root/process-groups"
        response = requests.get(url)
        json_resp = json.loads(response.text)
        nifi_status = []
        for x in json_resp.values():
            for y in x:
                name = y['component']['name']
                runningCount = y['component']['runningCount']
                stoppedCount = y['component']['stoppedCount']
                disabledCount = y['component']['disabledCount']
                invalidCount = y['component']['invalidCount']
                component_dict = {"name": name, "runningCount": runningCount, "stoppedCount": stoppedCount,
                                  "disabledCount": disabledCount, "invalidCount": invalidCount}
                nifi_status.append((component_dict))
        return nifi_status

    def get_runningCount(self, processor_name):
        cal = GetData()
        nifi_componets = cal.get_nifi_status()
        for x in nifi_componets:
            if x.get('name') == processor_name:
                self.runningCount = x.get('runningCount')
        return self.runningCount

    def get_stoppedCount(self, processor_name):
        cal = GetData()
        nifi_componets = cal.get_nifi_status()
        for x in nifi_componets:
            if x.get('name') == processor_name:
                self.stoppedCount = x.get('stoppedCount')
        return self.stoppedCount

    def get_invalidCount(self, processor_name):
        cal = GetData()
        nifi_componets = cal.get_nifi_status()
        for x in nifi_componets:
            if x.get('name') == processor_name:
                self.invalidCount = x.get('invalidCount')
        return self.invalidCount

    def get_disabledCount(self, processor_name):
        cal = GetData()
        nifi_componets = cal.get_nifi_status()
        for x in nifi_componets:
            if x.get('name') == processor_name:
                self.disabledCount = x.get('disabledCount')
        return self.disabledCount

    def get_time_zone(self):
        cal = GetData()
        nifi_domain = cal.get_domain_name()
        url = nifi_domain + "/nifi-api/process-groups/root/process-groups"
        response = requests.get(url)
        json_resp = json.loads(response.text)
        for x in json_resp.values():
            for y in x:
                self.time = y['status']['statsLastRefreshed']
                break
        return self.time

    def get_basedir(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['basedirpath']

    def connect_to_postgres(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        con = psycopg2.connect(host=config['config']['host'], database=config['config']['database'],
                               user=config['config']['user'], password=config['config']['db_password'])
        return con

    def get_db_name(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['database']

    def get_table_data_count(self,query,con):
        cursor = con.cursor()
        cursor.execute(query)
        count = cursor.fetchall()
        return count


    # admin console data replay

    def click_data_replay(self, driver):
        self.driver = driver
        self.driver.find_element_by_id(Data.data_replay_icon_id).click()

    def select_data_replay_data_source(self,driver,data_source_name):
        self.driver = driver
        select =Select(self.driver.find_element_by_id(Data.data_source_select_box_id))
        select.select_by_visible_text(data_source_name)

    def select_data_replay_year(self,driver,year):
        self.driver =driver
        select = Select(self.driver.find_element_by_class_name(Data.data_replay_select_year_class))
        select.select_by_visible_text(year)

    #managemets_resuable_functions

    def select_management_to_student_report(self,n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_student_report()
        year = Select(self.driver.find_element_by_id(Data.sar_year))
        month = Select(self.driver.find_element_by_id(Data.sar_month))
        self.year = year.first_selected_option.text
        self.month = month.first_selected_option.text
        return self.year,self.month

    def select_management_to_teacher_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_teacher_attendance_report()
        year = Select(self.driver.find_element_by_id(Data.sar_year))
        month = Select(self.driver.find_element_by_id(Data.sar_month))
        self.year = year.first_selected_option.text
        self.month = month.first_selected_option.text
        return self.year, self.month

    def select_management_to_infra_map_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_school_infrastructure_map()
        self.data.page_loading(self.driver)

    def select_management_to_udise_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_udise_report()
        self.data.page_loading(self.driver)

    def select_management_to_teacher_exception_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_teacher_exception()
        self.data.page_loading(self.driver)

    def select_management_to_semester_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_semester_report()
        self.data.page_loading(self.driver)

    def select_management_to_student_exception_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_student_exception()
        self.data.page_loading(self.driver)

    def select_management_to_pat_exception_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_pat_exception()
        self.data.page_loading(self.driver)

    def select_management_to_sat_exception_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_semester_exception()
        self.data.page_loading(self.driver)

    def select_management_to_crc_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_crc_report()
        self.data.page_loading(self.driver)

    def select_management_to_infra_table_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_composite_infrastructure()
        self.data.page_loading(self.driver)

    def select_management_to_composite_across_metrics_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_composite_report()
        self.data.page_loading(self.driver)

    def select_management_to_sat_heatchart_report(self, n):
        self.data = GetData()
        management = Select(self.driver.find_element_by_id('management'))
        management.select_by_index(n)
        print(management.options[n].text, 'is selected')
        self.data.page_loading(self.driver)
        self.data.navigate_to_sat_heatchart_report()
        self.data.page_loading(self.driver)

    def get_no_data_found_status(self):
        count = 0
        self.data = GetData()
        if 'No data found' in self.driver.page_source:
             print(self.driver.current_url,'Report showing no data found!...')
        else:
             print(self.driver.current_url,'is not showing no data found!')
             count = count+1
        self.driver.find_element_by_id("homeBtn").click()
        self.data.page_loading(self.driver)
        return count

    #data source config code
    def get_data_sources_status(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['data_source']['data_source']

    def get_student_status(self,resource):
        config = configparser.ConfigParser()
        config.read(self.p.get_data_source_ini_path())
        return config['data_source'][resource]

    def get_storage_type(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['storage_type']

    #Nifi data processing

    def get_response(self):
        self.cal=GetData()
        self.url = self.cal.get_domain_name() + "/nifi-api/process-groups/root/process-groups"
        response = requests.get(self.url)
        json_resp = json.loads(response.text)
        for x in json_resp.values():
            for y in x:
                result = y['bulletins']
                print(result)

    def get_processor_group_info(self, processor_name):
        while 1:
            if self.cal.check_nifi_status() == 200:
                self.cal = GetData()
                response = requests.get(self.url)
                json_resp = json.loads(response.text)
                for x in json_resp.values():
                    for y in x:
                        if y['status']['name'] == processor_name:
                            # return y['bulletins']
                            return y['id']
                        break
            else:
                print("Nifi is not running \n please start the nifi")
                time.sleep(2 * 60)


    def get_processor_group_id(self, processor_name):
            self.cal = GetData()
            if self.cal.check_nifi_status() == 200:
                self.url = self.cal.get_domain_name() + "/nifi-api/process-groups/root/process-groups"
                lst = []
                response = requests.get(self.url)
                json_resp = json.loads(response.text)
                for x in json_resp.values():
                    for y in x:
                        lst.append({"name": y['status']['name'], "id": y['id']})
                        # print(y['status']['name']+" "+y['id'])
                for x in lst:
                    if x['name'] == processor_name:
                        return x['id']
            else:
                print("Nifi is not running \n please start the nifi")

    def start_nifi_processor(self, id):
        self.cal = GetData()
        self.processor_id= self.cal.get_processor_group_id(id)
        while 1 :
            if self.cal.check_nifi_status() == 200:
                self.url = self.cal.get_domain_name()+"/nifi-api/flow/process-groups/" + self.processor_id
                payload = {"id": self.processor_id, "state": "RUNNING",
                           "disconnectedNodeAcknowledged": "false"}
                headers = {"Content-Type": "application/json"}
                pg_resp = requests.put(self.url, headers=headers, json=payload)
                if pg_resp.status_code == 200:
                    print("successfully started the "+id+" processor")
                    break
                else:
                    print("Not started the "+id+" processor")
                    break
            else:
                print("Nifi is not running \n please start the nifi")
                time.sleep(2*60)

    def stop_nifi_processor(self, id):
        self.cal = GetData()
        self.processor_id = self.cal.get_processor_group_id(id)
        while 1:
            if self.cal.check_nifi_status() == 200:
                self.url = self.cal.get_domain_name()+"/nifi-api/flow/process-groups/" + self.processor_id
                payload = {"id": self.processor_id, "state": "STOPPED",
                           "disconnectedNodeAcknowledged": "false"}
                headers = {"Content-Type": "application/json"}
                pg_resp = requests.put(self.url, headers=headers, json=payload)
                if pg_resp.status_code == 200:
                    print("successfully stopped the "+id+" processor")
                    break
                else:
                    print("Not stopped the "+id+" processor")
                    break
            else:
                print("Nifi is not running \n please start the nifi")
                time.sleep(2 * 60)

    def get_ini_path(self):
        cwd = os.path.dirname(__file__)
        ini = os.path.join(cwd, 'config.ini')
        return ini

    def get_nifi_static(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_static']

    def get_nifi_crc(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_crc']

    def get_nifi_attendance(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_attendance']

    def get_nifi_infra(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_infra']

    def get_nifi_diksha(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_diksha']

    def get_nifi_telemetry(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_telemetry']

    def get_nifi_udise(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_udise']

    def get_nifi_pat(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_pat']

    def get_nifi_composite(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_composite']


    def get_nifi_progresscard(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_progresscard']

    def get_nifi_teacher_attendance(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_teacher_attendance']

    def get_nifi_data_replay(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_data_replay']

    def get_nifi_sat(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['datasource']['nifi_sat']

    def get_filepath(self, config_name):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['filepath'][config_name]

    def get_emission_directory(self):
        config = configparser.ConfigParser()
        config.read(self.p.get_config_ini_path())
        return config['config']['emission_directory']


    def copy_file_to_s3(self, filepath, folder_name):
        value = "aws s3 cp " + filepath + " s3://cqube-qa-emission/" + folder_name + "/"
        result = subprocess.run([value], shell=True)
        return result

    def copy_files_to_s3(self, filepath, folder_name):
        value = "aws s3 cp " + filepath + " s3://cqube-qa-emission/" + folder_name + "/" + " --recursive"
        result = subprocess.run([value], shell=True)
        return result

    def copy_file_to_local(self,filepath,folder_name):
        self.cal = GetData()
        create_dir= "mkdir "+self.cal.get_emission_directory()+folder_name
        copy_file = "cp "+filepath+" "+self.cal.get_emission_directory()+folder_name
        dir_created_result = subprocess.run([create_dir], shell=True)
        file_copied_result = subprocess.run([copy_file], shell=True)
        return dir_created_result, file_copied_result

    def copy_files_to_local(self,filepath,folder_name):
        self.cal = GetData()
        create_dir= "mkdir "+self.cal.get_emission_directory()+" "+folder_name
        copy_file = "cp source_filepath" + self.cal.get_emission_directory()
        dir_created_result = subprocess.run([create_dir], shell=True)
        file_copied_result = subprocess.run([copy_file], shell=True)
        return dir_created_result,file_copied_result


    def check_nifi_status(self):
        self.cal = GetData()
        #self.url = self.cal.get_domain_name() + "/nifi-api/process-groups/root/process-groups"
        self.url = self.cal.get_domain_name() + "/nifi-api/process-groups/root/process-groups"
        response = requests.get(self.url)
        result = response.status_code
        return result

    # def get_queued_count(self,processor_name):
    #     while 1:
    #         self.cal = GetData()
    #         if self.cal.check_nifi_status() == 200:
    #             self.url = self.cal.get_domain_name() + "/nifi-api/process-groups/root/process-groups"
    #             response = requests.get(self.url)
    #             json_resp = json.loads(response.text)
    #             for x in json_resp.values():
    #                 for y in x:
    #                     if y['status']['name'] == processor_name:
    #                         # return y['bulletins']
    #                           return y['status']['aggregateSnapshot']['queued']
    #                     break
    #         else:
    #             print("Nifi is not running \n please start the nifi")
    #             time.sleep(2 * 60)
    def get_bytes(self,lst):
        bytes = lst[0]
        bytes = bytes.split(' ')
        print(bytes)
        return int(float(bytes[0]))

    def get_queued_count(self,processor_name):
        while 1:
            lst=[]
            self.cal = GetData()
            if self.cal.check_nifi_status() == 200:
                self.url = self.cal.get_domain_name() + "/nifi-api/process-groups/root/process-groups"
                response = requests.get(self.url)
                json_resp = json.loads(response.text)
                for x in json_resp.values():
                    for y in x:
                        if y['status']['name'] == processor_name:
                            # return y['bulletins']
                            lst.append( y['status']['aggregateSnapshot']['queued'])
                            break
                    break
                bytes = self.cal.get_bytes(lst)
                time.sleep(5)
                return bytes
            else:
                print("Nifi is not running \n please start the nifi")
                time.sleep(2 * 60)

    def get_processor_group_error_msg(self,processor_name):
        lst=[]
        while 1:
            self.cal = GetData()
            if self.cal.check_nifi_status() == 200:
                self.url = self.cal.get_domain_name() + "/nifi-api/process-groups/root/process-groups"
                response = requests.get(self.url)
                json_resp = json.loads(response.text)
                for x in json_resp.values():
                    for y in x:
                        if y['status']['name'] == processor_name:
                            if len(y['bulletins']) == 0:
                                break
                            else:
                                for x in y['bulletins']:
                                    lst.append(x['bulletin']['message'])
                            break
                    break


                return lst

            else:
                print("Nifi is not running \n please start the nifi")
                time.sleep(2 * 60)

    def clear_error_message_list(self,processor_name):
        self.cal = GetData()
        self.cal.get_processor_group_error_msg(processor_name)

    def click_on_logout_button(self):
        self.driver.find_element_by_id(Data.cQube_logo).click()
        time.sleep(1)
        self.driver.find_element_by_id(Data.logout)
        time.sleep(3)
        print(self.driver.title)

    #find out legend card color

    def get_legend_card_background_color(self,legend_card):
        res = []
        for sub in legend_card.split('; '):
            if ':' in sub:
                res.append(map(str.strip, sub.split(":", 1)))
        res = dict(res)
        background_color = res.get('background-color')
        value = ImageColor.getcolor(background_color, "RGB")
        return value

    def get_hex_to_rgb(self,hexvalue):
        value = ImageColor.getcolor(hexvalue, "RGB")
        print(value)
        return value


