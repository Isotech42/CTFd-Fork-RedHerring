from CTFd.models import db, Teams, Challenges, Flags

class RedHerringTeamChallFlag(db.Model):
    __tablename__ = 'red_herring_team_chall_flag'

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Integer, db.ForeignKey('teams.id'))
    challenge = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    flag = db.Column(db.String(80))

    def __init__(self, team, challenge, flag):
        self.target = team
        self.challenge = challenge
        self.flag = flag

    def __repr__(self):
        return "<RedHerringTeamChallFlag {0} {1} {2}>".format(self.team, self.challenge, self.flag)