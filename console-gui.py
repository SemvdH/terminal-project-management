import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from enum import Enum
# doc: https://docs.python.org/3/howto/curses.html, https://docs.python.org/3/library/curses.html#module-curses.textpad

# color combos
CYAN_MAGENTA = 1
RED_BLACK = 2
MAGENTA_CYAN = 3
YELLOW_BLACK = 4
WHITE_BLUE = 5
CYAN_BLACK = 6
MAGENTA_BLACK = 7
WHITE_MAGENTA = 8
WHITE_GREEN = 9
WHITE_YELLOW = 10
WHITE_CYAN = 11

menu_width = 27
controls_lines = 5

STATUS_DONE = WHITE_GREEN
STATUS_WORKING = WHITE_CYAN
STATUS_IDLE = WHITE_MAGENTA

statuses = [STATUS_WORKING,STATUS_IDLE,STATUS_DONE,0]


# TODO add description viewing
# TODO add description editing
# TODO add adding of projects
# TODO add deleting of projects
# TODO add adding of tasks
# TODO add deleting of tasks
# TODO add indicator of project even when switching task

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
        self.status = Status.NONE

class Status(Enum):
    WORKING = 0
    IDLE = 1
    DONE = 2
    NONE = 3

    def prev(self):
        print("previous of {}".format(self))
        v = self.value - 1
        if v < 0:
            v = 3
        print("previous is {}".format(Status(v)))
        return Status(v)
    
    def next(self):
        print("next of {}".format(self))
        v = self.value + 1
        if v > 3:
            v = 0
        print("next is {}".format(Status(v)))
        return Status(v)

        

# TODO maybe get rid of this enum and just use a number
class SelectedWindow(Enum):
    PROJECTS = 1
    TASKS = 2

def get_x_pos_center(text: str):
    return curses.COLS // 2 - len(text) // 2

def draw_instructions(stdscr):
    controls = "CONTROLS"
    # draw line
    h, w = stdscr.getmaxyx()
    instructions_start = h - controls_lines-1
    stdscr.hline(instructions_start,0,curses.ACS_HLINE,menu_width//2 - len(controls)//2,curses.color_pair(MAGENTA_BLACK))
    stdscr.addstr(instructions_start,menu_width//2-len(controls)//2,controls,curses.color_pair(WHITE_MAGENTA))
    stdscr.hline(instructions_start,menu_width//2+len(controls)//2,curses.ACS_HLINE,menu_width//2-len(controls)//2+1,curses.color_pair(MAGENTA_BLACK))
    stdscr.addstr(instructions_start + 1, 0, "UP/DOWN - move selection")
    stdscr.addstr(instructions_start + 2, 0, "LEFT/RIGHT - switch section")
    stdscr.addstr(instructions_start + 3, 0, "SPACE - change task status")

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
        stdscr.attron(curses.color_pair(statuses[task.status.value]))
        stdscr.addstr(y,menu_width+1," " * (width-1))
        if i == idx and SelectedWindow(selected_window) == SelectedWindow.TASKS:
            stdscr.addstr(y, menu_width + 1, task.title, curses.A_REVERSE)
        else:
            stdscr.addstr(y, menu_width + 1, task.title)
        if task.status != Status.NONE:
            stdscr.addstr(y, menu_width + width - len(task.status.name), task.status.name)
        stdscr.attroff(curses.color_pair(statuses[task.status.value]))
        y = y + 1
    
    # draw color instructions
    legend = "LEGEND"
    instructions_start = h - controls_lines-1
    stdscr.hline(instructions_start,menu_width+1,curses.ACS_HLINE,width//2-len(legend)//2-1,curses.color_pair(MAGENTA_BLACK))
    stdscr.addstr(instructions_start, menu_width + width // 2 - len(legend)//2,legend,curses.color_pair(WHITE_MAGENTA))
    stdscr.hline(instructions_start,menu_width+width//2+len(legend)//2,curses.ACS_HLINE,width//2- len(legend)//2,curses.color_pair(MAGENTA_BLACK))

    stdscr.addstr(instructions_start + 1, menu_width + 1, " " * 3, curses.color_pair(STATUS_DONE))
    stdscr.addstr(instructions_start + 1,menu_width + 4 + width - 2*len("DONE"),"DONE",curses.color_pair(STATUS_DONE))
    stdscr.addstr(instructions_start + 2, menu_width + 1, " " * 3, curses.color_pair(STATUS_IDLE))
    stdscr.addstr(instructions_start + 2,menu_width + 4 + width - 2*len("IDLE"),"IDLE",curses.color_pair(STATUS_IDLE))
    stdscr.addstr(instructions_start + 3, menu_width + 1, " " * 3, curses.color_pair(STATUS_WORKING))
    stdscr.addstr(instructions_start + 3,menu_width + 4 + width - int(1.5*len("WORKING")+1),"WORKING",curses.color_pair(STATUS_WORKING))




def main(stdscr):

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_CYAN)


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
                selected_window = len(SelectedWindow)
            
            # set the task selection to the first for when we select a task next
            # because the previous task we were on might have more tasks than this one,
            # so we don't want the index to be out of bounds
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS: task_index = 0

        elif k == 32:  # space key
            projects[project_index].tasks[task_index].status = projects[project_index].tasks[task_index].status.next()

            
            
        
        stdscr.clear()
        draw_menu(stdscr, projects, project_index, selected_window)
        draw_tasks(stdscr, projects[project_index].tasks, selected_window, task_index)
        draw_instructions(stdscr)
        
        # draw botton text
        stdscr.addstr(stdscr.getmaxyx()[0]-1,0,"TPM by Sem van der Hoeven",)
        k = stdscr.getch()
        stdscr.refresh()

    curses.endwin()

# wrapper already calls noecho() and cbreak() and stdcr.keypad(True)
# it also resets the settings upon closing or upon error
wrapper(main)
