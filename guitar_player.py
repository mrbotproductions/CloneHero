import mss.tools
from PIL import Image
import pyautogui 
import time
import numpy as np
import threading
import mss

# 100 keyboard keystrokes per second
pyautogui.PAUSE = 0.01

class CloneHero:
    def __init__(self):
        # vars for if key is currently held down
        self.A = False
        self.S = False
        self.J = False
        self.K = False
        self.L = False

        # screen pixels for gems in screenshot
        self.monitor = {"left": 650, "top": 910, "width": 586, "height": 15}
        self.screenshot = None

        # vertical line pixel within the screenshot for each key
        self.green = 51
        self.red = 184
        self.yellow = 311
        self.blue = 432
        self.orange = 565

    def startGame(self):
        # start pressing h every 25 seconds to unlock star bonus in game
        threading.Thread(target=self.runStarBonus, daemon=True, args=()).start()

        with mss.mss() as sct:
            while True:
                # screenshot
                sct_img = sct.grab(self.monitor)
                img = Image.new("RGB", sct_img.size)
                pixels = zip(sct_img.raw[2::4], sct_img.raw[1::4], sct_img.raw[0::4])
                img.putdata(list(pixels))
                self.screenshot = np.array(img)

                # each thread will check for each color gem
                g = threading.Thread(target=self.keyAnalyzer, daemon=True, args=(self.green, 'a', self.A))
                r = threading.Thread(target=self.keyAnalyzer, daemon=True, args=(self.red, 's', self.S))
                y = threading.Thread(target=self.keyAnalyzer,  daemon=True, args=(self.yellow, 'j', self.J))
                b = threading.Thread(target=self.keyAnalyzer,  daemon=True, args=(self.blue, 'k', self.K))
                o = threading.Thread(target=self.keyAnalyzer,  daemon=True, args=(self.orange, 'l', self.L))

                # start each thread
                g.start()
                r.start()
                y.start()
                b.start()
                o.start()

                # wait for all threads so we can start next screenshot cycle
                g.join()
                r.join()
                y.join()
                b.join()
                o.join()

    def runStarBonus(self):
        while True:
            time.sleep(25)
            pyautogui.press('h')

    def keyAnalyzer(self, x, keypress, keydown):
        for j in range(len(self.screenshot)):
            curPixel = self.screenshot[j][x]
            if keydown:
                if keypress == 'a' and (Color.isGreen(curPixel) or Color.isTeal(curPixel)):
                    return
                if keypress == 's' and (Color.isRed(curPixel) or Color.isTeal(curPixel)):
                    return
                if keypress == 'j' and (Color.isYellow(curPixel) or Color.isTeal(curPixel)):
                    return
                if keypress == 'k' and (Color.isBlue(curPixel) or Color.isTeal(curPixel)):
                    return
                if keypress == 'l' and (Color.isYellow(curPixel) or Color.isTeal(curPixel)):
                    return
            else:
                if Color.isWhite(curPixel) or Color.isTeal(curPixel):
                    pyautogui.keyDown(keypress)
                    if (keypress == 'a'):
                        self.A = True
                    elif (keypress == 's'):
                        self.S = True
                    elif (keypress == 'j'):
                        self.J = True
                    elif (keypress == 'k'):
                        self.K = True
                    elif (keypress == 'l'):
                        self.L = True
                    return
        if (keydown):
            pyautogui.keyUp(keypress)
            if (keypress == 'a'):
                self.A = False
            elif (keypress == 's'):
                self.S = False
            elif (keypress == 'j'):
                self.J = False
            elif (keypress == 'k'):
                self.K = False
            elif (keypress == 'l'):
                self.L = False

class Color:
    @staticmethod
    def isWhite(color):
        r,g,b = color
        L = 0.2126*r + 0.7152*g + 0.0722*b
        return L > 200

    @staticmethod
    def isRed(color):
        r,g,b = color
        threshold = max(r, g, b)
        return (
            threshold > 8
            and r == threshold
            and g < threshold*0.5
            and b < threshold*0.5
        )

    @staticmethod
    def isGreen(color):
        r,g,b = color
        threshold = max(r, g, b)
        return (
            threshold > 8
            and g == threshold
            and r < threshold*0.5
            and b < threshold*0.5
        )

    @staticmethod
    def isBlue(color):
        r,g,b = color
        threshold = max(r, g, b)
        return (
            threshold > 8
            and r < 150
            and b > 150
        )

    @staticmethod
    def isYellow(color):
        r,g,b = color
        threshold = max(r, g, b)
        return (
            threshold > 8
            and r >= 150
            and g >= 150
            and b <= 150
        )

    @staticmethod
    def isTeal(color):
        r,g,b = color
        return (
            b > 120 and g > 120 and ((g >= b and b >= r) or (b >= g and g >= r)) and r < 100
        )

if __name__ == '__main__':
    clonehero = CloneHero()
    clonehero.startGame()