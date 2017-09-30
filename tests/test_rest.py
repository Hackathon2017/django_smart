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




    #Test 4
    logging.info("TEST4: Description: check Posting specialist")
    ret = check_post_specialists(config['backend_host'], config['backend_port'])
    if (len(ret)>0):
        logging.warn("check_post_specialists(): ret={} Number of items={}".format(json.dumps(ret, indent=2, sort_keys=True),len(ret)))
        logging.info("check_post_specialists(): TEST OK !!!!!!")
    else:
        logging.error("check_post_specialists(): TEST KO !!!!!!!")


    #Test 6
    logging.info("TEST6: Description: check specialities by domain")
    ret = check_get_specialists_by_domain(config['backend_host'], config['backend_port'], 1)
    if (len(ret)>0):
        logging.warn("check_get_specialists_by_domain(): ret={} Number of items={}".format(json.dumps(ret, indent=2, sort_keys=True),len(ret)))
        logging.info("check_get_specialists_by_domain(): TEST OK !!!!!!")
    else:
        logging.error("check_get_specialists_by_domain(): TEST KO !!!!!!!")


    # Test 7
    # logging.info("TEST7: Description: check Posting avis")
    # ret = check_post_avis(config['backend_host'], config['backend_port'])
    # if (len(ret)>0):
    #     logging.warn("check_post_avis(): ret={} Number of items={}".format(json.dumps(ret, indent=2, sort_keys=True),len(ret)))
    #     logging.info("check_post_avis(): TEST OK !!!!!!")
    # else:
    #     logging.error("check_post_avis(): TEST KO !!!!!!!")


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



def check_get_specialists_by_domain(url, port, domain):
    # Assemble url
    url = 'http://{0}:{1}/specialities?domain={2}'.format(url, port,domain)

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
        logging.error("post: Failed to create {0}".format(e))



def check_post_specialists(url, port):
    # Assemble url
    backend_url = 'http://{0}:{1}/specialists/'.format(url, port)


    print(names.get_first_name(),names.get_last_name())
    print(names.get_first_name(),names.get_last_name())
    print(names.get_first_name(),names.get_last_name())
    
    random_name = names.get_first_name() + " " + names.get_last_name()
    print("selected name:",random_name, "to be posted on:", backend_url)
    
    try:
        datas = json.dumps({
            "name": random_name,
            "geocode": "36.808314, 10.183735",
            "about_website": "no web site",
            "phone": "71 455233",
            "speciality": 2 
        })
        headers = {'content-type': 'application/json'}
        request = requests.post(backend_url, data=datas, headers=headers)
        request.raise_for_status()
        print("response: ", request.text)
        return json.loads(request.text)        
    except ConnectionError as e:
        logging.error("post: Failed to create {0}".format(e))
        logging.error(json.loads(request.text))
    except requests.exceptions.HTTPError as e:
        logging.error("post: Failed to create {0}".format(e))
        logging.error(json.loads(request.text)['error']['reason'])
    except requests.exceptions.ConnectionError as e:
        logging.error("post: Failed to create {0}".format(e))


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



def check_post_avis(url, port):
    # Assemble url
    backend_url = 'http://{0}:{1}/posts/'.format(url, port)


    random_name = names.get_first_name() + " " + names.get_last_name()
    print("selected name:",random_name, "to be posted on:", backend_url)
    
    try:
        datas = json.dumps({'Specialist': {'phone': '1233333', 'speciality': 1, 'geocode': 'adresse 1', 'about_website': 'Special site 1', 'id': 1, 
           'name': 'ahmed'}, 'rate': [{'rate_name': 'ponctuality', 'rate_value': 5}], 'traitement': 5, 'description': 'assaas', 
           'title': 'title', 'tags': [1], 'author': 1, 'ponctualite': 5, 'slug': "comment0", 'publish_date': '2017-09-24T17:35:12.375Z', 'avis': 'assaas'
         })
        headers = {'content-type': 'application/json'}
        request = requests.post(backend_url, data=datas, headers=headers)
        request.raise_for_status()
        print("response: ", request.text)
        return json.loads(request.text)        
    except ConnectionError as e:
        logging.error("post: Failed to create {0}".format(e))
        logging.error(json.loads(request.text))
    except requests.exceptions.HTTPError as e:
        logging.error("post: Failed to create {0}".format(e))
        logging.error(json.loads(request.text)['error']['reason'])
    except requests.exceptions.ConnectionError as e:
        logging.error("post: Failed to create {0}".format(e))



if __name__ == '__main__':
    main()
