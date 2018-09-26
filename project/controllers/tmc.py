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
    ano_f = StringField('año inicial', validators=[DataRequired()])
    mes_f = StringField('mes inicial', validators=[DataRequired()])

@app.route('/tmc', methods=['GET'])
def tmc_form_get():
    form = CreateForm(request.form)    
    return render_template('printer/tmc_form.html', form=form)
    
@app.route('/tmc', methods=['POST'])
def tmc():
    form = CreateForm(request.form)
    ano_i = form.ano_i.data
    mes_i = form.mes_i.data    
    ano_f = form.ano_f.data
    mes_f = form.mes_f.data
    
    url_req = app.config['url_short'] + 'tmc/periodo/' + ano_i + '/' + mes_i + '/' + ano_f + '/' + mes_f + app.config['apikey'] + app.config['formato']
    
    if request.method == 'POST':
        # variables para la obtencion del promedio, max y min
        iteration = 0
        total = 0        
        # listas de ploteo
        x_axis = []
        # (21)
        # Operaciones reajustables en moneda nacional 
        y_axis_21 = []
        # (22)
        # Operaciones reajustables en moneda nacional
        # De un año o más. Superiores al equivalente de 2000 unidades de fomento
        y_axis_22 = []
        # (24)
        # Operaciones reajustables en moneda nacional 
        # De un año o más. Superiores al equivalente de 2000 unidades de fomento
        y_axis_24 = []
        # (25)
        # Operaciones no reajustables en moneda nacional de menos de 90 días
        # Superiores al equivalente de 5.000 unidades de fomento        
        y_axis_25 = []
        # (26)
        # Operaciones no reajustables en moneda nacional de menos de 90 días
        # Inferiores o iguales al equivalente de 5.000 unidades de fomento
        y_axis_26 = []
        # (33)
        # Operaciones no reajustables en moneda nacional 90 días o más
        # Inferiores o iguales al equivalente de 200 unidades de fomento
        y_axis_33 = []
        # (34)
        # Operaciones no reajustables en moneda nacional 90 días o más
        # Superiores al equivalente de 5.000 unidades de fomento
        y_axis_34 = []
        # (35)
        # Operaciones no reajustables en moneda nacional 90 días o más
        # Inferiores o iguales al equivalente de 5.000 unidades de fomento y superiores al equivalente de 200 unidades de fomento
        y_axis_35 = []
        # (36)
        # Operaciones expresadas en moneda extranjera
        y_axis_36 = []
        
        # request data api sbif, formateo como json
        data = requests.get(url_req).content
        data = data.decode('utf8')
        data = json.loads(data)              
               
        for key, value in data.items():
            pass

        for i in value:                         
            valor_tmc = value[iteration]['Valor'].replace(",", ".")
            valor_tmc = float(valor_tmc)
            fecha_tmc = value[iteration]['Fecha']            
            if(value[iteration]):                                 
                x_axis.append(iteration)
            # obtener valores para plotear
            if(value[iteration]['Tipo'] == '21'):                                 
                y_axis_21.append(valor_tmc)    
            if(value[iteration]['Tipo'] == '22'):                                 
                y_axis_22.append(valor_tmc)    
            if(value[iteration]['Tipo'] == '24'):                                 
                y_axis_24.append(valor_tmc)    
            if(value[iteration]['Tipo'] == '25'):                                 
                y_axis_25.append(valor_tmc)    
            if(value[iteration]['Tipo'] == '26'):                                 
                y_axis_26.append(valor_tmc)    
            if(value[iteration]['Tipo'] == '33'):                                 
                y_axis_33.append(valor_tmc)    
            if(value[iteration]['Tipo'] == '34'):                                 
                y_axis_34.append(valor_tmc)    
            if(value[iteration]['Tipo'] == '35'):                                 
                y_axis_35.append(valor_tmc)       
            if(value[iteration]['Tipo'] == '36'):                                 
                y_axis_36.append(valor_tmc)          
            
            """ Obtener dolar total y promedio"""
            total += valor_tmc
            iteration += 1
        
        promedio = total/iteration            

        # data plot        
        def make_patch_spines_invisible(ax):
            ax.set_frame_on(True)
            ax.patch.set_visible(False)            
            for sp in ax.spines.values():
                sp.set_visible(False)
        
        fig, host = plt.subplots()
        fig.subplots_adjust(right=0.5)

        par1 = host.twinx()
        par2 = host.twinx()
        par3 = host.twinx()
        par4 = host.twinx()
        par5 = host.twinx()
        par6 = host.twinx()
        par7 = host.twinx()
        par8 = host.twinx()
        par9 = host.twinx()

        # Offset the right spine of par2.  The ticpar2.spines["right"].set_visible(True)ks and label have already been
        # placed on the right by twinx above.
        par2.spines["right"].set_position(("axes", 1.1))
        par3.spines["right"].set_position(("axes", 1.2))
        par4.spines["right"].set_position(("axes", 1.3))
        par5.spines["right"].set_position(("axes", 1.4))
        par6.spines["right"].set_position(("axes", 1.5))
        par7.spines["right"].set_position(("axes", 1.6))
        par8.spines["right"].set_position(("axes", 1.7))
        par9.spines["right"].set_position(("axes", 1.8))        
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.
        make_patch_spines_invisible(par2)
        make_patch_spines_invisible(par3)
        make_patch_spines_invisible(par4)
        make_patch_spines_invisible(par5)
        make_patch_spines_invisible(par6)
        make_patch_spines_invisible(par7)
        make_patch_spines_invisible(par8)
        make_patch_spines_invisible(par9)
        # Second, show the right spine.
        par2.spines["right"].set_visible(True)
        par3.spines["right"].set_visible(True)
        par4.spines["right"].set_visible(True)
        par5.spines["right"].set_visible(True)
        par6.spines["right"].set_visible(True)
        par7.spines["right"].set_visible(True)
        par8.spines["right"].set_visible(True)
        par9.spines["right"].set_visible(True)

        p1, = host.plot(y_axis_21, "b-", label="21")
        p2, = par1.plot(y_axis_22, "g-", label="22")
        p3, = par2.plot(y_axis_24, "r-", label="24")
        p4, = par3.plot(y_axis_25, "c-", label="25")
        p5, = par4.plot(y_axis_26, "m-", label="26")
        p6, = par5.plot(y_axis_33, "y-", label="33")
        p7, = par6.plot(y_axis_34, "k-", label="34")
        p8, = par7.plot(y_axis_35, "b-", label="35")
        p9, = par8.plot(y_axis_36, "g-", label="36")
       
        host.set_xlabel("")
        host.set_ylabel("21")
        par1.set_ylabel("22")
        par2.set_ylabel("24")
        par3.set_ylabel("25")
        par4.set_ylabel("26")
        par5.set_ylabel("33")
        par6.set_ylabel("34")
        par7.set_ylabel("35")
        par8.set_ylabel("36")

        host.yaxis.label.set_color(p1.get_color())
        par1.yaxis.label.set_color(p2.get_color())
        par2.yaxis.label.set_color(p3.get_color())
        par3.yaxis.label.set_color(p4.get_color())
        par4.yaxis.label.set_color(p5.get_color())
        par5.yaxis.label.set_color(p6.get_color())
        par6.yaxis.label.set_color(p7.get_color())
        par7.yaxis.label.set_color(p8.get_color())
        par8.yaxis.label.set_color(p9.get_color())

        tkw = dict(size=10, width=1.5)
        host.tick_params(axis='y', colors=p1.get_color(), **tkw)
        par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
        par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
        par3.tick_params(axis='y', colors=p4.get_color(), **tkw)
        par4.tick_params(axis='y', colors=p5.get_color(), **tkw)
        par5.tick_params(axis='y', colors=p6.get_color(), **tkw)
        par6.tick_params(axis='y', colors=p7.get_color(), **tkw)
        par7.tick_params(axis='y', colors=p8.get_color(), **tkw)
        par8.tick_params(axis='y', colors=p9.get_color(), **tkw)
        host.tick_params(axis='x', **tkw)

        lines = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

        host.legend(lines, [l.get_label() for l in lines])

        plt.show()
    
        return render_template('printer/index.html', **locals())
