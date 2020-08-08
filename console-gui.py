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

class Project:
    def __init__(self, title: str):
        self.title = title
        self.tasks = []
    
    def addTask(self, task):
        self.tasks.append(task)
    
    def removeTask(self, task):
        self.tasks.remove(task)

class Task:
    def __init__(self,name: str,desc=""):
        self.name = name
        self.status = Status.IDLE

class Status(Enum):
    DONE = 1
    WORKING = 2
    IDLE = 3

def get_x_pos_center(text: str):
    return curses.COLS // 2 - len(text) // 2

def draw_menu(stdscr, projects: list, idx: int):
    menu_width = 20
    # draw line
    stdscr.attron(curses.color_pair(RED_BLACK))
    stdscr.vline(0, menu_width, curses.ACS_VLINE, stdscr.getmaxyx()[0] - 1)
    stdscr.attroff(curses.color_pair(RED_BLACK))

    # draw project title
    title = "PROJECTS"
    title_start = menu_width // 2 - len(title) // 2
    stdscr.attron(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)
    stdscr.addstr(0,0," " * (title_start-1))
    stdscr.addstr(0, title_start-1, title)
    stdscr.addstr(0, len(title) + title_start - 1, " " * (menu_width - (len(title) + title_start)))
    stdscr.attroff(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)

    # draw projects
    y = 1
    for i, project in enumerate(projects):
        if i == idx:
            stdscr.addstr(y, 0, project.title,curses.A_REVERSE)
        else:    
            stdscr.addstr(y, 0, project.title)
        y = y + 1

def main(stdscr):

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

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)

    k = 0 # input key
    i = 0 # projects index
    projects = []
    test_project = Project("Test")
    test_project.addTask(Task("testtask", "testdesc"))
    projects.append(test_project)
    
    while (k != ord('q')):

        if k == ord('e'):
            editing = not editing
        elif k == 450:  # up key
            i = i - 1
            if i < 0:
                i = len(projects) - 1
        elif k == 456:  # down key
            i = i + 1
            
            if i > len(projects) - 1:
                i = 0
            
        
        

        stdscr.clear()
        draw_menu(stdscr,projects,i)

        # add the text box
            # editwin = curses.newwin(10, 30, 5, edit_window_x)
            # editwin.border()
            # rectangle(stdscr, 4,edit_window_x - 1, 1+10+1 + 4, 1+30+1 + edit_window_x - 1)
            # stdscr.refresh()
            # box = Textbox(editwin)
        # Wait for next input
        k = stdscr.getch()
        stdscr.refresh()

    curses.endwin()

# wrapper already calls noecho() and cbreak() and stdcr.keypad(True)
# it also resets the settings upon closing or upon error
wrapper(main)
