from flask import Flask, request, render_template
import pandas as pd
import def_diabetic
import def_glutenfree
import def_keto
import def_cholesterol
import def_sodium
import def_vegan
import def_vegetarian

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('form_index.html')


@app.route('/classify', methods=['POST', 'GET'])
def classify_type():
    global diet_types, prediction
    try:
        if request.method == 'POST':
            text = request.form['text']
            diet_types = request.form['diet_types']

            if diet_types == "diabetic":
                prediction = def_diabetic.get_similar_diabetic(text)
            elif diet_types == "gluten_free":
                prediction = def_glutenfree.get_similar_glutenfree(text)
            elif diet_types == "ketogenic":
                prediction = def_keto.get_similar_keto(text)
            elif diet_types == "vegetarian":
                prediction = def_vegetarian.get_similar_vegetarian(text)
            elif diet_types == "vegan":
                prediction = def_vegan.get_similar_vegan(text)
            elif diet_types == "low_sodium":
                prediction = def_sodium.get_similar_lowsodium(text)
            elif diet_types == "low_cholesterol":
                prediction = def_cholesterol.get_similar_lowcholesterol(text)

            headings = ('Food Name', 'Ingredients', 'Recipe', 'Time (min)', 'Nutrition Facts', 'Review')
            data = tuple(prediction.values)
            #print(data)

            return render_template('result_rec.html', headings=headings, data=data)

        else:
            render_template('result_rec.html', hata='Formdan veri gelmedi')
    except Exception as e:
        print(e)
        return e

@app.route('/reviews', methods=['POST', 'GET'])
def reviews_df():
    if request.method == 'POST':
        datas = request.form
        print('VERILER: ', datas['veri'])

        print('reviews are here')
        if diet_types == "gluten_free":
            prediction2 = def_glutenfree.reviews_all(datas['veri'].rstrip())
        elif diet_types == "ketogenic":
            prediction2 = def_keto.reviews_all(datas['veri'].rstrip())
        elif diet_types == "vegetarian":
            prediction2 = def_vegetarian.reviews_all(datas['veri'].rstrip())
        elif diet_types == "vegan":
            prediction2 = def_vegan.reviews_all(datas['veri'].rstrip())
        elif diet_types == "low_sodium":
            prediction2 = def_sodium.reviews_all(datas['veri'].rstrip())
        elif diet_types == "low_cholesterol":
            prediction2 = def_cholesterol.reviews_all(datas['veri'].rstrip())
        elif diet_types == "diabetic":
            prediction2 = def_diabetic.reviews_all(datas['veri'].rstrip())

        #data2 = tuple(prediction2.values)
        data2 = str(prediction2.values)
        #print(data2)


        #return render_template('reviews.html', headings='Reviews', data=data2)
        return data2


@app.route('/ingredients', methods=['POST', 'GET'])
def ingredients():
    print('ingredients are here!')
    if request.method == 'POST':
        data = request.form
        print('VERILER: ', data['veri'])

        print('ingredients are here')
        if diet_types == "gluten_free":
            prediction_ing = def_glutenfree.ingredients(data['veri'].rstrip())
        elif diet_types == "ketogenic":
            prediction_ing = def_keto.ingredients(data['veri'].rstrip())
        elif diet_types == "vegetarian":
            prediction_ing = def_vegetarian.ingredients(data['veri'].rstrip())
        elif diet_types == "vegan":
            prediction_ing = def_vegan.ingredients(data['veri'].rstrip())
        elif diet_types == "low_sodium":
            prediction_ing = def_sodium.ingredients(data['veri'].rstrip())
        elif diet_types == "low_cholesterol":
            prediction_ing = def_cholesterol.ingredients(data['veri'].rstrip())
        elif diet_types == "diabetic":
            prediction_ing = def_diabetic.ingredients(data['veri'].rstrip())


        data_ing = str(prediction_ing.values)
        ingredients_list = ' '.join(data_ing.split(","))

        grocery_list = pd.read_csv('grocery_list.csv')

        amazon_list = []
        for i in grocery_list.ingredients:
            if i in ingredients_list and not i in amazon_list:
                amazon_list.append(i)
                final_list = '\n'.join(amazon_list)

        return final_list

if __name__ == '__main__':
    app.run()
