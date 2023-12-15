import configparser

config = configparser.ConfigParser()

# 섹션과 키-값 설정 추가
config['dev'] = {
    'host': 'database-1.cklu0egki5of.ap-northeast-2.rds.amazonaws.com',
    'port': '3306',
    'user': 'root',
    'password': '1234deepqwer!',
    'database': 'AIstore'
}

# config.ini 파일에 쓰기
with open('config.ini', 'w') as configfile:
    config.write(configfile)
