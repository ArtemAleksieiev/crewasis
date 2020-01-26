# "Database code"

import os
import psycopg2

DATABASE_URL = 'crewasis'

def add_population(state, pop, percent, adults):
  db = psycopg2.connect(database = DATABASE_URL)
  c = db.cursor()
  c.execute("insert into population values (%s, %s, %s, %s)", (state, pop, percent, adults))
  db.commit()
  db.close()

def add_colorado(id, year, category, state, code, january, february, march, april, may, june, july, august, september, october, november, december):
  db = psycopg2.connect(database = DATABASE_URL)
  c = db.cursor()
  c.execute("insert into colorado values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, year, category, state, code, january, february, march, april, may, june, july, august, september, october, november, december))
  db.commit()
  db.close()

def add_california(lic_num, lic_type, owner, contact, e_mail, phone, website, structure, adress, status, issue, expiration, activities, use):
  db = psycopg2.connect(database = DATABASE_URL)
  c = db.cursor()
  c.execute("insert into california values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (lic_num, lic_type, owner, contact, e_mail, phone, website, structure, adress, status, issue, expiration, activities, use))
  db.commit()
  db.close()

def add_colorado_bis(bus_file_num, lic_type, entity_name, trade_name, status, exp_data, adress, city, zip_code):
  db = psycopg2.connect(database = DATABASE_URL)
  c = db.cursor()
  c.execute("insert into colorado_bis values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (bus_file_num, lic_type, entity_name, trade_name, status, exp_data, adress, city, zip_code))
  db.commit()
  db.close()

def add_oregon_bis(lic_num, lic_name, bus_name, lic_type, active, county, retail, medical, hemp):
  db = psycopg2.connect(database = DATABASE_URL)
  c = db.cursor()
  c.execute("insert into oregon_bis values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (lic_num, lic_name, bus_name, lic_type, active, county, retail, medical, hemp))
  db.commit()
  db.close()
