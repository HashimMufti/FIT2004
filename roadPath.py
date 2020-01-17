"""
Name of File: roadPath.py
Author: Hashim Talal Mufti
Language: Python 3.7
Date of Creation: 24/05/2019
Last Edited: 31/05/2019
Description: This file contains three tasks, Task 1 is responsible for finding the quickest path from starting location
u to a destination v, using Dijksta's algorithm and a min heap. Task 2 is resposible for finding the quickest path
while avoiding cameras and tolls, this is known as the safe path. Task 3 is responsible for finding the quickest detour
path from a file containing a list of services.
List of Functions for Task 1:
buildGraph(self, FileName)
quickestPath(self, source, target)
List of Functions for Task 2:
augmentGraph(self, filename_camera, filename_toll)
quickestSafePath(self, source, target)
List of Functions for Task 3:
addService(self, filename_service)
quickestDetourPath(self, source, target)
"""
import sys      # Used to set an arbitrary max size, specific to any system for compatibility
import heapq    # Used built in heapq function (permission was provided in Moodle forums)

"""
Assignment 4 - FIT 2004, Semester 1, 2019
"""


class Graph:  # Graph class used for the Assignment

    def __init__(self):                         # Initializing Graph class
        self.cameras = []                       # Used to store positions of cameras
        self.tolls = []                         # Used to store positions of tolls
        self.services = []                      # Used to store positions of services
        self.visited = []                       # Used to store the positions of visited nodes
        self.Node_Array = []                    # Used to store distances to node
        self.maxVertex = -sys.maxsize - 1       # Arbitrary large value for comparison (infinity)
        self.tolls_left = []                    # Starting point of toll relative to right
        self.tolls_right = []                   # Ending points of toll relative to left

    """
    TASK 1 -> Finding the quickest path from source to destination.
    """

    def buildGraph(self, FileName):
        '''
        Description:        This function creates a Graph using FileName.
        Time Complexity:    O(N).
        Space Complexity:   O(N).
        Error Handle:       Not required, is handled by the caller function.
        Return:             Does not return a value.
        Precondition:       A FileName must be passed to this function.
        '''
        file = open(FileName, "r")                          # Opening the file
        for lines in file:                                  # Reading in every line in the file
            line = lines.split()                            # Splitting the line (linear time complexity)
            if int(line[0]) > int(self.maxVertex):          # Finding the max vertex by checking the start vertex
                self.maxVertex = int(line[0])               # Setting to max if greater
            if int(line[1]) > int(self.maxVertex):          # Finding the max vertex by checking the end vertex
                self.maxVertex = int(line[1])               # Setting to max if greater
        for x in range(int(self.maxVertex) + 1):            # Iterating through size of the greatest vertex + one
            self.Node_Array.append([])                      # Creating an space in the array for every iteration
        file2 = open(FileName, "r")                         # Opening the file again
        for lines in file2:                                 # Reading every line in the file
            line = lines.split()                            # Splitting the line (linear time complexity)
            tuple = (int(line[1]), int(line[2]))            # Creating a tuple of the end vertex and distance
            self.Node_Array[int(line[0])].append(tuple)     # Appending it to the location represented by start vertex

    def quickestPath(self, source, target):
        '''
        Description:        This function is responsible for finding the quickest safe path from source to target, this
                            is done by using a Dijkstra's algorithm and a min heap (see comments for further details).
        Time Complexity:    O(E log V) where V is the total number of nodes and E is the number of edges.
        Space Complexity:   O(E + V) where V is the total number of nodes and E is the number of edges.
        Error Handle:       Not required, is handled by the caller function.
        Return:             Solutions which contains the path and minimum distance, or will return [[], -1] as per
                            Assignment spec.
        Precondition:       Source and target must be passed to this function.
        '''
        quick_array = []                   # Used to store the minimum distance to the vertex (represented by the index)
        path_finder = []                   # Used to find the path between source and target
        path_finder_checker = []           # Used to check if a valid solution exists
        if int(source) == int(target):     # If the source is equal to the target, return target and 0
            solutions = []                 # Generating solutions array
            solutions.append(target)       # Appending target to solutions
            solutions = solutions[::-1]    # Flipping solutions
            return (solutions, 0)          # Return Assignment spec requirement
        for x in range(int(self.maxVertex) + 1):                 # Iterating through max vertex size + 1
            quick_array.append([sys.maxsize, x])                 # Dijkstra's algorithm, infinity at indexes
            path_finder.append([None])                           # Path finder used to trace route
            path_finder_checker.append([None])                   # Checker used to check if route exists
        quick_array[int(source)][0] = 0                          # Setting source to 0, Dijkstra's algorithm
        for x in range(len(quick_array) + 1):                    # Iterating through size of the array + 1
            heapq.heapify(quick_array)                           # Pushing all the elements into a heap
            self.visited.append(heapq.heappop(quick_array))      # Popping the minimum element in the heap into visited
            heapq.heapify(quick_array)                           # Recreating the heap
            if int(self.visited[-1][1]) == int(target):          # If the minimum element is the target
                solutions = []                                   # Create a solutions array
                solutions.append(target)                         # Append the target to the solutions
                while True:                                      # Keep repeating until return
                    if path_finder == path_finder_checker:       # If the path_finder is equal to checker, no route
                        return [[], -1]                          # Return Assignment spec requirement
                    value = path_finder[int(target)]             # Else, the required value is in path finder at target
                    solutions.append(value)                      # Append the required value to solutions
                    if int(value) == int(source):                # If the value is the source
                        solutions = solutions[::-1]              # Flip the solutions (linear time)
                        return (solutions, self.visited[-1][0])  # Return as spec required
                    else:
                        target = value                           # Else, set target to value and repeat to find route
            for neighbors in self.Node_Array[self.visited[-1][1]]:  # Check the children of the popped node
                (n_edge, n_distance) = neighbors  # Get the neighbor's edge and distance in tuple form
                count = 0  # Set count = 0
                for value in quick_array:  # For every value in the quick_array
                    (distance, edge) = value  # Get the quick_array index vertex's distance and edge in tuple form
                    if edge == n_edge:  # Compare the neighbor's edge to the vertex's edge
                        if int(n_distance + self.visited[-1][0]) < int(quick_array[count][0]):  # If new min lower
                            quick_array[count] = [n_distance + self.visited[-1][0], edge]  # Set new min in quick array
                            path_finder[edge] = int(self.visited[-1][1])  # Set path finder to reflect new route
                    count = count + 1  # Increment count
        return [[], -1]  # No solution exists, return Assignment spec requirement

    """
    TASK 2 -> Finding the quickest safe path from source to destination.
    """

    def augmentGraph(self, filename_camera, filename_toll):
        '''
        Description:        This function is responsible for reading in the cameras and tolls and storing them.
        Time Complexity:    O(N).
        Space Complexity:   O(N).
        Error Handle:       Not required, is handled by the caller function.
        Return:             Nothing.
        Precondition:       filename_camera and filename_toll must be passed to this function.
        '''
        file = open(filename_camera)                    # Opening the camera file
        for line in file:                               # For every line in the camera file
            self.cameras.append(int(line.strip('\n')))  # Append the line (cameras) to self.cameras, stripping new line
        file = open(filename_toll)                      # Opening the toll file
        for line in file:                               # For every line in toll
            self.tolls.append(line)                     # Append the line (toll) to self.tolls

    def quickestSafePath(self, source, target):
        '''
        Description:        This function is responsible for finding the quickest safe path from source to target.
        Time Complexity:    O(E log V), where V is the total number of nodes and E is the number of edges.
        Space Complexity:   O(E + V), where V is the total number of nodes and E is the number of edges.
        Error Handle:       Not required, is handled by the caller function.
        Return:             Returns either solutions which contains the path and minimum distance or it will return
                            [[], -1] as per Assignment spec.
        Precondition:       Source and target must be passed to this function.
        '''
        if source in self.cameras or target in self.cameras:    # No route exists
            return [[], -1]                                     # Return Assignment spec requirements
        for values in self.tolls:                               # For every value in self.tolls
            values = values.strip('\n')                         # Strip new line character
            value = values.split()                              # Split every line into two values
            self.tolls_left.append(int(value[0]))               # Put starting vertex into self.tolls_left
            self.tolls_right.append(int(value[1]))              # Put ending vertex into self.tolls_right
        quick_array = []                   # Used to store the minimum distance to the vertex (represented by the index)
        path_finder = []                   # Used to find the path between source and target
        path_finder_checker = []           # Used to check if a valid solution exists
        if int(source) == int(target):     # If the source is equal to the target, return target and 0
            solutions = []                 # Generating solutions array
            solutions.append(target)       # Appending target to solutions
            solutions = solutions[::-1]    # Flipping solutions
            return (solutions, 0)          # Return Assignment spec requirement
        for x in range(int(self.maxVertex) + 1):    # Iterating through max vertex size + 1
            quick_array.append([sys.maxsize, x])    # Dijkstra's algorithm, infinity at indexes
            path_finder.append([None])              # Path finder used to trace route
            path_finder_checker.append([None])      # Checker used to check if route exists
        quick_array[int(source)][0] = 0             # Setting source to 0, Dijkstra's algorithm
        for x in range(len(quick_array) + 1):       # Iterating through size of the array + 1
            heapq.heapify(quick_array)              # Pushing all the elements into a heap
            self.visited.append(heapq.heappop(quick_array))       # Popping the minimum element in the heap into visited
            heapq.heapify(quick_array)                            # Recreating the heap
            if int(self.visited[-1][1]) == int(target):           # If the minimum element is the target
                solutions = []                                    # Create a solutions array
                solutions.append(target)                          # Append the target to the solutions
                while True:                                       # Keep repeating until return
                    if path_finder == path_finder_checker:        # If the path_finder is equal to checker, no route
                        return [[], -1]                           # Return Assignment spec requirement
                    value = path_finder[int(target)]              # Else, the required value is in path finder at target
                    solutions.append(value)                       # Append the required value to solutions
                    if int(value) == int(source):                 # If the value is the source
                        solutions = solutions[::-1]               # Flip the solutions (linear time)
                        return (solutions, self.visited[-1][0])   # Return as spec required
                    else:
                        target = value                            # Else, set target to value and repeat to find route
            for neighbors in self.Node_Array[self.visited[-1][1]]:  # Check the children of the popped node
                (n_edge, n_distance) = neighbors                    # Get the neighbor's edge and distance in tuple form
                if n_edge in self.cameras:                          # If the n_edge is in cameras, ignore it
                    pass                                            # Ignore it
                else:                                               # Otherwise
                    if n_edge in self.tolls_right:                  # If the n_edge exists in as a child node
                        list_index = [n for n, x in enumerate(self.tolls_right) if x == n_edge]  # Generate indexes list
                        checker = False                                     # Set checker to False
                        for x in list_index:                                # Search through indexes
                            if self.tolls_left[x] == self.visited[-1][1]:   # If pair of parent and n_edge in tolls
                                checker = True                              # Set checker to True
                        if checker == False:                                # If checker is not True
                            count = 0                                       # Start count
                            for value in quick_array:                       # For values in quick_array
                                (distance, edge) = value                    # Turn tuple into distance and edge
                                if edge == n_edge:                          # Compare edge to neighboring edge
                                    if int(n_distance + self.visited[-1][0]) < int(quick_array[count][0]):  # Compare
                                        quick_array[count] = [n_distance + self.visited[-1][0], edge]  # Set new path
                                        path_finder[edge] = int(self.visited[-1][1])  # Update path finder with route
                                count = count + 1  # Increment count
                    else:   # If n_edge does not exist as a child node
                        count = 0                     # Set count = 0
                        for value in quick_array:     # For every value in the quick_array
                            (distance, edge) = value  # Get the quick_array index vertex's distance and edge in a tuple
                            if edge == n_edge:  # Compare the neighbor's edge to the vertex's edge
                                if int(n_distance + self.visited[-1][0]) < int(quick_array[count][0]):  # Compare min's
                                    quick_array[count] = [n_distance + self.visited[-1][0], edge]  # Set new min
                                    path_finder[edge] = int(self.visited[-1][1])  # Set path finder to reflect new route
                            count = count + 1   # Increment count
        return [[], -1]                         # No solution exists, return Assignment spec requirement

    """
    TASK 3 -> Finding the quickest detour path from source to destination.
    """

    def addService(self, filename_service):
        '''
        Description:        This function is responsible for adding services for Task 3.
        Time Complexity:    O(N).
        Space Complexity:   O(N).
        Error Handle:       Not required, is handled by the caller function.
        Return:             Nothing.
        Precondition:       A filename_service must be passed to this function.
        '''
        file = open(filename_service)                   # Opening the services file
        for line in file:                               # Read lines (service) in file
            self.services.append(line.strip('\n'))      # Stripping new line and appending vertex to self.services

    def quickestDetourPath(self, source, target):
        '''
        Description:        This function is responsible for finding the quickest detour path between source and target.
        Time Complexity:    O(E log V) where V is the total number of nodes and E is the total number of edges.
        Space Complexity:   O(E + V) where V is the total number of nodes and E is the total number of edges.
        Error Handle:       If an error occurs, it signifies that a path does not exist and is passed.
        Return:             checker which contains the route and the minimum distance, or will return [[], -1] if no
                            route exists, as per the Assignment spec.
        Precondition:       A source and target must be passed onto this function.
        '''
        checker = [[0],[99999999]]                      # Place holder for final values
        for value in self.services:                     # For every value in services
            main = []                                   # Main array
            saved = []                                  # Array to format answer for Assignment Spec
            saved2 = []                                 # Array to format answer for Assignment Spec
            try:                                        # If exception is raised, no path exists
                important = self.quickestPath(source, value)        # important contains path from source to value
                if important != [[], -1]:                           # If it isn't invalid
                    important2 = self.quickestPath(value, target)   # important2 contains path from value to target
                    if important2 != [[], -1]:                      # If it isn't invalid
                        for x in important[0]:                      # For every value in path from source to value
                            saved.append(int(x))                    # Append it to saved
                        count = 0                                   # Count to ignore repeating variable (first pos)
                        for x in important2[0]:                     # For every value in path from value to source
                            if count == 0:                          # Ignore repeating value
                                pass                                # Ignore repeating value
                            else:                                   # If it isn't repeating value
                                saved.append(int(x))                # Append it to saved, completing the path
                            count = count + 1                       # Increment count
                        value = int(important[1]) + int(important2[1])  # Adding distances between the two paths
                        saved2.append(value)                            # Appending the distance to saved2 for Spec
                        main.append(saved)                              # Appending saved to main array
                        main.append(saved2)                             # Appending saved2 to main array
                        if int(main[1][0]) < int(checker[1][0]):        # Comparing min distances to saved array
                            checker = main                              # Set if min in new array < saved array
            except:                                                     # Route doesn't exist
                pass                                                    # Pass, trying next service
        if checker[1] == [99999999]:                    # If checker value is unchanged to original set, no route
            return [[], -1]                             # Return Assignment Spec requirement
        else:                                           # Otherwise, a route exists
            r_array = checker[0]                        # Return array is equal to the path found
            r_main_tuple = (r_array, checker[1][0])     # Return tuple is equal to the array and the value in checker
            checker = r_main_tuple                      # checker is used to return tuple
        return checker                                  # Return checker


if __name__ == '__main__':
    try:
        print("---------------------------------------------------------------------")
        file1 = input("Enter the file name for the graph: ")
        file2 = input("Enter the file name for camera nodes: ")
        file3 = input("Enter the file name for the toll roads: ")
        file4 = input("Enter the file name for the service nodes: ")
        print("---------------------------------------------------------------------")
        source = input("Source node: ")
        target = input("Sink node: ")
        print("---------------------------------------------------------------------")
        graph = Graph()
        graph.buildGraph(file1)
        print("Quickest path:")
        try:
            (Route, Distance) = graph.quickestPath(source, target)
            count = 0
            while count < len(Route) - 1:
                print(Route[count], end=" ---> ")
                count = count + 1
            print(Route[-1])
            print("Time: ", Distance, "minute(s)")
        except:
            print("No path exists")
            print("Time: 0 minute(s)")
        print("---------------------------------------------------------------------")
        print("Safe quickest path:")
        graph = Graph()
        graph.buildGraph(file1)
        graph.augmentGraph(file2, file3)
        try:
            (Route, Distance) = graph.quickestSafePath(source, target)
            count = 0
            while count < len(Route) - 1:
                print(Route[count], end=" ---> ")
                count = count + 1
            print(Route[-1])
            print("Time: ", Distance, "minute(s)")
        except:
            print("No path exists")
            print("Time: 0 minute(s)")
        print("---------------------------------------------------------------------")
        print("Quickest detour path:")
        graph = Graph()
        graph.buildGraph(file1)
        graph.addService(file4)
        try:
            (Route, Distance) = graph.quickestDetourPath(source, target)
            count = 0
            while count < len(Route) - 1:
                print(Route[count], end=" ---> ")
                count = count + 1
            print(Route[-1])
            print("Time: ", Distance, "minute(s)")
            print("---------------------------------------------------------------------")
            print("Program end")
        except:
            print("No path exists")
            print("Time: 0 minute(s)")
    except:
        print("E R R O R")
        print("You have entered an incorrect value, a non existent file or gibberish!")
        print("R E R U N")