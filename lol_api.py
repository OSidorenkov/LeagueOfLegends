from requests import HTTPError
from riotwatcher import RiotWatcher
import config

watcher = RiotWatcher(config.riot_token)

my_region = 'ru'
sumname = "Busido"


def summoner(sumname):
    try:
        me = watcher.summoner.by_name(my_region, sumname)
        level = str(me['summonerLevel'])
        return str(me['id'])
    except HTTPError:
        print('Summoner not found')
        return 0

# def ranked(sumname):
#     my_ranked_stats = watcher.league.positions_by_summoner(my_region, summoner(sumname))
#     return(my_ranked_stats[0])


def ranked(sumname):
    my_ranked_stats = watcher.league.positions_by_summoner(my_region, int(summoner(sumname)))
    if len(my_ranked_stats) > 0:
        text = "Твой дивизион: *{}* \n" \
               "Твой ранг: *{}* \n" \
               "Твои очки лиги: *{}* \n".format(my_ranked_stats[0]['tier'],
                                              my_ranked_stats[0]['rank'],
                                              str(my_ranked_stats[0]['leaguePoints']))
    else:
        text = "Этот чампион не участвовал в ранговых играх."
    print(text)
    return text


def get_runes(sumname):
    runes = watcher.runes.by_summoner(my_region, summoner(sumname))
    rune_names = watcher.static_data.runes(my_region, locale='ru_RU')
    if len(runes) > 0:
        for rune in runes['pages']:
            print(rune['name'])
    else:
        print("no")


get_runes(sumname)
# summoner(sumname)
