"""
Project 4C
Canvas Analyzer
CISC108 Honors
Fall 2019

Access the Canvas Learning Management System and process learning analytics.

Edit this file to implement the project.
To test your current solution, run the `test_my_solution.py` file.
Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: YOUR NAME HERE
"""
import matplotlib.pyplot as plt
import canvas_requests
import datetime

__version__ = 7


# 1) main
def main(user_id: str):
    '''
    Consumes a user token and calls other functions

    Args:
        user_id (str): The string of text that represents the user token
    '''
    user = canvas_requests.get_user(user_id)
    print_user_info(user)
    courses = canvas_requests.get_courses(user_id)
    filtered_courses = filter_available_courses(courses)
    print_courses(filtered_courses)
    course_ids = get_course_ids(filtered_courses)
    course_id = choose_course(course_ids)
    submissions = canvas_requests.get_submissions(user_id, course_id)
    summarize_points(submissions)
    summarize_groups(submissions)
    plot_scores(submissions)
    plot_grade_trends(submissions)

# 2) print_user_info
def print_user_info(user: dict):
    '''
    Consumes a User dictionary and prints out the user's name, title, primary email, and bio.

    Args:
        user (dict): dictionary that has information about the user
    '''
    print('Name: ' + user['name'])
    print('Title: ' + user['title'])
    print('Primary Email: ' + user['primary_email'])
    print('Bio: ' + user['bio'])

# 3) filter_available_courses
def filter_available_courses(courses: [dict]) -> [dict]:
    '''
    Consumes a list of Course dictionaries and returns a list of Course dictionaries where the workflow_state key's
    value is 'available' ).

     Args:
        courses (list): a list of course dictionaries

    Returns:
        list: The modified version of the list of course dictionaries.
    '''
    available_list = []
    for course in courses:
        if course['workflow_state'] == 'available':
            available_list.append(course)
    return available_list

# 4) print_courses
def print_courses(courses: [dict]):
    '''
    Consumes a list of Course dictionaries and prints out the ID and name of each course on separate lines.

    Args:
        courses (list): a list of course dictionaries

   '''
    for course in courses:
        print(str(course['id']) + ' : ' + str(course['name']))

# 5) get_course_ids
def get_course_ids(courses: [dict]) -> [int]:
    '''
    Consumes a list of Course dictionaries and produces a list of integers representing course IDs.

    Args:
        courses (list): a list of course dictionaries
    Returns:
        list: new list of integers that are course ID's.
    '''

    ids = []
    for course in courses:
        ids.append(course['id'])
    return ids

# 6) choose_course

def choose_course(ids: [int]) -> int:
    '''
    Consumes a list of integers representing course IDs and prompts the user to enter a valid ID, and then
    produces an integer representing the user's chosen course ID. If the user does not enter a valid ID, the
    function repeatedly loops until they type in a valid ID.

    Args:
        ids (list): a list of course ids that are integers
    Returns:
        int: the ID that the user chose.
    '''

    chosen_id = int(input('Enter a valid ID'))
    while chosen_id not in ids:
        chosen_id = int(input('Enter a valid ID'))
    return chosen_id

# 7) summarize_points
def summarize_points(submissions: [dict]):
    '''
    Consumes a list of Submission dictionaries and prints out three summary statistics about the submissions where there is a score

    Args:
        submissions (list): a list of submission dictionaries

    '''
    points_possible_so_far = 0
    points_obtained = 0
    for submission in submissions:
        if submission['score'] != None:
            points_possible_so_far += submission['assignment']['points_possible'] * submission['assignment']['group'][
                'group_weight']
            points_obtained += submission['score'] * submission['assignment']['group']['group_weight']
    current_grade = round(points_obtained / points_possible_so_far * 100)
    print('Points possible so far: ' + str(points_possible_so_far))
    print('Points obtained: ' + str(points_obtained))
    print('Current grade: ' + str(current_grade))

# 8) summarize_groups
def summarize_groups(submissions: [dict]):
    '''
    Consumes a list of Submission dictionaries and prints out the group name and unweighted grade for each group.

    Args:
        submissions (list): a list of submission dictionaries

     '''
    group_scores = {}
    possible_points = {}
    unweighted_grades = {}
    for submission in submissions:
        if submission['score'] != None:
            if submission['assignment']['group']['name'] in group_scores:
                group_scores[submission['assignment']['group']['name']] += submission['score']
            else:
                group_scores[submission['assignment']['group']['name']] = submission['score']
    for submission in submissions:
        if submission['score'] is not None:
            if submission['assignment']['group']['name'] in possible_points:
                possible_points[submission['assignment']['group']['name']] += submission['assignment']['points_possible']
            else:
                possible_points[submission['assignment']['group']['name']] = submission['assignment']['points_possible']
    for key in group_scores.keys():
        unweighted_grades[key] = round(group_scores[key] / possible_points[key] * 100)
    for key in unweighted_grades.keys():
        print(key, ":", unweighted_grades[key])



# 9) plot_scores
def plot_scores(submissions: [dict]):
    '''
    Consumes a list of Submission dictionaries and plots each submissions' grade as a histogram.

    Args:
        submissions (list): a list of submission dictionaries

    '''
    grades = []
    for submission in submissions:
        if submission['score'] != None and submission['assignment']['points_possible'] > 0:
            grades.append(((submission['score'] * 100) / submission['assignment']['points_possible']))
    plt.hist(grades)
    plt.title('Distribution of Grades')
    plt.xlabel('Grades')
    plt.ylabel('Number of Assignments')
    plt.show()


# 10) plot_grade_trends
def low_points(submissions: [dict]) -> [int]:
    low_points = []
    for submission in submissions:
        weight = submission['assignment']['group']['group_weight']
        score = submission['score']
        if submission['workflow_state'] == 'graded':
            low_points.append(100 * score * weight)
        else:
            low_points.append(0)
    return low_points


def high_points(submissions: [dict]) -> [int]:
    high_points = []
    for submission in submissions:
        weight = submission['assignment']['group']['group_weight']
        score = submission['score']
        points = submission['assignment']['points_possible']
        if submission['workflow_state'] == 'graded':
            high_points.append(100 * score * weight)
        else:
            high_points.append(100 * points * weight)
    return high_points


def running_sum(points:list):
    running_sum = 0
    running_sums = []
    running_points =[]
    for point in points:
        running_sum = running_sum + point
        running_sums.append(running_sum)
    return running_sums




def plot_grade_trends(submissions: [dict]):
    '''
    Consumes a list of Submission dictionaries and plots the grade trend of the submissions as a line plot.
    The grade trend contains three lines (ordered by the assignments' due_at date) that show you the range
    of grades you could get in the course: Highest, Lowest, Maximum.

    Args:
        submissions (list): a list of submission dictionaries

    '''

    max_points = []
    highest = []
    lowest = []
    maximum = []
    submission_dates = []
    for submission in submissions:
        submission_date = submission['assignment']['due_at']
        submission_dates.append(datetime.datetime.strptime(submission_date, "%Y-%m-%dT%H:%M:%SZ"))
    for submission in submissions:
        max_points.append(100 * (submission['assignment']['points_possible']) * submission['assignment']['group']['group_weight'])
    total_max = sum(max_points) / 100
    running_high = running_sum(high_points(submissions))
    running_low = running_sum(low_points(submissions))
    running_max = running_sum(max_points)
    for point in running_high:
        highest.append(point/total_max)
    for point in running_low:
        lowest.append(point/total_max)
    for point in running_max:
        maximum.append(point/total_max)

    plt.title("Grade Trend")
    plt.plot(submission_dates, highest, label="Highest")
    plt.plot(submission_dates, lowest, label="Lowest")
    plt.plot(submission_dates, maximum, label="Maximum")
    plt.legend()
    plt.ylabel("Grade")
    plt.show()












# Keep any function tests inside this IF statement to ensure
# that your `test_my_solution.py` does not execute it.
if __name__ == "__main__":
    main('hermione')
    # main('ron')
    # main('harry')

    # https://community.canvaslms.com/docs/DOC-10806-4214724194
    # main('YOUR OWN CANVAS TOKEN (You know, if you want)')
