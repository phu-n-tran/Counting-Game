# ----------------------------------------------------------------------
# Name:        The counting game
# Author:       Phu Tran
# Purpose:     implement the game using tkinter
#
# Date:       Spring 2019
# ----------------------------------------------------------------------
"""
This is a counting game using tkinter

Rules:
    1. Use cmd line to set player name and difficulty or will use
       the default
    2. Each round of the game will start after click the 'next round'
       button
    3. Player need to keep count of the number of time a specific
       image appears
    4. Game will end when the user give up or run out of lives
    5. Uncover your score after at the end game phrase
"""

import tkinter
import argparse
import random

class CountingGame:

    """
    GUI for counting game

    Argument:
    parent (tkinter.Tk): the root window object

    Attributes:
        parent (tkinter.Tk): copy of the root window object
        welcome_frame (tkinter.Frame): the frame the display
                                       welcome screen
        main_frame (tkinter.Frame): the frame that holds all
                                    player progress
        bottom_frame (tkinter.Frame): the frame inside the main_frame
                that hold buttons and info in the bottom of the screen
        canvas (tkinter.Canvas): the widget defining the area to
                                animate moving images
        canvas1 (tkinter.Canvas): the widget the bind with an event
        count_canvas: (tkinter.Canvas): the widget hold the guess image
        image_on_canvas (image obj): the widget hold the guess image
        image_list (list): list of images objects that will be use
                            for animate
        list_of_after (list): the after id of each images
        reset_button (tkinter.Button): let the player reset the game
        next_round_button (tkinter.Button): let the player move to
                                            next round
        end_button (tkinter.Button): let the player give up mid-way
        submit_button (tkinter.Button): let player submit their answer
        current_lives (int): hold the player's lives
        current_round (int): hold the current round that player is play
        current_score (int): hold the score that player has earn
        user_answer (int): hold player answer
        answer (int): hold the correct answer
        user_input (tkinter.StringVar): display text on entry widget
        status (tkinter.StringVar): display text on entry widget
        difficulty (String): hold the difficulty mode
        name (String): hold the player's name
        speed(int): the speed of animation
        new_round(boolean): Indicates that current round hasn't ended
                            and player can submit an answer
        next_round(boolean): Indicates that the current round is over
                            and can moves onto next round

    """



    def __init__(self, parent):
        self.difficulty, self.name = self.get_arguments()

        # for later use
        self.user_answer = None


        # - A list to store the after IDs of all the after method
        #   waiting to be invoked
        # - new_round boolean variable to clarify if this is the
        #   beginning of a round(if yes, we can submit player's answer
        #   with submit button)
        # - next_round boolean variable to see if we can move onto next
        #  round and animates the moving icons for next round with
        #  next_round_button
        self.list_of_after_id = []
        self.new_round = True
        self.next_round = True

        # Initialize the stage of the game
        # Give amount of lives depending on difficulty and sets speed
        # Easy - 3 lives, 1 pixel speed
        # Medium - 2 lives, 2 pixel speed
        # Hard - 1 live, 2 pixel speed
        if self.difficulty == 'easy':
            self.current_lives = 3
            self.speed = 1
        elif self.difficulty == 'medium':
            self.current_lives = 2
            self.speed = 2
        else:
            self.current_lives = 1
            self.speed = 2

        self.current_round = 1
        self.current_score = 0

        # upload images first
        spartan_icon_img = tkinter.PhotoImage(file='SpartanSpirit.gif')
        butterfly_icon_img = tkinter.PhotoImage(file='butterfly.gif')
        logo1_img = tkinter.PhotoImage(file='logo1.gif')
        logo2_img = tkinter.PhotoImage(file='logo2.gif')

        self.image_list = [spartan_icon_img, butterfly_icon_img,
                           logo1_img, logo2_img]

        # Create the initial screen: Welcome screen
        self.parent = parent
        self.parent.title("Counting Game")
        self.parent.geometry('500x580')

        self.main_frame = tkinter.Frame(parent)
        self.main_frame.grid()

        # call method to make the welcome screen
        self.make_welcome_screen()

    def get_arguments(self):
        """
        Parse and validate the command line arguments.
        :return: tuple containing the difficulty (string)
                 and name (string)
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('difficulty',
                            help='What level of difficulty do you like?',
                            choices=['easy', 'medium', 'hard'], nargs='?',
                            default="easy")

        parser.add_argument('name',
                            help='What is the name of the main character?',
                            nargs='?',
                            default='Player')

        arguments = parser.parse_args()
        name = arguments.name
        difficulty = arguments.difficulty
        return difficulty, name

    def make_welcome_screen(self):
        """
        Display the rule on welcome screen for player
        :return:
        """
        wel_message = tkinter.Label(self.main_frame, text="\n\n   WELCOME TO "
                                    "THE COUNTING GAME!",
                                    font=('arial', 19, 'bold'), fg='steelblue')
        wel_message.grid()

        instruction = tkinter.Label(self.main_frame, text="\n\nRULES:",
                                    font=('arial', 12, 'bold'),
                                    fg='dark goldenrod')
        instruction.grid()
        rule = tkinter.Label(self.main_frame,
                              text=
                              "1. You will start with set amount of lives "
                                  "depend on the level of difficulty\n"
                                  "the default mode is 'easy', use cmd line "
                                  "to change mode\n\n"
                              "2. Multiple items will appear on screen when "
                                  "game start and you need   \nto count the "
                                  "number of one specific items that appear "
                                  "on screen   \n\n"
                             "3.  The game will end when you press the give "
                                  "up button or you have run\nout of "
                                  "lives\n\n"
                             "4.  Check out the hidden mystery at the end of"
                                  " game and HAVE FUN!!!       \n\n\n",
                             font='arial 9')
        rule.grid()

        # Start game button invokes start_game method when clicked
        start_game = tkinter.Button(self.main_frame, text="Start Game",
                                    width=15, command=self.start_game,
                                    fg='light goldenrod', font='arial 12 bold',
                                    bg='steelblue')
        start_game.grid()


    def start_game(self):
        """
        move from welcome screen to in_game screen
        :return:
        """
        # Destroys the welcome screen
        self.main_frame.destroy()
        # Move to the next stage: game_page
        self.game_page()


    def game_page(self):
        """
        Display how the game page should look like
        :return:
        """
        self.main_frame = tkinter.Frame(self.parent)
        self.main_frame.grid()

        player_display = tkinter.Label(self.main_frame,
                                       text=f'\nWelcome {self.name}!',
                                       fg='steelblue',
                                       font='arial 15 italic bold')
        player_display.grid()

        # establish player info
        game_info_frame = tkinter.Frame(self.main_frame)
        game_info_frame.grid()

        self.num_lives = tkinter.Label(game_info_frame,
                                  text=f'Lives remain  {self.current_lives}',
                                  font=('arial', 12, 'bold'), fg='steelblue')
        self.num_lives.grid(row=0, column=1)

        spacing = tkinter.Label(game_info_frame, text="\t")
        spacing.grid(row=0, column=2)

        self.num_round = tkinter.Label(game_info_frame,
                                  text=f'Round  {self.current_round}',
                                  font=('arial', 12, 'bold'), fg='steelblue')
        self.num_round.grid(row=0, column=3)

        spacing2 = tkinter.Label(game_info_frame, text="\t")
        spacing2.grid(row=0, column=4)

        self.score = tkinter.Label(game_info_frame,
                              text=f'Score  {self.current_score}',
                                  font=('arial', 12, 'bold'), fg='steelblue')
        self.score.grid(row=0, column=5)

        # establish game screen
        self.canvas = tkinter.Canvas(self.main_frame, width=500, height=350,
                                     background='white')
        # register our canvas with a geometry manager
        self.canvas.grid()

        # establish button
        self.bottom_frame = tkinter.Frame(self.main_frame)
        self.bottom_frame.grid()

        # Attaches method reset_func to reset_button
        self.reset_button = tkinter.Button(self.bottom_frame, text="Reset",
                                           command=self.reset_func)
        self.reset_button.grid(row=3, column=0)

        # Attaches the game_logic method to next_round_button
        self.next_round_button = tkinter.Button(self.bottom_frame, width=10,
                                                bg='steelblue',
                                                fg='light goldenrod',
                                                font='arial 9 bold',
                                                text="Start",
                                                command=self.game_logic)
        self.next_round_button.grid(row=3, column=1)

        # Attaches the end_game method to end_button aka
        # the give up button
        self.end_button = tkinter.Button(self.bottom_frame, text="Give Up",
                                         command=self.end_game)
        self.end_button.grid(row=3, column=2)

        # Create the count canvas here before starting the first round
        # The count canvas is the canvas that stores the image that we
        # are counting each round
        self.create_count_canvas()

    def game_logic(self):
        """
        Contain the logic of the game
        Responsible for generating images and animating them each round
        Also picks a random image to count each round
        :return:
        """

        # Change next_round_button text from "Start" to "Next Round"
        self.next_round_button.configure(text="Next Round")

        # If next_round is false then player hasn't submitted an answer
        # so return and do nothing
        if not self.next_round:
            return

        # reset info on the display screen to let player know what
        # going on
        self.status.set('Enter your answer in text field above and '
                        'press submit!')

        # Randomizes an index and retrieves an image from
        # self.image_list as the image to count. If there is no image on
        # count canvas, create an image and stores the image_ID. If
        # there is already an image, simply replaces that image with
        # the new image
        index_of_obj = random.randint(0,3)
        new_obj = self.image_list[index_of_obj]
        if self.image_on_count_canvas is None:
            self.image_on_count_canvas = self.count_canvas.create_image(25, 25,
                                                                 image=new_obj)
        else:
            self.count_canvas.itemconfig(self.image_on_count_canvas,
                                         image=new_obj)

        # Randomizes the amount of images to be created for each
        # of the 4 icon
        num_of_first_image = random.randint(1, self.current_round+1)
        num_of_second_image = random.randint(1, self.current_round+1)
        num_of_third_image = random.randint(1, self.current_round+1)
        num_of_fourth_image = random.randint(1, self.current_round+1)

        # Find and stores the correct answer to the question
        self.answer = None
        if index_of_obj == 0:
            self.answer = num_of_first_image
        elif index_of_obj == 1:
            self.answer = num_of_second_image
        elif index_of_obj == 2:
            self.answer = num_of_third_image
        else:
            self.answer = num_of_fourth_image

        # ~~for debug purpose~~
        # print(num_of_first_image)
        # print(num_of_second_image)
        # print(num_of_third_image)
        # print(num_of_fourth_image)

        # Use a random wait timer for after method. These after methods
        # creates an image on the canvas and animates them
        # Add the after_id of each after method to list_of_after_id
        # After each iteration, increases wait_timer by 1500 for the
        # next image's after method
        wait_timer = random.randint(500, 1000)
        for x in range(num_of_first_image):
            after_id = self.parent.after(wait_timer,
                                lambda: self.create_image(self.image_list[0]))
            self.list_of_after_id.append(after_id)
            wait_timer += 1500
        wait_timer = random.randint(300, 500)
        for x in range(num_of_second_image):
            after_id = self.parent.after(wait_timer,
                                lambda: self.create_image(self.image_list[1]))
            self.list_of_after_id.append(after_id)
            wait_timer += 1500
        wait_timer = random.randint(500, 1000)
        for x in range(num_of_third_image):
            after_id = self.parent.after(wait_timer,
                                lambda: self.create_image(self.image_list[2]))
            self.list_of_after_id.append(after_id)
            wait_timer += 1500
        wait_timer = random.randint(600, 1000)
        for x in range(num_of_fourth_image):
            after_id = self.parent.after(wait_timer,
                                lambda: self.create_image(self.image_list[3]))
            self.list_of_after_id.append(after_id)
            wait_timer += 1500

        # Prints the correct answer to console
        # for error checking purposes
        print("For convenience purpose -> Correct Answer: ", self.answer)

        # Since we just called next_round method to start the next round
        # Set self.next_round to false until player submit an answer
        # Set new_round to True to indicate that the player can
        # submit an answer
        self.new_round = True
        self.next_round = False

    def create_count_canvas(self):
        """
        This method create the count canvas once and all the widgets
        that come with it
        :return:
        """
        # create question label
        question = tkinter.Label(self.bottom_frame, fg='steelblue',
                                 font='arial 10 italic bold',
                                 text="How many times did this appear on the "
                                      "screen?")
        question.grid(row=0, column=1)

        self.count_canvas = tkinter.Canvas(self.bottom_frame, width=50,
                                           height=50, background='white')

        self.image_on_count_canvas = None
        self.count_canvas.grid(row=1, column=0)

        # the entry widget that get user answer
        self.user_input = tkinter.StringVar()
        entry_field = tkinter.Entry(self.bottom_frame, width=8,
                                    textvariable=self.user_input,
                                    bg='light goldenrod')
        entry_field.grid(row=1, column=1)

        # the entry widget that let the user know what to do
        self.status = tkinter.StringVar()
        entry_field1 = tkinter.Entry(self.bottom_frame, width=50,
                                    textvariable=self.status, state='disabled')
        self.status.set('Press start to starts the first round!')
        entry_field1.grid(row=2, column=1)

        # Attaches the get_user_answer method to submit button
        submit_button = tkinter.Button(self.bottom_frame, text="submit",
                                       bg='light goldenrod', fg='steelblue',
                                       command=self.get_user_answer)
        submit_button.grid(row=1, column=2)

    def create_image(self, obj):
        """
        This method creates an image on the canvas based on the image
        passed in as parameter but randomizes the y-axis placement
        location on the canvas. This method also stores the image_id of
        the newly created image and passes it to the animation method
        :param obj:(image object) the image that will be drawn on canvas
        :return:
        """
        randomize = random.randint(0,3)
        if randomize == 0:
            image_id = self.canvas.create_image(25, 50, image=obj)
        elif randomize == 1:
            image_id = self.canvas.create_image(25, 125, image=obj)
        elif randomize == 2:
            image_id = self.canvas.create_image(25, 200, image=obj)
        else:
            image_id = self.canvas.create_image(25, 275, image=obj)
        self.animation(image_id)

    def get_user_answer(self):
        """
        Try to convert the user inputted answer into an integer.
        if encounters ValueError, simply do nothing and return
        :return:
        """
        try:
            self.user_answer = int(self.user_input.get())
            self.user_input.set('')
        except ValueError:
            self.status.set('Invalid input! Please try again')
            return

        # If it is not the beginning of a new round set user_answer
        # do nothing else and return
        if not self.new_round:
            return

        # After receiving a valid answer from player, set new_round to
        # False indicating that player can no longer submit another
        # answer and set next_round to True which mean it is now
        # valid to starts the next round
        self.new_round = False
        self.next_round = True

        # If you presses the submit button early before animation
        # finishes, this section:
        # - cancel all the after method in queue waiting to create
        #   new images on canvas.
        # - Clear the list_of_after_id to hold fresh new after_ids
        #   of next round
        # - Delete all items(images still moving) on canvas
        ###
        for after_id in self.list_of_after_id:
            self.parent.after_cancel(after_id)
        self.list_of_after_id.clear()
        self.canvas.delete("all")

        # Increments and update the current round label
        self.current_round += 1
        self.num_round.configure(text=f'Round  {self.current_round}')

        # If answer is correct, increments and updates the score
        if self.user_answer == self.answer:
            self.current_score += 1
            self.score.configure(text=f'Score  {self.current_score}')
            self.status.set('Correct Answer! Press next round to continue')
        else:
            # If answer is incorrect, decrements player's remaining
            # lives
            # If lives hit 0, invokes end_game() function and return
            # Else, update the remaining lives of player
            self.current_lives -= 1
            if self.current_lives == 0:
                self.end_game()
                return
            self.num_lives.configure(text=f'Lives remain {self.current_lives}')
            self.status.set('Incorrect Answer! Press next round to continue')


    def animation(self, image_id):
        """
        Create animation of the picture
        :param image_id: the image_id to animates
        :return:
        """
        # Declare variables x, y
        x = None
        y = None

        # If the canvas is not empty(has images), then retrieves the
        # x,y coordinates of the image
        if self.canvas.find_all():
            x, y = self.canvas.coords(image_id)

        # If x and y are None or the x coordinates is > 520 then returns
        # and stop animating
        if x is None and y is None or x > 520:
            return
        else:
            # Else, moves the image by the speed amount according
            # to self.speed
            # If there is an overlapped object and the object is
            # farther along the x-axis don't move the image only moves
            # the other overlapped object by self.speed+1 else if there
            # is no overlapping object then moves the image by
            # self.speed
            #
            # obj_id is a tuple that always contain at least 1
            # coordinate
            # If there is no overlap object, it still returns the obj_id
            # of the closest image at boundary (x,y) and (x+20, y) which
            # is image_id that why we check x != x1 if they
            # are different then it mean there are indeed overlapping
            # objects otherwise  just move the image at the normal speed
            obj_id = self.canvas.find_overlapping(x,y,x+20,y)
            x1, y1 = self.canvas.coords(obj_id[0])
            if x != x1:
                self.canvas.move(obj_id[0], self.speed+1, 0)
            else:
                self.canvas.move(image_id, self.speed, 0)
            self.parent.after(20, lambda: self.animation(image_id))


    def reset_func(self):
        """
        To reset, all info and data of the game. Start game from
        beginning
        :return:
        """
        # cancel all after method waiting to create new
        # images on canvas and clear all moving animation
        # clear all moving animation
        for after_id in self.list_of_after_id:
            self.parent.after_cancel(after_id)
        self.list_of_after_id.clear()
        self.canvas.delete("all")

        # reset everything to beginning
        self.new_round = True
        self.next_round = True

        # reinitialize the score
        self.current_score = 0
        self.current_round = 1

        if self.difficulty == 'easy':
            self.current_lives = 3
        elif self.difficulty == 'medium':
            self.current_lives = 2
        else:
            self.current_lives = 1

        self.canvas.destroy()
        self.main_frame.destroy()

        # call the start_game() method to restart the game
        self.start_game()

    def end_game(self):
        """
        Get rid of everything and display the end screen with mystery
        event
        :return:
        """
        self.main_frame.grid_forget()
        self.canvas1 = tkinter.Canvas(self.parent, width=500, height=580,
                                      background='white')
        self.canvas1.grid()
        self.canvas1.create_text(250, 50, fill="goldenrod",
                                 font=('arial', 30, 'italic', 'bold'),
                                 text="GAME OVER")

        self.canvas1.create_text(250, 150, text=f'Your score is',
                                 font=('arial', 15))
        self.canvas1.create_text(250, 250, text=f'{self.current_score}',
                                 font=('arial', 40))

        self.canvas1.create_image(180, 200, image=self.image_list[1])
        self.canvas1.create_rectangle(200, 200, 300, 300, fill='goldenrod')
        self.canvas1.create_rectangle(210, 210, 290, 290, fill='steelblue')
        self.canvas1.create_image(250, 250, image=self.image_list[2])

        self.canvas1.create_polygon(230, 340, 250, 320, 270, 340)
        self.canvas1.create_rectangle(240, 340, 260, 370, fill='black')

        self.canvas1.create_text(250, 390, text='Click and keep clicking on '
                                                'the box to uncover '
                                                'your score...')

        # Attaches select method to button clicks on canvas
        self.canvas1.bind("<Button-1>", self.select_to_delete)

    def select_to_delete(self, event):
        """
        Find the widget closest to point of button click and
        delete that widget
        If there are no widgets, destroy the root window
        :param event (tkinter.Event)
        :return: None
        """
        shape = self.canvas1.find_closest(event.x, event.y)
        self.canvas1.delete(shape)

        if not shape:
            self.parent.destroy()


def main():
    root = tkinter.Tk()
    game = CountingGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
