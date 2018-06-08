#Author: Victor G. Balcazar
#Contact Info: victorbalcazar3@hotmail.com
#Class: CPSC 386 - Project 5
#Title: Vanguard Protect the Earth! (project 5)
#External Requirements: Python 2.7. Obtained in python.org
#			Pygame 1.9 and above. Obtained in pygame.org
#Instructions: A quick video search in youtube will show you how to install both of these dependencies in your particular machine.
#Resources Used:
#   KidsCanCode video series. Retrieved from: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
#   Sources from Open Game Art . org:
#       SHMUP SHIPS by surt. Retrieved from: http://opengameart.org/content/shmup-ships
#       through space by maxstack. Retrieved from: http://opengameart.org/content/through-space
#       bullet collection 1 m484 by Master484. Retrieved from: http://opengameart.org/content/bullet-collection-1-m484
#       explosion set 1 m484 by Master484. Retrieced from: http://opengameart.org/content/explosion-set-1-m484-games
#   Laser and explosion sound effects generated using: http://www.bfxr.net/
#   Space Background by kidscancode. Retrieved from: http://imgur.com/bHiPMju

#Game Description: A classic arcade-y shoot em up. There's a ship at the bottom of the screen, you press space bar to shoot asteroids and
#enemy ships while avoiding the ones you can't shoot down. The game opens with a title screen, this serves as both the main "menu" and
#"game over" screen. Within the menu screen the player only has two options: press the window x to exit, or press any keyboard key to 
#start the game. In the main game you have you ship on the bottom of the screen, you can only move left or right. You can press the space
#bar to fire bullets. On the top left you have your lives, represented by little sprites in the shape of your ship, whenever you are hit 
#one will disapear from the right until you reach zero lives at which moment an animation of your ship exploding and a command will take you
#back to the menu screen, this is the game over state. On the top center of the game screen there is a number that increases when you destroy
#enemies, this is your score, it doesn't transfer over, nor is it recorded. The point of the game is to see how far you can go without dying.
#There are two types of enemies. The asteroids which appear in waves so long as there doesn't exist more than 10, meaning that there will 
#always be at least 9 asteroids on screen. The biggest asteroid requires two bullets to destroy. The other kind of enemy is the green enemy
#ships that fire green bullets which are slower than the player's bullets. The enemy ships move horizontally and won't come down to attack
#the player. Enemy ships require two bullets to kill. When the player kills an enemy they are rewarded with some points for their score
#and these points are based on the radius of the asteroids, the biggest ones are worth less than the smaller ones. The ships are worth
#a set amount.
#Each sprite on screen has its own class. There is one game loop. sound effects for enemy fire and player bullets. One looping music track.
#Two animations for when an enemy is destroyed and one for when the player dies.
#The game creates a certain number of enemies in timed intervals up to a cap, preventing the player from become too overwhelmed. There is an
#interval at the beginning of each game where there are no enemies, this is to let the player quickly get a feel for the controls. Asteroids
#appear first and tackle the player. By themselves they are not much of a threat. But after the "adjusting period" the enemy ships appear 
#and shoot at the player, this makes the game much harder, but the player had enough time to adjust to the change in pace. To further help
#this adjusting peroid the player is given 5 lives instead of the traditional 3 lives. The player moves at a speed that is not too fast as
#to make the player more likely to accidentally hit a slow asteroid and the like and not so slow that the player can't maneuver through
#the potential bullet hell.

#Rules: you control a spaceship that moves left or right and shoots incoming asteroids while avoiding enemy fire, get hit 5 times and you lose.

#Bugs: Sometimes when playing the game at the start the enemy ships will spawn earlier than intended.
