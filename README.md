# CCRL Rating API

This is a restful HTTP API to query the [CCRL](http://ccrl.chessdom.com/ccrl/404/) rating lists for computer chess engines. It can be used to fetch overall statistics about any chess engine on any of the three lists:

  * [CCRL 40/4](http://ccrl.chessdom.com/ccrl/404/)
  * [CCRL 40/40](http://ccrl.chessdom.com/ccrl/4040/)
  * [CCRL 40/4 Fisher Random Chess (FRC)](http://ccrl.chessdom.com/ccrl/404FRC)

## API Documentation

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
