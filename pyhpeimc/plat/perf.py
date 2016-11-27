#!/usr/bin/env python3
# author: @netmanchris



# This section imports required libraries
import requests
import json
from pyhpeimc.auth import IMCAuth

HEADERS = {'Accept': 'application/json', 'Content-Type':
    'application/json', 'Accept-encoding': 'application/json'}

#auth = IMCAuth('http://','10.101.0.201','8080', 'admin','admin')

headers = {'Accept': 'application/json', 'Content-Type':
    'application/json', 'Accept-encoding': 'application/json'}

def add_perf_task(task, auth, url):
    """
        function takes the a python dict containing all necessary fields for a performance tasks, transforms the dict into
         JSON and issues a RESTFUL call to create the performance task.
        device.

        :param task: dictionary containing all required fields for performance tasks

        :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

        :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

        :return: 204

        :rtype: str

        >>> from pyhpeimc.auth import *

        >>> from pyhpeimc.plat.perf import *

        >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

        >>> new_task = {'indexDesc': '1.3.6.1.4.1.9.9.13.1.3.1.3','indexType': '[index1[0]:ciscoEnvMonTemperatureStatusValue:1:0]','itemFunction': '1.3.6.1.4.1.9.9.13.1.3.1.3','itemName': 'Cisco_Temperature','selectDefaultUnit': '400','unit': 'Celsius'}

        >>> new_perf_task = add_perf_task(new_task, auth.creds, auth.url)
        """
    add_perf_task_url = "/imcrs/perf/task"
    f_url = url + add_perf_task_url
    payload = json.dumps(task)
    # creates the URL using the payload variable as the contents
    r = requests.post(f_url, data = payload, auth=auth, headers=headers)
    try:
        return r.status_code

    except requests.exceptions.RequestException as e:
        return "Error:\n" + str(e) + ' add_perf_task: An Error has occured'


def get_perf_task(task_name, auth, url):
    """
        function takes the a str object containing the name of an existing performance tasks and issues a RESTFUL call
        to the IMC REST service. It will return a list

        :param task_name: str containing the name of the performance task

        :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

        :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

        :return: 204

        :rtype: dict

        >>> from pyhpeimc.auth import *

        >>> from pyhpeimc.plat.perf import *

        >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

        >>> selected_task = get_perf_task('Cisco_Temperature', auth.creds, auth.url)

        >>> assert type(selected_task) is dict

        >>> assert 'taskName' in selected_task
        """
    get_perf_task_url = "/imcrs/perf/task?name="+task_name+"&orderBy=taskId&desc=false"
    f_url = url + get_perf_task_url
    # creates the URL using the payload variable as the contents
    r = requests.get(f_url, auth=auth, headers=headers)
    try:
        if r.status_code == 200:
            perf_task_info = (json.loads(r.text))
            if 'task' in perf_task_info:
                perf_task_info = (json.loads(r.text))['task']
            else:
                perf_task_info = "Task Doesn't Exist"
            return perf_task_info
    except requests.exceptions.RequestException as e:
        return "Error:\n" + str(e) + ' get_perf_task: An Error has occured'


def delete_perf_task(task_name, auth, url):
    '''
    Function takes a str of the target task_name to be deleted and retrieves task_id using
    the get_perf_task function. Once the task_id has been successfully retrieved it is
    populated into the task_id variable and an DELETE call is made against the HPE IMC REST
    interface to delete the target task.
    :param task_name: str of task name
    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: int of 204 if successful, str of "Perf Task doesn't exist" i

    :rtype: int


    '''
    task_id = get_perf_task(task_name, auth, url)
    if type(task_id) is str:
        print ("Perf task doesn't exist")
        return 403
    task_id = task_id['taskId']
    get_perf_task_url = "/imcrs/perf/task/delete/"+str(task_id)
    f_url = url + get_perf_task_url
    # creates the URL using the payload variable as the contents
    r = requests.delete(f_url, auth=auth, headers=headers)
    try:
        if r.status_code == 204:
            print ("Perf Task successfully delete")
            return r.status_code
    except requests.exceptions.RequestException as e:
        return "Error:\n" + str(e) + ' delete_perf_task: An Error has occured'