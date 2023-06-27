from sqlalchemy.event import listen
from CTFd.models import db, Teams, Challenges, Flags
from .models import RedHerringTeamChallFlag

from mnemonic import Mnemonic

def generate_flag(prefix="flag"):
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)

    # Take only the first 4 words
    words = words.split(" ")[0:4]

    # Insert the header of the flag and "_" between words like "flag{word1_word2_word3_word4}"
    flag = prefix + "{" + "_".join(words) + "}"
    return flag

def on_team_create(mapper, conn, team):
    # When a team is created, create a new flag for each challenge that is a "red_herring" type
    red_herring_challenges = Challenges.query.filter_by(type="red_herring").all()

    for challenge in red_herring_challenges:
        flag = generate_flag()
        
        # Create the flag
        flag = Flags(challenge.id, flag)

        # Create the association between the team and the flag
        team_flag = RedHerringTeamChallFlag(team.id, challenge.id, flag.id)

        # Add the flag and the relation team-flag to the database
        db.session.add(flag)
        db.session.add(team_flag)

    db.session.commit()

def load_hooks():
    listen(Teams, "after_insert", on_team_create)