from sqlalchemy import *
from sqlalchemy.orm import *

# 数据库配置
database_setting = {'database_type': 'mysql',
                    'connector': 'mysqlconnector',
                    'user_name': 'root',
                    'password': '123456',
                    'host_name': 'localhost',
                    'database_name': 'UserManager',

                    }

# 实体类
class User(object):
    def __init__(self, user_name, user_age, user_sex, user_score,
                 user_subject):
        self.user_name = user_name
        self.user_age = user_age
        self.user_sex = user_sex
        self.user_score = user_score
        self.user_subject = user_subject

# 操作数据库的类
class UserManagerORM(object):
    def __init__(self):
        self.engine = create_engine(database_setting['database_type'] +
                                '+' +
                                database_setting['connector'] +
                                '://' +
                                database_setting['user_name'] +
                                ':' +
                                database_setting['password'] +
                                '@' +
                                database_setting['host_name'] +
                                '/' +
                                database_setting['database_name']
                            )

        self.metadata = MetaData(self.engine)
        self.user_table = Table('user', self.metadata, autoload=True)

        #   将实体类User映射到user表
        mapper(User, self.user_table)

        #   生成一个会话类，并与上面的数据库引擎绑定
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        #   创建一个会话
        self.session = self.Session()


    def CreateNewUser(self, user_info):
        '''
         # 这个方法根据传递过来的用户信息列表新建一个用户
         # user_info是一个列表，包含了从表单提交上来的信息
        '''

        new_user = User(
            user_info['user_name'],
            user_info['user_age'],
            user_info['user_sex'],
            user_info['user_score'],
            user_info['user_subject']
        )

        self.session.add(new_user)
        self.session.commit()

    def GetUserByName(self, user_name):
        return self.session.query(User).filter_by(user_name=user_name).all()[0]

    def GetAllUser(self):
        return self.session.query(User)

    def UpdateUserInfoByName(self, user_info):
        user_name = user_info['user_name']
        user_info_without_name = {'user_age':user_info[ 'user_age' ],
                                'user_sex':user_info[ 'user_sex' ],
                                'user_score':user_info[ 'user_score' ],
                                'user_subject':user_info[ 'user_subject' ]
                            }
        self.session.query(User).filter_by(user_name=user_name).update(user_info_without_name)
        self.session.commit()

    def DeleteUserByName(self, user_name):
        user_need_to_delete = self.session.query(User).filter_by(user_name=user_name).all()[0]
        self.session.delete(user_need_to_delete)
        self.session.commit()