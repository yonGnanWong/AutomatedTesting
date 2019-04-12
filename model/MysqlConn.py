import pymysql
import configparser

class Connection(object):
    #单例模式实例化数据库驱动
    __instance=None

    def __new__(cls):

        if cls.__instance == None:
            cls.__instance = cls.mysql()
            return  cls.__instance
        else:
            return cls.__instance

    def mysql(arg1=[]):
        config = configparser.ConfigParser()
        config.read("./DB.conf")
        ip = config.get("db", "db_host")
        user = config.get("db", "db_user")
        pass_word = config.get("db", "db_password")
        db_name = config.get("db", "db_name")
        db_conn = pymysql.connect(ip,user,pass_word,db_name)
        cursor = db_conn.cursor()
        return cursor
