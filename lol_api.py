from riotwatcher import RiotWatcher
import config

watcher = RiotWatcher(config.riot_token)

my_region = 'ru'


def summoner(sumname):
    me = watcher.summoner.by_name(my_region, sumname)
    level = str(me['summonerLevel'])
    return str(me['id'])


def ranked(sumname):
    my_ranked_stats = watcher.league.positions_by_summoner(my_region, summoner(sumname))
    return(my_ranked_stats[0])

# ranked()