"""Vehicles Routing Problem (VRP) with Time Windows."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
import time as t


def create_data_model():
    f = open('test.txt', 'r')
    allData = []
    for line in f:
        allData.append(refineLine(line))
    f.close()
    """Stores the data for the problem."""
    data = {}
    data['time_matrix'] = []
    # Creating time matrix using distance between locations
    # multiply by (average demand + 1)
    for r in range(len(allData)):
        data['time_matrix'].append([])
        for c in range(len(allData)):
            distance = distance_between(
                allData[r][1], allData[r][2], allData[c][1], allData[c][2])
            time = distance * ((allData[r][3] + allData[c][3])/200 + 1)/10
            data['time_matrix'][r].append(int(time))

    # Creating time windows
    #
    data['time_windows'] = []
    for p in range(len(allData)):
        data['time_windows'].append((int(allData[p][4]), int(allData[p][5])))

    """ data['time_matrix'] = [
        [0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7],
        [6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14],
        [9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9],
        [8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16],
        [7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14],
        [3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8],
        [6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5],
        [2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10],
        [3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6],
        [2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5],
        [6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4],
        [6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10],
        [4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8],
        [4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6],
        [5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2],
        [9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9],
        [7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0],
    ]
    data['time_windows'] = [
        (0, 5),  # depot
        (7, 12),  # 1
        (10, 15),  # 2
        (16, 18),  # 3
        (10, 13),  # 4
        (0, 5),  # 5
        (5, 10),  # 6
        (0, 4),  # 7
        (5, 10),  # 8
        (0, 3),  # 9
        (10, 16),  # 10
        (10, 15),  # 11
        (0, 5),  # 12
        (5, 10),  # 13
        (7, 8),  # 14
        (10, 15),  # 15
        (11, 15),  # 16
    ] """
    data['num_vehicles'] = 3
    data['depot'] = 0
    return data


def distance_between(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def refineLine(line):
    numbers = []
    currentnumber = ""
    for c in line:
        if (c == ' ' and currentnumber != ""):
            numbers.append(float(currentnumber))
            currentnumber = ''
        elif (c != ' '):
            currentnumber += c
    return numbers


def print_solution(data, manager, routing, solution):
    f = open("output.txt", 'w')
    """Prints solution on console."""
    f.write(f'Objective: {solution.ObjectiveValue()}')
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            solution.Min(time_var))
        f.write("\n")
        f.write(plan_output)
        total_time += solution.Min(time_var)
    f.write('Total time of all routes: {}min'.format(total_time))
    f.close()


def main():
    currentTime = t.time()
    """Solve the VRP with time windows."""
    print("Instantiate the data problem.")
    data = create_data_model()

    print("Create the routing index manager.")
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'], data['depot'])

    print("Create Routing Model.")
    routing = pywrapcp.RoutingModel(manager)

    print("Create and register a transit callback.")

    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    print("Define cost of each arc.")
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    print("Add Time Windows constraint.")
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        30000000000,  # allow waiting time
        30000000000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    print("Add time window constraints for each location except depot.")
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    print("Add time window constraints for each vehicle start node.")
    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0],
            data['time_windows'][depot_idx][1])

    print("Instantiate route start and end times to produce feasible times.")
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    print("Setting first solution heuristic.")
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    print("Solve the problem.")
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print("Am solving the problem")
        print_solution(data, manager, routing, solution)
    print("failed")
    print(t.time() - currentTime)


if __name__ == '__main__':
    main()
