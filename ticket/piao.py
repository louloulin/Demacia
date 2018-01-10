from time import sleep

from splinter import Browser

from ticket.cites import cities
import configparser


class Ticket:
    # 读取配置文件
    configs = configparser.ConfigParser()
    configs.read('user.cfg')
    driver_name = ''
    executable_path = ''
    # 用户名，密码
    username = configs.get('user', 'username')
    passwd = configs.get('user', 'passwd')
    # cookies值得自己去找, 下面两个分别是
    starts = cities[configs.get('from', 'starts')]
    ends = cities[configs.get('from', 'ends')]
    # 时间格式2018-01-19
    dtime = configs.get('date', 'time')
    # 车次，选择第几趟，0则从上之下依次点击
    order = int(configs.get('passenger', 'order'))
    ###乘客名
    users = [s for s in configs.get('passenger', 'users').split(',')]
    xb = u"二等座"
    pz = u"儿童票"

    """网址"""
    ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
    login_url = "https://kyfw.12306.cn/otn/login/init"
    initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
    buy = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

    def __init__(self):
        self.driver_name = self.configs.get('driver', 'driver_name')
        self.executable_path = self.configs.get('driver', 'executable_path')

    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill("loginUserDTO.user_name", self.username)
        # sleep(1)
        self.driver.fill("userDTO.password", self.passwd)
        print(u"等待验证码，自行输入...")
        while True:
            if self.driver.url != self.initmy_url:
                sleep(1)
            else:
                break

    def qiang_piao(self):
        try:
            print("购票页面开始...")
            # sleep(1)
            # 加载查询信息
            self.driver.visit(self.ticket_url)
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()

            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    try:
                        # if self.driver.find_by_id('qd_closeDefaultWarningWindowDialog_id') is not None:
                        self.driver.find_by_text(u"查询").click()
                        count += 1
                        print(u"循环点击查询... 第 %s 次" % count)
                        print("循环")
                        self.driver.find_by_text("预订")[self.order - 1].click()
                    except Exception as e:
                        print(e)
                        print("werwerwer")
                        print(u"还没开始预订")
                        self.driver.find_by_id('qd_closeDefaultWarningWindowDialog_id').click()
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text(u"查询").click()
                    count += 1
                    print(u"循环点击查询... 第 %s 次" % count)
                    print("循环")
                    try:
                        for i in self.driver.find_by_text(u"预订"):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print(u"还没开始预订 %s" % count)
                        continue
            print("开始预订...")
            # sleep(3)
            # self.driver.reload()
            # sleep(1)
            print('开始选择用户...')
            for user in self.users:
                self.driver.find_by_text(user).last.click()
            print("提交订单...")
            # sleep(0)

            # self.driver.find_by_xpath('//select[@id="%s"]//option[@value="%s"]' % ('ticketType_1', '2')).first._element.click()

            # self.driver.find_by_id('').select(self.pz)
            # sleep(4)
            # self.driver.find_by_text(self.xb).click()
            s = self.driver.find_by_id('submitOrder_id').click()
            print(s)
            print("开始选座...")
            sleep(1)
            self.driver.find_by_text('1D')
            print("确认选座...")
            self.driver.find_by_id('qr_submit_id').click()

        except Exception as e:
            sleep(4)
            #递归操作异常继续执行抢票
            self.qiang_piao()

    def start(self):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        self.driver.driver.set_window_size(1400, 1000)
        self.login()
        # sleep(1)
        self.qiang_piao()


if __name__ == '__main__':
    ticket = Ticket()
    ticket.start()
