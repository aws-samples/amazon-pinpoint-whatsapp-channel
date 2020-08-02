import json
import os
import pytest

ROOT_DIR = os.path.abspath(os.curdir)

@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    with open(os.path.join(ROOT_DIR, 'env.json')) as json_file:
        data = json.load(json_file)
        monkeypatch.setenv('ACCOUNT_SID', data['AmazonPinpointWhatsappChannelFunction']['ACCOUNT_SID'])
        monkeypatch.setenv('AUTH_TOKEN', data['AmazonPinpointWhatsappChannelFunction']['AUTH_TOKEN'])