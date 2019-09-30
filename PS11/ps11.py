# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:


from __future__ import division
import math
import random
import pylab
import ps11_visualize



class Position(object):  ## Nothing to do
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

    
    def getNewPosition(self, angle, speed):
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
        return Position(new_x, new_y)





class RectangularRoom(object):
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

        print "width: {}, height: {}".format(self.width, self.height)
        print "self.tiles: {}".format(self.tiles)
        print "clean/total: {}/{}".format(self.getNumCleanedTiles(), self.getNumTiles())
        return ""
    


    def tile_dict(self):
        '''return a dict with tiles to be cleaned'''

        result = {}

        for i in range(0, self.width):
            for y in range(0, self.height):
                result[(i,y)] = False

        return result



    def reset_room(self):
        '''return the room into original state'''

        self.tiles = self.tile_dict()

        return self.tiles
    


    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """


        self.tiles[(int(pos.x),int(pos.y))] = True

        return self.tiles
    
        
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """

        try:
            if self.tiles[(int(m),int(n))] == True:
                return True

            else:
                return False
        except:
            return False
        

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """

        return len(self.tiles)



    def getNumCleanedTiles(self):
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

        cov = self.getNumCleanedTiles() / self.getNumTiles()
        
        return cov



    def getRandomPosition(self): 
        """
        Return a random position inside the room.

        returns: a Position object.
        """

        a = random.choice(list(self.tiles.keys()))

        b = Position(a[0],a[1])

        return b



    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """

        if self.tiles.get((int(pos.x),int(pos.y))) == None or pos.x < 0 or pos.y < 0:
            
            return False
        
        return True





class BaseRobot(object):
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
        self.angle = self.setRobotDirection()
        self.current_pos = self.room.getRandomPosition()
    


    def __str__(self):
        '''Print base data'''

        print "speed: {}".format(self.speed)
        print "angle: {}".format(self.angle)
        print "current_pos: {}, {}".format(self.current_pos.x,self.current_pos.y)
        

        return ""



    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """

        return self.current_pos



    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        
        return self.angle




    def setRobotPosition(self, pos):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """

        self.current_pos = pos.new_pos(self.angle, self.speed)

        return self.current_pos



    def setRobotDirection(self): ## (self, direction) old version
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """

        self.angle = random.randint(0,360)

        return self.angle





class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """

    def updatePositionAndClean(self): ## Move function
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        ## Check if new position exist
        if self.room.isPositionInRoom(self.current_pos.getNewPosition(self.angle, self.speed)) == False:
            self.angle = self.setRobotDirection() # not found, set new angle
##            print "Bang, hit the wall"
            return 

        else:
            ## move to new position, set current_pos
            self.current_pos = self.current_pos.getNewPosition(self.angle, self.speed)

        ## Clean the current_pos tile

        self.room.cleanTileAtPosition(self.current_pos)
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

    result = []

    
    for y in range(num_trials):

        switch = True

        the_room = RectangularRoom(width, height)
        robot_list = []
        ticks = 0


        for t in range(num_robots):
            robot_list.append(Robot(the_room, speed)) 


        if visualize == True:
            anim = ps11_visualize.RobotVisualization(num_robots, width, height)


        while switch == True:

            ticks += 1
            
            if visualize == True:
                anim.update(the_room, robot_list)

            if min_coverage <= the_room.get_coverage():
                if visualize == True:
                    anim.done()
                result.append([ticks])
                switch = False

            else:
                for i in robot_list:
                    i.updatePositionAndClean()
            
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

    size = [5,10,15,20,25]

    for i in size:
        a = runSimulation(1, 1.0, i, i, 0.75, 10, Robot)
        b = computeMeans(a)
        pylab.plot(i, b, "b.")

    pylab.title("Cleaning time and room size dependency")
    pylab.xlabel("Room size")
    pylab.ylabel("Step")
    pylab.show()



def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    

    for i in range(1,10):
        a = runSimulation(i, 1.0, 25, 25, 0.75, 10, Robot)
        b = computeMeans(a)
        pylab.plot(i, b, "b.")

        
    pylab.title("75% coverage, 25x25 room, various amount of robots")
    pylab.xlabel("Number of robots")
    pylab.ylabel("Step")
    pylab.show()



def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """

    ratio = lambda x,y: y/x
    size = [[20,20],[25,16],[40,10],[50,8],[80,5],[100,4]]
    
    for i in size:
        a = runSimulation(2, 1.0, i[0], i[1], 0.75, 10, Robot)
        b = computeMeans(a)
        pylab.plot(ratio(i[0],i[1]), b, "b.")
        print ratio(i[0],i[1])

        
    pylab.title("75% coverage, 2 robots, various size of rooms")
    pylab.xlabel("Ratio")
    pylab.ylabel("Step")
    pylab.show()




def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """

    color_list = ['r.', 'g.', 'b.', 'c.', 'm.']
    coverage_time = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    for i in range(1,6):
    
        for y in coverage_time:
            
            a = runSimulation(i, 1.0, 25, 25, y, 1, Robot)
            b = computeMeans(a)
            pylab.plot(y, b, color_list[i-1])
            print i, y, b

        
    pylab.title("Coverage percentage vs time, 25x25 room, 1 to 5 robots")
    pylab.xlabel("Percentage cleaned")
    pylab.ylabel("Step")
    pylab.show()




# === Problem 5

class RandomWalkRobot(Robot):
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

##    a = runSimulation(1, 1.0, 10, 10, 1, 25, Robot)
##    print computeMeans(a)
    showPlot4()
##    print dir(pylab)
