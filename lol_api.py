from requests import HTTPError
from riotwatcher import RiotWatcher
import config
import time

watcher = RiotWatcher(config.riot_token)

my_region = 'ru'
sumname = "Busido"
season = 9

def summoner(sumname):
    try:
        me = watcher.summoner.by_name(my_region, sumname)
        return str(me['id'])
    except HTTPError:
        print('Summoner not found')
        return 0


def icons(sumname):
    icon = watcher.summoner.by_name(my_region, sumname)
    icon = str(icon['profileIconId'])
    return "http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/{}.png".format(icon)


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


def get_kda(sumname, season):
    champs = []
    account = watcher.summoner.by_name(my_region, sumname)['accountId']
    ranked_matches = watcher.match.matchlist_by_account(my_region, account, season=int(season))
    if ranked_matches['matches']:
        for match in ranked_matches['matches']:
            champ_id = match['champion']
            if champ_id not in champs:
                champs.append(champ_id)

        # for game in ranked_matches['gameId']:
        #     kills = 0
        #     assists = 0
        #     deaths = 0

        # stats = watcher.match.by_id(my_region, game)
    print(champs)
    champ_names = []
    for champ in champs:
        try:
            champ_name = watcher.static_data.champion(my_region, int(champ), locale="ru_RU")['name']
            champ_names.append(champ_name)
            time.sleep(1)
        except HTTPError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.')
                print('this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            else:
                raise
    print(champ_names)


def get_kda20(sumname):
    account = watcher.summoner.by_name(my_region, sumname)['accountId']
    ranked_matches = watcher.match.matchlist_by_account_recent(my_region, account)
    print(ranked_matches)
    kills = 0
    assists = 0
    deaths = 0
    for match in ranked_matches['matches']:
        stats = watcher.match.by_id(my_region, match['gameId'])
        #kills += stats


get_kda20(sumname)
# icons()
# get_runes(sumname)
# summoner(sumname)
