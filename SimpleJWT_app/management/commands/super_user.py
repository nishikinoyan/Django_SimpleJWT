from django.core.management import BaseCommand
from SimpleJWT_app.models import User
from django.db import transaction
from django.contrib.auth import *


# 添加管理员用户
# 添加新用户指令：python manage.py super_user
class Command(BaseCommand):
    help = '创建一个超级用户'

    def handle(self, *args, **options):
        while 1:
            self.stdout.write('''

 1.添加管理员用户
 2.修改管理员密码
 3.删除管理员用户
 4.用户列表
 
            ''')
            choose = input('输入选择序号：')
            if choose == '1':
                self.stdout.write('输入要添加的管理员用户名')
                user_username = input()
                self.stdout.write('输入要添加的用户密码')
                user_password = input()
                try:
                    with transaction.atomic():
                        add_user = User.objects.create_user(username=user_username, password=user_password)
                        add_user.save()
                        self.stdout.write('添加成功！')
                except Exception as err:
                    self.stdout.write('添加管理员错误：' + str(err))
            elif choose == '2':
                try:
                    self.stdout.write('输入你要修改的用户账号（是账号不是序号）')
                    user_list = User.objects.all()
                    for user_item in user_list:
                        self.stdout.write(str(user_item.id) + '.' + user_item.username)
                    self.stdout.write()
                    user_change_username = input()
                    # change_user = authenticate(user_username=user_change_username)
                    change_user = User.objects.filter(username=user_change_username).first()
                    if change_user is None:
                        self.stdout.write('用户不存在！')
                        exit()
                    else:
                        self.stdout.write('请输入新的用户密码')
                        user_new_password = input()
                        self.stdout.write('修改的用户：' + change_user.username)
                        change_user.set_password(user_new_password)
                        change_user.save()
                        self.stdout.write('修改成功！')
                except Exception as err:
                    self.stdout.write('用户密码修改错误：' + str(err))
            elif choose == '3':
                self.stdout.write('输入你要删除的用户账号（是账号不是序号）')
                user_list = User.objects.all()
                for user_item in user_list:
                    self.stdout.write(str(user_item.id) + '.' + user_item.username)
                self.stdout.write()

                user_delete_username = input()
                try:
                    with transaction.atomic():
                        delete_user = User.objects.filter(username=user_delete_username).first()
                        if delete_user is None:
                            self.stdout.write('要删除的用户不存在！')
                            exit()
                        else:
                            User.objects.filter(username=user_delete_username).delete()
                            self.stdout.write('删除成功！')

                except Exception as err:
                    self.stdout.write('用户删除错误：' + str(err))

            elif choose == '4':
                self.stdout.write('用户列表：')
                user_list = User.objects.all()
                for user_item in user_list:
                    self.stdout.write(str(user_item.id) + '.' + user_item.username)

            else:
                exit()
