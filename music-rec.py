import pandas as pd

tracks = pd.read_csv('/Users/tariqgeorges/Documents/Riq Coding/result.csv')

tracks = tracks[tracks.popularity > 70]

ids = input('Enter comma-seperated ids of your favrite songs \n sample input: 1xK1Gg9SxG8fy2Ya373oqb,1xQ6trAsedVPCdbtDAmk0c,7ytR5pFWmSjzHJIeQkgog4,079Ey5uxL04AKPQgVQwx5h \n\n\n')

ids_list = ids.strip().split(',')

favorites = tracks[tracks.id.isin(ids_list)]

cluster_numbers = list(favorites['type'])
clusters = {}
for i in cluster_numbers:
    clusters[i] = cluster_numbers.count(i)


user_favorite_cluster = [(k, v) for k, v in sorted(
    clusters.items(), key=lambda item: item[1])][0][0]

print('\nFavorite cluster:', user_favorite_cluster, '\n')

# finally get the tracks of that cluster
suggestions = tracks[tracks.type == user_favorite_cluster]

print(tracks.columns)

#Only want to output , name, uri, 


# now print the first 5 rows of the data frame having that cluster number as their type
print(suggestions.head(subset=['name','uri']))
