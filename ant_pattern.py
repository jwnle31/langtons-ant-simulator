import pyglet as pg
from pyglet.window import key, mouse
from pyglet.gl import glTranslatef, glScalef


# Pattern Display
class Pattern:
    def __init__(self, colors, batch):
        self.rects = {}
        self.scale = 1
        self.scale_depth = 0
        self.mouse = [0, 0]
        self.colors = colors
        self.batch = batch

    def new_pix(self, new_x, new_y):
        if new_x not in self.rects:
            self.rects[new_x] = {}
        self.rects[new_x][new_y] = pg.shapes.Rectangle(new_x, new_y, 1, 1, color=self.colors[0], batch=self.batch)


# Langton's Ant
class Ant:
    def __init__(self, x, y, pattern):
        self.x = x
        self.y = y
        self.dir = [1, 0]
        self.pattern = pattern
        self.steps = 0
        self.paused = True

    def iterate(self, steps, ruleset):
        for iteration in range(steps):
            idx = 0
            try:
                idx = self.pattern.colors.index(tuple(self.pattern.rects[self.x][self.y].color))
            except KeyError:
                self.pattern.new_pix(self.x, self.y)
            self.pattern.rects[self.x][self.y].color = self.pattern.colors[
                (idx + 1) % len(self.pattern.colors)]
            rule = ruleset[idx]
            if rule == 'R':
                self.dir = [self.dir[1], -1 * self.dir[0]]
            if rule == 'L':
                self.dir = [-1 * self.dir[1], self.dir[0]]
            if rule == 'U':
                self.dir = [-1 * self.dir[0], -1 * self.dir[1]]
            if rule == 'N':
                pass
            self.x += self.dir[0]
            self.y += self.dir[1]


def ant_run(rule_input, rate_input):
    # Global Constants
    rule = rule_input
    rule_set = [x for x in rule]
    rate = rate_input

    # Color Text File
    c_file = open('colors.txt')
    colors = list(map(eval, c_file.readlines()[:len(rule_set)]))
    c_file.close()

    # Pyglet Window Setup
    window = pg.window.Window(width=1000, height=600, caption=rule,
                              fullscreen=False, resizable=False)
    stats = pg.window.Window(width=260, height=130, caption='Simulator Stats',
                             fullscreen=False, resizable=False)
    pg.gl.glClearColor(240 / 255, 240 / 255, 240 / 255, 1)
    window.set_icon(pg.image.load('ant_img.ico'))
    stats.set_icon(pg.image.load('ant_img.ico'))

    ww = window.width
    wh = window.height
    pix = pg.graphics.Batch()
    text = pg.graphics.Batch()
    window.set_mouse_cursor(window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR))
    fps_display = pg.window.FPSDisplay(window)

    # Instantiations
    ant_patt = Pattern(colors, pix)
    ant = Ant(ww / 2, wh / 2, ant_patt)

    # Stats Window Text Labels
    st_pause_1 = pg.text.Label("State ('Space'):",
                               font_name='Arial', font_size=10, bold=True,
                               x=10, y=100,
                               color=(0, 0, 0, 255),
                               batch=text)
    st_pause_2 = pg.text.Label('Running',
                               font_name='Arial', font_size=10, bold=True,
                               x=117, y=100,
                               color=(50, 205, 50, 255),
                               batch=text)
    st_steps = pg.text.Label('Steps: 0',
                             font_name='Arial', font_size=10, bold=True,
                             x=10, y=75,
                             color=(0, 0, 0, 255),
                             batch=text)
    st_cur_pos = pg.text.Label('Cursor Pos.:',
                               font_name='Arial', font_size=10, bold=True,
                               x=10, y=50,
                               color=(0, 0, 0, 255),
                               batch=text)
    st_cur_color = pg.text.Label('Color:',
                                 font_name='Arial', font_size=10, bold=True,
                                 x=10, y=25,
                                 color=(0, 0, 0, 255),
                                 batch=text)

    @stats.event
    def on_draw():
        stats.clear()
        text.draw()

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        ant_patt.mouse[0] += dx * ant_patt.scale
        ant_patt.mouse[1] += dy * ant_patt.scale

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        window.switch_to()
        if buttons & mouse.LEFT:
            glTranslatef(dx * ant_patt.scale, dy * ant_patt.scale, 0)

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        window.switch_to()
        if scroll_y > 0 and ant_patt.scale_depth < 15:
            ant_patt.scale /= 1.25
            ant_patt.scale_depth += 1
            glTranslatef(ant_patt.mouse[0], ant_patt.mouse[1], 0)
            glScalef(1.25, 1.25, 1)
            glTranslatef(-ant_patt.mouse[0], -ant_patt.mouse[1], 0)
        elif scroll_y < 0 and ant_patt.scale_depth <= 15:
            ant_patt.scale /= 0.8
            ant_patt.scale_depth -= 1
            glTranslatef(ant_patt.mouse[0], ant_patt.mouse[1], 0)
            glScalef(0.8, 0.8, 1)
            glTranslatef(-ant_patt.mouse[0], -ant_patt.mouse[1], 0)

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.SPACE:
            if ant.paused:
                ant.paused = False
            else:
                ant.paused = True

    @window.event
    def on_close():
        stats.close()

    @window.event
    def on_draw():
        window.clear()
        pix.draw()
        fps_display.draw()

    # Periodic Update for Each Frame
    def update(dt):
        ant.iterate(rate * (not ant.paused), rule_set)
        ant.steps += rate * (not ant.paused)
        st_pause_2.text = 'Paused' if ant.paused else 'Running'
        st_pause_2.color = (255, 0, 0, 255) if ant.paused else (50, 205, 50, 255)
        st_steps.text = 'Steps: ' + str(ant.steps)
        st_cur_pos.text = 'Cursor Pos.: (' + str(round(ant_patt.mouse[0] - ww / 2, 2)) + ', ' \
                          + str(round(ant_patt.mouse[1] - wh / 2, 2)) + ')'
        try:
            st_cur_color.text = \
                'Color (RGB, #): ' \
                + str(tuple(ant_patt.rects[int(ant_patt.mouse[0])][int(ant_patt.mouse[1])].color)) + ', ' \
                + str(colors.index(tuple(ant_patt.rects[int(ant_patt.mouse[0])][int(ant_patt.mouse[1])].color)))
        except KeyError:
            st_cur_color.text = 'Color (RGB, #): Background'

    pg.clock.schedule_interval(update, 1 / 120)
    pg.app.run()
