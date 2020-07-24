from github import Github
import ast


class Syllabus:

    def __init__(self):
        self.token = '1625be1949a00603fa29bfda296abf1ca19876d2'  # here comes token!! need to understand how to keep it secured and still online
        self.owner = 'arturisto'
        self.g = Github(self.token)
        self.u = self.g.get_user()
        self.repo = self.u.get_repo("DI-Learning-Exercises")  # get repo where the courses are stored

        # get list of courses
        self.list_of_courses = self.get_list_of_courses(self.repo)

        self.syllabuses = {}

        # get syllabus of all of the courses
        for course in self.list_of_courses:
            course_path = "courses/" + course + ".json"
            cont = self.repo.get_contents(course_path)  # get syllabus
            byte_str = cont.decoded_content  # decoded repo data
            dict_str = byte_str.decode("UTF-8")  # parse the bytes to string
            self.syllabuses[course] = ast.literal_eval(dict_str)  # eval string to dict

    def get_list_of_courses(self, repo):
        list_of_courses = []
        cont = repo.get_contents("courses")
        for item in cont:
            name = item.name
            list_of_courses.append(name.strip(".json"))

        return list_of_courses
