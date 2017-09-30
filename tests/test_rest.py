#!/usr/bin/env python
import os
import sys
import logging
import requests, json, yaml
import coloredlogs, names

def main():
    coloredlogs.install()


    logging.warn("============== Start Testing =======================")

    # Find config file, and read in config
    config = find_config('test.yaml')

    logfile = 'test_smart.log' 


    # Check if logging level was specified
    try:
        logging_level = logging.getLevelName(config['logging_level'])
    except KeyError as e:
        logging_level = logging.getLevelName('ERROR')

    # Set up logging
    logging.basicConfig(filename=logfile, level=logging_level,
    format='%(asctime)s - %(levelname)s - %(message)s')

    # Test 1
    logging.info("TEST1: Description: check specialists by speciality")
    ret = check_specialists_by_speciality(config['backend_host'], config['backend_port'], 2)
    if (len(ret)>0):
        logging.warn("check_specialists_by_speciality(): ret={} Number of items={}".format(json.dumps(ret, indent=2, sort_keys=True),len(ret)))
        logging.info("check_specialists_by_speciality(): TEST OK !!!!!!")
    else:
        logging.error("check_specialists_by_speciality(): TEST KO !!!!!!!")


    # Test 2
    logging.info("TEST2: Description: check all specialities")
    ret = check_all_specialities(config['backend_host'], config['backend_port'])
    if (len(ret)>0):
        logging.warn("check_all_specialities(): ret={} Number of items={}".format(json.dumps(ret, indent=2, sort_keys=True),len(ret)))
        logging.info("check_all_specialities(): TEST OK !!!!!!")
    else:
        logging.error("check_all_specialities(): TEST KO !!!!!!!")


    # Test 3
    logging.info("TEST3: Description: check all posts of a specialist")
    ret = check_specialist_posts(config['backend_host'], config['backend_port'],1)
    if (len(ret)>0):
        logging.warn("check_specialist_posts(): ret={} Number of items={}".format(json.dumps(ret, indent=2, sort_keys=True),len(ret)))
        logging.info("check_specialist_posts(): TEST OK !!!!!!")
    else:
        logging.error("check_specialist_posts(): TEST KO !!!!!!!")


    #check_post_specialist(config['backend_host'], config['backend_port']) 




def check_specialists_by_speciality(url, port, speciality):
    # Assemble url
    url = 'http://{0}:{1}/specialists?speciality={2}'.format(url, port,speciality)

    try:
        #Send REST API call
        logging.warn("REQUEST: GET {}".format(url))
        request = requests.get(url)
        request.raise_for_status()
        return json.loads(request.text)
    except ConnectionError as e:
        logging.error("check_specialists_by_speciality: Failed {0}".format(e))
        logging.error(json.loads(request.text))
    except requests.exceptions.HTTPError as e:
        logging.error("check_specialists_by_speciality: Failed {0}".format(e))
        logging.error(json.loads(request.text)['error']['reason'])
    except requests.exceptions.ConnectionError as e:
        logging.error("check_specialists_by_speciality: Failed {0}".format(e))


def check_all_specialities(url, port):
    # Assemble url
    url = 'http://{0}:{1}/specialities/all'.format(url, port)

    try:
        #Send REST API call
        logging.warn("REQUEST: GET {}".format(url))
        request = requests.get(url)
        request.raise_for_status()
        return json.loads(request.text)
    except ConnectionError as e:
        logging.error("check_all_specialities: Failed {0}".format(e))
        logging.error(json.loads(request.text))
    except requests.exceptions.HTTPError as e:
        logging.error("check_all_specialities: Failed {0}".format(e))
        logging.error(json.loads(request.text)['error']['reason'])
    except requests.exceptions.ConnectionError as e:
        logging.error("check_all_specialities: Failed {0}".format(e))


def check_specialist_posts(url, port, specialist):
    # Assemble url
    url = 'http://{0}:{1}/posts?specialist={2}'.format(url, port,specialist)

    try:
        #Send REST API call
        logging.warn("REQUEST: GET {}".format(url))
        request = requests.get(url)
        request.raise_for_status()
        return json.loads(request.text)
    except ConnectionError as e:
        logging.error("check_specialist_posts: Failed {0}".format(e))
        logging.error(json.loads(request.text))
    except requests.exceptions.HTTPError as e:
        logging.error("check_specialist_posts: Failed {0}".format(e))
        logging.error(json.loads(request.text)['error']['reason'])
    except requests.exceptions.ConnectionError as e:
        logging.error("check_specialist_posts: Failed {0}".format(e))



# def check_specialities_by_domain(url, port, specialist):
#     # Assemble url
#     url = 'http://{0}:{1}/posts?specialist={2}'.format(url, port,specialist)

#     try:
#         #Send REST API call
#         logging.warn("REQUEST: GET {}".format(url))
#         request = requests.get(url)
#         request.raise_for_status()
#         return json.loads(request.text)
#     except ConnectionError as e:
#         logging.error("check_specialists_by_speciality: Failed {0}".format(e))
#         logging.error(json.loads(request.text))
#     except requests.exceptions.HTTPError as e:
#         logging.error("check_specialists_by_speciality: Failed {0}".format(e))
#         logging.error(json.loads(request.text)['error']['reason'])
#     except requests.exceptions.ConnectionError as e:
#         logging.error("check_specialists_by_speciality: Failed {0}".format(


def check_post_specialist(url, port):
    # Assemble url
    backend_url = 'http://{0}:{1}/specialists \
    '.format(url, port)

 #    try:
 #    	datas = json.dumps({
	#         "name": "Hechmi hamdi",
	#         "geocode": "36.808314, 10.183735",
	#         "about_website": "no web site",
	#         "phone": "71 455233",
	#         "speciality": 2 
	#         })
 #    	headers = {'content-type': 'application/json'}
	#     response = requests.post(backend_url, data=datas, headers=headers)
 #    except ConnectionError as e:
 #        logging.error("post: Failed to create {0}".format(e))
 #        logging.error(json.loads(request.text))
 #    except requests.exceptions.HTTPError as e:
 #        logging.error("post: Failed to create {0}".format(e))
 #        logging.error(json.loads(request.text)['error']['reason'])
 #    except requests.exceptions.ConnectionError as e:
 #        logging.error("post: Failed to create {0}".format(e))


	# print("response: ", response.text)


def find_config(configfile):
    # Read in config from config file
    try:
        with open(configfile, 'r') as ymlfile:
            config = yaml.load(ymlfile)
            return(config)
    except FileNotFoundError as e:
        print(e)
        exit()


if __name__ == '__main__':
    main()
