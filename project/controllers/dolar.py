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
      mes_i = StringField('mes inicial', validators=[DataRequired()])
      dia_i = StringField('dia inicial', validators=[DataRequired()])
      ano_f = StringField('año inicial', validators=[DataRequired()])
      mes_f = StringField('mes inicial', validators=[DataRequired()])
      dia_f = StringField('dia inicial', validators=[DataRequired()])

@app.route('/dolar', methods=['GET'])
def dolar_form_get():
    form = CreateForm(request.form)    
    return render_template('printer/dolar_form.html', form=form)
    
@app.route('/dolar', methods=['POST'])
def dolar_form_post():
    form = CreateForm(request.form)
    ano_i = form.ano_i.data
    mes_i = form.mes_i.data
    dia_i = form.dia_i.data
    ano_f = form.ano_f.data
    mes_f = form.mes_f.data
    dia_f = form.dia_f.data
    url_req = app.config['url_short'] + 'dolar/periodo/' + ano_i + '/' + mes_i + '/dias_i/' + dia_i + '/' + ano_f + '/' + mes_f + '/dias_f/' + dia_f + app.config['apikey'] + app.config['formato']
    
    if request.method == 'POST':
        # variables para la obtencion del promedio, max y min
        iteration = 0
        total = 0
        data_max = 0
        data_min = 10000        
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
            valor_dolar = value[iteration]['Valor'].replace(",", ".")
            valor_dolar = float(valor_dolar)
            fecha_dolar = value[iteration]['Fecha']            

            # obtener valors para plotear
            x_axis.append(iteration)
            y_axis.append(valor_dolar)
        
            """ Obtener dolar máximo"""
            if(valor_dolar > data_max):
                data_max = valor_dolar
            """ Obtener dolar mínimo"""
            if(valor_dolar < data_min):
                data_min = valor_dolar
            """ Obtener dolar total y promedio"""
            total += valor_dolar
            iteration += 1
        
        promedio = total/iteration            

        # data plot        
        df=pd.DataFrame({'x': x_axis, 'y': y_axis })
        plt.plot( 'x', 'y', data=df, color='skyblue')
        plt.show()
        
        return render_template('printer/index.html', **locals())
