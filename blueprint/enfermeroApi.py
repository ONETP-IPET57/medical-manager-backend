# Import libraries
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request

# Import moduls
from blueprint.helpers.queryEnfermero import qEnfermero

# Init blueprint
enfermeroApi = Blueprint('enfermeroApi', __name__, template_folder='app/templates')

# Routes of Efermero Api

# Route general
@enfermeroApi.route('/api/enfermeros', methods = ['GET','POST'])
def emfermeros():
    
    # Fetch all enfermeros
    if request.method == 'GET':
        
        colum = []
        data = []
        for x in request.args:
            colum.append(x)
            data.append(request.args.get(x))
        dataEnfermeros = qEnfermero.traer_enfermeros(colum,data)
        
        jsonEnfermero = []
        
        for data in dataEnfermeros:
            jsonEnfermero.append({
                'dni_enfermero': data[0],
                'nombre': data[1],
                'apellido': data[2],
                'sexo': data[3],
                'telefono': data[4],
                'fecha_nac': data[5],
                'estado': data[6]
            })
            
        return jsonify(jsonEnfermero), 200
    
    # Insert new enfermero
    if request.method == 'POST':
        dni = request.json.get('dni_enfermero',None)
        nombre = request.json.get('nombre', None)
        apellido = request.json.get('apellido', None)
        sexo = request.json.get('sexo', None)
        telefono = request.json.get('telefono', None)
        fecha_nac = request.json.get('fecha_nac', None)
        estado = request.json.get('estado', None)
        
        return jsonify(qEnfermero.insertar_enfermero(dni,nombre, apellido,sexo, telefono,fecha_nac,estado)), 200

# Route protected
@enfermeroApi.route('/api/enfermeros/<dni>', methods=['POST','GET','DELETE'])
@jwt_required(locations=['cookies','headers'])
def emfermero(dni):
    
    # Fetch one enfermero
    if request.method == 'GET':
        data = qEnfermero.trar_un_enfermero(dni)
        if data != None:
            return jsonify({
                'dni_enfermero': data[0],
                'nombre': data[1],
                'apellido': data[2],
                'sexo': data[3],
                'telefono': data[4],
                'fecha_nac': data[5],
                'estado': data[6]
            }), 200
        else:
            return jsonify({
                'msg': 'Not Found'
            }) ,404
            
    # Verifies the role is Administrador
    if get_jwt_identity()['role'] == 'administrador':
        
        # Edit one efermero
        if request.method == 'POST':
            dni = dni
            nombre = request.json.get('nombre', None)
            apellido = request.json.get('apellido', None)
            sexo = request.json.get('sexo', None)
            telefono = request.json.get('telefono', None)
            fecha_nac = request.json.get('fecha_nac', None)
            estado = request.json.get('estado', None)
            
            return jsonify(qEnfermero.editar_enfermero(dni,nombre, apellido,sexo, telefono, fecha_nac, estado)), 200
            
        if request.method == 'DELETE':
            return jsonify(qEnfermero.borrar_enfermero(dni)), 200
        
        
    else:
        return jsonify({'msg': 'No autorizado'}), 403
    