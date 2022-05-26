import wecs

from stageflow.wecs import WECSStage

# STARTPROJECT: Turn MainGameStage into your game.


class MainGameStage(WECSStage):
    system_specs = [
        ## Set up newly added models/camera, tear down removed ones
        #(0, 0, wecs.panda3d.prototype.ManageModels),
        #(0, -5, wecs.panda3d.spawnpoints.Spawn),
        #(0, -10, wecs.panda3d.camera.PrepareCameras),
        ## Update clocks
        #(0, -20, wecs.mechanics.clock.DetermineTimestep),
        ## Character AI
        #(0, -30, wecs.panda3d.ai.Think),
        ## Character controller
        #(0, -40, wecs.panda3d.character.UpdateCharacter),
        #(0, -50, wecs.panda3d.character.Floating),
        #(0, -60, wecs.panda3d.character.Walking),
        #(0, -70, wecs.panda3d.character.Inertiing),
        #(0, -75, wecs.panda3d.character.Frictioning),
        #(0, -77, wecs.panda3d.character.WalkSpeedLimiting),
        #(0, -80, wecs.panda3d.character.Bumping),
        #(0, -110, wecs.panda3d.character.TurningBackToCamera),
        #(0, -120, wecs.panda3d.character.ExecuteMovement),
        ## Camera
        #(0, -150, wecs.panda3d.camera.ReorientObjectCentricCamera),
        #(0, -160, wecs.panda3d.camera.CollideCamerasWithTerrain),
        # Debug keys (`escape` to close, etc.)
        (0, -1000, wecs.panda3d.debug.DebugTools),
    ]

    def setup(self, data):
        """
        Set up the game.

        data
            Data that was passed to this stage.
        """
        pass

    def teardown(self, data):
        """
        Tear down the game.

        data
            Data that was passed to :class:`Stage.exit`.

        :returns:
            Data to be passed on o the next stage
        """
        return data
