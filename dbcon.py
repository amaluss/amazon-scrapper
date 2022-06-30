import sqlite3

db='products'
conn=sqlite3.connect(db)
cursor=conn.cursor()
query="""create table if not exists product(id integer primary key  autoincrement,
          product_name text(200) not null,
          buyer_count int(7),
          price int(6),
          og_price int(6),
          offer char(4),
          item char(20))
          """
try:
  cursor.execute(query)
  conn.commit()
  conn.close()
except sqlite3.Error as err:
  print(err)


def product_insert(product):
  query="insert into product(product_name,buyer_count,price,og_price,offer,item) values(?,?,?,?,?,?)"
  try:
    conn = sqlite3.connect(db)
    cursor=conn.cursor()
    cursor.execute(query,product)
    conn.commit()
    return 'success'
  except sqlite3.Error as err:
    print(err)
  conn.close()


def show_product():
  query = "select * from product"
  try:
    conn = sqlite3.connect(db)
    cursor=conn.execute(query)
    res=cursor.fetchall()
    return res
  except sqlite3.Error as err:
    print(err)
  conn.close()


def del_product(p_name):
  query = "delete  from product where item=?"
  try:
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(query, [p_name,])
    conn.commit()
    return 'success'
  except sqlite3.Error as err:
    print(err)
  conn.close()

def show_single(it):
  try:
    qi="select * from product where item=?"
    conn = sqlite3.connect(db)
    cursor = conn.execute(qi,[it,])
    res = cursor.fetchall()
    return res
  except sqlite3.Error as err:
    print(err)
  conn.close()


if __name__ != '__main__':
  pass
else:
  #print(product_insert(product=('hard disk', 6, 2500, 150, 15, 'hard disk')))
  #print(product_insert(product=('red me note 5', 5, 15000, 200, 10, 'mobile')))
  #print(product_insert(product=('dell inspiron',5,50000,200,10,'laptop')))
  del_product('graphics+card')
  print(show_product())