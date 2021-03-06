import arcade
import random

class GameTracker:
    def __init__(self):
        self.playerBtnInfo = PlayerBtnInfo()
        self.playerScoreInfo = PlayerScoreInfo()
        self.gameSound = GameSound()
        self.userInputHandlerInGame = UserInputHandlerInGame(self.playerBtnInfo
            , self.playerScoreInfo, self.gameSound)
        self.phaseTracker = PhaseTracker(self.gameSound)
        self.userInputHandlerInGameOver = UserInputHandlerInGameOver(self.playerBtnInfo
            , self.playerScoreInfo, self.phaseTracker, self.userInputHandlerInGame)

    def on_key_press(self, key, key_modifiers):
        if self.phaseTracker.current_phase == self.phaseTracker.PHASE_PLAY:
            self.userInputHandlerInGame.on_key_press(key, key_modifiers)
        elif  self.phaseTracker.current_phase == self.phaseTracker.PHASE_GAMEOVER:
            self.userInputHandlerInGameOver.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        if self.phaseTracker.current_phase == self.phaseTracker.PHASE_PLAY:
            self.userInputHandlerInGame.on_key_release(key, key_modifiers)

    def update(self, delta_time):
        self.phaseTracker.update(delta_time)
        self.userInputHandlerInGame.update(delta_time)

class GameSound:
    def __init__(self):
        self.soundtrack = arcade.sound.load_sound("sounds/SoundTrack.mp3")
        self.time_up = arcade.sound.load_sound("sounds/TimeUp.mp3")
        self.game_over = arcade.sound.load_sound("sounds/GameOver.wav")
        self.incorrect_1 = arcade.sound.load_sound("sounds/InCorrect_1.mp3")
        self.incorrect_2 = arcade.sound.load_sound("sounds/InCorrect_2.mp3")

class PlayerBtnInfo:
    def __init__(self):
        self.MAX_QUEUE = 6
        self.BLOCK_QUEUE = 2
        self.BTN_TOTAL = 4
        self.BTN_UP = 0
        self.BTN_LEFT = 1
        self.BTN_DOWN = 2
        self.BTN_RIGHT = 3
        self.add_all_to_list()

    def delete_front(self, player):
        if player == 1:
            del self.player_1_btn[0]
            self.player_1_btn.append(random.randrange(self.BTN_TOTAL))
        elif player == 2:
            del self.player_2_btn[0]
            self.player_2_btn.append(random.randrange(self.BTN_TOTAL))

    def reset(self):
        del self.player_1_btn
        del self.player_2_btn

        self.add_all_to_list()

    def add_all_to_list(self):
        self.player_1_btn = []
        self.player_2_btn = []

        for i in range(self.MAX_QUEUE):
            self.player_1_btn.append(random.randrange(self.BTN_TOTAL))
            self.player_2_btn.append(random.randrange(self.BTN_TOTAL))

class PlayerScoreInfo:
    def __init__(self):
        self.set_init_score()

        self.score_1_combo = 100
        self.score_10_combo = 150
        self.score_20_combo = 200
        self.score_reduce = 300

    def update(self, player, isCorrect):
        self.edit_combo(player, isCorrect)
        if isCorrect:
            self.edit_score(player)

    def edit_combo(self, player, isCorrect):
        if player == 1:
            if isCorrect:
                self.player_1_combo += 1
            else:
                self.player_1_combo = 0
        elif player == 2:
            if isCorrect:
                self.player_2_combo += 1
            else:
                self.player_2_combo = 0

    def edit_score(self, player):
        if player == 1:
            if self.player_1_combo < 10:
                self.player_1_score += self.score_1_combo
            elif self.player_1_combo < 20:
                self.player_1_score += self.score_10_combo
            else:
                self.player_1_score += self.score_20_combo
        elif player == 2:
            if self.player_2_combo < 10:
                self.player_2_score += self.score_1_combo
            elif self.player_2_combo < 20:
                self.player_2_score += self.score_10_combo
            else:
                self.player_2_score += self.score_20_combo

    def reduce_score(self,player):
        if player == 1:
            self.player_1_score -= self.score_reduce
        elif player == 2:
            self.player_2_score -= self.score_reduce

    def reset(self):
        self.set_init_score()

    def set_init_score(self):
        self.player_1_score = 0
        self.player_2_score = 0
        self.player_1_combo = 0
        self.player_2_combo = 0

class UserInputHandlerInGame:
    def __init__(self, btnInfo, scoreInfo, gameSound):
        self.INCORRECT_PAUSE_TIME = 1.5
        self.btnInfo = btnInfo
        self.scoreInfo = scoreInfo
        self.gameSound = gameSound
        self.set_var()

    def update(self, delta_time):
        if self.player_1_pause_time:
            self.player_1_pause_time -= delta_time
            if self.player_1_pause_time < 0:
                self.player_1_pause_time = 0
        if self.player_2_pause_time:
            self.player_2_pause_time -= delta_time
            if self.player_2_pause_time < 0:
                self.player_2_pause_time = 0


    def on_key_press(self, key, key_modifiers):
        if (key == arcade.key.W and self.player_1_btn_ready
            and self.player_1_pause_time <= 0.0):
            self.player_1_btn_ready = False
            self.checkInput(1, self.btnInfo.BTN_UP)
        elif (key == arcade.key.A and self.player_1_btn_ready
            and self.player_1_pause_time <= 0.0):
            self.player_1_btn_ready = False
            self.checkInput(1, self.btnInfo.BTN_LEFT)
        elif (key == arcade.key.S and self.player_1_btn_ready
            and self.player_1_pause_time <= 0.0):
            self.player_1_btn_ready = False
            self.checkInput(1, self.btnInfo.BTN_DOWN)
        elif (key == arcade.key.D and self.player_1_btn_ready
            and self.player_1_pause_time <= 0.0):
            self.player_1_btn_ready = False
            self.checkInput(1, self.btnInfo.BTN_RIGHT)
        elif (key == arcade.key.SPACE and self.player_1_btn_ready
            and self.player_1_pause_time <= 0.0):
            self.player_1_btn_ready = False
            self.player_1_disable_block = True
            self.scoreInfo.reduce_score(1)
            self.scoreInfo.edit_combo(1, False)


        if (key == arcade.key.UP and self.player_2_btn_ready
            and self.player_2_pause_time <= 0.0):
            self.player_2_btn_ready = False
            self.checkInput(2, self.btnInfo.BTN_UP)
        elif (key == arcade.key.LEFT and self.player_2_btn_ready
            and self.player_2_pause_time <= 0.0):
            self.player_2_btn_ready = False
            self.checkInput(2, self.btnInfo.BTN_LEFT)
        elif (key == arcade.key.DOWN and self.player_2_btn_ready
            and self.player_2_pause_time <= 0.0):
            self.player_2_btn_ready = False
            self.checkInput(2, self.btnInfo.BTN_DOWN)
        elif (key == arcade.key.RIGHT and self.player_2_btn_ready
            and self.player_2_pause_time <= 0.0):
            self.player_2_btn_ready = False
            self.checkInput(2, self.btnInfo.BTN_RIGHT)
        elif (key == arcade.key.NUM_0 and self.player_2_btn_ready
            and self.player_1_pause_time <= 0.0):
            self.player_2_btn_ready = False
            self.player_2_disable_block = True
            self.scoreInfo.reduce_score(2)
            self.scoreInfo.edit_combo(2, False)

    def on_key_release(self, key, modifiers):
        if (key == arcade.key.W or key == arcade.key.A
            or key == arcade.key.S or key == arcade.key.D):
                self.player_1_btn_ready = True
        elif key == arcade.key.SPACE:
            self.player_1_btn_ready = True
            self.player_1_disable_block = False
        elif (key == arcade.key.UP or key == arcade.key.LEFT
            or key == arcade.key.DOWN or key == arcade.key.RIGHT):
                self.player_2_btn_ready = True
        elif key == arcade.key.NUM_0:
            self.player_2_btn_ready = True
            self.player_2_disable_block = False

    def checkInput(self, player, input):
        if player == 1:
            if self.btnInfo.player_1_btn[0] == input:
                self.scoreInfo.update(1, True)
                self.btnInfo.delete_front(1)
            else:
                self.scoreInfo.update(1, False)
                self.player_1_pause_time = self.INCORRECT_PAUSE_TIME
                arcade.sound.play_sound(self.gameSound.incorrect_1)
        elif player == 2:
            if self.btnInfo.player_2_btn[0] == input:
                self.scoreInfo.update(2, True)
                self.btnInfo.delete_front(2)
            else:
                self.scoreInfo.update(2, False)
                self.player_2_pause_time = self.INCORRECT_PAUSE_TIME
                arcade.sound.play_sound(self.gameSound.incorrect_2)

    def get_player_1_pause_time(self):
        return self.player_1_pause_time / self.INCORRECT_PAUSE_TIME

    def get_player_2_pause_time(self):
        return self.player_2_pause_time / self.INCORRECT_PAUSE_TIME

    def reset(self):
        self.set_var()

    def set_var(self):
        self.player_1_btn_ready = True
        self.player_2_btn_ready = True
        self.player_1_disable_block = False
        self.player_2_disable_block = False
        self.player_1_pause_time = 0.0
        self.player_2_pause_time = 0.0

class UserInputHandlerInGameOver:
    def __init__(self, btnInfo, scoreInfo, phaseInfo, inputInfo):
        self.btnInfo = btnInfo
        self.scoreInfo = scoreInfo
        self.phaseInfo = phaseInfo
        self.inputInfo = inputInfo

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.R:
            self.btnInfo.reset()
            self.scoreInfo.reset()
            self.phaseInfo.reset()
            self.inputInfo.reset()

class PhaseTracker:
    def __init__(self, gameSound):
        self.gameSound = gameSound

        self.PHASE_PREP = 0
        self.PHASE_PLAY = 1
        self.PHASE_TIMEOUT = 2
        self.PHASE_GAMEOVER = 3
        self.PHASE_TIME = [0.0, 10.0, 70.0, 74.0]

        self.time_from_start = 0.0
        self.current_phase = self.PHASE_PREP

    def update(self, delta_time):
        self.time_from_start += delta_time
        if self.current_phase < self.PHASE_GAMEOVER:
            if self.time_from_start > self.PHASE_TIME[self.current_phase + 1]:
                self.current_phase += 1
                if self.current_phase == self.PHASE_PLAY:
                    arcade.sound.play_sound(self.gameSound.soundtrack)
                elif self.current_phase == self.PHASE_TIMEOUT:
                    arcade.sound.play_sound(self.gameSound.time_up)
                elif self.current_phase == self.PHASE_GAMEOVER:
                    arcade.sound.play_sound(self.gameSound.game_over)

    def reset(self):
        self.time_from_start = 0.0
        self.current_phase = self.PHASE_PREP

    def get_prep_time(self):
        return 1.0 - (self.time_from_start / self.PHASE_TIME[1])

    def get_timer_time(self):
        return 1.0 - ((self.time_from_start - self.PHASE_TIME[1])
            / (self.PHASE_TIME[2] - self.PHASE_TIME[1]))

    def get_time_remain(self):
        time_remain = self.PHASE_TIME[self.current_phase + 1] - self.time_from_start
        if time_remain < 0.0:
            time_remain = 0.0

        return time_remain
