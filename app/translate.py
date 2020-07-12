import json
import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    if not all([current_app.config['MS_TRANSLATOR_KEY'],
                current_app.config['MS_TRANSLATOR_REGION']]):
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key':
            current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region':
            current_app.config['MS_TRANSLATOR_REGION']
    }
    response = requests.get(f'https://api.microsofttranslator.com/v2/Ajax.svc'
                            f'/Translate?text={text}&from={source_language}&'
                            f'to={dest_language}',
                            headers=auth)

    if response.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(response.content.decode('utf-8-sig'))
