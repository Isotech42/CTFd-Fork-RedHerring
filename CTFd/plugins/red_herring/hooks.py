from sqlalchemy.event import listen
from CTFd.models import db, Teams, Challenges, Flags
from .utils import generate_flag

def on_team_create(mapper, conn, team):
    # When a team is created, create a new flag for each challenge that is a "red_herring" type
    red_herring_challenges = Challenges.query.filter_by(type="red_herring").all()

    for challenge in red_herring_challenges:
        generated_flag = generate_flag()

        # Create the flag
        flag = Flags(challenge_id = challenge.id, type = "red_herring", content = generated_flag, data = team.id)
        db.session.add(flag)

def load_hooks():
    listen(Teams, "after_insert", on_team_create)