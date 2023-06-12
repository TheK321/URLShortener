from flask import Flask, request, jsonify, redirect
import shortuuid
from database import create_connection

def create_short_link(original_url):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            existing_link = get_link_by_url(original_url)
            print("existing_link: ", existing_link)
            if existing_link is not None:
                print("existing_link: is not none ", existing_link)
                return existing_link
            else:
                short_code = shortuuid.uuid()[:8]
                print("short_code: ", short_code)
                sql = "INSERT INTO urls (link, short_url) VALUES (%s, %s)"
                cursor.execute(sql, (original_url, short_code))
                connection.commit()
                return short_code
    finally:
        connection.close()

def get_link_by_url(original_url):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT short_url FROM urls WHERE link = %s"
            cursor.execute(sql, (original_url,))
            result = cursor.fetchone()
            print("result: ", result)
            if result:
                short_url = result["short_url"]
                return short_url
            else:
                return None
    finally:
        connection.close()

def shorten_url(url):
    original_url = url
    print("shorten url original_url: ", original_url)
    short_code = create_short_link(original_url)
    print("shorten url short_code: ", short_code)
    short_url = f"http://digital.nao/{short_code}"
    print("shorten url short_url: ", short_url)
    return jsonify({'short_url': short_url})

shorten_url('https://www.google.com/')