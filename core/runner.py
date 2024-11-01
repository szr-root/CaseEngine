# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2024/11/01
# @File : runner.py

from basecase import db, ENV, BaseCase, my_functools


class TestRunner:
    def __init__(self, cases, env):
        """

        :param cases: 要执行的测试护具
        cases格式:[
            {
                "name":"业务流名称",
                "cases":[
                            {
                                "title": "登录成功用例",
                                "interface":
                                    {
                                        "url": "/api/users/login/",
                                        "method": "post",
                                    },
                                "headers":
                                    {
                                        "Content-Type": "application/json",
                                    },
                                "request": {
                                    "params": {},
                                    "json": {
                                        "username": "admin",
                                        "password": "admin"
                                    },
                                },
                                "setup_script": open('../setup_script.txt', 'r', encoding='utf-8').read(),
                                "teardown_script": open('../teardown_script.txt', 'r', encoding='utf-8').read(),
                            },
                            ....
                    ]
            }
        ]
        :param env: 测试环境
        """
        self.cases = cases
        self.env_data = env

    def run(self):
        # 初始数据库连接
        db.init_connect(self.env_data.pop('db'))

        ENV.update(self.env_data)

        # 通过exec将字符串中的python变量加载到functools这个模块的命名空间中
        exec(ENV["my_functools"], my_functools.__dict__)

        # 遍历所有测试用例
        for items in self.cases:
            ENV.clear()
            ENV.update(self.env_data)
            name = items["name"]  # 业务流名称
            print(name)
            for testcase in items["cases"]:
                self.perform(testcase)

        # 断开连接
        db.close_db_connection()

    def perform(self, case):
        c = BaseCase()
        try:
            c.perform(case)
        except AssertionError as e:
            print('用例断言失败')
        except Exception as e:
            print('用例执行错误')
        else:
            print('用例执行通过')


if __name__ == '__main__':
    cases = [
        {
            "name": "登录",
            "cases": [
                {
                    "title": "登录成功用例0",
                    "interface":
                        {
                            "url": "/api/users/login/",
                            "method": "get",
                        },
                    "headers":
                        {
                            "Content-Type": "application/json",
                        },
                    "request": {
                        "params": {},
                        "json": {
                            "username": "john",
                            "password": "1111"
                        },
                    },
                    "setup_script": '',
                    "teardown_script": '',
                },
                {
                    "title": "登录成功用例",
                    "interface":
                        {
                            "url": "/api/users/login/",
                            "method": "post",
                        },
                    "headers":
                        {
                            "Content-Type": "application/json",
                        },
                    "request": {
                        "params": {},
                        "json": {
                            "username": "admin",
                            "password": "admin"
                        },
                    },
                    "setup_script": '',
                    "teardown_script": '',
                },
                {
                    "title": "登录成功用例2",
                    "interface":
                        {
                            "url": "/api/users/login/",
                            "method": "post",
                        },
                    "headers":
                        {
                            "Content-Type": "application/json",
                        },
                    "request": {
                        "params": {},
                        "json": {
                            "username": "john",
                            "password": "666666"
                        },
                    },
                    "setup_script": open('../setup_script.txt', 'r', encoding='utf-8').read(),
                    "teardown_script": open('../teardown_script.txt', 'r', encoding='utf-8').read(),
                },
            ]
        }
    ]

    test_env_data = {
        "base_url": "http://172.20.20.54:8001",
        "headers": {
            "Content-Type": "application/json"
        },
        # 用来存放全局变量（用例执行过程中需要存储的变量）
        "Envs": {
            "username": "123qwe",
            "password": "666666"
        },
        "my_functools": open("../my_functools.py", 'r', encoding='utf-8').read(),
        "db": {
            "name": "local",
            "type": "mysql",
            "config": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "songzhaoruizx"
            }
        }
    }

    TestRunner(cases, test_env_data).run()
