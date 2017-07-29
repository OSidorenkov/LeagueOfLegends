from riotwatcher import RiotWatcher
import config

watcher = RiotWatcher(config.riot_token)

my_region = 'ru'
sumname = 'Barichpock'


def summoner(sumname):
    me = watcher.summoner.by_name(my_region, sumname)
    level = str(me['summonerLevel'])
    return str(me['id'])


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


ranked(sumname)
