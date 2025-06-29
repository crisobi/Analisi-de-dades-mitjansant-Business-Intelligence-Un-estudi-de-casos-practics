import os
import pandas as pd
from load_data import load_user_data, load_steam_data
from recommendation import *
from collaborative import *

def normalitza(col):
    min_v = col.min()
    max_v = col.max()
    if max_v == min_v:
        return col.copy()
    return (col - min_v) / (max_v - min_v)

def main():
    usuari_id = 76561198831548361  

    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Steam'))
    arxiu_usuaris = os.path.join(base, 'steam_games.csv')
    arxiu_jocs = os.path.join(base, 'steam_database.csv')

    df_usuaris = load_user_data(arxiu_usuaris)
    df_jocs = load_steam_data(arxiu_jocs)

    jocs_usuari = df_usuaris[df_usuaris['SteamID'] == usuari_id]

    recs_contingut = generate_recommendations(jocs_usuari, df_jocs)
    print(f"\n Recomanacions per contingut per {usuari_id}:")
    print(recs_contingut)

    recs_colab = generate_collaborative_recommendations(df_usuaris, df_jocs, usuari_id)
    print(f"\n Recomanacions col·laboratives per {usuari_id}:")
    print(recs_colab)

    recs_contingut['sim_norm'] = normalitza(recs_contingut['sim'])
    recs_colab['score_norm'] = normalitza(recs_colab['score'])

    if 'appid' not in recs_contingut.columns:
        recs_contingut = recs_contingut.merge(df_jocs[['name', 'appid']], on='name', how='left')

    part1 = recs_contingut[['appid', 'name', 'genres', 'steamspy_tags', 'sim_norm']].rename(columns={'sim_norm': 'score'})
    part2 = recs_colab[['appid', 'name', 'genres', 'steamspy_tags', 'score_norm']].rename(columns={'score_norm': 'score'})

    tot = pd.concat([part1, part2])
    hibrid = tot.groupby(['appid', 'name', 'genres', 'steamspy_tags'], as_index=False)['score'].mean()
    top10 = hibrid.sort_values(by='score', ascending=False).head(10)

    print(f"\n Recomanacions híbrides per {usuari_id}:")
    print(top10)

if __name__ == '__main__':
    main()
