#!/usr/bin/python
# the list of demos to use

omegalibDemos = {
    "127.0.0.1" : {
	"Wombeyan Caves": "misc/LoadWombeyan.py",
	"Water Pipe": "pipe",
	"Fashion Turntable": "ft",
	"DAB Fashion Show": "fs.solo.sound",
	"Pong": "p",
	"Parallel Coordinates": "pcm",
	"Motion Capture movies": "dance",
	"Storm Surfers": "bondi.solo",
        "Box": "box/LoadBox.py",
        "Earth": "earth/LoadEarth.py",
        "Parallel Coords": "parallel/DAParallelCoords.py",
        "Mocap": "box/LoadOTL.py",
        "Bar Chart": "barchart/LoadBarChart.py",
        "Weld": "misc/LoadWeld.py",
        "Brain": "misc/LoadBrain.py",
    },
}

movieDemos = {
	"Spitzer Spectroscopy": "SpitzerL2_HighRes.mp4",
	"Spitzer Labels (Large)": "videoSpitzer.labelsLarge.mp4",
	"Spitzer Labels (Small)": "videoSpitzer.labelsSmall.mp4",
	"Bacteria Trails": "bacteria_trailD.mp4",
	"Parasites": "parasite.drishti.2.mkv",
	"Zebedee Flight": "06a.zebedee_mvi_0058.mp4",
	"Motion Capture": "dancer3.mkv",
}

scripts = {
	"Zeb": ["ssh ig2 vdesk 2", "ssh ig2 vdesk 1"],
	"Rig": ["ssh ig3 vdesk 2", "ssh ig3 vdesk 1"],
}
