# Cuttlefish CMDB
# Configuration Management Database leveraging Neo4j

#=======#
# LEGAL #
#=======#

# Copyright (C) 2016 Brandon Tsao
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



#=========#
# MODULES #
#=========#

from flask import Flask, render_template, url_for, request, redirect
from py2neo import Graph
import os

#======#
# MAIN #
#======#

app = Flask(__name__)

#database connect

graph = Graph(os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474'),bolt=False)

#print(graph.neo4j_version)
#graph = Graph(password="origami abase squander costive")

#==================#
# GLOBAL FUNCTIONS
#==================#


#========#
# ROUTES #
#========#


#index
@app.route('/')
def index():

    data = graph.data("MATCH (b:Person)-[:OWNS]->(a:Asset) RETURN a AS asset, b AS person, id(a) AS uid, id(b) as pid")

    return render_template("index.html",data=data)

#add new assets / items
@app.route('/api/add/asset', methods=['POST'])
def assetAdd():

    #localaize data
    uid = request.form['uid']
    model = request.form['model']
    make = request.form['make']
    serial = request.form['serial']
    ip = request.form['ip']
    mac = request.form['mac']
    date_issued = request.form['date_issued']
    date_renewel = request.form['date_renewel']
    condition = request.form['condition']
    owner = request.form['owner']
    location = request.form['location']

    statement = """MERGE (asset:Asset {
                    uid:{uid},
                    model:{model},
                    make:{make},
                    serial:{serial},
                    ip:{ip},
                    mac:{mac},
                    date_issued:{date_issued},
                    date_renewel:{date_renewel},
                    condition:{condition},
                    location:{location}
                    })

                MERGE (owner:Person {name:{owner}})
                MERGE (owner)-[:OWNS]->(asset)"""

    graph.run(statement,
                uid=uid,
                model=model,
                make=make,
                serial=serial,
                ip=ip,
                mac=mac,
                date_issued=date_issued,
                date_renewel=date_renewel,
                condition=condition,
                location=location,
                owner=owner)

    return redirect("/")

# GET
@app.route('/api/return/person/<person>',methods=['GET'])
def returnPerson(person):

    statement = "MATCH (a:Person {name:{person}}) RETURN a AS person"
    data = graph.data(statement,person=person)[0]['person']

    return str(data)

@app.route('/api/return/asset/<asset>',methods=['GET'])
def returnAsset(asset):

    statement = "MATCH (a:Asset {model:{asset}}) RETURN a AS asset"
    data = graph.data(statement,asset=asset)[0]['asset']

    return str(data)

@app.route('/api/update/asset/',methods=['POST'])
def assetUpdate():

    #locallize data
    uid = request.form['uid']
    model = request.form['model']
    make = request.form['make']
    serial = request.form['serial']
    ip = request.form['ip']
    mac = request.form['mac']
    date_issued = request.form['date_issued']
    date_renewel = request.form['date_renewel']
    condition = request.form['condition']
    owner = request.form['owner']
    location = request.form['location']

    statement = """MATCH (asset:Asset {uid:{uid}})
                SET asset.model={model}
                SET asset.make={make}
                SET asset.serial={serial}
                SET asset.ip={ip}
                SET asset.mac={mac}
                SET asset.date_issued={date_issued}
                SET asset.date_renewel={date_renewel}
                SET asset.condition={condition}
                SET asset.location={location}
                """

    graph.run(statement,
                uid=uid,
                model=model,
                make=make,
                serial=serial,
                ip=ip,
                mac=mac,
                date_issued=date_issued,
                date_renewel=date_renewel,
                condition=condition,
                location=location)

    return redirect("/")

#delete
@app.route('/api/delete/asset/<int:uid>',methods=['GET'])
def assetDeleteByUID(uid):

    statement = "MATCH (asset:Asset) WHERE id(asset)={uid} DETACH DELETE asset"
    graph.run(statement, uid=uid)

    return redirect("/")


#=====#
# RUN #
#=====#

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=(int(os.environ.get('PORT', 33507))))
    app.run()
