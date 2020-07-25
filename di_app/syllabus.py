from github import Github
import ast


class Syllabus:
    """
    Class to download locally the syllabus of DI learning.
    Through this class the webapp is finidng data and building required paths to speciic files

    methods:
    init
    get_list_of_course(repo)
    get_file_path(course, week, day, file):


    """
    def __init__(self):
        self.token = ''  # here comes token!! need to understand how to keep it secured and still online
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
        """
        Download the list of courses availabe on DI learning platform
        :param repo:
        :return:
        """
        list_of_courses = []
        cont = repo.get_contents("courses")
        for item in cont:
            name = item.name
            list_of_courses.append(name.strip(".json"))

        return list_of_courses

    def get_file_path(self,course, week, day, file):
        """
        Create path for a specific file that the user chose to view
        :param course:
        :param week:
        :param day:
        :param file:
        :return:
        """
        if day in ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]:
            day = self.syllabuses[course]['weeks'][week]['Days'][day]

            # check if file is "day" file or other resources

            for key, value in day.items():
                if key == "onsite":
                    if file in value["Class Files"]:
                        file_type = "class"
                    else:
                        file_type = "exercise"
                elif key == "online":
                    if file in value['Exercises']:
                        file_type = "exercise"
                else:
                    continue

            if file_type == "exercise":
                return self.syllabuses[course]['weeks'][week]["Notion"] + "/Exercises/" + \
                       file + ".md"
            else:
                return self.syllabuses[course]['weeks'][week]["Notion"] + "/" + \
                       file + ".md"

        elif day in self.syllabuses[course]['weeks'][week]["other resources"]:

            return self.syllabuses[course]['weeks'][week]["Notion"] + "/" + day + "/" + \
                   file + ".md"