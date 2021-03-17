# -*- coding: utf-8 -*-
from src.models.shared import db

class Visit(db.Model):
    __tablename__ = 'Visit'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _visited_at = db.Column(db.DateTime)
    ip_address = db.Column(db.String(255))
    url_visited = db.Column(db.String(255))
    user_agent = db.Column(db.String(255))

    def __init__(self, ip_address, url_visited, user_agent):
        self.ip_address = ip_address
        self.url_visited = url_visited
        self.user_agent = user_agent

    def __repr__(self):
        content = {"id": self._id,
                    "ip_address": self.ip_address,
                    "url_visited": self.url_visited,
                    "user_agent": self.user_agent
                    }
        return str({"Visit": content})

    def to_dict(self):
        return {"id": self._id,
                "ip_address": self.ip_address,
                "url_visited": self.url_visited,
                "user_agent": self.user_agent
                }
