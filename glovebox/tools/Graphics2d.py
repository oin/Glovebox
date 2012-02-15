# from http://py-fun.googlecode.com/svn-history/r10/trunk/toolbox/graphics2d.py
'''graphics2d.py

Basic 2d graphics shapes to use with pyglet/opengl.

To make use of some of the advanced options (for example, line stippling),
one must be familiar with the opengl documentation.
'''
from pyglet.gl import *

__all__ = ["draw_arc", "draw_circle", "draw_line", "draw_rect", "draw_ring"]

def draw_line(x1, y1, x2, y2, color=(1.0, 1.0, 1.0, 1.0), line_width=1,
    line_stipple=False):
    '''draws a line from (x1, y1) to (x2, y2).

        Note: line_stipple, which has a default value of False, needs to be
        specified as a 2-tuple (factor and stipple pattern e.g. 0x00FF)

    '''
    glLineWidth(line_width)
    if line_stipple:
        glLineStipple(*line_stipple)
        glEnable(GL_LINE_STIPPLE)
    glBegin(GL_LINES)
    glColor4f(*color)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
    if line_width != 1:  # reset to default
        glLineWidth(1)
    if line_stipple:
        glDisable(GL_LINE_STIPPLE)

def draw_rect(x, y, width, height, color=(1.0, 1.0, 1.0, 1.0),
            filled=True, line_width=1):
    '''draws a rectangle starting at (x, y) with width and height specified.

       Note: line_width is only relevant if filled==False.

    '''

    if filled:
        glBegin(GL_QUADS)
    else:
        glLineWidth(line_width)
        glBegin(GL_LINE_LOOP)
    glColor4f(*color)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    if not filled and line_width != 1:  # reset to default
        glLineWidth(1)

def draw_circle(x, y, r, color=(1.0, 1.0, 1.0, 1.0)):
    '''draws a circle of radius r centered at (x, y)'''
    draw_ring(x, y, 0, r, color)

def draw_ring(x, y, inner, outer, color=(1.0, 1.0, 1.0, 1.0)):
    '''draws a ring of inner radius "inner" and outer radius "outer"
       centered at (x, y).

    '''
    glPushMatrix()
    glColor4f(*color)
    glTranslatef(x, y, 0)
    q = gluNewQuadric()
    # a circle is written as a number of triangular slices; we use
    # a maximum of 360 which looked smooth even for a circle as
    # large as 1500 px.
    # Smaller circles can be drawn with fewer slices - the rule we
    # use amount to approximately 1 slice per px on the circumference
    slices = 10 * min(10, 10*outer)
    gluDisk(q, inner, outer, int(slices), 1)
    glPopMatrix()

def draw_arc(x, y, inner, outer, start=0, sweep=180, color=(1.0, 1.0, 1.0, 1.0)):
    '''draws an arc of circle of inner radius "inner" and outer radius "outer"
       centered at (x, y).   The arc will start at a value "start" which is
       specified in degrees as measured counterclockwise starting from the
       x-axis and will "sweep" over a specified angle measured in degrees.

    '''
    glPushMatrix()
    glColor4f(*color)
    glTranslatef(x, y, 0)
    q = gluNewQuadric()
    # a circle is written as a number of triangular slices; we use
    # a maximum of 360 which looked smooth even for a circle as
    # large as 1500 px.
    # Smaller circles can be drawn with fewer slices - the rule we
    # use amount to approximately 1 slice per px on the circumference
    slices = 10 * min(10, 10*outer)
    # the opengl convention is to start on the +y axis in the clockwise
    # direction; we follow the mathematical notation, starting on the
    # +x axis, in the counterclockwise direction
    gluPartialDisk(q, inner, outer, int(slices), 1, 90-start, -sweep)
    glPopMatrix()

# to do
##draw_polygon
##create classes corresponding to each graphical object

if __name__ == '__main__':
    from pyglet import window
    from pyglet import clock
    from pyglet.window import key

    win = window.Window(800, 600, vsync=False)
    glEnable(GL_BLEND)
    fps_display = clock.ClockDisplay()

    while not win.has_exit:

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        win.dispatch_events()
        clock.tick()
        win.clear()
        draw_line(0, 0, 300, 300)
        color = (0, 1.0, 0, 1)
        draw_line(10, 10, 300, 200, color)
        color = (1.0, 1.0, 0, 1)
        draw_line(10, 30, 300, 370, color, line_width=5, line_stipple=(3, 0x0C0F))
        color = (1.0, 0, 0, 0.5)
        draw_rect(200, 100, 50, 75, color)
        color = (0, 0, 1.0, 1)
        draw_rect(300, 100, 50, 75, color, filled=False)
        color = (0, 1.0, 1.0, 1)
        draw_rect(300, 100, 50, 75, color, filled=False, line_width=3)
        color = (1, 1, 1, 0.5)
        draw_circle(200, 200, 50, color)
        draw_circle(260, 200, 5)
        color = (1.0, 0, 1.0, 1.0)
        draw_circle(200, 260, 10, color)
        draw_arc(400, 100, 30, 80, 45, 135)
        draw_ring(400, 300, 50, 70)
        fps_display.draw()
        win.flip()