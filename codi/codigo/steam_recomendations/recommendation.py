from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def generate_recommendations(user_df, cataleg, top=10):
    cataleg['text'] = cataleg[['genres', 'steamspy_tags']].fillna('').agg(' '.join, axis=1)

    tfidf = TfidfVectorizer(stop_words='english')
    matriu = tfidf.fit_transform(cataleg['text'])

    jugats = cataleg[cataleg['appid'].isin(user_df['AppID'])]
    idxs = jugats.index

    temps = user_df.set_index('AppID').loc[jugats['appid'], 'Playtime (Minutes)'].values
    pesos = np.log1p(temps)
    pesos = pesos / pesos.sum()

    perf = pesos @ matriu[idxs]
    perf = perf.reshape(1, -1)

    sim = cosine_similarity(perf, matriu).flatten()
    cataleg['sim'] = sim

    recom = cataleg[~cataleg['appid'].isin(user_df['AppID'])]

    recom = recom.sort_values(by='sim', ascending=False).head(top)

    return recom[['name', 'genres', 'steamspy_tags', 'sim']]
