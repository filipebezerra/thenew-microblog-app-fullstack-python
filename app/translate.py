import json
import requests
from flask_babel import _
from app import app


def translate(text, source_language, dest_language):
    if not all([app.config['MS_TRANSLATOR_KEY'],
                app.config['MS_TRANSLATOR_REGION']]):
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': app.config['MS_TRANSLATOR_REGION']
    }
    response = requests.get(f'https://api.microsofttranslator.com/v2/Ajax.svc'
                            f'/Translate?text={text}&from={source_language}&'
                            f'to={dest_language}',
                            headers=auth)

    if response.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(response.content.decode('utf-8-sig'))
