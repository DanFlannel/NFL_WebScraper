from requests import get
from bs4 import BeautifulSoup

import re
import json
import time


class NFL_Webpage_Scraper(object):

    def __init__(self):
        self.url = "https://www.giants.com/"
        self._nfl_game_strip_id = "nfl-c-game-strip__front-layer"
        self._nfl_game_live_indicator_id = "nfl-c-game-strip__game-clock"

        self._team_container_id = "nfl-c-game-strip__team"
        self._team_name_span_id = "nfl-c-game-strip__team-fullname"
        self._team_record_id = "nfl-c-game-strip__team-record"
        self._team_points = "nfl-c-game-strip__points"

        self._home_const = "home"
        self._away_const = "away"

        self._soup = ""
        self._nfl_game_strip = ""

        self._is_live = False
        self._home_team_soup = ""
        self._away_team_soup = ""

        self._game_object = lambda: None
        self._game_object.teams = list()

    def get_game_score(self):
        self.__get_page()
        self.__check_is_live()
        self.__get_game_strip()
        self.__set_teams()
        self.__set_winner()

        return self._game_object

    def __get_page(self):

        response = get(self.url)
        self._soup = BeautifulSoup(response.content, 'html.parser')

    def __check_is_live(self):

        self._is_live = len(self._soup.findAll(
            "span", {"class": self._nfl_game_live_indicator_id})) != 0

    def __get_game_strip(self):

        self._nfl_game_strip = BeautifulSoup(str(self._soup.find(
            "div", {"class": self._nfl_game_strip_id})), 'html.parser')

    def __set_teams(self):

        teams = self._nfl_game_strip.findAll(
            "div", {"class": self._team_container_id})

        for team in teams:
            # print(team)
            if("away" in str(team)):
                self._away_team_soup = BeautifulSoup(str(team), 'html.parser')
                self.__set_team_info(self._away_team_soup, self._away_const)
            if("home" in str(team)):
                self._home_team_soup = BeautifulSoup(str(team), 'html.parser')
                self.__set_team_info(self._home_team_soup, self._home_const)

    def __set_team_info(self, team, status):

        name = str(team.find(
            "span", {"class": self._team_name_span_id}).text).strip()

        record = str(team.find(
            "span", {"class": self._team_record_id}).text).strip()

        points = team.find(
            "div", {"class": self._team_points})

        if(points):
            points = re.sub('[^0-9]', '', str(points).strip())

        team_info = Team_Info(name, record, points, status)

        self._game_object.teams.append(team_info)

    def __set_winner(self):
        if(self._is_live):
            self._game_object.is_live = True

        score_1 = self._game_object.teams[0].points
        score_2 = self._game_object.teams[1].points

        # they haven't played yet
        if(not score_1 or not score_2):
            # self.__print_game_object()
            return

        if(self._is_live):
            self._game_object.teams[0].status = "live"
            self._game_object.teams[1].status = "live"
            # self.__print_game_object()
            return

        if(score_1 > score_2):
            self._game_object.teams[0].status = "win"
            self._game_object.teams[1].status = "loss"
        if(score_1 < score_2):
            self._game_object.teams[0].status = "win"
            self._game_object.teams[1].status = "loss"

        if(score_1 == score_2):
            self._game_object.teams[0].status = "draw"
            self._game_object.teams[1].status = "draw"

        # self.__print_game_object()

    def __print_game_object(self):
        json_obj = json.dumps(self._game_object, default=lambda x: x.__dict__)

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


class NFL_Scraper():

    def __init__(self):
        self._team_urls = list()
        self.__afc()
        self.__nfc()
        self._games = lambda: None
        self._games.played = list()

    def __afc(self):
        self.__afc_east()
        self.__afc_west()
        self.__afc_north()
        self.__afc_south()

    def __afc_east(self):
        buffalo_bills = "https://www.buffalobills.com/"
        miami_dolphins = "https://www.miamidolphins.com/"
        new_england_patriots = "https://www.patriots.com/"
        # nj_jets = "https://www.newyorkjets.com/"

        self._team_urls.append(buffalo_bills)
        self._team_urls.append(miami_dolphins)
        self._team_urls.append(new_england_patriots)
        # self._team_urls.append(nj_jets)

    def __afc_west(self):
        kansas_city_chiefs = "https://www.chiefs.com/"
        las_vegas_raiders = "https://www.raiders.com/"
        denver_broncos = "https://www.denverbroncos.com/"
        la_chargers = "https://www.chargers.com/"

        self._team_urls.append(kansas_city_chiefs)
        self._team_urls.append(las_vegas_raiders)
        self._team_urls.append(denver_broncos)
        self._team_urls.append(la_chargers)

    def __afc_north(self):
        # steelers = "https://www.steelers.com/"
        clevland_browns = "https://www.clevelandbrowns.com/"
        # baltimore_ravens = "https://www.baltimoreravens.com/"
        cincinatti_bengals = "https://www.bengals.com/"

        self._team_urls.append(clevland_browns)
        self._team_urls.append(cincinatti_bengals)

    def __afc_south(self):
        tenessee_titans = "https://www.tennesseetitans.com/"
        indianappolis_colts = "https://www.colts.com/"
        houston_texans = "https://www.houstontexans.com/"
        jacksonville_jackguars = "https://www.jaguars.com/"

        self._team_urls.append(tenessee_titans)
        self._team_urls.append(indianappolis_colts)
        self._team_urls.append(houston_texans)
        self._team_urls.append(jacksonville_jackguars)

    def __nfc(self):
        self.__nfc_east()
        self.__nfc_west()
        self.__nfc_north()
        self.__nfc_south()

    def __nfc_east(self):
        ny_giants = "https://www.giants.com/"
        washington_football_team = "https://www.washingtonfootball.com/"
        philadelphia_eagles = "https://www.philadelphiaeagles.com/"
        # dallas_cowboys = "https://www.dallascowboys.com/"

        self._team_urls.append(ny_giants)
        self._team_urls.append(washington_football_team)
        self._team_urls.append(philadelphia_eagles)

    def __nfc_west(self):
        seattle_seahawks = "https://www.seahawks.com/"
        la_rams = "https://www.therams.com/"
        arizona_cardinals = "https://www.azcardinals.com/"
        sf_49ers = "https://www.49ers.com/"

        self._team_urls.append(seattle_seahawks)
        self._team_urls.append(la_rams)
        self._team_urls.append(arizona_cardinals)
        self._team_urls.append(sf_49ers)

    def __nfc_north(self):
        greenbay_packers = "https://www.packers.com/"
        chicago_bears = "https://www.chicagobears.com/"
        minnesota_vikings = "https://www.vikings.com/"
        detriot_lions = "https://www.detroitlions.com/"

        self._team_urls.append(greenbay_packers)
        self._team_urls.append(chicago_bears)
        self._team_urls.append(minnesota_vikings)
        self._team_urls.append(detriot_lions)

    def __nfc_south(self):
        neworleans_saints = "https://www.neworleanssaints.com/"
        tampabay_buccaneers = "https://www.buccaneers.com/"
        atlanta_falcons = "https://www.atlantafalcons.com/"
        carolina_panthers = "https://www.panthers.com/"

        self._team_urls.append(neworleans_saints)
        self._team_urls.append(tampabay_buccaneers)
        self._team_urls.append(atlanta_falcons)
        self._team_urls.append(carolina_panthers)

    def scrape_all_teams(self):
        start = time.time()

        for url in self._team_urls:
            web_scraper = NFL_Webpage_Scraper()
            web_scraper.url = url
            self._games.played.append(web_scraper.get_game_score())

        end = time.time()
        self._games.execution_time = (end - start)
        json_obj = json.dumps(self._games, default=lambda x: x.__dict__)
        print(json_obj)

# web_scraper = NFL_Webpage_Scraper()
# web_scraper.get_game_score()


nfl_scraper = NFL_Scraper()
nfl_scraper.scrape_all_teams()
