from CTFd.models import db, Teams, Challenges, Flags

class RedHerringChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "red_herring"}
    id = db.Column(
        db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True
    )

    def __init__(self, *args, **kwargs):
        super(RedHerringChallenge, self).__init__(**kwargs)


class CheaterTeams(db.Model):
    __tablename__ = 'cheater_teams'

    id = db.Column(db.Integer, primary_key=True)
    challengeid = db.Column(db.Integer, db.ForeignKey('challenges.id', ondelete="CASCADE"))
    cheaterid = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    cheatteamid = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete="CASCADE"))
    sharerteamid = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete="CASCADE"))
    flagid = db.Column(db.Integer, db.ForeignKey('flags.id', ondelete="CASCADE"))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, challengeid, cheaterid, cheatteamid, sharerteamid, flagid):
        self.challengeid = challengeid
        self.cheaterid = cheaterid
        self.cheatteamid = cheatteamid
        self.sharerteamid = sharerteamid
        self.flagid = flagid

    def __repr__(self):
        return "<CheaterTeams Team {0} maybe cheated for challenge {1} with the flag {2} belonging to the team {3} at {4} >".format(self.cheatteamid, self.challengeid, self.flagid, self.sharerteamid, self.date)
    
    def cheated_team_name(self):
        return Teams.query.filter_by(id=self.cheatteamid).first().name

    def shared_team_name(self):
        return Teams.query.filter_by(id=self.sharerteamid).first().name

    def challenge_name(self):
        return Challenges.query.filter_by(id=self.challengeid).first().name
    
    def flag_content(self):
        return Flags.query.filter_by(id=self.flagid).first().content