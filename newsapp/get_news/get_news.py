from pymysql import connect
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
        host= 'db' if os.getenv('DJANGO_ENV')=='development' else config['host'],
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
  '''카테고리 이름으로 카테고리 ID를 반환'''
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
  '''테이블의 전체 레코드 수를 반환'''
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
  
  
def insert_article(conn, config_file, category):  
  try:
    # articles 테이블의 전체 레코드수 가져오기
    old_count = get_row_count(conn, 'articles')
    
    # 카테고리 이름으로 카테고리 ID 가져오기
    category_id = select_one_by_category_name(conn, category)
    
    # API에서 제공하는 해당 카테고리의 전체 기사수
    total_results = 0
    
    # 페이지당 기사 수
    cpp = 20
    
    # 페이지 번호
    page = 1
    
    # 전체 페이지 수
    total_page = 0
    
    while True:    
      url = make_url(config_file, category, page)
      res = requests.get(url)
      if res.status_code != 200:      
        print('API 호출 실패: ', res.status_code, url)
        return
    
      result = res.json()
      total_results = result['totalResults']
      if total_results == 0:
        print('데이터가 없습니다.')
        return
            
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
          
      # 첫번째 request에서 전체 페이지 수를 계산
      if total_page == 0:
        total_page = total_results // cpp + 1
      
      # 마지막 페이지까지 도달하면 종료  
      if page >= total_page:
        break
      
      # 다음 페이지로 이동
      page += 1
      
    conn.commit()
    cursor.close()
    
    new_count = get_row_count(conn, 'articles')
    print("="*30)
    print(f'카테고리: {category}에서 신규 데이터: {new_count-old_count}건이 추가되었습니다.')
    print("="*30)
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
  

def make_url(config_file, category, page=1):
  with open(config_file, 'r', encoding='utf-8') as f:
    res = json.load(f)
    url = f"https://newsapi.org/v2/top-headlines?country={res['country']}&category={category}&page={page}&apiKey={res['news_api_key']}"
    return url


if __name__ == '__main__':  
  conn = init_db(DB_CONFIG)
  if conn is not None:        
    insert_category(conn, CATEGORY_FILE)    
    
    url = f'https://newsapi.org/v2/top-headlines/sources?apiKey={get_api_key(CONFIG_FILE)}'    
    insert_source(conn, url)
    
    for id, name in select_all_category(conn):
      # url = make_url(CONFIG_FILE, name)
      insert_article(conn, CONFIG_FILE, name)    
        
    close_db(conn)