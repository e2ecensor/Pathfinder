from http import server
import os
from sqlite3 import Timestamp
import sys
import json
import random
from multiprocessing.pool import ThreadPool
from urllib import response
import requests
import time
import socket
import socks
import dns.query
import dns.message
import dns.name
import dns.rdatatype
import ssl
import base64
import struct
import OpenSSL
import random
from io import BytesIO
from proxy_request import proxy_http
import urllib.parse
import os
import ipaddress
import random
import datetime
import setup
import joblib



def read_domain(file):
    """
    read domain info from plain file
    args:
        file: str. full file path or relevant file path
    returns:
        dict
    raises:
        None
    """
    with open(file, "r") as f:
        data = []
        for r in f.readlines():
            # skip empty lines
            if r == "\n":
                continue
            r = r.replace("false", "False")
            r = r.replace("true", "True")
            try:
                # convert string to dictionary
                data.append(eval(r))
            except Exception as e:
                print(e)
    return data

def unpack_proxy_args(proxy):
    proxy_address = proxy['proxy_address']
    proxy_port = proxy['proxy_port']
    username = proxy['username']
    password = proxy['password']
    return proxy_address, proxy_port, username, password

def get_curl_cmd(proxy, url):
    proxy_address, proxy_port, username, password = unpack_proxy_args(proxy)
    return 'curl -m 10 -s -x ' + proxy_address + ':' + str(proxy_port) + ' -U ' + username + ':' + password + ' ' + url

def get_proxy_stats(proxy, timeout = 5):
    url = 'http://api.proxyrack.net/stats'
    curl_cmd = get_curl_cmd(proxy, url)
    try:
        stats = os.popen(curl_cmd).read()
        response = json.loads(stats)
    except:
        response = None
    
    return response

def release_exit_node(proxy, timeout = 5):
    url = 'http://api.proxyrack.net/release'
    curl_cmd = get_curl_cmd(proxy, url)

    flag = False
    try:
        response = os.popen(curl_cmd).read()
        
        if 'true' in response:
            flag = True
    except:
        pass
    
    return flag

def get_proxy_info(proxy, timeout = 5):
    url = 'http://ip-api.com/json'
    curl_cmd = get_curl_cmd(proxy, url)

    try:
        response = os.popen(curl_cmd).read()
        response = json.loads(response)
    except:
        response = None

    return response

def get(proxy, url, header = {}, timeout = 5):
    proxy_address, proxy_port, username, password = unpack_proxy_args(proxy)
    proxies = {
        "https":"socks5h://{}:{}@{}".format(username, password, proxy_address + ':' + str(proxy_port)),
        "http":"socks5h://{}:{}@{}".format(username, password, proxy_address + ':' + str(proxy_port))
        }
    try:
        response = requests.get(url, proxies=proxies, headers = header, timeout = timeout) 
    except Exception as e:
        print(e)
        response = None
    
    return response

def check_response(http_result, proxy, headers, url, domain, proxy_info, is_timeout):
    headers = dict()
    headers['Host'] = domain
    headers['User-Agent'] = 'Mozilla/5.0'
    print(url, domain)

    http_result = dict()
    http_result['timestamp'] = int(time.time())
    http_result['status'] = 'success'
    http_result['status_code'] = 0
    http_result['url'] = ''
    http_result['text'] = ''
    http_result['headers'] = dict()
    http_result['is_timeout'] = is_timeout

    if not is_timeout:
        if http_result == '':
            http_result['status'] = 'fail'
            result.append(http_result)
        else:
            http_result['text'] = result.text
            http_result['url'] = result.url
            http_result['status_code'] = result.status_code
            http_result['headers'] = dict(result.headers)
            result.append(http_result)
    else:
        http_result['status'] = 'fail'
        result.append(http_result)

    # return http_result

def local_cache_test(proxy):
    has_cache = False
    domain = 'a.test.dnsexp.xyz'

    # # cache phase
    # cache_dns_result = proxy_request.proxy_dns(domain, dns_validation_server, proxy=proxy, timeout=timeout)
    # # cache failure, drop proxy
    # if cache_dns_result[1]['ip_list'] != dns_validation_result:
    #     has_cache = True

    cache_http_result = proxy_http(domain, "44.200.143.229", proxy=proxy, timeout=5)
    # cache failure, drop proxy
    
    if cache_http_result[2]['text'] != 'validation\n':
        has_cache = True
    
    # test phase
    if not has_cache:
    #     test_dns_result = proxy_request.proxy_dns(domain, dns_server, proxy=proxy, timeout=timeout)
    #     if test_dns_result[1]['ip_list'] != ['100.100.100.100']:
    #         has_cache = True

        test_http_result = proxy_http(domain, "44.204.193.148", proxy=proxy, timeout=5)
        if 'linjin@udel.edu' not in test_http_result[2]['text']:
            has_cache = True

    return has_cache


if __name__ == "__main__":
    start = time.time()
    country_count = {}
    while True:
        end = time.time()
        if end - start > 86400 * 7:
            break
        if len(country_count) != 0:
            flag = True
            for item_count in country_count.items():
                if item_count[1]<=10:
                    flag = False
                    break
            if flag:
                break
        # read domain
        data = read_domain("./http_overall.txt")

        # read proxy info
        with open("./proxy.json") as f:
            proxy = json.loads(f.read())

        lower_port = 10000
        upper_port = 10249
        proxy["proxy_port"] = random.randint(lower_port, upper_port)
        print(proxy["proxy_port"])
        #with open("port_number_finished.txt","w") as file:
            #file.write(proxy["proxy_port"])
        proxy_info = get_proxy_info(proxy)
        
        # cache test start
        has_cache = local_cache_test(proxy)
        if has_cache:
            print("Cache test failure")
            continue


        if proxy_info is None or proxy_info == '':
            continue
        elif proxy_info is not None:
            country = proxy_info["country"]
            if country not in country_count.keys():
                country_count[country]=1
            else:
                country_count[country]=country_count[country]+1
            if country_count[country]>10:
                print(json.dumps(country_count, indent=4))
                print("skip country")
                continue


        
        # validate if proxy is working
        response = get_proxy_stats(proxy)
        if response is not None:
            print("Proxy is working")
            # working_proxy_number = working_proxy_number + 1
            # continuous_not_working_proxy_number = 0
        else:
            print("Proxy is not working")
            # continuous_not_working_proxy_number = continuous_not_working_proxy_number +1
            continue
        # validate if proxy is working after all threads finished

        IP = proxy_info['query']
        # the url we want to test
        url_list = ["control_server_IP1", "control_server_IP2", "control_server_IP3", "control_server_IP4", "control_server_IP5", "control_server_IP6"]

        # number of threads can be changed
        pool = ThreadPool(50)

        # test each domain in file
        result = []
        5
        print("Proxy info:", proxy_info)

        y = {}
        x = {}
        for http_result in data:
            # print(http_result)
            if http_result["country"] != country:
                continue
            
            list = []
            for domain in http_result["domain"]:
                for url in url_list:
                    list.append([domain, url])
            
            
                
                # print(domain)
                
                
            results = joblib.Parallel(n_jobs = 20,  backend="threading") (joblib.delayed(proxy_http) (item[0], item[1], proxy=proxy) for item in list)
            
            
                
                # print(json.dumps(results[0][2], indent=4))
                
            for result in results:
                if result[0] not in x.keys():
                    x[result[0]] = {}
                x[result[0]][result[1]]=result[2]
               
                
        

        z = {"proxy": proxy_info, "domain": x}
        print("Completed")
        
        proxy_info = get_proxy_info(proxy)
    
        if proxy_info is None or proxy_info == '':
            print("Proxy change to none")
            country_count[country]=country_count[country]-1
            continue
        elif proxy_info['query'] != IP:
            print("Proxy change to another")
            country_count[country]=country_count[country]-1
            continue
        # print(IP)
        # print(proxy_info['query'])
        print("Proxy does not change")


        # with open("result.json", "a") as f:
        with open(sys.argv[1], "a") as f:
            f.write(json.dumps(z) + '\n')
        # exit()
