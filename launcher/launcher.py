#!/usr/bin/python
import subprocess
import signal
import os

import cherrypy
from jinja2 import Environment, FileSystemLoader

import demos

jenv = Environment(loader=FileSystemLoader('.'))

class DAVM_Launcher(object):

    myHost = ""
    fifo = None

    @cherrypy.expose
    def index(self):
        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos)

    @cherrypy.expose
    def stopIt(self):
        if cherrypy.session.has_key('mySession'):
            os.killpg(cherrypy.session['mySession'].pid, signal.SIGKILL)
            # make this specific to running demo
            del cherrypy.session['mySession']
            if DAVM_Launcher.fifo != None:
                try:
                    os.close(DAVM_Launcher.fifo)
                except OSError:
                    print "stale file descriptor"

        subprocess.Popen([
            'killall', 'orun'
        ])
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def runScript(self, bino, movie):
        if movie=="":
            return self.index()

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

        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos, currentDemo=movie)

    @cherrypy.expose
    def runOmega(self, button):
        args = [
            'orun',
            '-s',
            '/local/examples/' + button,
        ]
        result = subprocess.Popen(args, preexec_fn=os.setsid)
        cherrypy.session['mySession'] = result

        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos, currentDemo=button)

    @cherrypy.expose
    def runMovie(self, button):
        moviePath = '/local/davm.movies/'

	pipePath = "/local/bino/fifo/bino.pipe"

        args = [
        	"/local/bino/install/bin/bino",
		"--loop",
		"-i",
		"mono",
		"--log-file=/var/tmp/bino.log",
		"-o",
		"equalizer",
		"--eq-config",
		"/etc/eq/local.auto.eqc",
		"--read-commands",
		pipePath,
		str(moviePath + button)
	]

        result = subprocess.Popen(args, preexec_fn=os.setsid)
        cherrypy.session['mySession'] = result

        DAVM_Launcher.fifo = os.open(pipePath, os.O_WRONLY)

        os.write(DAVM_Launcher.fifo, 'pause\n')
        os.write(DAVM_Launcher.fifo, 'step\n')

        jtemp = jenv.get_template('index.html')
        return jtemp.render(omegaList=demos.omegalibDemos[DAVM_Launcher.myHost], movieList=demos.movieDemos, currentDemo=button)

if __name__ == '__main__':
    cherrypy.config.update({'tools.sessions.on' : True, 'server.socket_port' : 8002})
    conf = {
        '/images': {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : '/local/examples/launcher/images'
        }
    }

    DAVM_Launcher.myHost = cherrypy.server.socket_host
    cherrypy.tree.mount(DAVM_Launcher(), "/", conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
