#!/usr/bin/env python3

import os
import time
import json
import logging
import sqlite3
from infojobs import InfoJobs
from dotenv import load_dotenv

logging.basicConfig(level = logging.ERROR, filename = 'logs/log.txt', format = "%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

con = sqlite3.connect("models/jobs")
cur = con.cursor()

bot = InfoJobs(os.environ.get('USER_EMAIL'), os.environ.get('USER_PASSWORD'))
bot.login()

while True:
    text = input('press a command: ')

    if text == '/pull':

        with open('params.json', 'r') as f:
            data = json.load(f)

        keywords = data.get('keywords')
        city = data.get('city')
        state = data.get('state')
        limit = data.get('limit')
        publicationTime = data.get('publicationTime', [])
        profissionalArea = data.get('profissionalArea', [])
        contract = data.get('contract', [])
        journey = data.get('journey', [])
        pwd = data.get('pwd', [])
        workplaceType = data.get('workplaceType')
        salary = data.get('salary')

        if len(profissionalArea) == 0:
            profissionalArea = None

        if len(contract) == 0:
            contract = None

        if len(journey) == 0:
            journey = None

        if len(pwd) == 0:
            pwd = None

        links = bot.search_jobs(keywords, city, state = state, limit = limit, publicationTime = publicationTime, profissionalArea = profissionalArea, contract = contract, journey = journey, pwd = pwd, workplaceType = workplaceType, salary = salary)

        print(f'{len(links)} jobs were downloaded from the infojobs website')

        for link in links:
            cur.execute("INSERT OR IGNORE INTO jobs (id, url, applied) VALUES (NULL, ?, 0)", (link, ))
   
        con.commit()
    elif text == '/candidate':
        MAX_TIME_RESTART = 10 * 60

        count = int(input('count of jobs: '))

        cur.execute("SELECT id, url FROM jobs WHERE applied = 0 LIMIT ?", (count, ))

        urls = cur.fetchall()

        last_time = time.time()

        for id, url in urls:
            cur_time = time.time()

            if cur_time - last_time >= MAX_TIME_RESTART:
                bot.createDriver()
                bot.login()
                cur_time = last_time

            if bot.apply(url):
                cur.execute("UPDATE jobs SET applied = ? WHERE id = ?", (1, id))

        con.commit()
    elif text == '/view':
        cur.execute("SELECT count(*), min(visited) FROM jobs WHERE applied = 0")

        applied = cur.fetchone()

        print('diagnostics...')

        print(f'number of jobs to be applied = {applied[0]}, min date visit = {applied[1]}')

        cur.execute("SELECT count(*) FROM jobs WHERE applied = 1")

        non_applied = cur.fetchone()

        print(f'number of applied jobs = {non_applied[0]}')
    elif text == '/clear':
        cur.execute("DELETE FROM jobs WHERE applied = 0")
        con.commit()

    elif text == '/quit':
        break

    elif text == '/help':
        with open('help.txt', 'r') as f:
            for line in f.readlines():
                print(line, end = '')
    else:
        print('invalid command')

bot.quit()
con.close()
