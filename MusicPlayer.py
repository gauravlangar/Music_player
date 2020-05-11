
from tkinter.filedialog import *
from PIL import Image, ImageTk
import pygame
import _thread




from mutagen.id3 import ID3
from mutagen.mp3 import MP3



isPlaying = True
listOfSongs = []
playingTime = []
report = {}
realNames = []
index = 0
root = Tk()
root.wm_title('Music Player')
root.geometry('1150x647+100+60')
root.configure(bg='#4d0000')
root.resizable(0,0)
playingSong = StringVar()
availableSongs = StringVar()
currentPlayingSong = StringVar()
vol = StringVar()
vol.set('Volume')
availableSongs.set("Available Songs")
currentPlayingSong.set('Current Playing')

back_img = ImageTk.PhotoImage(Image.open('back.jpg'))
play_img = ImageTk.PhotoImage(Image.open('play-song.png'))
pause_img = ImageTk.PhotoImage(Image.open('pause-song.png'))
next_img = ImageTk.PhotoImage(Image.open('next-song.png'))
prev_img = ImageTk.PhotoImage(Image.open('prev-song.png'))
stop_img = ImageTk.PhotoImage(Image.open('stop-song.png'))

background_label = Label(root, image=back_img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

btn_play = Button(root, image=pause_img, border='0', bg='#200003', fg='#343a40')
btn_play.place(x=470, y=500)

btn_next = Button(root, image=next_img, border='0', bg='#450D00', fg='#343a40')
btn_next.place(x=570, y=500)

btn_prev = Button(root, image=prev_img, border='0', bg='#240000', fg='#240000')
btn_prev.place(x=370, y=500)

btn_stop = Button(root, image=stop_img, border='0', bg='#4E1408', fg='#343a40')
btn_stop.place(x=670, y=500)

volume = Scale(root, from_=0, to=100, fg='red', orient=HORIZONTAL, length=200, bg='white', label='Volume')
volume.place(x=790, y=515)

seeker = Scale(root, fg='red', orient=HORIZONTAL, length=1150, bg='white', sliderlength=15, resolution=0.01, variable=StringVar())
seeker.place(x=0, y=430)

'''

Sets the Playing time of the song converting all the formats of the time in seconds.
'''


def set_playing_time():
	global index
	timer = playingTime[index]
	totalTime = ((timer // 60) * 1.0) + ((timer % 60) / 100)
	seeker['from_'] = 0.0
	seeker['to'] = totalTime
	try:
		while seeker.get() <= totalTime:
			seeker.set(fetch_playing_time())
	except ValueError:
		print("Floating Point error")


'''
Returns the Playing time of the song converting all the formats of the time in minutes.
'''


def fetch_playing_time():
	return (pygame.mixer.music.get_pos()/1000)/60


'''
Sets the text of the Play button.
'''


def validate_play_button():
	btn_play.configure(image=pause_img)
	btn_play.image = pause_img
	play['text'] = 'Play'


'''
Plays the next song from the list of songs.
'''


def next_song(event):
	global index
	if index == len(listOfSongs) - 1:
		index = 0
	else:
		index += 1
		
	pygame.mixer.music.load(listOfSongs[index])
	pygame.mixer.music.play()
	updatelabel()
	report[playingSong.get()] += 1
	validate_play_button()
	try:
		_thread.start_new_thread(set_playing_time, tuple())
	except MemoryError:
		print("Out of memory due to threads :)")
	
	
'''
Plays the previous song from the list of songs.
'''


def prev_song(event):
	global index
	if index == 0:
		index = len(listOfSongs) - 1
	else:
		index -= 1
	
	pygame.mixer.music.load(listOfSongs[index])
	pygame.mixer.music.play()
	updatelabel()
	report[playingSong.get()] += 1
	validate_play_button()
	try:
		_thread.start_new_thread(set_playing_time, tuple())
	except MemoryError:
		print("Out of memory due to threads :)")


'''
Stops the current playing song.
'''


def stop_song(event):
	pygame.mixer.music.stop()
	playingSong.set("")
	

'''
Updates the label of the current playing song.
'''


def updatelabel():
	global index
	playingSong.set(realNames[index])


'''
Plays/Pauses the current playing song from the list of songs.
'''


def play_song(event):
	global isPlaying
	if isPlaying != True:
		btn_play.configure(image=play_img)
		btn_play.image = play_img
		play['text'] = 'Pause'
		pygame.mixer.music.pause()
		updatelabel()
		isPlaying = True
	else:
		btn_play.configure(image=pause_img)
		btn_play.image = pause_img
		play['text'] = 'Play'
		pygame.mixer.music.unpause()
		updatelabel()
		isPlaying = False
	
	
'''
Sets the volume of the current playing song.
'''


def set_volume(event):
	changer = volume.get()
	changer *= 1.0
	pygame.mixer.music.set_volume(changer/100)

'''
Opens the underlying File Directory Structure.
'''


def DirectoryChooser():
	directory = askdirectory()
	os.chdir(directory)
	for files in os.listdir(directory):
		if files.endswith(".mp3"):
			realDir = os.path.realpath(files)
			audio = ID3(realDir)
			realNames.append(audio.get('TIT2'))
			listOfSongs.append(files)
			playingTime.append(round(MP3(files).info.length))
	
	pygame.mixer.init()
	pygame.mixer.music.load(listOfSongs[index])
	pygame.mixer.music.set_volume(0.1)
	volume.set(pygame.mixer.music.get_volume() * 100)
	pygame.mixer.music.play()
	_thread.start_new_thread(set_playing_time, tuple())
	playingSong.set(realNames[index])
	
	
DirectoryChooser()

songLabel = Label(root, textvariable=playingSong, width=40, font=("Courier", 14, 'bold'), bg='grey', fg='black')
songLabel.place(x=50, y=297)

currentPlayingSongLabel = Label(root, textvariable=currentPlayingSong, width=40, font=("Courier", 14, 'underline'), fg='black', bg='grey')
currentPlayingSongLabel.place(x=50, y=270)

availableSongsLabel = Label(root, textvariable=availableSongs, width=40, font=("Courier", 14, 'underline'), fg='black', bg='grey')
availableSongsLabel.place(x=50, y=21)

volLabel = Label(root, textvariable=vol, bg='#CD4B19', fg='white', font=("Courier", 14))
volLabel.place(x=825, y=590)

listBox = Listbox(root, width=40, height=10, font=("Courier", 14), bg='black', fg='white')
listBox.place(x=50, y=48)

realNames.reverse()

for items in realNames:
	listBox.insert(0, items)

for songs in range(0, listBox.size()):
	report[listBox.get(songs)] = 0

realNames.reverse()

play = Label(text="Play", bg='#190101', fg='white', font=("Courier", 14))
play.place(x=485, y=590)

stop = Label(text="Stop", bg='#4E1408', fg='white', font=("Courier", 14))
stop.place(x=685, y=590)

prev = Label(text="Previous", bg='#240000', fg='white', font=("Courier", 14))
prev.place(x=365, y=590)

next = Label(text="Next", bg='#190101', fg='white', font=("Courier", 14))
next.place(x=585, y=590)

btn_play.bind('<Button-1>', play_song)
btn_next.bind('<Button-1>', next_song)
btn_prev.bind('<Button-1>', prev_song)
btn_stop.bind('<Button-1>', stop_song)
volume.bind('<Button-1>', set_volume)


root.mainloop()
