#!/usr/bin/python

import random
import string
import subprocess
import signal
import os

import demos

import cherrypy
from jinja2 import Environment, FileSystemLoader

jenv = Environment(loader=FileSystemLoader('.'))

timeout = 2

class DAVM_Launcher(object):

    myHost = ""
    fifo = None

    @cherrypy.expose
    def index(self):
        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos, scripts=demos.scripts)

    @cherrypy.expose
    def stopIt(self):
        if cherrypy.session.has_key('mySession'):
            os.killpg(cherrypy.session['mySession'].pid, signal.SIGKILL)
            # make this specific to running demo
            del cherrypy.session['mySession']
            #jtemp = jenv.get_template('index.html')
            if DAVM_Launcher.fifo != None:
                try:
                    os.close(DAVM_Launcher.fifo)
                except OSError:
                    print "stale file descriptor"

        subprocess.Popen([
            #'echo',
            'killall', 'orun'
        ])
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def runShellScript(self, button):
        args = [
            #'echo',
        ] + button.split()
        result = subprocess.Popen(args, preexec_fn=os.setsid)
        cherrypy.session['mySession'] = result
        #return "running " + " ".join(args)
        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos, scripts=demos.scripts, currentScript=button)

    @cherrypy.expose
    def runScript(self, bino, movie):
        # useful: http://bino3d.org/doc/bino.html#Script-Commands

        binoCmd = str(bino)
        print binoCmd
        if DAVM_Launcher.fifo:
            if 'rewind' in binoCmd:
                binoCmd='set-pos 0'
            if 'seekF' in binoCmd:
                binoCmd='seek 15.0'
            if 'seekB' in binoCmd:
                binoCmd='seek -15.0'
            os.write(DAVM_Launcher.fifo, binoCmd + '\n')

        #result = subprocess.Popen(args, preexec_fn=os.setsid)
        #cherrypy.session['mySession'] = result
        #return "running " + " ".join(args)
        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos, scripts=demos.scripts, currentDemo=movie)

    @cherrypy.expose
    def runOmega(self, button):
        args = [
            #'echo',
            'orun',
            '-s',
            '/local/examples/' + button,
        ]
        result = subprocess.Popen(args, preexec_fn=os.setsid)
        cherrypy.session['mySession'] = result

        if "bondi" in button:
            if 'dev1' in DAVM_Launcher.myHost:
                DAVM_Launcher.fifo = os.open('/da/tmp/bino.dev1', os.O_WRONLY)

            if 'solo' in DAVM_Launcher.myHost:
                DAVM_Launcher.fifo = os.open('/local/bino.fifos/bino.solo', os.O_WRONLY)

            if 'ig1' in DAVM_Launcher.myHost:
                DAVM_Launcher.fifo = os.open('/da/fifos/bino.ig1', os.O_WRONLY)

            os.write(DAVM_Launcher.fifo, 'pause\n')
            os.write(DAVM_Launcher.fifo, 'step\n')

        #return "running " + " ".join(args)
        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos, scripts=demos.scripts, currentDemo=button)

    @cherrypy.expose
    def runMovie(self, button):
        # dv is the script we created for displaying videos
        myDv = "dv"
        moviePath = '/local/movies/'
        if 'solo' in DAVM_Launcher.myHost:
            myDv = "dv.solo"

        if 'dev1' in DAVM_Launcher.myHost:
            myDv = "dv.dev1"
            moviePath = '/da/movies/'

        args = [
            #'echo',
            myDv,
            moviePath + button
        ]

        print " ".join(args)

        result = subprocess.Popen(args, preexec_fn=os.setsid)
        cherrypy.session['mySession'] = result
        #return "running " + " ".join(args)

        if 'dev1' in DAVM_Launcher.myHost:
            DAVM_Launcher.fifo = os.open('/da/tmp/bino.dev1', os.O_WRONLY)

        if 'solo' in DAVM_Launcher.myHost:
            DAVM_Launcher.fifo = os.open('/local/bino.fifos/bino.solo', os.O_WRONLY)

        if 'ig1' in DAVM_Launcher.myHost:
            DAVM_Launcher.fifo = os.open('/da/fifos/bino.ig1', os.O_WRONLY)

        os.write(DAVM_Launcher.fifo, 'pause\n')
        os.write(DAVM_Launcher.fifo, 'step\n')

        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos, scripts=demos.scripts, currentDemo=button)

if __name__ == '__main__':
    # use this to deploy on ig1 or solo
    #cherrypy.config.update({
        #'server.socket_host' : os.getenv("DA_HOST") + '.da.uts.edu.au'
    #})
    cherrypy.config.update({'tools.sessions.on' : True})
    conf = {
        '/images': {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : '/local/examples/launcher/images'
        }
    }

    DAVM_Launcher.myHost = cherrypy.server.socket_host
    print "host: ", DAVM_Launcher.myHost
    cherrypy.tree.mount(DAVM_Launcher(), "/", conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
