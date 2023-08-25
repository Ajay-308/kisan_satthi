from flask import Flask , render_template,request


import pickle
import numpy as np

app = Flask(__name__)



airquality = pickle.load(open('Air_Quality.pkl','rb'))
fertilizer = pickle.load(open('Fertilizer.pkl','rb'))
crop_recommendation = pickle.load(open('croprecommendation2.pkl','rb'))
crop_trading  = pickle.load(open('crop_trading.pkl','rb'))



@app.route('/')
def main():
    return render_template('index.html')

@app.route('/croprecommendation/')
def croprecommendation():
    return render_template('crop_recommend.html')

@app.route('/fertilizer/')
def fertilizer():
    return render_template('fertilizer.html')

@app.route('/croptrade/')
def croptrade():
    return render_template('Trading.html')

@app.route('/airquality/')
def airquality():
    return render_template('airquality.html')



@app.route('/predict_airquality',methods=['GET','POST'])
def predictairquality():
    if request.method=='GET':
        return render_template('airquality.html')
    else:
        soi = float(request.form['so2_individual_pollutant_index'])
        noi = float(request.form['no2_individual_pollutant_index'])
        rpi = float(request.form['rspm_individual_pollutant_index'])
        spmi = float(request.form['spm_individual_pollutant_index'])
        sample_data = [[soi,noi,rpi,spmi]]
        prediction = airquality.predict(sample_data)

        return render_template('airquality.html',output = prediction)

@app.route('/predict_fertilizer',methods=['GET','POST'])
def predictfertilizer():
    if request.method=='GET':
        return render_template('fertilizer.html')
    else:
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        moisture = float(request.form['Moisture'])
        soil_type = request.form['Soil_Type']
        crop_type = request.form['Crop_Type']
        nitrogen = float(request.form['Nitrogen'])
        potassium = float(request.form['Potassium'])
        phosphorus = float(request.form['Phosphorus'])

        if soil_type == 'Black':
            soil_type = 0
        elif soil_type == 'Clayey':
            soil_type = 1
        elif soil_type == 'Loamy':
            soil_type = 2
        elif soil_type == 'Red':
            soil_type = 3
        else:
            soil_type=4

        if crop_type == 'Barley':
            crop_type=0
        if crop_type == 'Cotton':
            crop_type=1
        if crop_type == 'Ground Nuts':
            crop_type=2
        if crop_type == 'Maize':
            crop_type=3
        if crop_type == 'Millets':
            crop_type=4
        if crop_type == 'Oil seeds':
            crop_type=5
        if crop_type == 'Paddy':
            crop_type=6
        if crop_type == 'Pulses':
            crop_type=7
        if crop_type == 'Sugarcane':
            crop_type=8
        if crop_type == 'Tobacco':
            crop_type=9
        else:
            crop_type=10

        fertilizer_data = [[temp,humidity,moisture,soil_type,
                            crop_type,nitrogen,
                            potassium,phosphorus]]
        fertilizer_prediction = fertilizer.predict(fertilizer_data)
        if fertilizer_prediction == 0:
            fertilizer_prediction = '10-26-26'
        if fertilizer_prediction == 1:
            fertilizer_prediction = '14-35-14'
        if fertilizer_prediction == 2:
            fertilizer_prediction = '17-17-17'
        if fertilizer_prediction == 3:
            fertilizer_prediction = '20-20'
        if fertilizer_prediction == 4:
            fertilizer_prediction = '28-28'
        if fertilizer_prediction == 5:
            fertilizer_prediction='DAP'
        else:
            fertilizer_prediction = 'Urea'
        

        return render_template('fertilizer.html',fertilizer_output = fertilizer_prediction)
    
@app.route('/predict_crop',methods=['GET','POST'])
def predictcrop():
    if request.method=='GET':
        return render_template('crop_recommend.html')
    else:
        nitrogen = float(request.form['Nitrogen'])
        phosphorus = float(request.form['Phosphorus'])
        potassium = float(request.form['Potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])
        crop_data = [[nitrogen,phosphorus,potassium,temperature,humidity,ph,rainfall]]
        crop_mapping = {
            0: 'apple', 1: 'banana', 2: 'blackgram', 3: 'chickpea', 4: 'coconut',
            5: 'coffee', 6: 'cotton', 7: 'grapes', 8: 'jute', 9: 'kidneybeans',
            10: 'lentil', 11: 'maize', 12: 'mango', 13: 'mothbeans', 14: 'mungbean',
            15: 'muskmelon', 16: 'orange', 17: 'papaya', 18: 'pigeonpeas',
            19: 'pomegranate', 20: 'rice', 21: 'watermelon'
}
        predictcrop =crop_recommendation.predict(crop_data)
        if predictcrop[0] in crop_mapping:
            predictcrop = crop_mapping[predictcrop[0]]
        else:
            predictcrop = "Unknown"
        return render_template('crop_recommend.html',crop_output = predictcrop)
    
@app.route('/predict_tradingvalue',methods=['GET','POST'])
def predicttradingvalue():
    if request.method=='GET':
        return render_template('trading.html')
    else:
        element = float(request.form['Element'])
        item = float(request.form['Item'])
        year = float(request.form['Year'])
        Unit = float(request.form['Unit'])
        trading_data = [[element,item,year,Unit]]
        predicttradingvalue = crop_trading(trading_data)
        return render_template('trading.html',trading_output = predicttradingvalue)

if __name__ == "__main__":
    app.run(debug=True, port=5500) 