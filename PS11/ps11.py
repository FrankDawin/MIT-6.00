# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:


from __future__ import division
import math
import random
import pylab
import ps11_visualize



class position(object):  ## Nothing to do
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y


    def __str__(self):
        '''print function'''

        print "x: {}, y: {}".format(self.x, self.y)

        return ""


    def getX(self):
        return self.x


    def getY(self):
        return self.y

    
    def new_pos(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return position(new_x, new_y)





class room(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """


    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """

        self.width = width
        self.height = height
        self.tiles = self.tile_dict()
       


    def __str__(self):

##        print "width: {}, height: {}".format(self.width, self.height)
##        print "self.tiles: {}".format(self.tiles)
        print "clean/total: {}/{}".format(self.num_clean_tiles(), self.total_tiles())
        return ""
    


    def tile_dict(self):
        '''return a dict with tiles to be cleaned'''

        result = {}

        for i in range(1, self.width+1):
            for y in range(1, self.height+1):
                result[(i,y)] = False

        return result



    def reset_room(self):
        '''return the room into original state'''

        self.tiles = self.tile_dict()

        return self.tiles
    


    def clean(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """


        self.tiles[(int(pos.x),int(pos.y))] = True

        return self.tiles
    
        
        
    def is_clean(self, pos):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """

        if self.tiles[(int(pos.x),int(pos.y))] == True:
            return True

        else:
            return False

        

    def total_tiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """

        return len(self.tiles)



    def num_clean_tiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """

        count = 0

        for i in self.tiles:
            if self.tiles[i] == True:
                count += 1

        return count



    def get_coverage(self):
        '''Return a coverage as a float representing the percentage cleaned (0 to 1)'''

        cov = self.num_clean_tiles() / self.total_tiles()

        return cov



    def random_pos(self): 
        """
        Return a random position inside the room.

        returns: a Position object.
        """

        a = random.choice(list(self.tiles.keys()))

        b = position(a[0],a[1])

        return b



    def pos_exist(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """

    
        if self.tiles.get((int(pos.x),int(pos.y))) == None:
            
            return False
        
        return True





class robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """



    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """

        self.room = room
        self.speed = speed                  
        self.angle = self.set_angle()
        self.current_pos = self.room.random_pos()
    


    def __str__(self):
        '''Print base data'''

##        print "speed: {}".format(self.speed)
        print "angle: {}".format(self.angle)
        print "current_pos: {}, {}".format(self.current_pos.x,self.current_pos.y)
        

        return ""



    def get_pos(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """

        return self.current_pos



    def get_angle(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        
        return self.angle




    def set_pos(self, pos):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """

        self.current_pos = pos.new_pos(self.angle, self.speed)

        return self.current_pos



    def set_angle(self): ## (self, direction) old version
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """

        self.angle = random.randint(0,360)

        return self.angle





class robot_a(robot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """

    def update_clean(self): ## Move function
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        ## Check if new position exist
        if self.room.pos_exist(self.current_pos.new_pos(self.angle, self.speed)) == False:
            self.angle = self.set_angle() # not found, set new angle
##            print "Bang, hit the wall"
            return 

        else:
            ## move to new position, set current_pos
            self.current_pos = self.current_pos.new_pos(self.angle, self.speed)

        ## Clean the current_pos tile

        self.room.clean(self.current_pos)
##        print "Tile cleaned"
        return 




def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize=False):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """

    

    sim_count = 0
    step = 0
    the_room = room(width, height)

    anim = ps11_visualize.RobotVisualization(num_robots, width, height)

    while sim_count < num_trials:

        
        rob = robot_a(the_room, speed)

        for i in range(num_trials):

##            print "\nStep {} ----------------".format(step)
##            print rob
##            print the_room
            anim.update(the_room, rob)
            step += 1

            if min_coverage <= the_room.get_coverage():
                sim_count += 1
                the_room.reset_room()
                anim.done()
                return step

            else:
                rob.update_clean()
                


def multiple_sim(amt):
    '''Run multiple roomba simulation'''

    result = []
    count = 0
    

    while amt >= count:
        a = runSimulation(1, 1.0, 3, 4, 0.5, 1, robot_a)
        b = runSimulation(1, 1.0, 3, 4, 0.5, 1, robot_a)
        c = runSimulation(1, 1.0, 3, 4, 0.5, 1, robot_a)
        result.append([a,b,c])
        count += 1

    print result

    return result
    
    

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means


# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    # TODO: Your code goes here

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    # TODO: Your code goes here

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    # TODO: Your code goes here

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    # TODO: Your code goes here


# === Problem 5

class RandomWalkRobot(robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    # TODO: Your code goes here


# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    # TODO: Your code goes here




if __name__ == "__main__":
    runSimulation(1, 1.0, 3, 4, 0.5, 1, robot_a)

##    a = multiple_sim(500)
##    
##    print computeMeans(a)
    
