#!/usr/bin/python
# the list of demos to use

omegalibDemos = {
    "127.0.0.1" : {
	"Wombeyan Caves": "cave",
	"Water Pipe": "pipe",
	"Fashion Turntable": "ft",
	"DAB Fashion Show": "fs.solo.sound",
	"Pong": "p",
	"Parallel Coordinates": "pcm",
        "Earth": "earth/LoadEarth.py",
        "Motion Capture": "box/LoadOTL.py",
        "Bar Chart": "barchart/LoadBarChart.py",
        "Box": "box/LoadBox.py",
    },
}

movieDemos = {
	"Spitzer Spectroscopy": "SpitzerL2_vm.mp4",
	"Spitzer Labels": "videoSpitzer.label_vm.mp4",
	"Bacteria Trails": "bacteria_trailD_vm.mp4",
	"Parasites": "parasite.drishti.2_vm.mkv",
	"Zebedee Flight": "06a.zebedee_mvi_0058_vm.mp4",
	"Motion Capture": "dancer3_vm.mkv",
}

scripts = {
	"Zeb": ["ssh ig2 vdesk 2", "ssh ig2 vdesk 1"],
	"Rig": ["ssh ig3 vdesk 2", "ssh ig3 vdesk 1"],
}
