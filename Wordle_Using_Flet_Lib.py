"Flet Wordle Clone Game"

#modules
import flet
from flet import *
from nltk.corpus import words #we're using the NLTK lib to get a list of valid ENGLISH words.
from time import sleep
from random import choice

# Create the control list where we store our rows
ROWS = []


# and we create a decorator function to help use with storing the control instance easily
def store_row_in_list(function):
    def wrapper(*args, **kwargs):
        res = function(*args, **kwargs)
        ROWS.append(res)
        return res

    return wrapper



# create a seprate class to display errors
class GameErrorHandler(UserControl):
    def __init__(self):
        super().__init__()

    # decorate it
    @store_row_in_list
    def set_error_text(self):
        return Text(size=11, weight="bold")

    def build(self):
        return Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                self.set_error_text()
            ]
        )


class GameInputField(UserControl):
    def __init__(self,word:str):
        # we need a few variables here to keep track of the game
        self.line = 0 # this keeps track of the rows
        self.guess = 5 # number of guesses although not necessarily for this particular game set up
        self.word = word # we'll change this letter but self.word is the word chosen by the random lib when we fire up the game.
        super().__init__()

    # Let's Start with the game logic now
    def get_letters(self, e):
        # first, set the submitted word to a variable
        # set another Variable to the same value
        word, is_word = e.control.value, e.control.value
        
        # first we check if the word is 5-letters long
        if len(word) == 5:
            # then we check if the word is a valid english word
            #recall that the letter gets a list of 24k english words.
            if word in words.words():
                # if all these are true, we need to first turn the string into a list of characters.
                word = [*word] #this is a SHort hand notation for it
                
                # now, first we need to cheeck if the submitted is the actual word
                if is_word == self.word:
                    # we can now generate text on the screen to display game stats
                    ROWS[6].value = f"CORRECT! The word was {self.word.upper()}."
                    ROWS[6].update()
                # next we check if the player has run out of guesses/lines => these are probably the same so one variable would be fine
                elif self.line > 5 or self.guess < 1:
                    ROWS[6].value = f"Sorry! You've run out of Tries. The word was {self.word.upper()}. Try again!"
                    ROWS[6].update()
                    print("No More Tries")

                # if none of the above are satisfied, we can carry on with the game
                # evrytime a player submits a word, we need to loop over the boxes grid and check several things:
                # 1.  is the leter in the word, is the letter in the correct place, or is the letter in the word but misplaced
                for index, box in enumerate(ROWS[self.line].controls[:]):
                    # now we need to check the parameters.
                    # we check to see if the letter in the word by the player matches the letter in secret word at the same index location... 
                    # add a if statement here!!
                    if word[index] in self.word:
                        if word[index] == self.word[index]:
                            box.content.value = word[index].upper()
                            box.content.offset = transform.Offset(0,0)
                            box.content.opacity = 1
                            box.bgcolor = "green900"
                            box.update()
                            sleep(0.4)

                        # the else here will handle the letter being in the word, but at the wrong place
                        else:
                            box.content.value = word[index].upper()
                            box.content.offset = transform.Offset(0,0)
                            box.content.opacity = 1
                            box.bgcolor = "#b59e38"
                            box.update()
                            sleep(0.4)

                    # if the letter is not in the word, show no colors
                    else:
                        box.content.value = word[index].upper()
                        box.content.offset = transform.Offset(0,0)
                        box.content.opacity = 1
                        box.update()
                        sleep(0.4)

                # make sure to increment th variables
                self.line += 1
                self.guess -= 1

            # let's handle submit errors
            else:
                ROWS[6].value = f"Must be a valid word. Try again!"
                ROWS[6].update()

        else:
            ROWS[6].value = f"Word must be a 5-letters long. Try again!"
            ROWS[6].update()

        # clear the entry
        e.control.value = ""
        e.control.update()


    def clear_error(self, e):
        ROWS[6].value = ""
        ROWS[6].update()

    # Let's first build the UI Textfield before using it
    def build(self):
        return Row(
            spacing=20,
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Container(
                    height=45,
                    width=250,
                    border=border.all(0.5, colors.WHITE24),
                    border_radius=6,
                    content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            TextField(
                                border_color="transparent",
                                bgcolor="transparent",
                                height=20,
                                width=200,
                                text_size=12,
                                content_padding=3,
                                cursor_color="white",
                                cursor_width=1,
                                color="white",
                                hint_text="Type a 5-letter word...",
                                text_align="center",
                                on_submit=lambda e: self.get_letters(e),
                                on_focus=lambda e: self.clear_errors(e),
                            ),
                        ],
                    ),
                )
            ],
        )


class GameGrid(UserControl):
    def __init__(self):
        super().__init__()
    
    # Make sure to decorate this function so we store these 6 rows
    @store_row_in_list 
    def create_single_row_grid(self):
        row = Row(alignment=MainAxisAlignment.CENTER)
        for __ in range(5):
            row.controls.append(
                Container(
                    width=52, height=52,
                    border=border.all(0.5, colors.WHITE24),
                    alignment=alignment.center,
                    clip_behavior=ClipBehavior.HARD_EDGE,
                    animate=animation.Animation(300, "decelerate"),
                    content= Text(
                        size=20,
                        weight="bold",
                        opacity=0,
                        offset=transform.Offset(0, 0.75),
                        animate_opacity=animation.Animation(400, "decelerate"),
                        animate_offset=animation.Animation(400, "decelerate"),

                    )
                )
            )

        # Make Sure to return the row!
        return row

    def build(self):
        return Column(
            controls=[
                self.create_single_row_grid(),
                self.create_single_row_grid(),
                self.create_single_row_grid(),
                self.create_single_row_grid(),
                self.create_single_row_grid(),
                self.create_single_row_grid(),
            ]
        )


# our main game function
def main (page: Page):
    # some dimenstions
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # we need to generate a random word from NLTK word list
    # we'll use some list comprehension to do this.
    word = words.words() # this generates a list of words, let's test this.
    # so there's about 24k words in the list 
    # This may look complex, but it can be broken down.
    # what we're doing here is using the lambda function to set x at a length of 5, and we pass it into the filter function so that every S-letter word in the 24K list we generated above will get put in a new list called word
    word = list(filter(lambda x: len(x) == 5, word))
    # let's test this => so there are 10K letters which are 5 letters long.
    word = choice(
        word
    ).lower() # here we use the random lib choice to randomly select a word from the list, and we make it all lower caps so it's easire to handle

    # our main UI place 
    page.add(
        Column(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[Text("Wordle",size=25, weight="bold")],
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text(
                            "Popular Word Game Clone Made Using Python & Flet",
                            size=11,
                            weight="bold",
                            color=colors.WHITE54,
                        )
                    ],
                ),
                # I'll skip the rules text UI.
                Divider(height=20, color=colors.TRANSPARENT),
                #first we will thw game grid...
                GameGrid(),
                Divider(height=10, color=colors.TRANSPARENT),
                # Now for Game logic + UI
                # finally, instead of using a predefined word we can now generate a random word and pass it to the main class 
                GameInputField(word),
                Divider(height=10, color=colors.TRANSPARENT),
                GameErrorHandler(),
            ],
        )
    )
 
    page.update()


if __name__ == "__main__":
    flet.app(target=main)