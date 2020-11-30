from requests import get
from bs4 import BeautifulSoup
import re
import json


class NFL_Webpage_Scraper(object):

    def __init__(self):
        self.url = "https://www.giants.com/"
        self.nfl_game_strip_id = "nfl-c-game-strip__front-layer"
        self.nfl_game_live_indicator_id = "nfl-c-game-strip__game-clock"

        self.team_container_id = "nfl-c-game-strip__team"
        self.team_name_span_id = "nfl-c-game-strip__team-fullname"
        self.team_record_id = "nfl-c-game-strip__team-record"
        self.team_points = "nfl-c-game-strip__points"

        self.home_const = "home"
        self.away_const = "away"

        self.soup = ""
        self.nfl_game_strip = ""

        self.is_live = False
        self.home_team_soup = ""
        self.away_team_soup = ""

        self.game_object = lambda: None
        self.game_object.teams = list()

    def get_game_score(self):
        self.__get_page()
        self.__check_is_live()
        self.__get_game_strip()
        self.__set_teams()
        self.__set_winner()

    def __get_page(self):

        response = get(self.url)
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def __check_is_live(self):

        self.is_live = len(self.soup.findAll(
            "span", {"class": self.nfl_game_live_indicator_id})) != 0

    def __get_game_strip(self):

        self.nfl_game_strip = BeautifulSoup(str(self.soup.find(
            "div", {"class": self.nfl_game_strip_id})), 'html.parser')

    def __set_teams(self):

        teams = self.nfl_game_strip.findAll(
            "div", {"class": self.team_container_id})

        for team in teams:
            # print(team)
            if("away" in str(team)):
                self.away_team_soup = BeautifulSoup(str(team), 'html.parser')
                self.__set_team_info(self.away_team_soup, self.away_const)
            if("home" in str(team)):
                self.home_team_soup = BeautifulSoup(str(team), 'html.parser')
                self.__set_team_info(self.home_team_soup, self.home_const)

    def __set_team_info(self, team, status):

        name = str(team.find(
            "span", {"class": self.team_name_span_id}).text).strip()

        record = str(team.find(
            "span", {"class": self.team_record_id}).text).strip()

        points = str(team.find(
            "div", {"class": self.team_points}).text).strip()

        points = re.sub('[^0-9]', '', points)

        team_info = Team_Info(name, record, points, status)

        self.game_object.teams.append(team_info)

    def __set_winner(self):
        if(self.is_live):
            self.game_object.is_live = True

        score_1 = self.game_object.teams[0].points
        score_2 = self.game_object.teams[1].points

        if(score_1 > score_2):
            self.game_object.teams[0].status = "win"
            self.game_object.teams[1].status = "loss"
        if(score_1 < score_2):
            self.game_object.teams[0].status = "win"
            self.game_object.teams[1].status = "loss"

        if(score_1 == score_2):
            self.game_object.teams[0].status = "draw"
            self.game_object.teams[1].status = "draw"

        json_obj = json.dumps(self.game_object, default=lambda x: x.__dict__)

        print(json_obj)


class Team_Info(object):
    name = ""
    record = ""
    points = ""
    game_type = ""
    status = ""

    def __init__(self, name, record, points, game_type):
        self.name = name
        self.record = record
        self.points = points
        self.game_type = game_type


web_scraper = NFL_Webpage_Scraper()
web_scraper.get_game_score()

# print(web_scraper.is_live)
# print(web_scraper.soup)
