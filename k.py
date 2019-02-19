#!/usr/bin/env python3
'''
Allow you to easily grind through problems on kattis. The problem IDs are taken from a
line-separated text file problems.txt, and problems will be deleted from the file as
they are completed.
'''

from lxml import html
import os
import subprocess
import time
import urllib.request
import webbrowser

from getch import getch
from submit.submit import *


PROBLEM_DIR = 'problems'


def main():
	problem_ids = read_problem_ids()
	if len(problem_ids) == 0:
		print("No problem IDs in problem.txt")
		sys.exit(1)
	
	repeat = False
	while True:
		start_problem(problem_ids[0], repeat)
		repeat = True
		submission_id = None
		try:
			with open(os.path.join(get_dir(problem_ids[0]), 'submission.txt')) as f:
				submission_id = f.read().strip()
		except OSError:
			pass

		if submission_id:
			cookies = get_cookies()
			status = False
			status_text = None
			time.sleep(0.5)
			while True:
				req = requests.get('https://open.kattis.com/submissions/' + submission_id, cookies=cookies)
				tree = html.fromstring(req.content)
				status_node = tree.cssselect('td.status')[0]
				status_text = status_node.text_content()

				status_class = status_node.get('class')
				if status_class.find('accepted') != -1:
					status = True
					break
				elif status_class.find('rejected') != -1:
					status = False
					break

				print('Waiting...')
				time.sleep(2)

			print(status_text)
			if status:
				repeat = False
				problem_ids = problem_ids[1:]
				write_problem_ids(problem_ids)
			else:
				ask_exit()
		else:
			ask_exit()


def ask_exit():
	while True:
		inp = input_ch('Exit? [y/N]')
		if inp == 'y':
			sys.exit(1)
		elif inp == 'n' or inp == '\r':
			break


def start_problem(problem_id, repeat=False):
	problem_url = 'https://open.kattis.com/problems/' + problem_id
	problem_path = get_dir(problem_id)
	samples_path = os.path.join(problem_path, 'samples.zip')

	if not repeat:
		webbrowser.open(problem_url)

	try:
		os.mkdir(PROBLEM_DIR)
	except FileExistsError:
		pass

	dir_exists = False
	try:
		os.mkdir(problem_path)
	except FileExistsError:
		dir_exists = True

	if dir_exists:
		try:
			os.remove(os.path.join(problem_path, 'submission.txt'))
		except:
			pass
	else:
		cookies = get_cookies()
		download_file(problem_url + '/file/statement/samples.zip', samples_path, cookies)
		# unzip into correct directory with -d
		subprocess.run(['unzip', samples_path, '-d', problem_path])

	subprocess.run(['vim', os.path.join(problem_path, problem_id + '.py')])


def download_file(url, path, cookies):
	req = requests.get(url, cookies=cookies)
	with open(path, 'wb') as f:
		f.write(req.content)


def get_cookies():
	''' Get the cookies from logging into kattis. '''
	try:
		cfg = get_config()
	except ConfigError as exc:
		print(exc)
		sys.exit(1)

	try:
		login_reply = login_from_config(cfg)
	except ConfigError as exc:
		print(exc)
		sys.exit(1)
	except requests.exceptions.RequestException as err:
		print('Login connection failed:', err)
		sys.exit(1)

	if not login_reply.status_code == 200:
		print('Login failed.')
		if login_reply.status_code == 403:
			print('Incorrect username or password/token (403)')
		elif login_reply.status_code == 404:
			print('Incorrect login URL (404)')
		else:
			print('Status code:', login_reply.status_code)
		sys.exit(1)

	return login_reply.cookies


def read_problem_ids():
	''' Read in a list of problem IDs from file. '''
	res = []
	with open('problems.txt', 'r') as f:
		res = f.read().split()

	return res


def write_problem_ids(problem_ids):
	''' Write a list of problem IDs to file. '''
	with open('problems.txt', 'w') as f:
		data = '\n'.join(problem_ids) + '\n'
		f.write(data)


def get_dir(problem_id):
	return os.path.join(PROBLEM_DIR, problem_id);


def input_ch(text):
	print(text)
	return getch()


if __name__ == '__main__':
	main()
