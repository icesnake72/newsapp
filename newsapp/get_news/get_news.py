from pymysql import connect
from dotenv import load_dotenv
import json, requests, os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_CONFIG = os.path.join(BASE_DIR, 'db_config.json') 
CATEGORY_FILE = os.path.join(BASE_DIR,'category.json')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

DEBUG = False

print(os.getenv('DJANGO_ENV'))

def init_db(db_config):
  try:
    with open(db_config, 'r', encoding='utf-8') as f:
      config = json.load(f)
      
      conn = connect(
        host= 'localhost' if os.getenv('DJANGO_ENV')=='development' else config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
      )
      print('데이터베이스 연결 성공')
      return conn
  except Exception as e:
    print(f'Error: {e}')
    return None
  
def close_db(conn):
  try:
    conn.close()
    print('데이터베이스 연결 종료')
  except Exception as e:
    print(f'Error: {e}')

def insert_category(conn, category_file):
  try:
    with open(category_file, 'r', encoding='utf-8') as f:
      categories = json.load(f) # file handle -> json
      cursor = conn.cursor()
      for category in categories:
        if select_one_by_category_name(conn, category['name']) is None:
          sql = "insert into category(name, memo) values(%s, %s)"
          cursor.execute(sql, (category['name'], category['memo']))
      
      conn.commit()  
      cursor.close()
  except Exception as e:
    print(f'Error: {e}')
    

def get_api_key(file_name):
  with open(file_name, 'r', encoding='utf-8') as f:
    res = json.load(f)
    return res['news_api_key']


def insert_source(conn, source_url):
  try:
    res = requests.get(source_url)
    if res.status_code != 200:
      return
    
    # 
    result = res.json()
    sources = result['sources']
    
    cursor = conn.cursor()
    for source in sources:    
      if select_one_by_source_name(conn, source['name']) is None:
        sql = '''insert into sources(source_id, name, description, url, category, language, country) 
                values(%s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql, (source['id'], source['name'], source['description'], source['url'], source['category'], source['language'], source['country']))
      
    conn.commit()
    cursor.close()
  except Exception as e:
    print(f'Error: {e}')
    
    
def insert_source_by_name(conn, source_name):
  try:
    sql = 'insert into sources(name) values(%s)'
    cursor = conn.cursor()
    cursor.execute(sql, (source_name,))
    inserted_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    return inserted_id
  except Exception as e:
    print(f'Error: {e}')
    return None
  
  
def select_one_by_source_name(conn, source_name):
  try:
    cursor = conn.cursor()
    sql = 'select id from sources where name = %s'
    cursor.execute(sql, (source_name,))
    res = cursor.fetchone()
    cursor.close()    
    
    if res is not None:
      print(f'{source_name}은 이미 존재합니다.')
      
    return res[0] if res is not None else None
  except Exception as e:
    print(f'Error: {e}')
    return None
  
  
def select_one_by_category_name(conn, category_name):
  try:
    cursor = conn.cursor()
    sql = 'select id from category where name = %s'
    cursor.execute(sql, (category_name,))
    res = cursor.fetchone()
    cursor.close()
    return res[0] if res is not None else None
  except Exception as e:
    print(f'Error: {e}')
    return None
  

def select_all_category(conn):
  try:
    cursor = conn.cursor()
    sql = 'select * from category'
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return tuple([ (x[0],x[1]) for x in res ])
  except Exception as e:
    print(f'Error: {e}')
    return None
  
  
def select_one_by_title(conn, title):
  try:
    cursor = conn.cursor()
    sql = 'select id from articles where title = %s'
    cursor.execute(sql, (title,))
    res = cursor.fetchone()
    cursor.close()
    if res is not None:
      print(f'{title}은 이미 존재합니다.')
      
    return res[0] if res is not None else None
  except Exception as e:
    print(f'Error: {e}')
    return None
  
  
def get_row_count(conn, table_name):
  try:
    cursor = conn.cursor()
    sql = f'select count(*) from {table_name}'
    cursor.execute(sql)
    res = cursor.fetchone()
    cursor.close()
    return res[0]
  except Exception as e:
    print(f'Error: {e}')
    return None
  
  
def insert_article(conn, url, category_id):  
  try:
    old_count = get_row_count(conn, 'articles')
    res = requests.get(url)
    if res.status_code != 200:      
      print('API 호출 실패: ', res.status_code, url)
      return
    
    result = res.json()
    articles = result['articles']
    for article in articles:
      if select_one_by_title(conn, article['title']) is None:
        source_id = select_one_by_source_name(conn, article['source']['name'])
        if source_id is None:
          source_id = insert_source_by_name(conn, article['source']['name'])
          
        sql = '''insert into articles(author, title, description, url, url_to_image, published_at, content, category, source) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor = conn.cursor()
        cursor.execute(sql, (article['author'], article['title'], article['description'], article['url'], article['urlToImage'], article['publishedAt'], article['content'], category_id, source_id))
    
    conn.commit()
    cursor.close()
    
    new_count = get_row_count(conn, 'articles')
    print(f'신규 데이터: {new_count-old_count}건이 추가되었습니다.')
  except Exception as e:
    print(f'Error: {e}')
    



# SQL
# Structure Query Language
def test_query(conn, sql):
  cursor = conn.cursor()
  cursor.execute(sql) # SQL 실행
  res = cursor.fetchall() # 결과 가져오기
  print(res)  # 결과 출력
  cursor.close()
  

def make_url(config_file, category):
  with open(config_file, 'r', encoding='utf-8') as f:
    res = json.load(f)
    url = f"https://newsapi.org/v2/top-headlines?country={res['country']}&category={category}&apiKey={res['news_api_key']}"
    return url


if __name__ == '__main__':  
  conn = init_db(DB_CONFIG)
  if conn is not None:        
    insert_category(conn, CATEGORY_FILE)    
    
    url = f'https://newsapi.org/v2/top-headlines/sources?apiKey={get_api_key(CONFIG_FILE)}'    
    insert_source(conn, url)
    
    for id, name in select_all_category(conn):
      url = make_url(CONFIG_FILE, name)
      insert_article(conn, url, id)    
        
    close_db(conn)