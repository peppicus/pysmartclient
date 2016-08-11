# -*- coding: utf-8 -*-
import sys
import logging
import json    # or `import simplejson as json` if on Python < 2.6


from smartClient import VerticalLayout, HorizontalLayout, KeyboardManager, ReplyClick, ActionUrl, Validator
from smartClient import Label, DateField, EditField, CheckBox, RadioGroup, SelectField, PasswordField, Button, Link
from smartClient import TextArea, Header, Spacer, RichEditor, ListGrid, DataSource, FileUpload, Window, ViewLoader
from smartClient import SectionStack, MainMenu, MenuLink, HTMLPane, Canvas


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')


def loginPage(page):
    login = Label()
    login.setProperty('contents','login')
    login.setProperty('height',40)

    user = EditField()
    user.setProperty('title','user','fields')
    user.setProperty('value','','fields')
    user.setProperty('autoFocus','true')
    user.setProperty('autoFocus','true','fields')
    user.transformValue = 'function(form, item, value, oldValue) {return value.toUpperCase()}'

    password = PasswordField()
    password.setProperty('title','password','fields')
    password.setProperty('value','','fields')

    v = Validator()
    v.setCondition("return value == 'password';")
    password.addValidator(v)

    spacer = Spacer()
    spacer.setProperty('width', '*')
    spacer0 = Spacer()
    spacer0.setProperty('width', '*')
    spacer1 = Spacer()
    spacer1.setProperty('width', '5%')
    spacer2 = Spacer()
    spacer2.setProperty('height', '5%')

    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('verifyPassword')
    strObj = '{"object":"User"}'
    actionURL.setObject(strObj)
    actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    check = Button(actionUrl=actionURL)
    check.setProperty('title', 'login')
    check.setProperty('width', 100)
    check.setProperty('height', 40)
    keyboardManager = page.keyboardManager
    keyboardManager.addEventList2Component(check, ['%s.setFocus(true);', '%s.click();'])


    v1 = VerticalLayout()
    h0 = HorizontalLayout()
    h1 = HorizontalLayout()
    v1.setProperty('width', 400)
    v1.setProperty('membersMargin', 5)
    v1.setProperty('layoutMargin', 20)


    #v1.addComponent(header)
    #v1.addComponent(spacer1)
    v1.addComponent(spacer2)
    v1.addComponent(login)
    v1.addComponent(user)
    v1.addComponent(password)
    #v1.addComponent(spacer2)
    v1.addComponent(h1)

    h1.addComponent(spacer)
    h1.addComponent(check)
    #v1.setProperty('layoutAlign', 'right')

    h0.addComponent(spacer0)
    h0.addComponent(v1)
    h0.addComponent(spacer1)

    return h0


def calculator(page):
    vly = VerticalLayout()
    vly.setProperty('layoutMargin', 10)
    page.add2Session('vly', vly)

    instance_win = str(page.getNewIdName())

    win = Window()
    win.pre_name = instance_win

    vly_container = VerticalLayout()

    expr = EditField('expr')
    page.add2Session('expr', expr, window=win)
    expr.setProperty('value', '', 'fields')

    str_button_height = '60'
    str_row_height = '65'
    row1 = HorizontalLayout()
    row2 = HorizontalLayout()
    row3 = HorizontalLayout()
    row4 = HorizontalLayout()
    row5 = HorizontalLayout()
    row1.setProperty('height', str_row_height)
    row2.setProperty('height', str_row_height)
    row3.setProperty('height', str_row_height)
    row4.setProperty('height', str_row_height)
    row5.setProperty('height', str_row_height)


    params = '{"expr":%s.getValue("%s")}'
    paramsList = []
    paramsList.append(expr)
    paramsList.append(expr)

    buttons = ['(', ')', '*', ':', '1', '2', '3', '+', '4', '5', '6', '-', '7', '8', '9', '0', 'reset', '=']

    i = 0
    for btn in buttons:
        actionURL = ActionUrl()
        actionURL.setEvent('click')
        actionURL.setOperation('calculator')
        strObj = '{"object":"assExpr", "val":"'+btn+'", "window":"'+instance_win+'"}'
        actionURL.setObject(strObj)
        actionURL.setParams(params, *paramsList)
        btn_obj= Button(actionUrl=actionURL)
        btn_obj.setProperty('title', btn)
        #uno.setProperty('width', '50')
        btn_obj.setProperty('height', str_button_height)

        if 0 <= i <= 3:
            row1.addComponent(btn_obj)
        if 4 <= i <= 7:
            row2.addComponent(btn_obj)
        if 8 <= i <= 11:
            row3.addComponent(btn_obj)
        if 12 <= i <= 15:
            row4.addComponent(btn_obj)
        if 16 <= i <= 17:
            row5.addComponent(btn_obj)
        i = i + 1

    win.addComponent(vly_container)
    vly_container.addComponent(expr)

    vly_container.addComponent(row1)
    vly_container.addComponent(row2)
    vly_container.addComponent(row3)
    vly_container.addComponent(row4)
    vly_container.addComponent(row5)

    vly.addComponent(win)

    return vly

    logging.debug('*[ GET DETAIL  END ]********************************************************')



def examples(page):
    vly_main = VerticalLayout()
    #vly_main.setProperty('membersMargin', 0)
    #vly_main.setProperty('layoutMargin', 10)

    hly_top = HorizontalLayout()
    hly_top.setProperty('height', 50)

    hly_data = HorizontalLayout()
    hly_data.setProperty('height', 150)

    vly_sx = VerticalLayout()
    vly_sx.setProperty('width', 260)

    vly_dx = VerticalLayout()
    vly_dx.setProperty('width', '*')

    sbm_1 = MenuLink()
    sbm_2 = MenuLink()
    sbm_3 = MenuLink()

    #sbm_1.setProperty('width', 200)
    #sbm_1.setProperty('height', 100)
    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('operationX')
    strObj = '{"object":"User"}'
    actionURL.setObject(strObj)
    # actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    actionURL.setParams('{}')
    sbm_1.setProperty('title', 'Users', 'data', 0)
    sbm_1.setProperty('click', actionURL, 'data', 0)

    actionURL = ActionUrl()
    actionURL.setEvent('click')
    #actionURL.setOperation('masterDetailDetail')
    actionURL.setOperation('operationY')
    strObj = '{"object":"Menu"}'
    actionURL.setObject(strObj)
    # actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    actionURL.setParams('{}')
    sbm_1.setProperty('title', 'Menù', 'data', 1)
    sbm_1.setProperty('click', actionURL, 'data', 1)

    #sbm_1.setProperty('width', 200)
    #sbm_1.setProperty('height', 100)
    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('redirect')
    strObj = '{"object":"test"}'
    actionURL.setObject(strObj)
    # actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    actionURL.setParams('{}')
    sbm_2.setProperty('title', 'Redirect test', 'data', 0)
    sbm_2.setProperty('click', actionURL, 'data', 0)

    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('voice_yyy')
    strObj = '{"object":"Menu"}'
    actionURL.setObject(strObj)
    # actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    actionURL.setParams('{}')
    sbm_2.setProperty('title', 'yyy', 'data', 1)
    sbm_2.setProperty('click', actionURL, 'data', 1)

    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('operationZ')
    strObj = '{"object":"Menu"}'
    actionURL.setObject(strObj)
    # actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    actionURL.setParams('{}')
    sbm_3.setProperty('title', 'xxx', 'data', 0)
    sbm_3.setProperty('click', actionURL, 'data', 0)

    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('operationK')
    strObj = '{"object":"Menu"}'
    actionURL.setObject(strObj)
    # actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    actionURL.setParams('{}')
    sbm_3.setProperty('title', 'zzz', 'data', 1)
    sbm_3.setProperty('click', actionURL, 'data', 1)
    sbm_2.setProperty('submenu', sbm_3, 'data', 1) # mettendo la submenu sulla voce non sente più il click

    mm_1 = MainMenu()
    mm_1.setProperty('width', '100%')
    mm_1.setProperty('height', 30)
    mm_1.setProperty('title', 'tables')
    mm_1.setProperty('menu', sbm_1)

    mm_2 = MainMenu()
    mm_2.setProperty('width', '100%')
    mm_2.setProperty('height', 30)
    mm_2.setProperty('title', 'utility')
    mm_2.setProperty('menu', sbm_2)

    vly_sx.addComponent(mm_1)
    vly_sx.addComponent(mm_2)

    link = Link()
    link.setProperty('value', '/main', 'fields')
    link.setProperty('linkTitle', 'main', 'fields')
    link.setProperty('target', '_self', 'fields')

    l1 = EditField()
    l2 = TextArea()
    l21 = DateField()
    l22 = CheckBox()
    l23 = RadioGroup()
    l24 = SelectField()
    l25 = PasswordField()

    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('tick')
    strObj = '{"object":"User"}'
    actionURL.setObject(strObj)
    actionURL.setParams('{}')
    #actionURL.setParams('{"user":%s.getValue("%s"),"password":%s.getValue("%s")}', user, user, password, password)
    l26 = Button(actionUrl=actionURL)

    l27 = RichEditor()
    l3 = Label()
    l3.setProperty('height', '*')

    l4 = Label()
    l5 = Label()
    l6 = Label()
    l4.setProperty('width', '50%')
    l5.setProperty('width', '*')
    l6.setProperty('width', '30%')

    ef1 = EditField()

    actionURL = ActionUrl('manageFileUpload/')
    actionURL.setEvent('click')
    actionURL.setOperation('tick')
    strObj = '{"object":"file"}'
    actionURL.setObject(strObj)
    actionURL.setParams('{"file":"cache.txt"}')
    #actionURL.setClickJs('function() { fu.saveData("if(response.status>=0) fu.editNewRecord()"); }')
    fu = FileUpload(actionUrl=actionURL)
    fu.setProperty('width', 350)
    fu.setProperty('height', 80)

    l24.setProperty('Ms', 'Ms', 'valueMap')
    l24.setProperty('Mr', 'Mr', 'valueMap')
    l24.setProperty('Mrs', 'Mrs', 'valueMap')

    #wl = ViewLoader()
    win = Window()

    vly_main.addComponent(hly_top)
    vly_main.addComponent(hly_data)

    hly_top.addComponent(l4)
    hly_top.addComponent(l5)
    hly_top.addComponent(l6)

    vly_sx.addComponent(link)
    vly_sx.addComponent(l1)
    vly_sx.addComponent(l2)
    vly_sx.addComponent(l21)
    vly_sx.addComponent(l22)
    vly_sx.addComponent(l23)
    vly_sx.addComponent(l24)
    vly_sx.addComponent(l25)
    vly_sx.addComponent(l3)
    vly_sx.addComponent(l26)
    vly_sx.addComponent(win)

    #win.addComponent(link)
    #vly_sx.addComponent(win)

    hly_detail = HorizontalLayout()
    page.add2Session('vly_sx', vly_sx)
    page.add2Session('vly_dx', vly_dx)
    page.add2Session('hly_detail', hly_detail)
    page.removeFromSession('vly_detail')

    hly_detail.addComponent(ef1)

    vlygrid = VerticalLayout()
    ef1.setProperty('title', 'search', 'fields')
    #ef1.setProperty('titleSuffix', '')
    #ef1.setProperty('titleWidth', 'fixme', 'fields')

    hly_search = HorizontalLayout()
    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('fetchDataURL')
    strObj = '{"object":"User"}'
    actionURL.setObject(strObj)
    actionURL.setParams('{"query":%s.getValue("%s")}', ef1, ef1)
    #actionURL.setClickJs('function () { lsg_42.setData([]); }')
    btn_search = Button(actionUrl=actionURL)
    btn_search.setProperty('width', '50')
    btn_search.setProperty('height', '25')
    btn_search.setProperty('title', 'search')

    actionURL = ActionUrl()
    actionURL.setEvent('click')
    actionURL.setOperation('new')
    strObj = '{"object":"User"}'
    actionURL.setObject(strObj)
    #actionURL.setParams('{"query":%s.getValue("%s")}', ef1, ef1)
    #actionURL.setClickJs('function () { lsg_42.setData([]); }')
    btn_new = Button(actionUrl=actionURL)
    btn_new.setProperty('width', '50')
    btn_new.setProperty('height', '25')
    btn_new.setProperty('title', 'new')

    ef1.setProperty('value', '', 'fields')
    hly_search.addComponent(ef1)
    hly_search.addComponent(btn_search)
    hly_search.addComponent(btn_new)

    vlygrid.addComponent(hly_search)
    hly_detail.addComponent(vlygrid)
    vly_dx.addComponent(l27)
    vly_dx.addComponent(hly_detail)
    lbl_fs = Label()

    lbl_fs.setProperty('contents','result')
    lbl_fs.setProperty('height',40)
    #lbl_fs.setProperty('')
    #iframe = Canvas()
    iframe = HTMLPane()
    fu.setProperty('target', 'myIframe')
    vly_dx.addComponent(fu)
    vly_dx.addComponent(lbl_fs)
    vly_dx.addComponent(iframe)

    hly_data.addComponent(vly_sx)
    hly_data.addComponent(vly_dx)

    return vly_main


def label(page):
    lx = Label()
    vly_sx = page.getFromSession('vly_sx')
    # page.componentList = []
    if vly_sx != None:
        page.componentList.append(vly_sx)
        vly_sx.addComponent(lx)
        #page.insertHereJS = ''
        #logging.debug('page.renderMainPage(page.componentList)')
        #page.idName = page.renderMainPage(page.componentList, page.idName)
        #logging.debug('page.renderAddMembers(page.componentList)')
        #page.renderAddMembers(page.componentList)
        # logging.debug('page.insertHereJS = ' + page.insertHereJS)


