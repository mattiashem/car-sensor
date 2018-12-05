# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Blueprint, redirect, render_template, request, url_for
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import datetime


crud = Blueprint('crud', __name__)

cred = credentials.Certificate('eu1-kubernetes-169431998c5e.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


# [START list]
@crud.route("/")
def list():
    print("Show books")
    users_ref = db.collection(u'users')
    docs = users_ref.get()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    return render_template(
            "list.html")
# [END list]



# [START add]
'''
curl -v -XPOST http://localhost:8080/books/saldo --header "Content-Type: application/json" --data '{"airport":"arlanda","saldo":"5"}'

'''

@crud.route('/saldo', methods=['POST'])
def add():
    if request.method == 'POST':
        print('Adding saldo to db')
        content = request.get_json(silent=True)
        airport="non"
        for key in content:
            if key == "airport":
                airport=content[key]
            print(content[key])
        content['timestamp']=datetime.datetime.now()
        doc_ref = db.collection(u'saldo').document(airport+"_"+str(datetime.datetime.now()))
        doc_ref.set(content
            )

    return render_template("form.html")
# [END add]
# [START add]
'''

curl -v -XPOST http://localhost:8080/books/action --header "Content-Type: application/json" --data '{"airport":"arlanda","run":"name","data":{"temp":"34","brushlenght":"20","power":"300"}}'

'''



@crud.route('/action', methods=['POST'])
def action():
    if request.method == 'POST':
        print('Action log')
        content = request.get_json(silent=True)
        airport="non"
        for key in content:
            if key == "airport":
                airport=content[key]
            print(content[key])
        content['timestamp']=datetime.datetime.now()
        doc_ref = db.collection(u'action').document(airport+"_"+str(datetime.datetime.now()))
        doc_ref.set(content
            )

    return render_template("form.html")

@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)



