import requests
import json
import time
import traceback
import ConfigParser
import sys
import io
import os
import readline
import argparse





global START, END, START_FILE_NAME, STEP, BASE_URL_TEMPL

config = ConfigParser.ConfigParser()
config.read("/Users/miachen/Desktop/Apache/config.ini")

START = int(config.get("global_params","START"))
END = int(config.get("global_params","END"))
START_FILE_NAME = config.get("global_params","START_FILE_NAME")
STEP = int(config.get("global_params","STEP"))
BASE_URL_TEMPL = config.get("global_params","BASE_URL_TEMPL")
PROJECT_NAME = config.get("global_params","PROJECT_NAME")
JSON_DIR = "/Users/miachen/Desktop/Apache/Json/"



def delete_directory(JSON_DIR):
    if os.path.isdir(JSON_DIR):
        for the_file in os.listdir(JSON_DIR):
            file_path = os.path.join(JSON_DIR, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print("delete")
            except Exception as e:
                print(e)


def check_directory():
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

    print(os.path.isdir(JSON_DIR))
    if os.path.isdir(JSON_DIR):
        line = raw_input('the directory is not empty, do you want to delete it, tap "yes" or "non" ')
        if line == "yes":
            delete_directory(JSON_DIR)
        else:
            pass

def keep_directory():
    if os.path.isdir(JSON_DIR):
        print("we are going to keep the directory")



def get_config(fname="./config.ini"):
    config = ConfigParser.ConfigParser()
    config.read(fname)
    return config


def init():
    global BASE_URL_TEMPL, URL_TEMPL, END, PROJECT_NAME
    url = BASE_URL_TEMPL % (PROJECT_NAME, int(STEP), int(START))
    print("init:url : %s" % url)
    try: #TODO:
        r = requests.request('GET', url)
        if r.status_code == 200:
        # payload
            t = r.text

            # convert payload to our happy format
            # TODO: catch bad json here - add exception handling and log
            try:
                j = json.loads(t)
            except:
                print("could not load the file")
        # get max number of JIRAS in db
        # from json header field 'total'
            END = int(j['total'])
        # note this number will increase with time
        # note it may also change in the middle of a run
            print("retrieved \'total\' = %d from json" % END)
    except: #TODO:
        print("could not init()")
        traceback.print_exc()
        sys.exit(100)

    return




# TODO: set globals via config, so function gets default values from config, effectively
# the only value that needs to be set dynamically is END which is read from the json after the call to init()

def fetch(num_fetches=1, start_val=START, end_val=END,  start_file_name=START_FILE_NAME, step=STEP):
    global END
    next_val = 0
    # start_file is read from only if start value provided is explicitly 0
    # however it is always written to after each call for future reference

    if start_val == 0:
        with open(start_file_name) as start_file:
            start_val = int(start_file.readline().strip())
    # useful while testing to run a few fetches rather than 100's of them
    if end_val == 0:
        end_val = min(END, start_val + num_fetches * step)

    cur_val = start_val

    print("start while: %d, %d, %d" % (start_val, end_val, step))

    while cur_val < end_val:
        try:
            f_name = "startAt%d" % cur_val
            print("start one more iteration:---  %s, %d" % (f_name, cur_val))

            url = BASE_URL_TEMPL % (PROJECT_NAME, step, cur_val)
            r = requests.request('GET', BASE_URL_TEMPL % (PROJECT_NAME, step, cur_val))
            #fetch_one(url)
            payload = r.text
            js_object = json.loads(payload)

            with open(JSON_DIR + f_name + '.json', 'w') as js_file:
                js_file.write(json.dumps(js_object))
            print("Done")

            # save it in case we quit now
            with open(start_file_name, 'w') as start_file:
                # save the next starting point
                next_val = cur_val + step
                start_file.write(str(next_val))

            print("--- end one more iteration:   %s, %d" % (f_name, cur_val))

            # next startAt value
            cur_val = next_val

            time.sleep(1)

        except:
            print("cur_val: %d" % (cur_val))
            traceback.print_exc()

    print("end while: %s, %d, %d" % (f_name, cur_val, end_val))



# refactor above and pull the get request into this
# fetch one takes an "address" and returns a json object
def fetch_one(address):
    dic = {}
    dic["url"] = address
    J = json.dump(dict)

    return J



if __name__ == '__main__':
    init()
    limit = 1
    print(limit)
    #check_directory()
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('c', action=check_directory(),
                        help='check the directory')
    parser.add_argument('k', action=keep_directory(),
                        help='keep the directory')

    #parser.add_argument('d', action=delete_directory(),
                        #help='delete files in the directory')
    while limit == 1:
        try:
			fetch(end_val=END)
        except:
            print("hello")
            limit = 0







