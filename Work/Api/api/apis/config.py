class BaseConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{password}@1{ip}:{port}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
