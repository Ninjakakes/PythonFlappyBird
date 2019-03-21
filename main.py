"""
Flappy bird made in python using pygame 
"""

# Import pygame for display and input handling
import pygame

# Import random for getting random numbers for pipe 'safe zone' postion
import random

class Pipe:
    """A class used for the pipes (one pipe is a top pipe and bottom pipe together) takes in a top x and width as well as the screen height"""
    def __init__(self, top, x, width, screen_height):
        self.top = top
        self.bottom = top + 75 # The height of the safe zone is always 75 pixels so the bottom will be the top + 75
        self.x = x
        self.width = width
        self.height = screen_height
        self.passed = False
        self.scored = False

    @property
    def offscreen(self):
        """A property that returns True if the pipe is offscreen"""
        return self.x < -self.width

    @property
    def top_rect(self):
        """A property that returns a rectangle for the top pipe"""
        return pygame.Rect(int(self.x), 0, self.width, self.top)
    
    @property
    def bottom_rect(self):
        """A property that returns a rectangle for the bottom pipe"""
        return pygame.Rect(int(self.x), self.bottom, self.width, self.bottom+self.height)

    @property
    def safe_rect(self):
        """A property that returns a rectangle for the area between the top and bottom pipe"""
        return pygame.Rect(int(self.x), self.top, self.width, 75)

    def draw(self, root):
        """This method draws the whole pipe"""
        pygame.draw.rect(root, (0,255,0), self.top_rect) #  Draws the top pipe
        pygame.draw.rect(root, (0,255,0), self.bottom_rect) # Draws the bottom pipe
        # pygame.draw.rect(root, (255,0,0), self.safe_rect) # Draws the safe zone for the pipe (uncomment to display the safezone)

    def update(self):
        """This method updates the pipe"""
        self.x -= 1 # Move the pipe left by 1 pixel

    def hit(self, bird):
        """This method takes a bird object and returns if the bird has scored or has hit the pipe"""
        if self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect): # If the bird has hit the top or bottom pipe
            return {'hit': self} # Return hit and this pipe
        elif self.safe_rect.collidepoint(bird.x, bird.y): # Else if the bird is in the 'safe zone'
            if not self.scored: # If this pipe has not been already scored
                self.scored = True # This pipe has now been scored
                return {'score': 1} # Return score and 1 

class Bird:
    """A class for the bird takes in the screen height for calcuations"""
    def __init__(self, screen_height):
        self.y = screen_height//2 # Start in the middle of the screen
        self.x = 64 # the x postion of the bird is static

        self.gravity = .5
        self.velocity = 0

        self.s_height = screen_height
        self.image = pygame.image.load('birb.png') # Load the bird image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    @property
    def rect(self):
        """A property that returns a rectangle used for collisions that is smaller than the image's rectangle for fairness"""
        rect = self.image.get_rect(center=(self.x, self.y))
        rect.x += 4
        rect.y += 4
        rect.w -= 8
        rect.h -= 8
        return rect
    
    def draw(self, root):
        root.blit(self.image, (self.x-(self.width//2), int(self.y-(self.height/2))))
        # pygame.draw.rect(root, (0, 0, 255), self.rect)
        # pygame.draw.circle(root, (255,255,255), (self.x, int(self.y)), 1)

    def update(self):
        """"This method updates the bird including gravity and what happens when the bird touches the bottom or the top of the screen"""
        self.velocity += self.gravity
        self.velocity *= 0.9
        self.y += self.velocity

        if self.y > self.s_height: # If the bird is at the bottom of the screen
            self.y = self.s_height # Move the bird the the bottom of the screen
            self.velocity = 0  # Set the velocity to 0

        if self.y < 0: # If the bird is at the top of the screen
            self.y = 0 # Move the bird to the bottom of the screen
            self.velocity = 0 # Set the velocity to 0

    def up(self):
        """This method moves the bird up"""
        self.velocity += -10

def setup():
    """This function sets up the program and can be used to reset the program retruns useful varables"""
    score = 0
    frame_count = 0

    pygame.init()

    screen_width = 400
    screen_height = 600

    root = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 32)

    bird = Bird(screen_height)

    pipe_list = []

    return score, frame_count, root, font, clock, bird, pipe_list, screen_width, screen_height

def draw(root, font, bird, pipe_list, score):
    """This function takes in varibles needed to draw the pipes and bird to the screen as well as update them and returns if the player hit the pipe or scored"""
    score_list = []
    add = None
    hit = None

    root.fill((135, 206, 235)) # Fill the background with a sky blue
    # root.fill((120, 127, 136)) # Fill the background with a smog grey

    # Go though the pipes backwards so deleting a pipe doesn't cause issues
    for i in range(len(pipe_list)-1, -1, -1):
        if not pipe_list[i].offscreen: # If the pipe is not offscreen
            pipe_list[i].update() # Update the pipe
            pipe_list[i].draw(root) # Draw the pipe
        else: # Else the pipe is offsceen
            pipe_list.pop(i) # Delete the pipe from the list

        result = pipe_list[i].hit(bird) # See if the bird hits the pipe 
        if result: # If the result exist
            hit = result.get('hit') 
            score = result.get('score')
            score_list.append(score)

        # If score add equals 1 
        if 1 in score_list:
            add = 1

    bird.update() # Update the bird
    bird.draw(root) # Draw the bird

    # Print the score onto the screen
    scr_screen = font.render(str(score), 1, (255,255,255))
    root.blit(scr_screen, (0,0))

    return add, hit


def main():
    """This funtion is the main function"""
    score, frame_count, root, font, clock, bird, pipe_list, screen_width, screen_height = setup() # Setup the window and varables

    # Game Loop 
    quit = False
    while not quit:
        clock.tick(60) # Limit the FPS to 60

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If you press the red x
                quit = True # Then quit
            elif event.type == pygame.KEYDOWN: # If we press any key
                bird.up() # Move the bird up
        
        if frame_count % 150 == 0: # Every 2.5 seconds or 150 frames add a new pipe
            pipe = Pipe(random.randint(75,screen_height-75), screen_width, 20, screen_height)
            pipe_list.append(pipe) 

        add, hit = draw(root, font, bird, pipe_list, score) # Draw the bird and pipes and get if we hit and if we scored

        if hit: # If we hit the pipe reset by calling setup  and restarting the game loop
            score, frame_count, root, font, clock, bird, pipe_list, screen_width, screen_height = setup()
            continue

        if add == 1: # If we scored then add 1 to the score
            score += add

        pygame.display.update() # Update the display

        frame_count += 1 # Increment the frame counter

if __name__ == '__main__': # If we run this file as the main script
    main()