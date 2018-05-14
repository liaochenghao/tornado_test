import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
import orm

define('port', default=9999, help='run on the given port', type=int)

user_orm = orm.UserManagerORM()     #   创建一个全局ORM对象


class MainHandler(tornado.web.RequestHandler):  #   主handler，用来响应首页的URL

    '''
        MainHandler shows all data and a form to add new user
    '''

    def get(self): #    处理主页面（UserManager.html）的GET请求

        #   show all data and a form
        title = 'User Manager V0.1'

        users = user_orm.GetAllUser()

        self.render('templates/UserManager.html', title=title, users=users)

    def post(self):
        pass


class AddUserHandler(tornado.web.RequestHandler):

    '''
        AddUserHandler collects info to create new user
    '''

    def get(self):
        pass

    def post(self):

        user_info = {
            'user_name':self.get_argument('user_name'),
            'user_age':self.get_argument('user_age'),
            'user_sex': self.get_argument('user_sex'),
            'user_score': self.get_argument('user_score'),
            'user_subject': self.get_argument('user_subject')
        }

        user_orm.CreateNewUser(user_info)

        self.redirect('http://localhost:9999')


class EditUserHandler(tornado.web.RequestHandler):  # 响应/EditUser的URL
        '''''
            Show a page to edit user info,
            user name is given by GET method
        '''

        def get(self):  # /EditUser的URL中，响应GET请求
            user_info = user_orm.GetUserByName(self.get_argument('user_name'))  # 利用ORM获取指定用户的信息
            self.render('templates/EditUserInfo.html', user_info=user_info)  # 将该用户信息发送到EditUserInfo.html以供修改

        def post(self):
            pass


class UpdateUserInfoHandler(tornado.web.RequestHandler):  # 用户信息编辑完毕后，将会提交到UpdateUserInfo，由此Handler处理
    '''''
        Update user info by given list
    '''

    def get(self):
        pass

    def post(self):  # 调用ORM层的UpdateUserInfoByName方法来更新指定用户的信息
        user_orm.UpdateUserInfoByName({
            'user_name': self.get_argument('user_name'),
            'user_age': self.get_argument('user_age'),
            'user_sex': self.get_argument('user_sex'),
            'user_score': self.get_argument('user_score'),
            'user_subject': self.get_argument('user_subject'),
        })
        self.redirect('http://localhost:9999')  # 数据库更新后，转到首页


class DeleteUserHandler(tornado.web.RequestHandler):  # 这个Handler用来响应/DeleteUser的URL
    '''''
        Delete user by given name
    '''

    def get(self):
        # 调用ORM层的方法，从数据库中删除指定的用户
        user_orm.DeleteUserByName(self.get_argument('user_name'))

        self.redirect('http://localhost:9999')  # 数据库更新后，转到首页

    def post(self):
        pass


def MainProcess():
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        [
            (r'/', MainHandler),  # 路由表中的URL是用正则表达式来过滤的
            (r'/AddUser', AddUserHandler),
            (r'/EditUser', EditUserHandler),
            (r'/DeleteUser', DeleteUserHandler),
            (r'/UpdateUserInfo', UpdateUserInfoHandler),
        ]

    )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    MainProcess()