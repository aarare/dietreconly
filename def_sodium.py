def get_similar_lowsodium(foods):
    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from psycopg2 import connect

    global df_output, df_output2

    '''params = {
        'host': 'ec2-52-72-56-59.compute-1.amazonaws.com',
        'user': 'klcuhixhvmvqdq',
        'port': 5432}
    connection = connect(**params, dbname='dd1grlpur41kha',
                         password="4afac244f4c208c38cf5de56328a2a586ee0962d86d3b82aa0d71df0d8bc1556")

    sodium = pd.read_sql("select * from sodium_similar", connection)'''

    sodium = pd.read_csv('sodiumyeni.csv', index_col=0, sep = ";")

    if len(sodium[sodium['ingredients_new'].str.contains(foods.lower())]) != 0:  # Eğer ingredientsta yoksa yemek ismine bak
        filtered_df = sodium[sodium['ingredients_new'].str.contains(foods.lower())]
    else:
        filtered_df = sodium[sodium['food_name'].str.lower().str.contains(foods.lower())]

    df_wide = pd.pivot_table(filtered_df, values=["stars"],
                             index=["food_name", "users"],
                             aggfunc=np.mean).unstack()

    df_wide = df_wide.fillna(0)
    try:
        dists = cosine_similarity(df_wide)
        dists = pd.DataFrame(dists, columns=df_wide.index)
        dists.index = dists.columns

        foods_summed = dists.apply(lambda row: np.sum(row), axis=1)
        foods_summed = foods_summed.sort_values(ascending=False)
        ranked_foods = foods_summed.index.tolist()

        # print(ranked_foods)

        df_output = pd.DataFrame(
            columns=['food_name', 'ingredients', 'recipe', 'total_time_new', 'nutrition', 'reviews'])

        for j in ranked_foods:
            for i in sodium["food_name"]:
                if j == i:
                    df_output = pd.concat(
                        [df_output, sodium[sodium["food_name"] == i].loc[:, ['food_name', 'ingredients', 'recipe',
                                                                             'total_time_new', 'nutrition', 'reviews']]])
        # df_review = df_output.drop_duplicates(subset="reviews_new")
        df_output2 = df_output.drop_duplicates(subset="food_name")
        df_output2 = df_output2.iloc[:3, :]

        return df_output2


    except ValueError:
        print("Oops, misspelled the word. Please check!")

def reviews_all(food):
    import pandas as pd
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_colwidth', 199)

    df_review = df_output.groupby("food_name")["reviews"]
    df_review = pd.DataFrame(df_review, columns=['Food_Name', 'Reviews'])
    df_review = df_review.set_index('Food_Name')

    return df_review.T[food]

def ingredients(food):
    import pandas as pd
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_colwidth', 199)

    df_ing = df_output2.groupby("food_name")["ingredients"]
    df_ing = pd.DataFrame(df_ing, columns=['Food_Name', 'Ingredients'])
    df_ing = df_ing.set_index('Food_Name')

    return df_ing.T[food]