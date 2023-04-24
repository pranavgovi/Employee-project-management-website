
from flask import Flask, render_template, url_for, request, redirect,session,jsonify,json,g,Response
app = Flask(__name__,template_folder="templates")
app.secret_key = 'pranav'
from urllib.parse import urlparse, parse_qs
import pymongo
from pymongo import MongoClient
error_message=""


cluster =MongoClient("mongodb+srv://pranav292005:Pranav123@cluster0.ynepebw.mongodb.net/?retryWrites=true&w=majority")
db = cluster["employee"]

mycol=db["emp"]
mycol1=db["project"]
mycol2=db["finished_project"]



@app.route("/ret.html",methods=["GET","POST"])
def rett():
    id = session.get('previous_info')

    total = mycol.find()
    ans = mycol1.find()

    curr_proj = []
    no_ongoing = 0
    no_prev = 0

    for i in ans:
        for x in i['members']:
            if (str(id) == x):
                no_ongoing += 1
                break

    prev = mycol2.find()
    fin_proj = []
    for i in prev:
        for x in i['members']:
            if (str(id) == x):
                no_prev += 1
                break

    msg = 0
    name = ''
    total = mycol.find()
    for i in total:
        if id == i['id']:
            x = i["key"]
            ss = i['admin']
            if (ss == 0):
                type_login = 'Employee'
            else:
                type_login = 'Admin'


            msg = 1
            if i['employee_name']:
                name = i['employee_name']

            else:
                msg = 0
    if msg == 1:
        session['previous_info'] = id

    return render_template('employee.html', id=id, name=name, type_login=type_login, no_prev=no_prev,
                           no_ongoing=no_ongoing)



@app.route("/sign_out",methods=["GET","POST"])
def signout():

    return render_template("index.html",error_message='')


@app.route("/",methods=["GET","POST"])
def hello():
  if request.method =="GET":
    return render_template("index.html",error_message='')


@app.route("/xxx.html",methods=["POST"])
def new():

    id=session.get('previous_info')
    name = ''
    total = mycol.find()
    for i in total:
        if id == i['id']:

            ss = i['admin']
            if (ss == 0):
                type_login = 'Employee'
            else:
                type_login = 'Admin'
            if i['employee_name']:
                name = i['employee_name']
            ans = mycol1.find()

            curr_proj = []
            no_ongoing = 0
            no_prev = 0

            for i in ans:
                for x in i['members']:
                    if (str(id) == x):
                        no_ongoing += 1
                        break

            prev = mycol2.find()
            fin_proj = []
            for i in prev:
                for x in i['members']:
                    if (str(id) == x):
                        no_prev += 1
                        break

    return render_template("employee.html", id=id, name=name, type_login=type_login, no_prev=no_prev,
                           no_ongoing=no_ongoing)




@app.route("/index.html",methods=["POST","GET"])
def h():
    parsed_url = urlparse(request.url)
    query_params = parse_qs(parsed_url.query)

    # Get the value of a specific parameter
    param_name = 'form_name'
    form_name = query_params.get(param_name, None)
    st=''

    id = request.args.get("Employee_ID")


    session['previous_info'] = id

    print(session.get('previous_info'))



    if form_name:
        for i in form_name:
            st=i

        if st == 'form1':
            id=session.get('previous_info')
            total = mycol.find()
            ans = mycol1.find()

            curr_proj = []
            no_ongoing = 0
            no_prev = 0

            for i in ans:
                for x in i['members']:
                    if (str(id) == x):
                        no_ongoing += 1
                        break

            prev = mycol2.find()
            fin_proj = []
            for i in prev:
                for x in i['members']:
                    if (str(id) == x):
                        no_prev += 1
                        break
            id = request.args.get("Employee_ID")
            key = request.args.get("Employee_passkey")
            msg=0
            name=''
            total=mycol.find()
            for i in total:
                if id == i['id']:
                    x=i["key"]
                    ss=i['admin']
                    if(ss==0):
                        type_login='Employee'
                    else:
                        type_login='Admin'

                    if key.lower() == x.lower():
                        msg=1
                        if i['employee_name']:
                            name=i['employee_name']

                    else:
                        msg=0
            if msg==1:
                session['previous_info'] = id
                return render_template("employee.html", id=id, key=key,name=name,type_login=type_login,no_prev=no_prev,no_ongoing=no_ongoing)
            else:
                error_message="Invalid ID or password.. Try Again"
                return render_template('index.html', error_message=error_message)
        elif st =='form2':

            new_name = request.args.get("name")
            new_id=request.args.get("id")
            new_password=request.args.get("password")
            con_pass=request.args.get("password1")
            if(new_password!=con_pass):
                message="The passwords you entered do not match. Please try again."
                return render_template('sign_up.html', error=message)
            elif(len(new_password)<8):
                message="Password should be minimum of length 8 characters"
                return render_template('sign_up.html', error=message)
            else:
                cap_count=0
                special_count=0
                numeric_count=0
                for i in new_password:
                    if(i.isupper()):
                        cap_count+=1
                    elif(i.isnumeric()):
                        numeric_count+=1
                    elif(i in ['@','#','$','*']):
                        special_count+=1
                if(cap_count==0):
                    message='Password should contain atleast one capital letter'
                    return render_template('sign_up.html', error=message)
                elif(special_count==0):
                    message='Password should contain atleast one special character'
                    return render_template('sign_up.html', error=message)

                elif (numeric_count == 0):
                    message = 'Password should contain atleast one numeric character'
                    return render_template('sign_up.html', error=message)





            new_dic={
                "employee_name":new_name,
                "id":new_id,
                "key":new_password,
                "admin":0
            }
            mycol.insert_one(new_dic)

            return render_template('index.html',error_message='')
        elif st =='form3':

            new_name = request.args.get("name")
            new_id=request.args.get("id")
            new_password=request.args.get("password")
            con_pass=request.args.get("password1")
            if(new_password!=con_pass):
                message="The passwords you entered do not match. Please try again."
                return render_template('sign_up.html',error=message)

            new_dic={
                "employee_name":new_name,
                "id":new_id,
                "key":new_password,
                "admin":1
            }
            mycol.insert_one(new_dic)

            return render_template('index.html',error_message='')

        else:
            id = session.get('previous_info')

            total = mycol.find()
            ans = mycol1.find()

            curr_proj = []
            no_ongoing = 0
            no_prev = 0

            for i in ans:
                for x in i['members']:
                    if (str(id) == x):
                        no_ongoing += 1
                        break

            prev = mycol2.find()
            fin_proj = []
            for i in prev:
                for x in i['members']:
                    if (str(id) == x):
                        no_prev += 1
                        break
            id = request.args.get("Employee_ID")
            key = request.args.get("Employee_passkey")
            msg = 0
            name = ''
            total = mycol.find()
            for i in total:
                if id == i['id']:
                    x = i["key"]
                    ss = i['admin']
                    if (ss == 0):
                        type_login = 'Employee'
                    else:
                        type_login = 'Admin'

                    if key.lower() == x.lower():
                        msg = 1
                        if i['employee_name']:
                            name = i['employee_name']

                    else:
                        msg = 0
            if msg == 1:
                session['previous_info'] = id

            return render_template('employee.html', id=id,name=name, type_login=type_login,no_prev=no_prev,no_ongoing=no_ongoing)


        # Exit the program


    # mycol.insert_one({
    #     "id":id,
    #     "key":key
    # })



@app.route('/test', methods=['POST','DELETE'])
def test():
    data=request.get_json()
    x = json.dumps(data)
    result=json.loads(x)

    if request.method == 'DELETE':

        completed_project=[]
        pending_steps = result['pending_steps']
        finished_steps = result['finished_steps']
        value = result['previousProgressValue']
        members = result['members']
        id = result['id']
        proj = result['proj']
        print(len(pending_steps))
        if (len(pending_steps) == 0):
            dic1 = {
                "proj_name": proj,
                "members": members

            }
            mycol2.insert_one(dic1)
            print("before")

            mycol1.delete_one({"proj_name": proj})

        return render_template('new_proj.html')


        #result = json.loads(output) #this converts the json output to a python dictionary






    elif request.method == 'POST':
        completed_project = []

        pending_steps = result['pending_steps']
        finished_steps = result['finished_steps']
        value = result['previousProgressValue']
        proj = result['proj']

        total = mycol1.find()
        ansss = mycol1.update_one(
            {"proj_name": proj},
            {"$set": {"steps": pending_steps}}
        )
        # if proj == i['proj_name']:
        #     finished_steps= i['steps']
        if 'finished_steps' not in result:

            query = {"proj_name": proj}

            new_values = {"$set": {"finished_steps": finished_steps}}

            aa = mycol1.update_one(query, new_values)
            n1 = {"$set": {"progress": value}}
            x = mycol1.update_one(query, n1)






        else:

            query = {"proj_name": proj}
            new_values = {"$push": {"finished_steps": {"$each": finished_steps}}}

            mycol1.update_one(query, new_values)
            new_value = value

            # Define the update operation
            update = {'$set': {'progress': new_value}}

            # Use the update_one() method to update the document
            res = mycol1.update_one(query, update)

        # mycol1.insert_one(dic)
        return render_template('new_proj.html')
        # output = request.get_json()
        # result = json.loads(output)  # this converts the json output to a python dictionary

    return render_template('new_proj.html')




@app.route("/sign_up.html",methods=["POST","GET"])
def f():
    sign_up_error=""
    return render_template("sign_up.html",error=sign_up_error)

@app.route("/info.html",methods=["POST","GET"])
def information():

    id = session.get('previous_info')
    proj = request.form['button_value']
    button_value_parts = proj.split(',')
    button_label = button_value_parts[1]
    proj_name = button_value_parts[0]
    steps=[]
    total=mycol1.find()
    for i in total:
        if proj_name==i['proj_name']:
            steps=i['steps']
            members=i['members']
            tot_steps=i['total_steps']
            # Check if the "my_var" variable is present in the document
            if 'progress' in i:
                value =i['progress']

            else:
                value=0

            break

    finished_steps=[]

    pending_steps=steps
    id = session.get('previous_info')



    return render_template("info.html",tot_steps=tot_steps,value=value,id=id,proj=proj_name,steps=steps,finished_steps=finished_steps,pending_steps=pending_steps,members=members)

@app.route("/new_proj.html",methods=["POST","GET"])
def ff():

    return render_template("new_proj.html")

@app.route("/dummy.html",methods=["POST","GET"])
def ffhu():

    return render_template("dummy.html")

@app.route("/update_info.html",methods=["POST","GET"])
def up_info():

    id = session.get('previous_info')
    proj = request.form['button_value']
    button_value_parts = proj.split(',')
    button_label = button_value_parts[1]
    proj_name = button_value_parts[0]
    steps=[]
    total=mycol1.find()
    for i in total:
        if proj_name==i['proj_name']:
            pending_steps=i['steps']

    return render_template("update_info.html",id=id,proj=proj_name,pending_steps=pending_steps)




@app.route("/update.html",methods=["POST","GET"])
def update():
    id1 = session.get('previous_info')
    ans = mycol1.find()


    curr_proj = []

    for i in ans:
        if id1 in i['members']:
            curr_proj.append(i['proj_name'])

    return render_template("update.html", id=id1, curr_proj=curr_proj)




# @app.route('/test', methods=['POST'])
# def test():
#     output = request.get_json()
#     print(output) # This is the output that was stored in the JSON within the browser
#     print(type(output))
#     result = json.loads(output) #this converts the json output to a python dictionary
#     print(result) # Printing the new dictionary
#     print(type(result))#this shows the json converted as a python dictionary
#     return result
#
# @app.route("/myflaskroute", methods=["POST"])
# def my_flask_route():
#     if request.is_json:
#         data = request.get_json()
#         pending_tasks = data['array1']
#         finished_tasks = data['array2']
#         proj = data['proj']
#
#
#         id1 = session.get('previous_info')
#         ans = mycol1.find()
#         for i in ans:
#             if proj == i['proj_name']:
#                 i['steps'] = pending_tasks
#         return jsonify({'message': f'Hello from Flask! You sent: {pending_tasks}'})
#
#     else:
#         return jsonify({'status': 'error', 'message': 'Invalid content type'})

@app.route("/project_status.html",methods=["POST","GET"])
def project():


        id1 = session.get('previous_info')
        ans = mycol1.find()
        prev=mycol2.find()

        curr_proj = []
        prev_proj=[]
        for i in ans:
            if id1 in i['members']:
                curr_proj.append(i['proj_name'])
        for i in prev:
            if id1 in i['members']:
                prev_proj.append(i['proj_name'])


        return render_template("project_status.html", id=id1, curr_proj=curr_proj,prev_proj=prev_proj)
        # array1 and array2 are now Python lists containing the arrays sent from JavaScript







@app.route("/employee.html",methods=["POST","GET"])
def emp():
    if 'newproj' in request.form:
        # Form 1 was submitted
        # handle form data from Form 1

        proj=request.form.get("proj_name")
        total_members= request.form.get("no_mem")
        total_steps = request.form.get("no_step")
        member_data = []
        steps_data=[]
        for i in range(int(total_members)):
            member_data.append(request.form[f'input-{i+1}'])
        for i in range(int(total_steps)):
            steps_data.append(request.form[f'step-{i+1}'])

        new_proj={
            "proj_name":proj,
            "members":member_data,
            "steps":steps_data,
            "total_steps":total_steps
        }
        mycol1.insert_one(new_proj)
        success_message='PROJECT CREATED!!!!!! '

        id = session.get('previous_info')
        total = mycol.find()
        ans = mycol1.find()

        curr_proj = []
        no_ongoing = 0
        no_prev = 0

        for i in ans:

            for x in i['members']:
                if (str(id) == x):
                    print("heree")
                    no_ongoing += 1
                    break

        prev = mycol2.find()
        fin_proj = []
        for i in prev:
            for x in i['members']:
                if (str(id) == x):
                    no_prev += 1
                    break

        for i in total:
            if id == i['id']:
                ss = i['admin']
                x = i["key"]
                msg = 1
                if i['employee_name']:
                    name = i['employee_name']
        if (ss == 0):
            type_login = 'Employee'
        else:
            type_login = 'Admin'

        return render_template("employee.html",type_login=type_login,id=id,name=name,success_message=success_message,no_prev=no_prev,no_ongoing=no_ongoing)

    elif 'update' in request.form:
        name=''
        success_message=''
        no_of_insertions = request.form.get("no_mem")

        steps_inserted = []
        deleted_steps=[]
        proj = request.form.get('my_value')


        if(no_of_insertions):
            success_message='Project updated successfully!!!!!'
            for i in range(int(no_of_insertions)):
                steps_inserted.append(request.form[f'input-{i + 1}'])

        if request.form.getlist('steps'):
            deleted_steps = request.form.getlist('steps')
            success_message='Project updated successfully!!!!'





        id = session.get('previous_info')
        total = mycol.find()
        ans = mycol1.find()


        for i in ans:
            if i['proj_name']==proj:
                steps=i['steps']

        if len(deleted_steps)!=0:

            for value in deleted_steps:
                if value in steps:
                    steps.remove(value)
        if len(steps_inserted)!=0:
            for i in steps_inserted:
                steps.append(i)

        if len(deleted_steps)!=0 or len(steps_inserted)!=0:

            query = {"proj_name": proj}

            new_values = {"$set": {"steps": steps}}

            aa = mycol1.update_one(query, new_values)

            query1 = {"proj_name": proj}

            new = {"$set": {"total_steps": len(steps)}}

            aa1 = mycol1.update_one(query1, new)



        no_ongoing = 0
        no_prev = 0
        ans=mycol1.find()
        for i in ans:
            for x in i['members']:
                if (str(id) == x):
                    no_ongoing += 1
                    break

        prev = mycol2.find()

        for i in prev:
            for x in i['members']:
                if (str(id) == x):
                    no_prev += 1
                    break

        for i in total:
            if id == i['id']:
                ss = i['admin']
                x = i["key"]
                msg = 1
                if i['employee_name']:
                    name = i['employee_name']
        if (ss == 0):
            type_login = 'Employee'
        else:
            type_login = 'Admin'

        return render_template("employee.html", type_login=type_login, id=id, name=name,
                               success_message=success_message, no_prev=no_prev, no_ongoing=no_ongoing)


if __name__ == "__main__":
  app.run(debug=True)