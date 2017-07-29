from requests import HTTPError
from riotwatcher import RiotWatcher
import config

watcher = RiotWatcher(config.riot_token)

my_region = 'ru'
sumname = 'TestBLYATb'


def summoner(sumname):
    try:
        me = watcher.summoner.by_name(my_region, sumname)
        level = str(me['summonerLevel'])
        return str(me['id'])
    except HTTPError:
        print('Summoner not found')


# def ranked(sumname):
#     my_ranked_stats = watcher.league.positions_by_summoner(my_region, summoner(sumname))
#     return(my_ranked_stats[0])


def ranked(sumname):
    my_ranked_stats = watcher.league.positions_by_summoner(my_region, int(summoner(sumname)))
    text = "Твой дивизион: {} \n" \
           "Твой ранг: {} \n" \
           "Твои очки лиги: {} \n".format(my_ranked_stats[0]['tier'],
                                          my_ranked_stats[0]['rank'],
                                          str(my_ranked_stats[0]['leaguePoints']))
    print(text)
    print(my_ranked_stats)
    return text


# ranked(sumname)
summoner(sumname)
