# Imports:
# --------
import sys
import pygame
import numpy as np
import gymnasium as gym
import os


### Build our own custom environment

class ZainEnv(gym.Env):
    def __init__(self, goal_coordinates=(0,4), grid_size=5) -> None:
        super(ZainEnv, self).__init__()
        self.grid_size = grid_size
        self.cell_size = 100
        self.state = None
        self.reward = 0
        self.info = {}
        self.goal = np.array([0,4])
        self.done = False
        self.hell_states = []
        
        # Action-space:
        self.action_space = gym.spaces.Discrete(4)
        
        # Observation space:
        self.observation_space = gym.spaces.Box(low=0, high=grid_size-1, shape=(2,), dtype=np.int32)

        # Initialize the window:
        pygame.init()
        self.screen = pygame.display.set_mode((self.cell_size*self.grid_size, self.cell_size*self.grid_size))
        self.font = pygame.font.SysFont("Arial", 24)

    def show_welcome_message(self):
        """ Show a start screen of the game """
        welcome_image = pygame.image.load('title_pic.JPG').convert_alpha()
        welcome_image = pygame.transform.scale(welcome_image, (self.cell_size*self.grid_size, self.cell_size*self.grid_size))  # Scale image to fit full screen
        welcome_image_rect = welcome_image.get_rect()
        self.screen.fill((0, 0, 0))
        self.screen.blit(welcome_image, welcome_image_rect)
        
        pygame.display.flip()
        pygame.time.delay(100)


    # Reset()
    # ---------
    def reset(self):
        """
        To reset Everything
        """
        self.state = np.array([4, 0])
        self.done = False
        self.reward = 0

        self.info["Distance to goal"] = np.sqrt(
            (self.state[0]-self.goal[0])**2 + 
            (self.state[1]-self.goal[1])**2
        )

        return self.state, self.info
    
    # Hell states
    # ---------
    def add_hell_states(self, hell_state_coordinates):
        self.hell_states.append(np.array(hell_state_coordinates))

    # Step()
    # ---------
    def step(self, action):
        ## Actions:
        ## --------
        # Up:
        if action==0 and self.state[0] > 0:
            self.state[0] -= 1

        # Down:
        elif action==1 and self.state[0] < self.grid_size-1:
            self.state[0] += 1

        # Right:
        elif action==2 and self.state[1] < self.grid_size-1:
            self.state[1] += 1

        # Left:
        elif action==3 and self.state[1] > 0:
            self.state[1] -= 1
        
        else:
            print("Select number from 0 to 3")

        

        ## Reward:
        ## -------
        if np.array_equal(self.state, self.goal): # Check goal condition
            self.reward += 100
            self.done = True
        elif True in [np.array_equal(self.state, each_hell) for each_hell in self.hell_states]: # Check hell-states
            self.reward += -2
            self.done = True
        else: # Every other state
            self.reward += -0.05
            self.done = False

        ## Info:
        ## -----
        self.info["Distance to goal"] = np.sqrt(
            (self.state[0]-self.goal[0])**2 + 
            (self.state[1]-self.goal[1])**2
        )
        
        return self.state, self.reward, self.done, self.info
    
    # Render()
    # ---------
    def render(self):
        # Closing the window:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        bg = pygame.image.load("mario_background.jpg").convert_alpha()
        bg = pygame.transform.smoothscale(bg,(self.cell_size*self.grid_size, self.cell_size*self.grid_size))
        self.screen.fill((255,255,255))
        self.screen.blit(bg,(0,0))

      
         # Draw the Goal-state:
        goal_or_image = pygame.image.load('Mario_goal_pic.JPG').convert_alpha()
        goal_ch_image = pygame.transform.smoothscale(goal_or_image,(self.cell_size,self.cell_size))
        goalRect = pygame.Rect(self.goal[1]*self.cell_size, self.goal[0]*self.cell_size, self.cell_size, self.cell_size)
        self.screen.blit(goal_ch_image,goalRect)

        gifpath = os.path.join(os.getcwd(),'cactus2a.png')
        hurdleImage = pygame.image.load(gifpath).convert_alpha()
        
        # # Hell-states:
        for each_hurdle in self.hell_states:
            hurdleChImage = pygame.transform.smoothscale(hurdleImage,(self.cell_size,self.cell_size))
            hellRect = pygame.Rect(each_hurdle[1]*self.cell_size, each_hurdle[0]*self.cell_size, self.cell_size, self.cell_size)
            self.screen.blit(hurdleChImage,hellRect)

        # Draw the agent:
        agent_or_image = pygame.image.load('Mario_pic.png').convert_alpha()
        agent_ch_image = pygame.transform.smoothscale(agent_or_image,(self.cell_size,self.cell_size))
        agentRect = pygame.Rect(self.state[1]*self.cell_size, self.state[0]*self.cell_size, self.cell_size, self.cell_size)
        # pygame.draw.rect(self.screen, (255,0,0), agent)
        self.screen.blit(agent_ch_image,agentRect)

        # Update contents on the window:
        pygame.display.flip()



    # Close()
    # ---------
    def close(self):
        pygame.display.quit()
        print("Window close: ",pygame.WINDOWCLOSE)
        pygame.quit()


# An instance of my environment and check the action and observation space

my_env = ZainEnv(grid_size=6)
my_env.show_welcome_message()


# Instance of the environment

def create_env(goal_coordinates,
               hell_state_coordinates):
    # Create the environment:

    env = ZainEnv(goal_coordinates=goal_coordinates)

    for i in range(len(hell_state_coordinates)):
        env.add_hell_states(hell_state_coordinates=hell_state_coordinates[i])

    return env