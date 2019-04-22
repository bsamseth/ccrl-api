# CCRL Rating API

This is a restful HTTP API to query the [CCRL](http://ccrl.chessdom.com/ccrl/404/) rating lists for computer chess engines. It can be used to fetch overall statistics about any chess engine on any of the three lists:

  * [CCRL 40/4](http://ccrl.chessdom.com/ccrl/404/)
  * [CCRL 40/40](http://ccrl.chessdom.com/ccrl/4040/)
  * [CCRL 40/4 Fisher Random Chess (FRC)](http://ccrl.chessdom.com/ccrl/404FRC)
  
There is also the option to get badges from [shields.io](https://shields.io/) with dynamicly loaded ratings.

## API Documentation

To use the API you have two options:

1. Clone this repository and run the web service localy on your own machine/server.
2. Use the server hosted by me.

The latter option is currently available at the following IP:

```text
    http://104.196.164.195
```

The reliability of this service is not guaranteed, and the IP could be subject to change, although this will be kept as stable as possible. If the badges at the top of this README has rendered succesfully, the service is available.

### JSON Queries

Query a list for a given engine:

``` text
GET /<List>/<Name>

Response:

{
    "rank": string  # Rank of the list. May be a range, e.g. "1-5".
    "name": string   # Full name of engine.
    "rating": integer  # ELO rating.
    "rating-pluss": integer  # Upper uncertainty in rating.
    "rating-minus": integer  # Lower uncertainty in rating.
    "score": float  # Percentage of average points per game (Win = 1, Draw = 1/2).
    "average-opponent-diff": float  # Average rating difference of opponents.
    "draw-rate": float  # Percentage draw rate.
    "games-played": integer  # Number of games recorded for this engine.
}
```
The `<List>` must be one of the following:

  * `4040` for CCRL 40/40
  * `404` for CCRL 40/4
  * `404FRC` for CCRL 40/4 FRC

The `<Name` can be any uniquely identifying string found on the corresponding CCRL rating list. The API will find the first entry where `<Name>` is found within the full name.

__Example__:
``` text
GET /4040/Goldfish%201.13.0
{
    "rank": "351-353",
    "name": "Goldfish 1.13.0 64-bit",
    "rating": 2044,
    "rating-pluss": 22,
    "rating-minus": -22,
    "score": 49.5,
    "average-opponent-diff": 5.5,
    "draw-rate": 26.6,
    "games-played": 751
}
```

### GitHub Badges

Optional URL parameters are available to the JSON queries that will yield a [shields.io](https://shields.io) badge with the rating information. 

__Parameters__:

<img alt="example-badge" src="https://img.shields.io/badge/label-rating__prefix_2000_rating__postfix-important.svg"/>

  * `badge`: Set to any non-falsy value to return a shields.io badge instead of the JSON
  * `label`: Left-side text. Default is `CCRL Rating` (remember to replace spaces with `%20`)
  * `rating_prefix`: Right-side text to prepend to the rating. Default is no prefix.
  * `rating_postfix`: Right-side text to append to the rating. Default is no postfix.
  * `color`: Color of right-side of badge. May be any of the below names (`red`, `blue` etc) or a hex number. Default is `orange`.
  * `link`: Specify what the badge should link to. Default is the corresponding CCRL rating list.
  * Any other parameters are forwarded to [shields.io](https://shields.io/), see their API documentation there for additional options available, including `cacheSeconds`, `logo`, `labelColor` and more.

<span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="brightgreen" src="https://img.shields.io/badge/-brightgreen-brightgreen.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="green" src="https://img.shields.io/badge/-green-green.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="yellowgreen" src="https://img.shields.io/badge/-yellowgreen-yellowgreen.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="yellow" src="https://img.shields.io/badge/-yellow-yellow.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="orange" src="https://img.shields.io/badge/-orange-orange.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="red" src="https://img.shields.io/badge/-red-red.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="blue" src="https://img.shields.io/badge/-blue-blue.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="lightgrey" src="https://img.shields.io/badge/-lightgrey-lightgrey.svg"/></span></span><br/><span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="success" src="https://img.shields.io/badge/-success-success.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="important" src="https://img.shields.io/badge/-important-important.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="critical" src="https://img.shields.io/badge/-critical-critical.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="informational" src="https://img.shields.io/badge/-informational-informational.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="inactive" src="https://img.shields.io/badge/-inactive-inactive.svg"/></span></span><br/><span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="blueviolet" src="https://img.shields.io/badge/-blueviolet-blueviolet.svg"/></span><span display="inline" height="20px" class="common__BadgeWrapper-sc-16zh6vt-3 ilKSRz"><img alt="ff69b4" src="https://img.shields.io/badge/-ff69b4-ff69b4.svg"/></span>


__Example__:

``` text
GET /4040/Goldfish?badge=1&label=Engine%20Rating&rating_postfix=%20ELO&color=informational
```
<img alt="example-badge" src="https://img.shields.io/badge/Engine%20Rating-2044%20ELO-informational.svg?badge=1&label=Engine+Rating&rating_postfix=+ELO&color=informational&cacheSeconds=86400&link=http%3A%2F%2Fccrl.chessdom.com%2Fccrl%2F4040"/>
