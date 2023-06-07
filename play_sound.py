from pygame import mixer

mixer.pre_init(44100, -16, 2, 32) # setup mixer to avoid sound lag
mixer.init() #Instantiate mixer

#create music
click_sound = mixer.Sound("sound_effects/click_sound.mp3")
pop_sound = mixer.Sound("sound_effects/pop_sound.mp3")
home_bgm = mixer.Sound("sound_effects/home_bgm.mp3")
level_bgm = mixer.Sound("sound_effects/level_bgm.mp3")
game_bgm = mixer.Sound("sound_effects/game_bgm.mp3")
INFIN_bgm = mixer.Sound("sound_effects/INFIN_bgm.mp3")

#create channels
click_channel = mixer.Channel(0)  
pop_channel = mixer.Channel(1)  
home_bgm_channel = mixer.Channel(2)  
level_bgm_channel = mixer.Channel(3)  
game_bgm_channel = mixer.Channel(4)  
INFIN_bgm_channel = mixer.Channel(5) 

#set the volume
click_channel.set_volume(0.8)  
pop_channel.set_volume(0.8) 
home_bgm_channel.set_volume(1) 
level_bgm_channel.set_volume(0.7) 
game_bgm_channel.set_volume(0.7) 
INFIN_bgm_channel.set_volume(0.8) 



def play_sound(music, loop=False):


	mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
	mixer.init() #Instantiate mixer

	# if music == "click_sound" or music == "pop_sound":
	# 	# #Load audio file
	# 	mixer.music.load("sound_effects/click_sound.mp3")
	# 	mixer.music.play()


	if music == "click_sound":
		click_channel.play(click_sound, loops = -1 if loop else 0)
	elif music == "pop_sound":
		pop_channel.play(pop_sound, loops = -1 if loop else 0)
	elif music == "home_bgm":
		mixer.stop()
		home_bgm_channel.play(home_bgm, loops = -1 if loop else 0)
	elif music == "level_bgm":
		mixer.stop()
		level_bgm_channel.play(level_bgm, loops = -1 if loop else 0)
	elif music == "game_bgm":
		mixer.stop()
		game_bgm_channel.play(game_bgm, loops = -1 if loop else 0)
	elif music == "INFIN_bgm":
		mixer.stop()
		INFIN_bgm_channel.play(INFIN_bgm, loops = -1 if loop else 0)




# #Infinite loop
# while True:
# 	print("------------------------------------------------------------------------------------")
# 	print("Press 'p' to pause the music")
# 	print("Press 'r' to resume the music")
# 	print("Press 'e' to exit the program")

# 	#take user input
# 	userInput = input(" ")
	
# 	if userInput == 'p':

# 		# Pause the music
# 		mixer.music.pause()	
# 		print("music is paused....")
# 	elif userInput == 'r':

# 		# Resume the music
# 		mixer.music.unpause()
# 		print("music is resumed....")
# 	elif userInput == 'e':

# 		# Stop the music playback
# 		mixer.music.stop()
# 		print("music is stopped....")
# 		break

