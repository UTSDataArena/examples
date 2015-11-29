#!/usr/bin/python

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
        "Mocap": "box/LoadOTL.py",
        "Bar Chart": "barchart/LoadBarChart.py",
        "Weld": "misc/LoadWeld.py",
        "Brain": "misc/LoadBrain.py",
        "Faces": "misc/LoadFaces.py",
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
