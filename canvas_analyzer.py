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

__version__ = 7


# 1) main
def main(user_id: str):
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

# 2) print_user_info
def print_user_info(user: dict):
    print('Name: ' + user['name'])
    print('Title: ' + user['title'])
    print('Primary Email: ' + user['primary_email'])
    print('Bio: ' + user['bio'])

# 3) filter_available_courses
def filter_available_courses(courses: [dict]) -> [dict]:
    available_list = []
    for course in courses:
        if course['workflow_state'] == 'available':
            available_list.append(course)
    return available_list

# 4) print_courses
def print_courses(courses: [dict]):
    for course in courses:
        print(str(course['id']) + ' : ' + str(course['name']))

# 5) get_course_ids
def get_course_ids(courses: [dict]) -> [int]:
    ids = []
    for course in courses:
        ids.append(course['id'])
    return ids

# 6) choose_course
def choose_course(ids: [int]) -> int:
    chosen_id = int(input('Enter a valid ID'))
    while chosen_id not in ids:
        chosen_id = int(input('Enter a valid ID'))
    return chosen_id

# 7) summarize_points
def summarize_points(submissions: [dict]):
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
    group_scores = {}
    possible_points = {}
    for submission in submissions:
        if submissions != None:
            if submission['assignment']['group']['name'] not in group_scores:
                group_scores[submissions['assignment']['group']['name']] = 0
                possible_points[submissions['assignment']['group']['name']] = 0
        group_scores[submissions['assignment']['group']['name']] += submission['score']
        possible_points[submissions['assignment']['group']['name']] = submission['assignment']['points_possible'] + possible_points[submissions['assignment']['group']['name']]
    for submissions["assignment"]["group"]["name"] in group_scores:
        k,v = group_scores[submissions["assignment"]["group"]["name"]],possible_points[submission['assignment']['points_possible']]
        print(submission['assignment']['points_possible'], ":", round(100*k/v))






# 9) plot_scores
def plot_scores(submissions: [dict]):
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
def plot_grade_trends(submissions: [dict]):
    max_points = []
    for submission in submissions:
        max_points.append(
            100 * (submission['assignment']['points_possible']) * submission['assignment']['group']['group_weight'])

    total_max = sum(max_points / 100)

    if submission['workflow_state'] == 'graded':
        low_score = submission['score']
    else:
        low_score = 0

    low_points = 100 * (low_score) * (submission['assignment']['group']['group_weight'])

    if submission['workflow_state'] == 'graded':
        high_score = submission['score']
    else:
        high_score = submission['assignment']['points_possible']
    high_points = 100 * (high_score) * (submission['assignment']['group']['group_weight'])


# Keep any function tests inside this IF statement to ensure
# that your `test_my_solution.py` does not execute it.
if __name__ == "__main__":
    main('hermione')
    # main('ron')
    # main('harry')

    # https://community.canvaslms.com/docs/DOC-10806-4214724194
    # main('YOUR OWN CANVAS TOKEN (You know, if you want)')
