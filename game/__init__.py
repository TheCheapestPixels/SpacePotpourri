import argparse

from panda3d.core import WindowProperties

from panda3d_logos.splashes import Colors
from panda3d_logos.splashes import Pattern

from stageflow import Flow
from stageflow import Stage
from stageflow.prefab import Quit
from stageflow.panda3d import Panda3DSplash

from stageflow.wecs import WECSStage

from .main_loop import MainGameStage


class BorderlessFullscreenMouseHidden(Stage):
    def __init__(self, exit_stage='main menu'):
        self.exit_stage = exit_stage

    def enter(self, data):
        self.data = data

        props = WindowProperties()
        
        #props.cursor_hidden = True
        props.fixed_size = True
        #props.foreground = True
        props.origin = (0, 0)
        props.size = (
            base.pipe.get_display_width(),
            base.pipe.get_display_height(),
        )
        props.title = ""  # STARTPROJECT: Window title
        #props.undecorated = True
        
        base.win.requestProperties(props)
        base.task_mgr.do_method_later(0.01, self.leave, "Leave")

    def exit(self, data):
        return self.data

    def leave(self,task):
        base.flow.transition(self.exit_stage, self.data)


stages=dict(
    start=BorderlessFullscreenMouseHidden(
        exit_stage='splashes',
    ),
    splashes=Panda3DSplash(
        exit_stage='main_game_stage',
        splash_args=dict(
            pattern=Pattern.WHEEL,
            colors=Colors.RAINBOW,
            pattern_freq=1,
            cycle_freq=5,
        ),
    ),
    main_game_stage=MainGameStage(),
    quit=Quit(),
    debug=BorderlessFullscreenMouseHidden(
        exit_stage='main_game_stage',
    ),
)


parser = argparse.ArgumentParser(
    description="",  # STARTPROJECT: Textual description for --help
)
parser.add_argument(
    "-s", "--stage",
    type=str,
    default='start',
    help="Name of the stage to start the game on",
    choices=stages.keys(),
)
args = parser.parse_args()


base.flow = Flow(
    stages=stages,
    initial_stage=args.stage,
)
