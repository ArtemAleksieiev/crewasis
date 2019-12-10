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
