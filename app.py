from flask import Flask, redirect, request, url_for
import urllib
from flask_restful import Resource, Api, abort
from bs4 import BeautifulSoup
import re
import requests

app = Flask(__name__)
api = Api(app)

CCRL_BASE_URL = "http://ccrl.chessdom.com/ccrl/"
CCRL_4040_URL = CCRL_BASE_URL + "4040"
CCRL_404_URL = CCRL_BASE_URL + "404"
CCRL_404FRC_URL = CCRL_BASE_URL + "404FRC"


def like(string):
    """
    Return a compiled regular expression that matches the given
    string with any prefix and postfix, e.g. if string = "hello",
    the returned regex matches r".*hello.*"
    """
    MATCH_ALL = r".*"
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(regex, flags=re.DOTALL)


def find_by_text(soup, text, tag, **kwargs):
    """
    Find the tag in soup that matches all provided kwargs, and contains the
    text.

    If no match is found, return None.
    If more than one match is found, raise ValueError.
    """
    elements = soup.find_all(tag, **kwargs)
    for element in elements:
        if element.find(text=like(text)):
            return element
    return None


class EngineInfo(Resource):
    def get(self, name):
        resp = requests.get(self.resource_url)
        if not 200 <= resp.status_code <= 299:
            abort(503, message="CCRL did not respond correctly.")

        html = resp.text
        soup = BeautifulSoup(html, features="html.parser")

        span = find_by_text(soup, name, "span", attrs={"class", "oss"})
        if span is None:
            abort(404, message=f"The engine {repr(name)} was not found on the list.")

        tr = span.parent.parent
        data = tr.find_all("b")

        data = {
            "rank": data[0].contents[0].replace('\u2011', '-'),
            "name": data[1].contents[0].contents[0],
            "rating": int(data[2].contents[0]),
            "rating-pluss": int(data[3].contents[0]),
            "rating-minus": int(data[4].contents[0].replace('\u2212', '-')),  # Subs strange unicode - for ascii -
            "score": float(data[5].contents[0][:-1]),
            "average-opponent-diff": float(data[6].contents[0].replace('\u2212', '-')),
            "draw-rate": float(data[7].contents[0][:-1]),
            "games-played": int(data[8].contents[0]),
            "link": self.resource_url,
        }

        if not request.args.get('badge'):
            return data

        params = request.args.copy()
        color = params.get('color', 'orange')
        label = params.get('label', 'CCRL%20rating')
        rating_prefix = params.get('rating_prefix', '')
        rating_postfix = params.get('rating_postfix', '')
        if 'cacheSeconds' not in params:
            params['cacheSeconds'] = 3600 * 24
        if 'link' not in params:
            params['link'] = self.resource_url
        return redirect(f"https://img.shields.io/badge/{label}-{rating_prefix}{data['rating']}{rating_postfix}-{color}.svg?{urllib.parse.urlencode(params)}", code=302)


class EngineInfo4040(EngineInfo):
    @property
    def resource_url(self):
        return CCRL_4040_URL


class EngineInfo404(EngineInfo):
    @property
    def resource_url(self):
        return CCRL_404_URL


class EngineInfo404FRC(EngineInfo):
    @property
    def resource_url(self):
        return CCRL_404FRC_URL


@app.route('/')
def homepage():
    return redirect("https://github.com/bsamseth/ccrl-api")

api.add_resource(EngineInfo4040, "/4040/<string:name>")
api.add_resource(EngineInfo404, "/404/<string:name>")
api.add_resource(EngineInfo404FRC, "/404FRC/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
