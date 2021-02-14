import logging
import requests
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    
    username = req.params.get('username')
    repo = req.params.get('repo')
    req_body = req.get_json()
    secret = req_body.get('secret')

    # verifiy that the call is from prismic
    prismiSecret = os.environ["prismic_secret"]
    if prismiSecret != str(secret):
        return func.HttpRequest("Verification failed", status_code = 400)

    data = {
        'event_type': 'prismic'
    }

    url = "https://api.github.com/repos/" + username + "/" + repo + "/dispatches" 

    headers = {
        'Authorization': 'token ' +secret,
        'Accept': 'application/vnd.github.everest-preview+json'
    }

    response = requests.post(url,json=data,headers=headers)
    if response.ok:
        return func.HttpResponse("Action dispatched")
    else:
        return func.HttpRequest("Error",
                                status_code = 500)    