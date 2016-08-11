# -*- coding: utf-8 -*-
import json  # or `import simplejson as json` if on Python < 2.6
import os
import sys
import logging


from bottle import Bottle, run
from bottle import static_file
from bottle import get, post, request, response, redirect  # or route
from beaker.middleware import SessionMiddleware

import smartClient
from smartClient import SessionManager, ReplyClick
#from smartClient import HTML5
#from smartClient import VerticalLayout, HorizontalLayout, KeyboardManager, ReplyClick, ActionUrl, Validator
#from smartClient import Label, DateField, EditField, CheckBox, RadioGroup, SelectField, PasswordField, Button, Link
#from smartClient import TextArea, Header, Spacer, RichEditor, ListGrid, DataSource, FileUpload, Window, ViewLoader
#from smartClient import SectionStack, MainMenu, MenuLink

from htmlPages import loginPage, calculator, examples, label

# SQLAlchemy as the ORM of choice
# alembic for handling database migrations


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 60*60, # 60s * 60m = 1 h
    'session.data_dir': './data',
    'session.auto': True
}
app = Bottle()
appWS = SessionMiddleware(app, session_opts)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

#import projectConfig
logging.debug('smartClient.SC_ROOT_PATH --->>> ' + smartClient.SC_ROOT_PATH)


def getClientInfo(request):
    idSession = ''
    remoteCheck = ''
    listId = str(request.get('HTTP_COOKIE')).split(';')
    for item in listId:
        if item.startswith('beaker.session.id'):
            idSession = item[18:]
        if item.startswith(' beaker.session.id'):
            idSession = item[19:]

        if item.startswith('remoteCheck'):
            remoteCheck = item[12:]
        if item.startswith(' remoteCheck'):
            remoteCheck = item[13:]

    clientInfo = {}
    clientInfo['user'] = str(request.get('beaker.session').get('remoteUser'))
    clientInfo['ip'] = str(request.get('REMOTE_ADDR'))
    clientInfo['session'] = str(idSession)
    clientInfo['browser'] = str(request.get('HTTP_USER_AGENT'))
    clientInfo['remoteCheck'] = remoteCheck

    logging.debug(str(clientInfo))
    logging.debug('')

    return clientInfo


@app.route('/')
def root():
    logging.debug('***[ / ]***************************************')
    clientInfo = getClientInfo(request)

    clientSession = request.environ.get('beaker.session')
    sm = SessionManager(clientSession, clientInfo=clientInfo)
    page = sm.getPage()
    page.clearSession()
    page.addComponent(loginPage(page))

    response.body = page.getMainPage()

    # Imposto la sessione client
    page.updateSession()
    clientSession.save()

    return response


@app.route('/main')
def main():
    logging.debug('***[ /main ]***************************************')
    clientInfo = getClientInfo(request)

    clientSession = request.environ.get('beaker.session')
    sm = SessionManager(clientSession, clientInfo=clientInfo)
    page = sm.getPage()
    page.clearSession()
    page.addComponent(examples(page))

    response.add_header('Set-Cookie', 'remoteCheck=' + clientSession.get('remoteCheck'))
    response.body = page.getMainPage()

    # Imposto la sessione client
    page.updateSession()
    clientSession.save()

    return response


@app.route('/test')
def main():
    logging.debug('***[ /test ]***************************************')
    clientInfo = getClientInfo(request)

    clientSession = request.environ.get('beaker.session')
    sm = SessionManager(clientSession, clientInfo=clientInfo)
    page = sm.getPage()
    page.clearSession()
    page.addComponent(calculator(page))

    response.body = page.getMainPage()

    # Imposto la sessione client
    page.updateSession()
    clientSession.save()

    return response


@app.route('/isomorphic/<filepath:path>')
def server_static(filepath):
    # print "filepath: " + filepath
    return static_file(filepath, root=smartClient.SC_ROOT_PATH)


@app.get('/manageFileUpload/<param>')
@app.post('/manageFileUpload/<param>')
def manageFileUpload(param):
    logging.debug('***[ /manageFileUpload/<param> ]***************************************')
    clientInfo = getClientInfo(request)

    clientSession = request.environ.get('beaker.session')
    sm = SessionManager(clientSession, clientInfo=clientInfo)
    page = sm.getPage()

    event = '???'
    operation = '???'
    obj = '???'

    try:
        json_object = json.loads(param)  # obj now contains a dict of the data
        if json_object != None:
            event = json_object.get('event')
            operation = json_object.get('operation')
            obj = json_object.get('object')
    except ValueError:
        logging.debug('***********************************************************************')
        logging.debug('***********************************************************************')
        logging.debug('*[ PARAM ]*************************************************************')
        logging.debug('')
        logging.debug('... ValueError: ' + str(ValueError))
        logging.debug('... param: ' + param)
        logging.debug('')
        logging.debug('***********************************************************************')
        logging.debug('***********************************************************************')

    logging.debug("param = " + str(param))
    logging.debug("event = " + str(event))
    logging.debug("operation = " + str(operation))
    logging.debug("obj = " + str(obj))
    logging.debug('')
    logging.debug('***[ REQUEST ]***************************************')
    for key in request.params:
        logging.debug("%s = %s" % (key, request.params[key]))
    logging.debug('')

    logging.debug('***[ FILE ]******************************************')
    for key in request.files:
        logging.debug("%s = %s" % (key, request.files[key]))
    logging.debug('')

    upload = request.files.get('UploadFile')
    if upload != None:
        name, ext = os.path.splitext(upload.filename)
        logging.debug(name + '---' + ext)
        upload.save('/tmp/' + 'bk.' + name + ext)  # appends upload.filename automatically

    response.body = "ok, check '/tmp/bk."+ name + ext

    page.updateSession()
    clientSession.save()

    return response


@app.get('/manageRequest/<param>')
@app.post('/manageRequest/<param>')
def manageRequest(param):
    logging.debug('***[ /manageRequest/<param> ]***************************************')
    clientInfo = getClientInfo(request)

    logging.debug(param)

    import json  # or `import simplejson as json` if on Python < 2.6
    json_object = json.loads(param)  # obj now contains a dict of the data

    # Leggo la sessione remota
    clientSession = request.environ.get('beaker.session')
    sm = SessionManager(clientSession, clientInfo=clientInfo)
    page = sm.getPage()

    if json_object.get('event') == 'click':
        replyClick = ReplyClick()

        if json_object.get('operation') == 'verifyPassword':
            user = request.params['user']
            pwd = request.params['password']
            logging.debug('user: ' + str(user))
            logging.debug('pwd: ' + str(pwd))

            replyClick.setStatus('ko')
            replyClick.setMsg('Wrong user or password, try root/password')
            if user.lower() == 'root' and pwd.lower() == 'password':
                replyClick.setData('{}')
                replyClick.setStatus('ok')
                replyClick.setJs("window.location.href = '/main'")

        elif json_object.get('operation') == 'redirect':
            replyClick.setData('{}')
            replyClick.setStatus('ok')
            replyClick.setJs("window.location.href = '/test'")

        elif json_object.get('operation') == 'calculator':
            replyClick.setData('{}')
            replyClick.setStatus('ko')
            replyClick.setMsg("let's calculate!")

            instance_win = json_object.get('object').get('window')

            expr = page.getFromSession('expr', istanza=instance_win)
            if json_object.get('object').get('val') == '=':
                str_expr = request.params.get('expr')
                str_expr = str_expr.replace(':', '/')
                try:
                    res = eval(str_expr)
                except:
                    res = str(sys.exc_info()[0])
                strTmp = '%s.setValue("%s","' + str(res) + '")'
                strTmp = strTmp % (expr.getID(), expr.getID())
                replyClick.setJs(strTmp)
                replyClick.setStatus('ok')
                str2Return = replyClick.getReply()
            elif json_object.get('object').get('val') == 'reset':
                strTmp = '%s.setValue("%s","")' % (expr.getID(), expr.getID())
                replyClick.setJs(strTmp)
                replyClick.setStatus('ok')
                str2Return = replyClick.getReply()
            else:
                strTmp = '%s.setValue("%s",%s.getValue("%s") + "%s")' % (expr.getID(), expr.getID(), expr.getID(), expr.getID(), json_object.get('object').get('val'))
                replyClick.setJs(strTmp)
                replyClick.setStatus('ok')

        else:
            lr = label(page)

            strJS = page.getMainPage(main=False)

            replyClick.setStatus('ok')
            replyClick.setMsg('???!')
            replyClick.setData('{}')
            replyClick.setJs(strJS, lastToken=False)
            logging.debug("??? what else ???")

    response.body = replyClick.getReply()

    logging.debug('*************************************************************************************************')
    # Imposto la sessione client
    page.updateSession()
    clientSession.save()

    return response


logging.debug('')
logging.debug('')
logging.debug('*************************************************************************************************')
# logging.info('                      ..::!!! Serving on %s:%d !!!::..'
#run(app=appWS, reloader=True, host='localhost', port=8080)
run(app=appWS, reloader=True, host='0.0.0.0', port=8080)


