import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def generate_collaborative_recommendations(user_df, steam_df, usuari, top=10):
    matriu = user_df.pivot_table(index='SteamID', columns='AppID', values='Playtime (Minutes)', fill_value=0)

    if usuari not in matriu.index:
        return pd.DataFrame(columns=['name', 'genres', 'steamspy_tags', 'score'])

    esc = StandardScaler()
    mat_escalada = esc.fit_transform(matriu)

    sim_mat = cosine_similarity(mat_escalada)
    sim_df = pd.DataFrame(sim_mat, index=matriu.index, columns=matriu.index)

    similars = sim_df.loc[usuari].drop(usuari)
    jugats_similars = matriu.loc[similars.index]

    puntuacions = jugats_similars.T.dot(similars) / similars.sum()

    ja_jugats = matriu.loc[usuari]
    ja_jugats = ja_jugats[ja_jugats > 0].index

    recom = puntuacions.drop(index=ja_jugats, errors='ignore').sort_values(ascending=False)

    top_ids = recom.head(top).index
    top_scores = recom.loc[top_ids]

    res = steam_df[steam_df['appid'].isin(top_ids)][['appid', 'name', 'genres', 'steamspy_tags']].copy()
    res = res.set_index('appid')
    res['score'] = top_scores.loc[res.index]
    res = res.reset_index()

    return res.sort_values(by='score', ascending=False)
