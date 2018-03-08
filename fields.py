#coding:utf8

import sqliteClient
import uuid
import md5

class User():
    def __init__(self,nome,login,pwd,admin,id = None):
        if id:
            self.id = id
        else:
            self.id = uuid.uuid4()
        self.nome = nome
        self.login = login
        if id:
            self.pwd = pwd
        else:
            self.set_pwd(pwd)
        
        self.admin = bool(admin)

    def set_pwd(self,pwd):
        self.pwd = md5.new(pwd).digest()

    def check_pwd(self,pwd):
        return self.pwd == md5.new(pwd).digest

    def create_table(self):
        sqliteClient.execute_create(
            'users',
            {
                'id':'VARCHAR(255)',
                'nome':'VARCHAR(255)',
                'login':'VARCHAR(255)',
                'pwd':'VARCHAR(255)',
                'admin':'INT'
            }
        )

    def save(self):
        sqliteClient.execute_insert('''
            INSERT INTO users (
                id,nome,login,pwd,admin
            )
            VALUES(
                '''+self.id+''',
                '''+self.nome+''',
                '''+self.login+''',
                '''+self.pwd+''',
                '''+self.admin+''',
            )
        ''')

    class objects:
        def fill(self,result = None):
            if not result:
                return None
            users = []
            for i in result:
                users.append(User(i[0],i[1],i[2],i[3],i[4]))
            return users

        def all(self):
            result = sqliteClient.execute_select('''
                select 
                    nome,login,pwd,admin,id
                from 
                    users;
            ''')
            return self.fill(result)

        def filter(self,filter = None):
            condition = ""
            for i in filter.keys():
                condition += i+"="+filter[i]
                if i != filter.keys()[-1]:
                    condition += " and "
            result = sqliteClient.execute_select('''
                select 
                    nome,login,pwd,admin,id
                from 
                    users 
                where 
                    '''+condition+''';
            ''')
            return self.fill(result)
            

class Enviroment():
    def __init__(self,id = None):
        if id:
            self.id = id
        else:
            self.id = uuid.uuid4()

    def create_table(self):
        sqliteClient.execute_create(
            'envs',
            {
                'id':'VARCHAR(255)',
            }
        )

    def save(self):
        sqliteClient.execute_insert('''
            INSERT INTO envs (
                id
            )
            VALUES (
            '''+self.id+'''
            );
        ''')
    
    class objects:
        def fill(self,results = None):
            if not results:
                return None
            envs = []
            for i in results:
                envs.append(Enviroment(i[0]))
            return envs

        def all(self):
            result = sqliteClient.execute_select('''
                SELECT 
                    id
                FROM
                    envs;
            ''')
            return self.fill(result)

        @staticmethod
        def filter(self,filter = None):
            if not filter:
                return None
            condition = ""
            for i in filter.keys():
                condition += i+"="+filter[i]
                if i != filter.keys()[-1]:
                    condition += " and "
            results = sqliteClient.execute_select('''
                SELECT 
                    id
                FROM
                    envs
                WHERE
                    '''+condition+'''
                ;
            ''')
            return self.fill(results)



class Enviroment_User():
    def __init__(self,env,user,id = None):
        if id:
            self.id = id
        else:
            self.id = uuid.uuid4()
        self.env = env
        self.user = user

    def create_table(self):
        sqliteClient.execute_create(
            'envs_user',
            {
                'id':'VARCHAR(255)',
                'user':'VARCHAR(255)',
                'env':'VARCHAR(255)'
            }
        )

    def save(self):
        sqliteClient.execute_insert('''
            INSERT INTO users (
                id,env,user
            )
            VALUES (
                '''+self.id+''',
                '''+self.env.id+''',
                '''+self.user.id+'''
            );
        ''')

    class objects:
        def fill(self,result):
            envs = []
            for i in result:
                envs.append(i[0],User.objects.filter({'id':i[1]})[0],Enviroment.objects.filter({'id':i[2]})[0])
            return envs

        def all(self):
            result = sqliteClient.execute_select('''
                select 
                    id,env,user
                from 
                    envs;
            ''')
            return self.fill(result)

        def filter(self,filter):
            condition = ""
            for i in filter.keys():
                condition += i+"="+filter[i]
                if i != filter.keys()[-1]:
                    condition += " and "
            result = sqliteClient.execute_select('''
                select 
                    id,env,user
                from 
                    envs
                where 
                    '''+condition+''';
            ''')
            return self.fill(result)


    


