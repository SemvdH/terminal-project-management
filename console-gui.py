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
controls_lines = 5
editing = False


STATUS_DONE = WHITE_GREEN
STATUS_WORKING = WHITE_CYAN
STATUS_IDLE = WHITE_MAGENTA

statuses = [STATUS_WORKING, STATUS_IDLE, STATUS_DONE, 0]


# TODO add controls for adding projects, tasks and deleting
# TODO add deleting of projects
# TODO add deleting of tasks

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
        print("previous of {}".format(self))
        v = self.value - 1
        if v < 0:
            v = 3
        print("previous is {}".format(Status(v)))
        return Status(v)

    def next(self):
        v = self.value + 1
        if v > 3:
            v = 0
        print("next is {}".format(Status(v)))
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
            "Example task", "This is an example of a task description.\nIt can be used to provide some extra information about the task.\n\nControls:\nt - add new task to selected project\np - add new project"))
        return [temp_project]



def delete_project(stdscr, projects: list,project_index):

    h, w = stdscr.getmaxyx()
    window_y = h // 2 - 3
    window_x = w // 2 - 25
    window = curses.newwin(6, 50, window_y, window_x)
    window.clear()
    window.border()

    window.addstr(0,5,"DELETE PROJECT", curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2,1,"Delete project '" + projects[project_index].title + "'?")

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

    window.addstr(0,5,"DELETE TASK", curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2,1,"Delete task '" + project.tasks[task_index].title + "'?")

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

    scr2 = curses.newwin(1, 47 - lnstr, window_y + 2, w // 2 - 23 + lnstr)
    scr2.clear()
    window.hline(3, lnstr + 1, curses.ACS_HLINE, 48 - lnstr)

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
                temp = Project(project_name)
                temp.addTask(Task("New task", ""))
                projects.append(temp)

    window.clear()
    scr2.clear()
    scr2.refresh()
    window.refresh()
    stdscr.refresh()
    del scr2
    del window


def create_task(project, stdscr):
    # TODO create task add window when add project window is made

    h, w = stdscr.getmaxyx()
    window_y = h // 2 - 3
    window_x = w//2 - 25
    window = curses.newwin(7, 50, window_y, window_x)
    window.clear()
    window.border()

    window.addstr(0, 5, "ADD TASK", curses.color_pair(
        YELLOW_BLACK) | curses.A_REVERSE)
    window.addstr(2, 1, "Task name:", curses.A_REVERSE)
    window.addstr(4, 25 - len("Enter to confirm") //
                  2, "Enter to confirm")
    lnstr = len("Task name:")

    scr2 = curses.newwin(1, 47 - lnstr, window_y + 2, w // 2 - 23 + lnstr)
    scr2.clear()
    window.hline(3, lnstr + 1, curses.ACS_HLINE, 48 - lnstr)

    window.refresh()

    textpad = Textbox(scr2, insert_mode=True)
    task_name = textpad.edit()
    task_name = task_name[:-1]
    # clear the "ctrl g to stop editing" message
    window.addstr(4, 1, " " * 48)

    text = "Add Task: '" + task_name + "'?"
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
                project.addTask(Task(task_name, ""))

    window.clear()
    scr2.clear()
    scr2.refresh()
    window.refresh()
    stdscr.refresh()
    del scr2
    del window

    pass


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
    stdscr.addstr(instructions_start + 1, 0, "UP/DOWN - move selection")
    stdscr.addstr(instructions_start + 2, 0, "LEFT/RIGHT - switch section")
    stdscr.addstr(instructions_start + 3, 0, "SPACE - change task status")


def draw_projects(stdscr, projects: list, idx: int, selected_window):
    # draw line
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


def draw_tasks(stdscr, tasks, selected_window, idx):
    h, w = stdscr.getmaxyx()

    # draw middle devidor line
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


def draw_description(projects, stdscr, task, selected_window):
    global editing
    h, w = stdscr.getmaxyx()
    begin = w // 2
    width = w // 2

    # put description if we haven't selected a task
    if SelectedWindow(selected_window) == SelectedWindow.TASKS:
        title = task.title.upper()
    else:
        title = "DESCRIPTION"

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

    scr2 = curses.newwin(edit_win_lines, edit_win_cols, 2, w // 2 + 2)
    rectangle(stdscr, 1, w//2+1, h - controls_lines-2, w-2)
    stdscr.refresh()
    scr2.refresh()
    textpad = Textbox(scr2, insert_mode=True)
    scr2.clear()
    if SelectedWindow(selected_window) == SelectedWindow.TASKS:
        scr2.addstr(0, 0, task.desc)
    scr2.refresh()

    if editing:
        entered_text = textpad.edit()
        task.desc = entered_text
        print(task.desc)
        scr2.clear()
        scr2.addstr(0, 0, entered_text)
        scr2.refresh()
        editing = False
        save(projects)


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
        
        

        if k == curses.KEY_ENTER or k == 10:  # enter key
            if SelectedWindow(selected_window) == SelectedWindow.TASKS:
                editing = not editing
        elif k == curses.KEY_UP or k == 450:  # up key
            # only move the projects selection if we're on that pane
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                project_index = project_index - 1
                if project_index < 0:
                    project_index = len(projects) - 1
            # only move the task selection if we're on that pane
            elif SelectedWindow(selected_window) == SelectedWindow.TASKS:
                task_index = task_index - 1
                if task_index < 0:
                    task_index = len(projects[project_index].tasks)-1

        elif k == curses.KEY_DOWN or k == 456:  # down key
            # only move the projects selection if we're on that pane
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                project_index = project_index + 1
                if project_index > len(projects) - 1:
                    project_index = 0
            # only move the task selection if we're on that pane
            elif SelectedWindow(selected_window) == SelectedWindow.TASKS:
                task_index = task_index + 1
                if task_index > len(projects[project_index].tasks) - 1:
                    task_index = 0

        elif k == curses.KEY_RIGHT or k == 454:  # right key
            selected_window = selected_window + 1
            if selected_window > len(SelectedWindow):
                selected_window = 1

            # set the task selection to the first for when we select a task next
            # because the previous task we were on might have more tasks than this one,
            # so we don't want the index to be out of bounds
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                task_index = 0

        elif k == curses.KEY_LEFT or k == 452:  # left key
            selected_window = selected_window - 1
            if selected_window < 1:
                selected_window = len(SelectedWindow)

            # set the task selection to the first for when we select a task next
            # because the previous task we were on might have more tasks than this one,
            # so we don't want the index to be out of bounds
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                task_index = 0

        elif k == 32:  # space key
            if SelectedWindow(selected_window) == SelectedWindow.TASKS:
                projects[project_index].tasks[task_index].status = projects[project_index].tasks[task_index].status.next()

        elif (k == ord('p') or k == 112) and not newp:  # p key
            newp = True
        elif (k == ord('t') or k == 116) and not newt:  # t key
            newt = True
        
        elif k == 330:  # delete key
            if SelectedWindow(selected_window) == SelectedWindow.PROJECTS:
                delete_project(stdscr, projects, project_index)
                project_index = 0
            elif SelectedWindow(selected_window) == SelectedWindow.TASKS:
                delete_task(stdscr, projects[project_index], task_index)
                task_index = 0
            


        stdscr.clear()

        # draw botton text
        stdscr.addstr(stdscr.getmaxyx()[0] - 1,
                      0, "TPM by Sem van der Hoeven",)

        draw_projects(stdscr, projects, project_index, selected_window)
        draw_tasks(stdscr, projects[project_index].tasks,
                   selected_window, task_index)
        draw_instructions(stdscr)
        draw_description(
            projects, stdscr, projects[project_index].tasks[task_index], selected_window)

        if newp:
            create_project(projects, stdscr)
            newp = False

            # TODO clean
            draw_projects(stdscr, projects, project_index, selected_window)
            draw_tasks(stdscr, projects[project_index].tasks,
                       selected_window, task_index)
            draw_instructions(stdscr)
            draw_description(
                projects, stdscr, projects[project_index].tasks[task_index], selected_window)

        if newt:
            create_task(projects[project_index], stdscr)
            newt = False

            # TODO clean
            draw_projects(stdscr, projects, project_index, selected_window)
            draw_tasks(stdscr, projects[project_index].tasks,
                       selected_window, task_index)
            draw_instructions(stdscr)
            draw_description(
                projects, stdscr, projects[project_index].tasks[task_index], selected_window)

        k = stdscr.getch()
        stdscr.refresh()

    curses.endwin()
    save(projects)


if __name__ == "__main__":
    # wrapper already calls noecho() and cbreak() and stdcr.keypad(True)
    # it also resets the settings upon closing or upon error
    wrapper(main)
