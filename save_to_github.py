# source https://gist.github.com/avullo/b8153522f015a8b908072833b95c3408

import requests
import base64
import json
import datetime
import string
import pickle


def push_to_repo_branch(file_or_variable, gitHubFileName, fileName, repo_slug, branch, user, token):
    '''
    Push file update to GitHub repo
    
    :param gitHubFileName: the name of the file in the repo
    :param fileName: the name of the file on the local branch
    :param repo_slug: the github repo slug, i.e. username/repo
    :param branch: the name of the branch to push the file to
    :param user: github username
    :param token: github user token
    :return None
    :raises Exception: if file with the specified name cannot be found in the repo
    '''
    
    message = "Automated update " + str(datetime.datetime.now())
    path = "https://api.github.com/repos/%s/branches/%s" % (repo_slug, branch)

    r = requests.get(path, auth=(user,token))
    if not r.ok:
        print("Error when retrieving branch info from %s" % path)
        print("Reason: %s [%d]" % (r.text, r.status_code))
        raise
    rjson = r.json()
    treeurl = rjson['commit']['commit']['tree']['url']
    r2 = requests.get(treeurl, auth=(user,token))
    if not r2.ok:
        print("Error when retrieving commit tree from %s" % treeurl)
        print("Reason: %s [%d]" % (r2.text, r2.status_code))
        raise
    r2json = r2.json()
    sha = None

    for file in r2json['tree']:
        # Found file, get the sha code
        if file['path'] == gitHubFileName:
            sha = file['sha']
            # here i am trying to read the file's content, definitely some bad code
            print(file)
            r_old_data = requests.get(file["url"])
            r_old_data_json = r_old_data.json()
            print(r_old_data_json)
            old_content = r_old_data_json["content"].encode().decode('utf-8')
            print(old_content)
            print(type(old_content))


    # if sha is None after the for loop, we did not find the file name!
    if sha is None:
        print("Could not find " + gitHubFileName + " in repos 'tree' ")
        raise Exception

    if file_or_variable == 'file':
        with open(fileName) as data:
            print(data)
            content = base64.b64encode(data.read().encode())
    elif file_or_variable == 'variable':
        new_content = json.dumps(fileName).encode()
        #content = pickle.dumps(fileName)
    else:
        print('Wrong parameter (file_or_variable)!')

    # gathered all the data, now let's push
    inputdata = {}
    inputdata["path"] = gitHubFileName
    inputdata["branch"] = branch
    inputdata["message"] = message
    if file_or_variable == 'file':
        inputdata["content"] = content.decode('utf8')
    if file_or_variable == 'variable':
        temp = old_content.decode('utf-8') + new_content.decode('utf-8')
        print(temp)
        inputdata["content"] = ''
        print('Input data content is:')
        print(inputdata["content"])
        #content = base64.b64encode(old_content + new_content)
        inputdata["content"] = base64.b64encode(inputdata["content"])
    if sha:
        inputdata["sha"] = str(sha)
    print(inputdata)

    updateURL = "https://api.github.com/repos/{0}/contents/{1}".format(repo_slug, gitHubFileName)
    try:
        rPut = requests.put(updateURL, auth=(user,token), data = json.dumps(inputdata))
        if not rPut.ok:
            print("Error when pushing to %s" % updateURL)
            print("Reason: %s [%d]" % (rPut.text, rPut.status_code))
            raise Exception
    except requests.exceptions.RequestException as e:
        print('Something went wrong! I will print all the information that is available so you can figure out what happend!')
        print(rPut)
        print(rPut.headers)
        print(rPut.text)
        print(e)