import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from enum import Enum
import pickle

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
FILENAME = "data"

menu_width = 27
controls_lines = 9
editing = False


STATUS_DONE = WHITE_GREEN
STATUS_WORKING = WHITE_CYAN
STATUS_IDLE = WHITE_MAGENTA

statuses = [STATUS_WORKING, STATUS_IDLE, STATUS_DONE, 0]


# TODO add controls for adding projects, tasks and deleting

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
    def __init__(self, title: str, desc: str):
        self.title = title
        self.status = Status.NONE
        self.desc = desc


# TODO maybe get rid of this enum and just use a number
class Status(Enum):
    WORKING = 0
    IDLE = 1
    DONE = 2
    NONE = 3

    def prev(self):
        v = self.value - 1
        if v < 0:
            v = 3
        return Status(v)

    def next(self):
        v = self.value + 1
        if v > 3:
            v = 0
        return Status(v)


class SelectedWindow(Enum):
    PROJECTS = 1
    TASKS = 2


def save(projects: list):
    with open(FILENAME, 'wb') as savefile:
        pickle.dump(projects, savefile, pickle.HIGHEST_PROTOCOL)


def load():
    try:
        with open(FILENAME, 'rb') as data:
            loaded = pickle.load(data)
            return loaded
    except FileNotFoundError as err:
        temp_project = Project("Example project")
        temp_project.addTask(Task(
            "Example task", "This is an example of a task description.\nIt can be used to provide some extra information about the task."))
        return [temp_project]


def delete_project(stdscr, projects: list, project_index):

    h, w = stdscr.getmaxyx()
    window_y = h // 2 - 3
    window_x = w // 2 - 25
    window = curses.newwin(6, 50, window_y, window_x)
    window.clear()
    window.border()

    window.addstr(0, 5, "DELETE PROJECT", curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2, 1, "Delete project '" +
                  projects[project_index].title + "'?")

    si = 1
    # highlight the option yes if the selected index = 1, otherwise highlight no
    window.addstr(4, 10, "YES", (2097152 << 1) >> (si == 1))
    window.addstr(4, 35, "NO", (2097152 << 1) >> (si != 1))

    k = 0
    while (k != 10):

        if k == curses.KEY_RIGHT or k == 454:
            si = 2 if si == 1 else 1

        elif k == curses.KEY_LEFT or k == 452:
            si = 1 if si == 2 else 2

        # highlight the option yes if the selected index = 1, otherwise highlight no
        window.addstr(4, 10, "YES", (2097152 << 1) >> (si == 1))
        window.addstr(4, 35, "NO", (2097152 << 1) >> (si != 1))

        window.refresh()
        stdscr.refresh()
        k = stdscr.getch()
        if k == 10:
            if si == 1:
                projects.remove(projects[project_index])


def delete_task(stdscr, project, task_index):
    h, w = stdscr.getmaxyx()
    window_y = h // 2 - 3
    window_x = w // 2 - 25
    window = curses.newwin(6, 50, window_y, window_x)
    window.clear()
    window.border()

    window.addstr(0, 5, "DELETE TASK", curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2, 1, "Delete task '" +
                  project.tasks[task_index].title + "'?")

    si = 1
    # highlight the option yes if the selected index = 1, otherwise highlight no
    window.addstr(4, 10, "YES", (2097152 << 1) >> (si == 1))
    window.addstr(4, 35, "NO", (2097152 << 1) >> (si != 1))

    k = 0
    while (k != 10):

        if k == curses.KEY_RIGHT or k == 454:
            si = 2 if si == 1 else 1

        elif k == curses.KEY_LEFT or k == 452:
            si = 1 if si == 2 else 2

        # highlight the option yes if the selected index = 1, otherwise highlight no
        window.addstr(4, 10, "YES", (2097152 << 1) >> (si == 1))
        window.addstr(4, 35, "NO", (2097152 << 1) >> (si != 1))

        window.refresh()
        stdscr.refresh()
        k = stdscr.getch()
        if k == 10:
            if si == 1:
                project.removeTask(project.tasks[task_index])
    pass


def create_project(projects: list, stdscr):
    h, w = stdscr.getmaxyx()
    window_y = h // 2 - 3
    window_x = w//2 - 25
    window = curses.newwin(7, 50, window_y, window_x)
    window.clear()
    window.border()

    window.addstr(0, 5, "ADD PROJECT", curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2, 1, "Project name:", curses.A_REVERSE)
    window.addstr(4, 25 - len("Enter to confirm") //
                  2, "Enter to confirm")
    lnstr = len("project name:")

    scr2 = curses.newwin(1, menu_width, window_y + 2, w // 2 - 23 + lnstr)
    scr2.clear()
    window.hline(3, lnstr + 1, curses.ACS_HLINE, menu_width)

    window.refresh()

    textpad = Textbox(scr2, insert_mode=True)
    project_name = textpad.edit()
    project_name = project_name[:-1]
    # clear the "ctrl g to stop editing" message
    window.addstr(4, 1, " " * 48)

    text = "Add project: '" + project_name + "'?"
    window.addstr(4, 25 - len(text) // 2, text)
    si = 1

    # highlight the option yes if the selected index = 1, otherwise highlight no
    window.addstr(5, 10, "YES", (2097152 << 1) >> (si == 1))
    window.addstr(5, 35, "NO", (2097152 << 1) >> (si != 1))

    k = 0
    while (k != 10):

        if k == curses.KEY_RIGHT or k == 454:
            si = 2 if si == 1 else 1

        elif k == curses.KEY_LEFT or k == 452:
            si = 1 if si == 2 else 2

        # highlight the option yes if the selected index = 1, otherwise highlight no
        window.addstr(5, 10, "YES", (2097152 << 1) >> (si == 1))
        window.addstr(5, 35, "NO", (2097152 << 1) >> (si != 1))

        window.refresh()
        scr2.refresh()
        stdscr.refresh()
        k = stdscr.getch()
        if k == 10:
            if si == 1:
                # selected yes
                projects.append(Project(project_name))

    window.clear()
    scr2.clear()
    scr2.refresh()
    window.refresh()
    stdscr.refresh()
    del scr2
    del window


def create_task(project, stdscr):
    h, w = stdscr.getmaxyx()

    allowed_width = w // 2 - menu_width
    window_width = allowed_width + len("Task name:") + 3

    window_y = h // 2 - 3
    window_x = w // 2 - window_width // 2
    
    
    window = curses.newwin(7, window_width, window_y, window_x)
    window.clear()
    window.border()

    window.addstr(0, 5, "ADD TASK", curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2, 1, "Task name:", curses.A_REVERSE)
    window.addstr(4, window_width//2 - len("Enter to confirm") //
                  2, "Enter to confirm")
    lnstr = len("Task name:")

    scr2 = curses.newwin(1, allowed_width, window_y + 2, w // 2 - (window_width//2-2) + lnstr)
    scr2.clear()
    window.hline(3, lnstr + 1, curses.ACS_HLINE, window_width-2 - lnstr)

    window.refresh()

    textpad = Textbox(scr2, insert_mode=True)
    task_name = textpad.edit()
    task_name = task_name[:-1]
    if len(task_name) == 0: task_name = " "
    # clear the "ctrl g to stop editing" message
    window.addstr(4, 1, " " * (window_width-2))

    text = "Add Task: '" + task_name + "' to " + project.title + "?"
    print(window_width)
    print(len(text))
    # window.addstr(4, window_width//2 - len(text) // 2, text)
    si = 1

    # highlight the option yes if the selected index = 1, otherwise highlight no
    window.addstr(5, window_width//2 - 10, "YES", (2097152 << 1) >> (si == 1))
    window.addstr(5, window_width//2 + 10, "NO", (2097152 << 1) >> (si != 1))

    k = 0
    while (k != 10):

        if k == curses.KEY_RIGHT or k == 454:
            si = 2 if si == 1 else 1

        elif k == curses.KEY_LEFT or k == 452:
            si = 1 if si == 2 else 2

        # highlight the option yes if the selected index = 1, otherwise highlight no
        window.addstr(5, window_width//2 - 10, "YES", (2097152 << 1) >> (si == 1))
        window.addstr(5, window_width//2 + 10, "NO", (2097152 << 1) >> (si != 1))

        window.refresh()
        scr2.refresh()
        stdscr.refresh()
        k = stdscr.getch()
        if k == 10:
            if si == 1:
                # selected yes
                project.addTask(Task(task_name, ""))

    window.clear()
    scr2.clear()
    scr2.refresh()
    window.refresh()
    stdscr.refresh()
    del scr2
    del window

def rename_project(projects: list, stdscr, project_index: int):
    h, w = stdscr.getmaxyx()
    window_y = h // 2 - 3
    window_x = w//2 - 25
    window = curses.newwin(7, 50, window_y, window_x)
    window.clear()
    window.border()

    window.addstr(0, 5, "RENAME TASK " + projects[project_index].title, curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2, 1, "new project name:", curses.A_REVERSE)
    window.addstr(4, 25 - len("Enter to confirm") //
                  2, "Enter to confirm")
    lnstr = len("new project name:")

    scr2 = curses.newwin(1, menu_width, window_y + 2, w // 2 - 23 + lnstr)
    scr2.clear()
    window.hline(3, lnstr + 1, curses.ACS_HLINE, menu_width)

    window.refresh()

    textpad = Textbox(scr2, insert_mode=True)
    project_name = textpad.edit()
    project_name = project_name[:-1]
    # clear the "ctrl g to stop editing" message
    window.addstr(4, 1, " " * 48)

    text = "Rename to: '" + project_name + "'?"
    window.addstr(4, 25 - len(text) // 2, text)
    si = 1

    # highlight the option yes if the selected index = 1, otherwise highlight no
    window.addstr(5, 10, "YES", (2097152 << 1) >> (si == 1))
    window.addstr(5, 35, "NO", (2097152 << 1) >> (si != 1))

    k = 0
    while (k != 10):

        if k == curses.KEY_RIGHT or k == 454:
            si = 2 if si == 1 else 1

        elif k == curses.KEY_LEFT or k == 452:
            si = 1 if si == 2 else 2

        # highlight the option yes if the selected index = 1, otherwise highlight no
        window.addstr(5, 10, "YES", (2097152 << 1) >> (si == 1))
        window.addstr(5, 35, "NO", (2097152 << 1) >> (si != 1))

        window.refresh()
        scr2.refresh()
        stdscr.refresh()
        k = stdscr.getch()
        if k == 10:
            if si == 1:
                # selected yes
                projects[project_index].title = project_name

    window.clear()
    scr2.clear()
    scr2.refresh()
    window.refresh()
    stdscr.refresh()
    del scr2
    del window

def rename_task(projects: list, stdscr, project_index: int, task_index: int):
    h, w = stdscr.getmaxyx()
    window_y = h // 2 - 3
    window_x = w//2 - 25
    window = curses.newwin(7, 50, window_y, window_x)
    window.clear()
    window.border()

    window.addstr(0, 5, "RENAME TASK " + projects[project_index].tasks[task_index].title, curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2, 1, "new task name:", curses.A_REVERSE)
    window.addstr(4, 25 - len("Enter to confirm") //
                  2, "Enter to confirm")
    lnstr = len("new task name:")

    scr2 = curses.newwin(1, menu_width, window_y + 2, w // 2 - 23 + lnstr)
    scr2.clear()
    window.hline(3, lnstr + 1, curses.ACS_HLINE, menu_width)

    window.refresh()

    textpad = Textbox(scr2, insert_mode=True)
    task_name = textpad.edit()
    task_name = task_name[:-1]
    # clear the "ctrl g to stop editing" message
    window.addstr(4, 1, " " * 48)

    text = "Rename to: '" + task_name + "'?"
    window.addstr(4, 25 - len(text) // 2, text)
    si = 1

    # highlight the option yes if the selected index = 1, otherwise highlight no
    window.addstr(5, 10, "YES", (2097152 << 1) >> (si == 1))
    window.addstr(5, 35, "NO", (2097152 << 1) >> (si != 1))

    k = 0
    while (k != 10):

        if k == curses.KEY_RIGHT or k == 454:
            si = 2 if si == 1 else 1

        elif k == curses.KEY_LEFT or k == 452:
            si = 1 if si == 2 else 2

        # highlight the option yes if the selected index = 1, otherwise highlight no
        window.addstr(5, 10, "YES", (2097152 << 1) >> (si == 1))
        window.addstr(5, 35, "NO", (2097152 << 1) >> (si != 1))

        window.refresh()
        scr2.refresh()
        stdscr.refresh()
        k = stdscr.getch()
        if k == 10:
            if si == 1:
                # selected yes
                projects[project_index].tasks[task_index].title = task_name

    window.clear()
    scr2.clear()
    scr2.refresh()
    window.refresh()
    stdscr.refresh()
    del scr2
    del window
    



def get_x_pos_center(text: str):
    return curses.COLS // 2 - len(text) // 2


def draw_instructions(stdscr):
    controls = "CONTROLS"
    # draw line
    h, w = stdscr.getmaxyx()
    instructions_start = h - controls_lines-1
    stdscr.hline(instructions_start, 0, curses.ACS_HLINE, menu_width //
                 2 - len(controls)//2, curses.color_pair(MAGENTA_BLACK))
    stdscr.addstr(instructions_start, menu_width//2-len(controls) //
                  2, controls, curses.color_pair(WHITE_MAGENTA))
    stdscr.hline(instructions_start, menu_width//2+len(controls)//2, curses.ACS_HLINE,
                 menu_width//2-len(controls)//2+1, curses.color_pair(MAGENTA_BLACK))
    stdscr.addstr(instructions_start + 1, 0, "UP/DOWN - Move selection")
    stdscr.addstr(instructions_start + 2, 0, "LEFT/RIGHT - Switch section")
    stdscr.addstr(instructions_start + 3, 0, "SPACE - Change task status")
    stdscr.addstr(instructions_start + 4, 0, "DEL - Delete selected item")
    stdscr.addstr(instructions_start + 5, 0, "p - Add new project")
    stdscr.addstr(instructions_start + 6, 0, "t - Add new task to project")
    stdscr.addstr(instructions_start + 7, 0, "r - Rename selected item")
    stdscr.addstr(instructions_start + 8, 0, "q - Quit")



def draw_projects(stdscr, projects: list, idx: int, selected_window):

    if len(projects) != 0:        
        # draw projects
        y = 1
        for project_index, project in enumerate(projects):
            if project_index == idx:
                if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                    stdscr.addstr(y, 0, project.title, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 0, "-- " + project.title)
            else:
                stdscr.addstr(y, 0, project.title)
            y = y + 1
    else:
        stdscr.addstr(1, menu_width//2 - len("NO PROJECTS")//2, "NO PROJECTS", curses.color_pair(WHITE_MAGENTA))
        text = "Press 'p' to add a new project"
        if len(text) > menu_width:
            stdscr.addstr(2, 0, text[: (menu_width - 1)])
            stdscr.addstr(3,0,text[(menu_width-1):])
        else:
            stdscr.addstr(2, 0, text)


def draw_tasks(stdscr, projects, project_index, selected_window, idx):
    h, w = stdscr.getmaxyx()

    if len(projects) != 0:
        width = w//2 - menu_width

        tasks = projects[project_index].tasks
        if len(tasks) != 0:
            # draw task names
            y = 1
            for i, task in enumerate(tasks):
                stdscr.attron(curses.color_pair(statuses[task.status.value]))
                stdscr.addstr(y, menu_width+1, " " * (width-1))
                if i == idx and SelectedWindow(selected_window) == SelectedWindow.TASKS:
                    stdscr.addstr(y, menu_width + 1, task.title, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, menu_width + 1, task.title)
                if task.status != Status.NONE:
                    stdscr.addstr(y, menu_width + width -
                                len(task.status.name), task.status.name)
                stdscr.attroff(curses.color_pair(statuses[task.status.value]))
                y = y + 1
        else:
            stdscr.addstr(1, menu_width + 1 + width//2 - len("NO TASKS")//2, "NO TASKS", curses.color_pair(WHITE_MAGENTA))
            text = "Press 't' to add a new task"
            if len(text) > width:
                stdscr.addstr(2, menu_width + 1, text[: (width - 1)])
                stdscr.addstr(3,menu_width+1,text[(width-1):])
            else:
                stdscr.addstr(2, menu_width + 1, text)


def draw_description(projects, stdscr, project_index,task_index, selected_window):
    global editing
    h, w = stdscr.getmaxyx()
    begin = w // 2
    width = w // 2
    title = ""
    task = None
    can_edit = len(projects) != 0 and len(projects[project_index].tasks) != 0

    if can_edit:
        task = projects[project_index].tasks[task_index]
        # put description if we haven't selected a task
        if SelectedWindow(selected_window) == SelectedWindow.TASKS:
            title = task.title.upper()
        else:
            title = "DESCRIPTION"
    else: title = "DESCRIPTION"


    # draw the title
    title_start = begin + width // 2 - len(title) // 2
    stdscr.attron(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)
    stdscr.addstr(0, begin + 1, " " * (title_start - begin))
    stdscr.addstr(0, title_start, title)
    stdscr.addstr(0, title_start + len(title), " " *
                  (width - len(title) - (title_start - begin)))
    stdscr.attroff(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)

    edit_win_lines = h - 4 - controls_lines
    edit_win_cols = w // 2 - 4

    scr2 = curses.newwin(edit_win_lines, edit_win_cols, 2, w // 2 + 2)
    rectangle(stdscr, 1, w//2+1, h - controls_lines-2, w-2)
    stdscr.refresh()
    scr2.refresh()
    textpad = Textbox(scr2, insert_mode=True)
    scr2.clear()
    if SelectedWindow(selected_window) == SelectedWindow.TASKS and can_edit:
        scr2.addstr(0, 0, task.desc)
    scr2.refresh()

    if editing and can_edit:
        entered_text = textpad.edit()
        task.desc = entered_text
        print(task.desc)
        scr2.clear()
        scr2.addstr(0, 0, entered_text)
        scr2.refresh()
        editing = False
        save(projects)


def draw_layout(stdscr):
    h, w = stdscr.getmaxyx()

    # draw botton text
    stdscr.addstr(stdscr.getmaxyx()[0] - 1,
                  0, "TPM by Sem van der Hoeven",)

    # DRAW PROJECTS
    stdscr.vline(0, menu_width, curses.ACS_VLINE, stdscr.getmaxyx()[
                 0] - 1, curses.color_pair(CYAN_BLACK))

    # draw project title
    title = "PROJECTS"
    title_start = menu_width // 2 - len(title) // 2
    stdscr.attron(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)
    stdscr.addstr(0, 0, " " * (title_start-1))
    stdscr.addstr(0, title_start-1, title)
    stdscr.addstr(0, len(title) + title_start - 1, " " *
                  (menu_width - (len(title) + title_start)+1))
    stdscr.attroff(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)

    # DRAW TASKS
    stdscr.vline(0, w // 2, curses.ACS_VLINE, h -
                 1, curses.color_pair(CYAN_BLACK))

    # draw tasks title
    title = "TASKS"
    width = w//2 - menu_width
    title_start = menu_width + (width//2 - len(title)//2)
    stdscr.attron(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)
    stdscr.addstr(0, menu_width + 1, " " * (title_start - menu_width))
    stdscr.addstr(0, title_start, title)
    stdscr.addstr(0, title_start + len(title), " " *
                  (w//2 - (title_start + len(title))))
    stdscr.attroff(curses.color_pair(YELLOW_BLACK) | curses.A_REVERSE)

    # draw color instructions
    legend = "LEGEND"
    instructions_start = h - controls_lines-1
    stdscr.hline(instructions_start, menu_width+1, curses.ACS_HLINE,
                 width//2-len(legend)//2-1, curses.color_pair(MAGENTA_BLACK))
    stdscr.addstr(instructions_start, menu_width + width // 2 -
                  len(legend)//2, legend, curses.color_pair(WHITE_MAGENTA))
    stdscr.hline(instructions_start, menu_width+width//2+len(legend)//2,
                 curses.ACS_HLINE, width//2 - len(legend)//2, curses.color_pair(MAGENTA_BLACK))

    stdscr.addstr(instructions_start + 1, menu_width + 1,
                  " " * 3, curses.color_pair(STATUS_DONE))
    stdscr.addstr(instructions_start + 1, menu_width + 4 + width -
                  2*len("DONE"), "DONE", curses.color_pair(STATUS_DONE))
    stdscr.addstr(instructions_start + 2, menu_width + 1,
                  " " * 3, curses.color_pair(STATUS_IDLE))
    stdscr.addstr(instructions_start + 2, menu_width + 4 + width -
                  2*len("IDLE"), "IDLE", curses.color_pair(STATUS_IDLE))
    stdscr.addstr(instructions_start + 3, menu_width + 1,
                  " " * 3, curses.color_pair(STATUS_WORKING))
    stdscr.addstr(instructions_start + 3, menu_width + 4 + width -
                  int(1.5*len("WORKING")+1), "WORKING", curses.color_pair(STATUS_WORKING))

    # display the controls
    controls_start = w // 2
    controls = "EDITING CONTROLS"
    instructions_start = h - controls_lines-1
    stdscr.hline(instructions_start, controls_start + 1, curses.ACS_HLINE, controls_start//2 -
                 len(controls)//2, curses.color_pair(MAGENTA_BLACK))

    stdscr.addstr(instructions_start, controls_start + (w//2)//2-len(controls)//2,
                  controls, curses.color_pair(WHITE_MAGENTA))
    stdscr.hline(instructions_start, controls_start + (w//2)//2 + len(controls)//2+1, curses.ACS_HLINE,
                 w // 2 - len(controls) // 2, curses.color_pair(MAGENTA_BLACK))
    stdscr.addstr(instructions_start + 1, controls_start +
                  1, "CTRL+G - Stop editing")
    stdscr.addstr(instructions_start+2, controls_start+1,
                  "ENTER - Edit selected task's description")

def draw_sections(stdscr, projects: list, project_index: int,task_index: int,selected_window: int):
    stdscr.clear()
    draw_layout(stdscr)

    draw_projects(stdscr, projects, project_index, selected_window)
    draw_tasks(stdscr, projects,project_index,
                   selected_window, task_index)
    draw_instructions(stdscr)
    draw_description(
            projects, stdscr, project_index, task_index,selected_window)


def main(stdscr):
    global editing

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
    projects = load()
    newp = False  # making new project
    newt = False  # making new task

    while (k != ord('q')):
        has_projects = len(projects) != 0

        if k == curses.KEY_ENTER or k == 10:  # enter key
            if SelectedWindow(selected_window) == SelectedWindow.TASKS and has_projects:
                editing = not editing
        elif k == curses.KEY_UP or k == 450:  # up key
            if has_projects:
                # only move the projects selection if we're on that pane
                if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                    project_index = project_index - 1
                    if project_index < 0:
                        project_index = len(projects) - 1
                # only move the task selection if we're on that pane
                elif SelectedWindow(selected_window) == SelectedWindow.TASKS and len(projects[project_index].tasks) != 0:
                        task_index = task_index - 1
                        if task_index < 0:
                            task_index = len(projects[project_index].tasks)-1

        elif k == curses.KEY_DOWN or k == 456:  # down key
            if has_projects:
                # only move the projects selection if we're on that pane
                if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                    project_index = project_index + 1
                    if project_index > len(projects) - 1:
                        project_index = 0
                # only move the task selection if we're on that pane
                elif SelectedWindow(selected_window) == SelectedWindow.TASKS and len(projects[project_index].tasks) != 0:
                    task_index = task_index + 1
                    if task_index > len(projects[project_index].tasks) - 1:
                        task_index = 0

        elif k == curses.KEY_RIGHT or k == 454:  # right key
            if has_projects:
                selected_window = selected_window + 1 if len(projects[project_index].tasks) != 0 else 1
                if selected_window > len(SelectedWindow):
                    selected_window = 1

                # set the task selection to the first for when we select a task next
                # because the previous task we were on might have more tasks than this one,
                # so we don't want the index to be out of bounds
                if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                    task_index = 0

        elif k == curses.KEY_LEFT or k == 452:  # left key
            if has_projects:
                selected_window = selected_window - 1
                if selected_window < 1:
                    if len(projects[project_index].tasks) != 0:
                        selected_window = len(SelectedWindow)
                    else:
                        selected_window = 1

                # set the task selection to the first for when we select a task next
                # because the previous task we were on might have more tasks than this one,
                # so we don't want the index to be out of bounds
                if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                    task_index = 0

        elif k == 32:  # space key
            if SelectedWindow(selected_window) == SelectedWindow.TASKS and has_projects and len(projects[project_index].tasks) != 0:
                projects[project_index].tasks[task_index].status = projects[project_index].tasks[task_index].status.next()

        elif (k == ord('p') or k == 112) and not newp:  # p key
            newp = True
        elif (k == ord('t') or k == 116) and not newt and has_projects:  # t key
            newt = True

        elif k == 330 and has_projects:  # delete key
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                delete_project(stdscr, projects, project_index)
                project_index = 0
            elif SelectedWindow(selected_window) == SelectedWindow.TASKS and len(projects[project_index].tasks) != 0:
                delete_task(stdscr, projects[project_index], task_index)
                if len(projects[project_index].tasks) == 0: selected_window = 1
                task_index = 0
        elif k == 114 and has_projects: # r key
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                rename_project(projects,stdscr,project_index)
            elif SelectedWindow(selected_window) == SelectedWindow.TASKS: 
                rename_task(projects,stdscr,project_index,task_index)
        stdscr.clear()

        draw_sections(stdscr,projects,project_index,task_index,selected_window)

        if newp:
            create_project(projects, stdscr)
            newp = False
            draw_sections(stdscr, projects, project_index, task_index, selected_window)

        if newt:
            create_task(projects[project_index], stdscr)
            newt = False

            draw_sections(stdscr,projects,project_index,task_index,selected_window)

        k = stdscr.getch()
        stdscr.refresh()

    curses.endwin()
    save(projects)


if __name__ == "__main__":
    # wrapper already calls noecho() and cbreak() and stdcr.keypad(True)
    # it also resets the settings upon closing or upon error
    wrapper(main)
