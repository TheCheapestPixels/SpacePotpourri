import wecs

from stageflow.wecs import WECSStage


class MainGameStage(WECSStage):
    system_specs = [
        # Debug keys (`escape` to close, etc.)
        (0, -1000, wecs.panda3d.debug.DebugTools),
    ]

    def setup(self, data):
        """
        Sets up the game.

        data
            Data that was passed to this stage; Ignored.
        """
        pass

    def teardown(self, data):
        """
        Should tear down the game, but does nothing yet.

        data
            Data that was passed to :class:`Stage.exit`.

        :returns:
            Data to be passed on to the next stage; In this case, 
            whatever was passed to this method.
        """
        return data
