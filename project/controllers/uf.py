from project import app
from flask import render_template, request
import requests
import json
# plot libs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# form libs
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class CreateForm(FlaskForm):
    ano_i = StringField('año inicial', validators=[DataRequired()])
    ano_f = StringField('año final', validators=[DataRequired()])

@app.route('/uf', methods=['GET'])
def uf_form_get():
    form = CreateForm(request.form)    
    return render_template('printer/uf_form.html', form=form)

@app.route('/uf', methods=['POST'])
def uf_form_post():
    form = CreateForm(request.form)
    ano_i = form.ano_i.data
    ano_f = form.ano_f.data
    url_req = app.config['url_short'] + 'uf/periodo/' + ano_i + '/' + ano_f + app.config['apikey'] + app.config['formato']
    
    if request.method == 'POST':
        # variables para la obtencion del promedio, max y min
        iteration = 0
        total = 0
        data_max = 0
        data_min = 100000
        valor_dolar = 0.0
        # listas de ploteo
        x_axis = []
        y_axis = []
        
        # request data api sbif, formateo como json
        data = requests.get(url_req).content
        data = data.decode('utf8')
        data = json.loads(data)     
        
        for key, value in data.items():
            pass

        for i in value:    
            valor_uf = value[iteration]['Valor'].replace(".", "")
            valor_uf = float(valor_uf.replace(",", "."))

            # obtener valors para plotear
            x_axis.append(iteration)
            y_axis.append(valor_uf)

            """ Obtener dolar máximo"""
            if(valor_uf > data_max):
                data_max = valor_uf
            """ Obtener dolar mínimo"""
            if(valor_uf < data_min):
                data_min = valor_uf
            """ Obtener dolar total y promedio"""
            total += valor_uf
            iteration += 1
        
        promedio = total/iteration
        
        # data plot        
        df=pd.DataFrame({'x': x_axis, 'y': y_axis })
        plt.plot( 'x', 'y', data=df, color='skyblue')
        plt.show()

        return render_template('printer/index.html', **locals())
