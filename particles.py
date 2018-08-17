import curses
import random
import time

random.seed()

def random_bounded_gauss(mu, sigma, lower, upper):
    rand = random.gauss(mu, sigma)
    if rand < lower:
        rand = lower
    elif rand > upper:
        rand = upper

    return rand

class Particle:
    """Represents a simple particle."""

    def __init__(self, pos, ang):
        """
        Initialize particle with x-axis position and angle of motion.

        X-Axis position is in units of characters. Angle of motion is in
        units of characters to move per frame - positive is right,
        negative is left.
        """

        # This is (or at least, should be) fixed at program run!
        self.pos = pos
        self.ang = ang

class ParticleError(Exception):
    """Raise when an attribute of a Particle is incorrect."""

def main(stdsrc):
    # Initialize curses
    curses.curs_set(False)
    #stdsrc.nodelay(True)

    # Initialize PRNG
    random.seed()

    # Initialize custom code
    particles = list()

    # Main program
    try:
        while True:
            # Curses
            # ----------
            stdsrc.clear()

            # Custom
            # ----------
            # '-2' not '-1' because of a quirk in curses that means you
            # can't use the rightmost column.
            rand_pos = random.randrange(0, curses.COLS-2, 5)

            # Generate angle (2 methods):
            # 1. Bounded gauss distribution (harder to do, but 'cleaner'
            #    looking results). change the standard deviation as
            #    desired.
            # 2. Linear distribution (easiest to do)
            std_dev = 1.5
            rand_ang = int(random_bounded_gauss(0, std_dev, -6, 6))
            ##rand_ang = random.randrange(-6, 7)

            if len(particles) > curses.LINES-1:
                del particles[len(particles)-1]
            particles.insert(0, Particle(rand_pos, rand_ang))

            # Calculate
            for i in range(len(particles)):
                particles[i].pos += particles[i].ang

                if (
                    particles[i].pos < 0 or
                    particles[i].pos > curses.COLS-2
                   ):
                    particles[i].pos %= curses.COLS-2

            # Display
            for i in range(len(particles)):
                if particles[i].ang > 4:
                    dir_char = "-"
                elif particles[i].ang > 0:
                    dir_char = "/"
                elif particles[i].ang == 0:
                    dir_char = "|"
                elif particles[i].ang < 0:
                    dir_char = "\\"
                elif particles[i].ang < -4:
                    dir_char = "-"

                try:
                    stdsrc.addch(
                        (curses.LINES-1)-i, particles[i].pos,
                        ord(dir_char))
                except curses.error:
                    raise ParticleError(
                        "position ({0},{1}) out-of-bounds".format(
                        str((curses.LINES-1)-i), str(particles[i].pos))
                        )

            # Back to curses
            # ----------
            stdsrc.refresh()

            # Frame delay
            # ----------
            time.sleep(0.05)

    except KeyboardInterrupt:
        # This is how to exit normally
        return

curses.wrapper(main)

