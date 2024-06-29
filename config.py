import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Config(object):
  try:
    conn = psycopg2.connect(
      host=os.getenv("POSTGRES_HOST"),
      port=os.getenv("POSTGRES_PORT"),
      user=os.getenv("POSTGRES_USER"),
      password=os.getenv("POSTGRES_PASSWORD")
    )
  except (Exception, psycopg2.DatabaseError) as e:
    print(f"[!] Database Error : {e}")
  