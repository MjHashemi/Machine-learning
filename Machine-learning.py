from bs4 import BeautifulSoup
import re
import requests
import mysql.connector
from sklearn import tree
from sklearn import preprocessing
from random import randint
from time import sleep

cnx = mysql.connector.connect(user='root', password='1234', host='127.0.0.1', database='cars')
# INPUT CODE
user_brand = input()
user_year = int(input())
user_mileage = float(input())
user_accidents = int(input())

a = 0
for i in range(2,200):
  if a == 1000:
    break
  cursor = cnx.cursor()
  page = requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page={}'.format(i))
  soup = BeautifulSoup(page.content, "html.parser")
  cars_elements = soup.find_all('div', {'data-test':'cardContent'}) 
  for element in cars_elements:     
    cartitle = (element.find('div',{'data-test':'vehicleCardYearMakeModel'}).text.strip())
    brand = (re.findall(r'\w*[A-Z]\w*', cartitle)[0])
    if brand == user_brand:
      a += 1
      nums = re.findall(r'\d+', cartitle)
      year = int(nums[0])
      price = float(element.find('div',{ 'data-test':"vehicleListingPriceAmount"}).text.replace('$','').replace(',','.'))
      mileage = float(element.find('div', {'data-test':"vehicleMileage"}).text.replace('miles','').replace(',','.')) 
      accidents = (element.find('div', {'data-test':"vehicleCardCondition"}).text.strip())[0]
      if accidents == 'N':
        accidents = 0    
      else:
        accidents = int(accidents) 
      cursor.execute("insert into caritem(year,mileage,accidents,price) values('{}','{}','{}','{}')".format(year,mileage,accidents,price))  
sleep(randint(1,5))

cnx.commit()
cursor.execute("SELECT * FROM caritem")
record = cursor.fetchall()

x = []
y = []
for line in record:
  x.append(line[:3])
  y.append(line[3])

label_encoder = preprocessing.LabelEncoder()
train_y = label_encoder.fit_transform(y)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, train_y)

new_data = [[user_year, user_mileage, user_accidents]]
answer = clf.predict(new_data)
print(answer[0])