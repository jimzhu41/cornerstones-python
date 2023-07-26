import os




basedir = os.path.abspath(os.path.dirname(__file__))



#
#app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{dbuser}:{dbpassword}@localhost/cornerstones"


class Config:
    dbuser = "cornerstones"
    dbpassword = "123#Alcazar"

    SECRET_KEY = os.environ.get('SECRET_KEY') or '123@Alcazar'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://')
   # SQLALCHEMY_DATABASE_URI = f"postgresql://{dbuser}:{dbpassword}@localhost/cornerstones"
   # \os.environ.get('DATABASE_URL', '').replace(
    #    'postgres://', 'postgresql://') or \
     #   'sqlite:///' + os.path.join(basedir, 'app.db')
   # app.config['MAIL_SERVER'] = 'smtp.cornerstones.tech'
   #app.config['MAIL_PORT'] = 465
    #app.config['MAIL_USE_TLS'] = False
  #  app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
   # app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['me@cornerstones.tech']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    POSTS_PER_PAGE = 25

@staticmethod
def init_app(app):
    pass

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABSE_URI')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABSE_URI')

config = {
    'development': DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}
