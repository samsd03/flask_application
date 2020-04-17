import datetime
import os
import sys
from flask_mail import Mail, Message
from flask import Flask,jsonify, request
from flask_restful import Resource, Api
from celery import Celery
from flask_sqlalchemy import SQLAlchemy


# Flask App initialization
app = Flask(__name__)
api = Api(app)

################### Email Setup ##################################
app.config.update(
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = os.environ.get('user_email'),
	MAIL_PASSWORD = os.environ.get('email_password')
	)

mail = Mail(app)


#################### Database #####################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SentEmailDetails.sqlite3'
db = SQLAlchemy(app)

class SentEmailDetails(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    body = db.Column(db.String(5000))
    event_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(100))   


#################### Celery Settings #######################
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='amqp://'
)
celery = make_celery(app)


###################### Celery Task #################################

@celery.task(name='Email')
def background_process(email, body):
    try:
        status = SendEmail(email,body)        
        details = SentEmailDetails(email=email,body=body,status=status)
        db.session.add(details)
        db.session.commit()        
    except Exception as e:
        print(e)
        print("line number of error {}".format(sys.exc_info()[-1].tb_lineno))

def SendEmail(email, body):
    status = "failure"
    try:
        subject = "Sending Email through Flask and Celery"
        sender_email = os.environ.get('user_email')
        receiver_email = [email]
        msg = Message(subject,sender=sender_email,recipients=receiver_email)
        msg.body = body           
        mail.send(msg)        
        status = "success"
    except Exception as e:
        print(e)    
        status = "failure"

    return status

####################### Main Logic Part  #############################
class EmailProcess(Resource):
    
    def __init__(self):
        self.response = {'is_success':False,'code':404,'message':'','data':''}

    def get(self):
        try:
            data = request.args
            filter_email = data.get('email')
            filter_status = data.get('status')
            filter_start_time = data.get('start_timestamp')
            filter_end_time = data.get('end_timestamp')

            details_obj = SentEmailDetails.query.filter_by()
            if filter_email:
                details_obj = details_obj.filter_by(email=filter_email)
            if filter_status:
                details_obj = details_obj.filter_by(status=filter_status)
            if filter_start_time:
                details_obj = details_obj.filter(SentEmailDetails.event_time >=filter_start_time)
            if filter_end_time:
                details_obj = details_obj.filter(SentEmailDetails.event_time <=filter_end_time)

            response_data = []
            for obj in details_obj:
                email = obj.email
                body = obj.body
                event_time = obj.event_time
                status = obj.status
                response_data.append({'email':email,'body':body,'event_time':event_time,'status':status})
            self.response.update({'is_success':True,'code':200,'message':'Success','data':response_data})
        except Exception as e:
            print(e)
            print("line number of error {}".format(sys.exc_info()[-1].tb_lineno))
            self.response.update({'message':'Some Error Occured'})

        return jsonify(self.response)

    def post(self):
        try:
            data = request.get_json()
            email = data['email']
            body = data['body']
            result = background_process.delay(email,body)                     
            self.response.update({'is_success':True,'code':200,'message':'Process Initiated'})
        except Exception as e:
            print(e)
            print("line number of error {}".format(sys.exc_info()[-1].tb_lineno))
            self.response.update({'message':'Some Error Occured'})

        return jsonify(self.response)       

api.add_resource(EmailProcess, '/')

if __name__ == '__main__':
    app.run(debug=True)