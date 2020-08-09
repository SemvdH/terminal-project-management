import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from enum import Enum
# doc: https://docs.python.org/3/howto/curses.html, https://docs.python.org/3/library/curses.html#module-curses.textpad
CYAN_MAGENTA = 1
RED_BLACK = 2
MAGENTA_CYAN = 3
YELLOW_BLACK = 4
WHITE_BLUE = 5
CYAN_BLACK = 6
menu_width = 20

ree = 30


"""
    COLOR_BLACK
    COLOR_RED
    COLOR_GREEN
    COLOR_YELLOW
    COLOR_BLUE
    COLOR_MAGENTA
    COLOR_CYAN
    COLOR_WHITE
    """

class Project:
    def __init__(self, title: str):
        self.title = title
        self.tasks = []
    
    def addTask(self, task):
        self.tasks.append(task)
    
    def removeTask(self, task):
        self.tasks.remove(task)

class Task:
    def __init__(self,title: str,desc=""):
        self.title = title
        self.status = Status.IDLE

class Status(Enum):
    DONE = 1
    WORKING = 2
    IDLE = 3

# TODO maybe get rid of this enum and just use a number
class SelectedWindow(Enum):
    PROJECTS = 1
    TASKS = 2
    DESCRIPTION = 3

def get_x_pos_center(text: str):
    return curses.COLS // 2 - len(text) // 2

def draw_menu(stdscr, projects: list, idx: int, selected_window):
    # draw line
    stdscr.vline(0, menu_width, curses.ACS_VLINE, stdscr.getmaxyx()[0] - 1, curses.color_pair(CYAN_BLACK))

    # draw project title
    title = "PROJECTS"
    title_start = menu_width // 2 - len(title) // 2
    stdscr.attron(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)
    stdscr.addstr(0,0," " * (title_start-1))
    stdscr.addstr(0, title_start-1, title)
    stdscr.addstr(0, len(title) + title_start - 1, " " * (menu_width - (len(title) + title_start)+1))
    stdscr.attroff(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)

    # draw projects
    y = 1
    for project_index, project in enumerate(projects):
        if project_index == idx and SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
            stdscr.addstr(y, 0, project.title,curses.A_REVERSE)
        else:    
            stdscr.addstr(y, 0, project.title)
        y = y + 1

def draw_tasks(stdscr, tasks, selected_window,idx):
    h, w = stdscr.getmaxyx()

    # draw middle devidor line
    stdscr.vline(0, w // 2, curses.ACS_VLINE, h - 1, curses.color_pair(CYAN_BLACK))

    # draw tasks title
    title = "TASKS"
    width = w//2 - menu_width
    title_start = menu_width + (width//2 - len(title)//2)
    stdscr.attron(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)
    stdscr.addstr(0, menu_width + 1, " " * (title_start - menu_width))
    stdscr.addstr(0,title_start,title)
    stdscr.addstr(0,title_start + len(title), " " * (w//2 - (title_start + len(title))))
    stdscr.attroff(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)
    
    # draw task names
    y = 1
    for i, task in enumerate(tasks):
        if i == idx and SelectedWindow(selected_window) == SelectedWindow.TASKS:
            stdscr.addstr(y, menu_width + 1, task.title,curses.A_REVERSE)
        else:
            stdscr.addstr(y, menu_width + 1, task.title)
        y = y + 1
    

def main(stdscr):

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)

    k = 0  # input key
    project_index = 0
    task_index = 0
    selected_window = 1
    projects = []
    test_project = Project("Test")
    test_project.addTask(Task("testtask", "testdesc"))
    test_project.addTask(Task("testtask2", "testdesc2"))
    test_project.addTask(Task("testtask3", "testdesc3"))
    projects.append(test_project)
    test_project2 = Project("Test2")
    test_project2.addTask(Task("yeet"))
    test_project2.addTask(Task("yeet2"))
    test_project2.addTask(Task("yeet3"))
    projects.append(test_project2)


    while (k != ord('q')):
        if k == ord('e'):
            editing = not editing
        elif k == 450:  # up key
            # only move the projects selection if we're on that pane
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS: 
                project_index = project_index - 1
                if project_index < 0: project_index = len(projects) - 1
            # only move the task selection if we're on that pane
            elif SelectedWindow(selected_window) == SelectedWindow.TASKS:
                task_index = task_index - 1
                if task_index < 0: task_index = len(projects[project_index].tasks)-1
        
        elif k == 456:  # down key
            # only move the projects selection if we're on that pane
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                project_index = project_index + 1
                if project_index > len(projects) - 1: project_index = 0
            # only move the task selection if we're on that pane
            elif SelectedWindow(selected_window) == SelectedWindow.TASKS:
                task_index = task_index + 1
                if task_index > len(projects[project_index].tasks) - 1: task_index = 0
        
        elif k == 454: # right key
            selected_window = selected_window + 1
            if selected_window > len(SelectedWindow):
                selected_window = 1

            # set the task selection to the first for when we select a task next
            # because the previous task we were on might have more tasks than this one,
            # so we don't want the index to be out of bounds
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS: task_index = 0
        
        elif k == 452: # left key
            selected_window = selected_window - 1
            if selected_window < 1:
                selected_window = 3
            
            # set the task selection to the first for when we select a task next
            # because the previous task we were on might have more tasks than this one,
            # so we don't want the index to be out of bounds
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS: task_index = 0
            
        
        stdscr.clear()
        draw_menu(stdscr, projects, project_index, selected_window)
        draw_tasks(stdscr, projects[project_index].tasks,selected_window,task_index)
        
        # draw botton text
        stdscr.addstr(stdscr.getmaxyx()[0]-1,0,"TPM by Sem van der Hoeven",)
        k = stdscr.getch()
        stdscr.refresh()

    curses.endwin()

# wrapper already calls noecho() and cbreak() and stdcr.keypad(True)
# it also resets the settings upon closing or upon error
wrapper(main)
