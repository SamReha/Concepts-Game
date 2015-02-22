# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

@auth.requires_login()
def index():
    playerList = db(db.player.caretakerID == auth.user.id).select()

    addPlayerButton = A('Add New Player', _class='btn', _href=URL('default', 'addPlayer'))
    logoutButton = A('Log Out', _class='btn', _href=URL('default', 'user', args=['logout']))

    return dict(playerList=playerList, addPlayerButton=addPlayerButton, logoutButton=logoutButton)

# This controller is for the player page
@auth.requires_login()
def player():
    verifiyCaretaker(auth.user.id, request.args(0))

    player = db(db.player.id==request.args(0)).select().first()

    startTestButton = A('Start in Test Mode', _class='btn', _href=URL('default', 'index'))
    startPracticeButton = A('Star in Practice Mode', _class='btn', _href=URL('default', 'index'))
    configureButton = A('Configure', _class='btn', _href=URL('default', 'configure', args=[request.args(0)]))
    removePlayerButton = A('Remove Player', _class='btn', _href=URL('default', 'removePlayer', args=[request.args(0)]))

    return dict(startTestButton=startTestButton,
                startPracticeButton=startPracticeButton,
                configureButton=configureButton,
                removePlayerButton=removePlayerButton,
                name=player.name,
               )

@auth.requires_login()
def configure():
    verifiyCaretaker(auth.user.id, request.args(0))

    player = db(db.player.id==request.args(0)).select().first()
    videos = db(db.videos.playerID==player.id).select()

    addVideoButton = A('Add a Video', _class='btn', _href=URL('default', 'addVideo', args=[player.id]))

    return dict(player=player, videos=videos, addVideoButton=addVideoButton)

@auth.requires_login()
def addPlayer():
    form = SQLFORM.factory(Field('name',
                                 label='Player Name',
                                 ),
                          )
    if form.process().accepted:
        db.player.insert(caretakerID = auth.user.id,
                         name = form.vars.name,
                        )
        redirect(URL('default', 'index'))

    return dict(form=form)

@auth.requires_login()
def removePlayer():
    verifiyCaretaker(auth.user.id, request.args(0))

    db(db.player.id == request.args(0)).delete()

    redirect(URL('default', 'index'))

@auth.requires_login()
def addVideo():
    form = SQLFORM.factory(Field('link',
                                 label='Video Link',
                                 ),
                          )
    if form.process().accepted:
        db.videos.insert(playerID = request.args(0),
                         link = form.vars.link,
                        )
        redirect(URL('default', 'configure', args=[request.args(0)]))

    return dict(form=form)

@auth.requires_login()
def removeVideo():
    db(db.videos.id == request.args(1)).delete()

    redirect(URL('default', 'configure', args=[request.args(0)]))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
