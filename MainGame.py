import arcade
import math
from MainGameTracker import GameTracker

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

class MainGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.set_texture()
        self.set_var()

    def set_texture(self):
        self.gameTracker = GameTracker()
        self.arrow_up_texture = arcade.load_texture("images/arrow/arrow_up.png")
        self.arrow_down_texture = arcade.load_texture("images/arrow/arrow_down.png")
        self.arrow_left_texture = arcade.load_texture("images/arrow/arrow_left.png")
        self.arrow_right_texture = arcade.load_texture("images/arrow/arrow_right.png")
        self.block_unknown_texture = arcade.load_texture("images/arrow/block_unknown.png")
        self.bar_pause = arcade.load_texture("images/bar/pause_bar.png")
        self.bar_pause_progress = arcade.load_texture("images/bar/pause_progress.png")
        self.bar_prep = arcade.load_texture("images/bar/prep_bar.png")
        self.bar_prep_progress = arcade.load_texture("images/bar/prep_progress.png")
        self.how_to_play_texture = arcade.load_texture("images/HowToPlay.png")

    def set_var(self):
        self.arrow_texture_size = 50
        self.block_unknown_texture_size = 50
        self.bar_pause_size_x = 306
        self.bar_pause_size_y = 12
        self.bar_pause_progress_size_x = 300
        self.bar_pause_progress_size_y = 6
        self.bar_prep_size_x = 510
        self.bar_prep_size_y = 20
        self.bar_prep_progress_size_x = 500
        self.bar_prep_progress_size_y = 10


    def on_key_press(self, key, key_modifiers):
        self.gameTracker.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.gameTracker.on_key_release(key, key_modifiers)

    def animate(self, delta_time):
        self.gameTracker.update(delta_time)

    def on_draw(self):
        arcade.start_render()
        self.draw_btn()
        self.draw_how_to()
        self.draw_score()
        self.draw_combo()
        self.draw_phase()

    def draw_btn(self):
        player_1_btn_position_x = 70
        player_1_btn_position_y = 400
        player_2_btn_position_x = 520
        player_2_btn_position_y = 400
        player_btn_x_offset = 60

        for i in range(self.gameTracker.playerBtnInfo.MAX_QUEUE):
            self.draw_arrow(self.gameTracker.playerBtnInfo.player_1_btn[i]
                , player_1_btn_position_x + (i * player_btn_x_offset)
                , player_1_btn_position_y)
            self.draw_arrow(self.gameTracker.playerBtnInfo.player_2_btn[i]
                , player_2_btn_position_x + (i * player_btn_x_offset)
                , player_2_btn_position_y)

            if(i < self.gameTracker.playerBtnInfo.BLOCK_QUEUE
                and self.gameTracker.phaseTracker.current_phase == self.gameTracker.phaseTracker.PHASE_PLAY):
                if self.gameTracker.userInputHandlerInGame.player_1_disable_block == False:
                    self.draw_block_unknown(player_1_btn_position_x + (i * player_btn_x_offset)
                        , player_1_btn_position_y)
                if self.gameTracker.userInputHandlerInGame.player_2_disable_block == False:
                    self.draw_block_unknown(player_2_btn_position_x + (i * player_btn_x_offset)
                        , player_2_btn_position_y)

    def draw_arrow(self, arrow, x, y):
        if arrow == self.gameTracker.playerBtnInfo.BTN_UP:
            arcade.draw_texture_rectangle(x, y, self.arrow_texture_size
                , self.arrow_texture_size, self.arrow_up_texture)
        elif arrow == self.gameTracker.playerBtnInfo.BTN_LEFT:
            arcade.draw_texture_rectangle(x, y, self.arrow_texture_size
                , self.arrow_texture_size, self.arrow_left_texture)
        elif arrow == self.gameTracker.playerBtnInfo.BTN_RIGHT:
            arcade.draw_texture_rectangle(x, y, self.arrow_texture_size
                , self.arrow_texture_size, self.arrow_right_texture)
        elif arrow == self.gameTracker.playerBtnInfo.BTN_DOWN:
            arcade.draw_texture_rectangle(x, y, self.arrow_texture_size
                , self.arrow_texture_size, self.arrow_down_texture)

    def draw_block_unknown(self, x, y):
        arcade.draw_texture_rectangle(x, y, self.block_unknown_texture_size
            , self.block_unknown_texture_size, self.block_unknown_texture)

    def draw_how_to(self):
        arcade.draw_texture_rectangle(450, 110, 882, 205, self.how_to_play_texture)

    def draw_score(self):
        player_1_score_position_x = 400
        player_1_score_text_position_x = 50
        player_1_score_position_y = 300

        player_2_score_position_x = 850
        player_2_score_text_position_x = 500
        player_2_score_position_y = 300

        score_font_size = 40

        arcade.draw_text("Score : "
            , player_1_score_text_position_x, player_1_score_position_y
            , arcade.color.BLACK, score_font_size, align="left"
            , anchor_x="left", anchor_y="center")
        arcade.draw_text("Score : "
            , player_2_score_text_position_x, player_1_score_position_y
            , arcade.color.BLACK, score_font_size, align="left"
            , anchor_x="left", anchor_y="center")

        arcade.draw_text(str(self.gameTracker.playerScoreInfo.player_1_score)
            , player_1_score_position_x, player_1_score_position_y
            , arcade.color.BLACK, score_font_size, align="right"
            , anchor_x="right", anchor_y="center")
        arcade.draw_text(str(self.gameTracker.playerScoreInfo.player_2_score)
            , player_2_score_position_x, player_2_score_position_y
            , arcade.color.BLACK, score_font_size, align="right"
            , anchor_x="right", anchor_y="center")

    def draw_combo(self):
        player_1_combo_position_x = 400
        player_1_combo_text_position_x = 50
        player_1_combo_position_y = 240
        player_1_combo_color = self.get_combo_color(self.gameTracker.playerScoreInfo.player_1_combo)
        player_1_combo_size = self.get_combo_size(self.gameTracker.playerScoreInfo.player_1_combo)

        player_2_combo_position_x = 850
        player_2_combo_text_position_x = 500
        player_2_combo_position_y = 240
        player_2_combo_color = self.get_combo_color(self.gameTracker.playerScoreInfo.player_2_combo)
        player_2_combo_size = self.get_combo_size(self.gameTracker.playerScoreInfo.player_2_combo)

        arcade.draw_text("Combo : "
            , player_1_combo_text_position_x, player_1_combo_position_y
            , player_1_combo_color, player_1_combo_size, align="left"
            , anchor_x="left", anchor_y="center")
        arcade.draw_text("Combo : "
            , player_2_combo_text_position_x, player_2_combo_position_y
            , player_2_combo_color, player_2_combo_size, align="left"
            , anchor_x="left", anchor_y="center")

        arcade.draw_text(str(self.gameTracker.playerScoreInfo.player_1_combo)
            , player_1_combo_position_x, player_1_combo_position_y
            , player_1_combo_color, player_1_combo_size, align="right"
            , anchor_x="right", anchor_y="center")
        arcade.draw_text(str(self.gameTracker.playerScoreInfo.player_2_combo)
            , player_2_combo_position_x, player_2_combo_position_y
            , player_2_combo_color, player_2_combo_size, align="right"
            , anchor_x="right", anchor_y="center")

    def get_combo_color(self, combo):
        if combo < 10:
            return arcade.color.BLACK
        elif combo < 20:
            return arcade.color.ORANGE
        elif combo % 2 == 0:
            return arcade.color.RED
        else:
            return arcade.color.CADMIUM_RED

    def get_combo_size(self, combo):
        if combo < 10:
            return 20
        elif combo < 20:
            return 30
        else:
            return 40

    def draw_phase(self):
        if self.gameTracker.phaseTracker.current_phase == self.gameTracker.phaseTracker.PHASE_PREP:
            self.draw_phase_prep()
        elif self.gameTracker.phaseTracker.current_phase == self.gameTracker.phaseTracker.PHASE_PLAY:
            self.draw_phase_play()
        elif self.gameTracker.phaseTracker.current_phase == self.gameTracker.phaseTracker.PHASE_TIMEOUT:
            self.draw_phase_timeout()
        elif self.gameTracker.phaseTracker.current_phase == self.gameTracker.phaseTracker.PHASE_GAMEOVER:
            self.draw_phase_gameover()

    def draw_phase_prep(self):
        arcade.draw_text("Remember the Sequence", 450, 550, arcade.color.BLACK, 50
            , align="center", anchor_x="center", anchor_y="center")
        self.draw_prep_bar()

    def draw_phase_play(self):
        self.draw_timer(self.gameTracker.phaseTracker.current_phase)
        self.draw_timer_bar()
        self.draw_pause_bar()

    def draw_phase_timeout(self):
        arcade.draw_text("Time's up", 450, 500, arcade.color.RED, 50
            , align="center", anchor_x="center", anchor_y="center")

    def draw_phase_gameover(self):
        player_1 = self.gameTracker.playerScoreInfo.player_1_score
        player_2 = self.gameTracker.playerScoreInfo.player_2_score
        text_x = 450
        text_y = 500
        text_size = 50

        if(player_1 > player_2):
            arcade.draw_text("Player 1 Win", text_x, text_y, arcade.color.RED
                , text_size , align="center", anchor_x="center", anchor_y="center")
        elif(player_1 < player_2):
            arcade.draw_text("Player 2 Win", text_x, text_y, arcade.color.BLUE
                , text_size , align="center", anchor_x="center", anchor_y="center")
        else:
            arcade.draw_text("Draw", text_x, text_y, arcade.color.BLACK
                , text_size , align="center", anchor_x="center", anchor_y="center")

    def draw_prep_bar(self):
        prep_bar_x = 450
        prep_bar_y = 475
        arcade.draw_texture_rectangle(prep_bar_x, prep_bar_y
            , self.bar_prep_size_x, self.bar_prep_size_y, self.bar_prep)
        arcade.draw_texture_rectangle(prep_bar_x, prep_bar_y
            , self.bar_prep_progress_size_x * self.gameTracker.phaseTracker.get_prep_time()
            , self.bar_prep_progress_size_y, self.bar_prep_progress)

    def draw_timer_bar(self):
        prep_bar_x = 450
        prep_bar_y = 475
        arcade.draw_texture_rectangle(prep_bar_x, prep_bar_y
            , self.bar_prep_size_x, self.bar_prep_size_y, self.bar_prep)
        arcade.draw_texture_rectangle(prep_bar_x, prep_bar_y
            , self.bar_prep_progress_size_x * self.gameTracker.phaseTracker.get_timer_time()
            , self.bar_prep_progress_size_y, self.bar_prep_progress)

    def draw_pause_bar(self):
        player_1_bar_x = 225
        player_1_bar_y = 340
        player_1_pause = self.gameTracker.userInputHandlerInGame.get_player_1_pause_time()

        player_2_bar_x = 675
        player_2_bar_y = 340
        player_2_pause = self.gameTracker.userInputHandlerInGame.get_player_2_pause_time()

        if player_1_pause > 0.0 :
            arcade.draw_texture_rectangle(player_1_bar_x, player_1_bar_y
                , self.bar_pause_size_x, self.bar_pause_size_y, self.bar_pause)
            arcade.draw_texture_rectangle(player_1_bar_x, player_1_bar_y
                , self.bar_pause_progress_size_x * player_1_pause
                , self.bar_pause_progress_size_y, self.bar_pause_progress)

        if player_2_pause > 0.0 :
            arcade.draw_texture_rectangle(player_2_bar_x, player_2_bar_y
                , self.bar_pause_size_x, self.bar_pause_size_y, self.bar_pause)
            arcade.draw_texture_rectangle(player_2_bar_x, player_2_bar_y
                , self.bar_pause_progress_size_x * player_2_pause
                , self.bar_pause_progress_size_y, self.bar_pause_progress)

    def draw_timer(self, phase):
        timer_position_x = 450
        timer_position_y = 550
        timer_size = 50
        time_remain = self.gameTracker.phaseTracker.get_time_remain()
        timer_color = self.get_timer_color(time_remain)

        arcade.draw_text(str(math.ceil(time_remain)), timer_position_x, timer_position_y
            , timer_color, timer_size, align="center"
            , anchor_x="center", anchor_y="center")

    def get_timer_color(self, time_remain):
        if time_remain > 30 :
            return arcade.color.BLACK
        elif time_remain > 20 :
            return arcade.color.GIANTS_ORANGE
        elif time_remain > 10 :
            return arcade.color.ORANGE_RED
        elif time_remain > 5 :
            return arcade.color.RED
        else :
            return arcade.color.RED_DEVIL

if __name__=='__main__':
    window = MainGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
