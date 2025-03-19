from pymysql import connect
import json, requests



DB_CONFIG = '/Users/eunbumkim/Documents/Practice/lesson/ky/Lesson/get_news/db_config.json'
CATEGORY_FILE = '/Users/eunbumkim/Documents/Practice/lesson/ky/Lesson/get_news/category.json'
CONFIG_FILE = '/Users/eunbumkim/Documents/Practice/lesson/ky/Lesson/get_news/config.json'


def init_db(db_config):
  try:
    with open(db_config, 'r', encoding='utf-8') as f:
      config = json.load(f)
      
      conn = connect(
        host=config['host'],
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
    return tuple( [ (x[0],x[1]) for x in res ] )
  except Exception as e:
    print(f'Error: {e}')
    return None
  
def select_one_by_article(conn, title):
  try:
    cursor = conn.cursor()
    sql = 'select id from articles where title = %s'
    cursor.execute(sql, (title,))
    res = cursor.fetchone()
    cursor.close()
    return res[0] if res is not None else None
  except Exception as e:
    print(f'Error: {e}')
    return None
  
  
def insert_articles(conn, category, article_url):
  try:
    res = requests.get(article_url)
    if res.status_code != 200:
      print(f'Error: {res.status_code}')
      return
    
    data = res.json()    
    with conn.cursor() as cursor:
      articles = data['articles']
      for article in articles:        
        source_name = article['source']['name']
        source_id = select_one_by_source_name(conn, source_name)
        if source_id is None: # source 테이블에 없는 경우 현재 source 이름으로 sources 테이블에 추가
          source_id = insert_source_by_name(conn, source_name)
        
        if select_one_by_article(conn, article['title']) is None:
          sql = '''insert into articles(author, title, description, url, url_to_image, published_at, content, category, source)
                  values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
          cursor.execute(sql, (article['author'], article['title'], article['description'], article['url'], article['urlToImage'], article['publishedAt'], article['content'], category, source_id))
          
      conn.commit()
      
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
    # insert_category(conn, CATEGORY_FILE)    
    
    # url = f'https://newsapi.org/v2/top-headlines/sources?apiKey={get_api_key(CONFIG_FILE)}'    
    # insert_source(conn, url)   
    for c_id, c_name in select_all_category(conn):  # 6개의 카테고리
      insert_articles(conn, c_id, make_url(CONFIG_FILE, c_name))
      print(f'{c_name} 카테고리의 기사를 가져왔습니다.')

    close_db(conn)
    
    
  # res = requests.get('https://nypost.com/2025/03/03/business/car-prices-may-surge-12k-after-trumps-canada-mexico-tariffs/')
  # bs = BeautifulSoup(res.text, 'html.parser')
  # text = bs.getText()

"""
'ai' : 'open ai api'
'web service'
"""    
    
'''
SELECT 
    a.author, 
    a.title, 
    a.published_at, 
    c.name AS category_name, 
    s.name AS source_name
FROM articles AS a
JOIN category AS c ON a.category = c.id
JOIN sources AS s ON a.source = s.id
where a.category = 7;
'''

    
'''
1. business
2. entertainment
3. general
4. health
5. science
6. sports
7. technology

원하는 메뉴를 선택하세요 >>> 1

author :
title :
url :
source : ABC News

author :
title :
url :
source :

author :
title :
url :
source :


business 카테고리의 기사를 가져왔습니다.
'''