import os
import json
from flask import render_template, Blueprint
from flask import request, jsonify,session

from CTFd.models import (
    ChallengeFiles,
    Challenges,
    Fails,
    Flags,
    Hints,
    Solves,
    Tags,
    db,
)

from .hooks import load_hooks

from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.migrations import upgrade
from CTFd.plugins.challenges import BaseChallenge, CHALLENGE_CLASSES
from CTFd.plugins.flags import FlagException, get_flag_class
from CTFd.utils.uploads import delete_file
from CTFd.utils.user import get_ip

from CTFd.config import Config

from mnemonic import Mnemonic

PLUGIN_PATH = os.path.dirname(__file__)
CONFIG = json.load(open("{}/config.json".format(PLUGIN_PATH)))

red = Blueprint('red_herring', __name__, template_folder="templates")

class RedHerringChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "red_herring"}
    id = db.Column(
        db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True
    )

    def __init__(self, *args, **kwargs):
        super(RedHerringChallenge, self).__init__(**kwargs)

class RedHerringTypeChallenge(BaseChallenge):
    id = "red_herring"  # Unique identifier used to register challenges
    name = "red_herring"  # Name of a challenge type
    templates = {  # Nunjucks templates used for each aspect of challenge editing & viewing
        'create': '/plugins/red_herring/assets/create.html',  # Used to render the challenge when creating/editing
        'update': '/plugins/red_herring/assets/update.html',  # Used to render the challenge when updating
        'view': '/plugins/red_herring/assets/view.html',  # Used to render the challenge when viewing
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        'create': '/plugins/red_herring/assets/create.js',  # Used to init the create template JavaScript
        'update': '/plugins/red_herring/assets/update.js',  # Used to init the create template JavaScript
        'view': '/plugins/red_herring/assets/view.js',  # Used to init the create template JavaScript
    }

    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = "/plugins/red_herring/assets/"
    challenge_model = RedHerringChallenge

def load(app):
    app.db.create_all() # Create all DB entities
    upgrade(plugin_name="red_herring")
    CHALLENGE_CLASSES['red_herring'] = RedHerringTypeChallenge
    app.register_blueprint(red)
    register_plugin_assets_directory(app, base_path="/plugins/red_herring/assets/")
    load_hooks()