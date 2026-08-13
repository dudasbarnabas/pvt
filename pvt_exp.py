from psychopy import visual, core, gui
from psychopy.hardware import keyboard
import random
import csv
import os
from datetime import datetime

from send_data import main as send_rows

def main():
    # =========================
    # Settings
    # =========================

    TASK_DURATION = 60

    RESPONSE_KEY = "space"
    QUIT_KEY = "escape"

    MIN_FOREPERIOD = 2.0      # seconds before stimulus can appear
    MAX_FOREPERIOD = 10.0

    MAX_RESPONSE_TIME = 1.5   # seconds after stimulus onset
    LAPSE_THRESHOLD = 0.500   # 500 ms lapse threshold

    FULLSCREEN = False

    ISI_MIN = 5
    ISI_MAX = 10

    # =========================
    # Participant dialog
    # =========================

    exp_info = {
        "participant": "sub-001",
        "session": "001",
        "FULLSCREEN": False,
        "TASK_DURATION": 60,
        "ISI_MIN": 5,
        "ISI_MAX": 10,
        "ISI_BOTTOM": 3,
        "ISI_TOP": 3
    }

    dlg = gui.DlgFromDict(exp_info, title="PVT start", order=["FULLSCREEN","participant", "session", "TASK_DURATION", "ISI_MIN", "ISI_MAX", "ISI_BOTTOM", "ISI_TOP"])
    if not dlg.OK:
        core.quit()


    # =========================
    # Prepare output
    # =========================

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("data", exist_ok=True)

    filename = os.path.join(
        "data",
        f"pvt_{exp_info['participant']}_{exp_info['session']}_{timestamp}.csv"
    )


    # =========================
    # PsychoPy setup
    # =========================

    win = visual.Window(
        size=[1000, 700],
        fullscr=exp_info['FULLSCREEN'],
        color="black",
        units="height"
    )

    kb = keyboard.Keyboard()

    instructions = visual.TextStim(
        win,
        text=(
            "Psychomotor Vigilance Task\n\n"
            "Press SPACE as quickly as possible\n"
            "when the target appears.\n\n"
            "Do not press before the target.\n\n"
            "Press SPACE to start.\n"
            "Press ESC to quit."
        ),
        color="white",
        height=0.035,
        wrapWidth=0.9
    )

    fixation = visual.TextStim(
        win,
        text="+",
        color="white",
        height=0.08
    )

    target = visual.Circle(
        win,
        fillColor="blue",
        size=0.06
    )


    too_soon_msg = visual.TextStim(
        win,
        text="Too soon!",
        color="white",
        height=0.05
    )

    miss_msg = visual.TextStim(
        win,
        text="No response",
        color="white",
        height=0.05
    )

    end_msg = visual.TextStim(
        win,
        text="Done!\n\nThank you.",
        color="white",
        height=0.05
    )


    # =========================
    # Helper functions
    # =========================

    def quit_if_escape(keys):
        if any(k.name == QUIT_KEY for k in keys):
            win.close()
            core.quit()


    def wait_for_space():
        kb.clearEvents()
        while True:
            keys = kb.getKeys(keyList=[RESPONSE_KEY, QUIT_KEY], waitRelease=False)
            quit_if_escape(keys)

            if any(k.name == RESPONSE_KEY for k in keys):
                return

            core.wait(0.001)


    def comp_foreperiod(foreperiod=None):
        if foreperiod is None:
            MIN_FOREPERIOD = ISI_MIN
            MAX_FOREPERIOD = ISI_MAX

        else:
            MIN_FOREPERIOD = foreperiod - ISI_BOTTOM
            MAX_FOREPERIOD = foreperiod + ISI_TOP
            if MIN_FOREPERIOD < ISI_MIN:
                MIN_FOREPERIOD = ISI_MIN
            if MAX_FOREPERIOD > ISI_MAX:
                MAX_FOREPERIOD = ISI_MAX

        foreperiod = random.uniform(MIN_FOREPERIOD, MAX_FOREPERIOD)
        return foreperiod

    # def comp_foreperiod(foreperiod=None):
    #     if foreperiod is None:
    #         MIN_FOREPERIOD = 5
    #         MAX_FOREPERIOD = 10

    #     else:
    #         MIN_FOREPERIOD = foreperiod - 3
    #         MAX_FOREPERIOD = foreperiod + 3
    #         if MIN_FOREPERIOD < 5:
    #             MIN_FOREPERIOD = 5
    #         if MAX_FOREPERIOD > 10:
    #             MAX_FOREPERIOD = 10

    #     foreperiod = random.uniform(MIN_FOREPERIOD, MAX_FOREPERIOD)
    #     return foreperiod

    # =========================
    # Instructions
    # =========================

    instructions.draw()
    win.flip()
    wait_for_space()


    # =========================
    # Main experiment
    # =========================

    results = [] # eredmenyek listaja
    foreperiod = None # leso ures isi
    trial = 0 # trial szama
    task_clock = core.Clock() # teljes feladat oraja

    while task_clock.getTime() < exp_info['TASK_DURATION']:
        trial += 1

        # -------------------------
        # Foreperiod / waiting phase 
        # -------------------------

        if foreperiod == None: # Ha nincs elozo isi
            foreperiod = comp_foreperiod()
        else:
            foreperiod = comp_foreperiod(foreperiod)

        # ------------
        # Fixacio
        # ------------

        fixation.draw()
        win.flip()

        # -------
        # Billentyure var
        # -------

        kb.clearEvents()
        kb.clock.reset()

        fore_clock = core.Clock() # trail-on belul isi oraja
        false_start = False # nincs rontas
        false_start_time = None

        while fore_clock.getTime() < foreperiod: # isi alatt keypressre var
            keys = kb.getKeys(
                keyList=[RESPONSE_KEY, QUIT_KEY],
                waitRelease=False,
                clear=True
            )

            quit_if_escape(keys) # quit-re kilép

            if any(k.name == RESPONSE_KEY for k in keys): #isi alatt response keypress volt
                false_start = True
                false_start_time = fore_clock.getTime()
                break

            core.wait(0.001)

        # -------------------------
        # If participant responded early
        # -------------------------

        if false_start:
            win.flip() # torli fixaciot
            core.wait(0.5)

            results.append({
                "participant": exp_info["participant"],
                "session": exp_info["session"],
                "trial": trial,
                "foreperiod_s": round(foreperiod, 6),
                "outcome": "false_start",
                "rt_s": "",
                "rt_ms": "",
                "false_start_time_s": round(false_start_time, 6),
                "lapse_500ms": "",
                "miss": 0
            })

            continue

        # -------------------------
        # Target presentation
        # -------------------------

        target.draw()
        kb.clearEvents()
        win.callOnFlip(kb.clock.reset)
        stim_onset_time = win.flip()

        response = None
        rt = None

        response_clock = core.Clock()

        while response_clock.getTime() < MAX_RESPONSE_TIME:
            keys = kb.getKeys(
                keyList=[RESPONSE_KEY, QUIT_KEY],
                waitRelease=False,
                clear=True
            )

            quit_if_escape(keys)

            if any(k.name == RESPONSE_KEY for k in keys):
                response = keys[0]
                rt = response.rt
                break

            core.wait(0.001)

        # -------------------------
        # Save trial result
        # -------------------------

        if rt is None:
            outcome = "miss"
            rt_ms = ""
            lapse = ""
            miss = 1

            win.flip()
            core.wait(0.3)

        else:
            outcome = "response"
            rt_ms = rt * 1000
            lapse = int(rt >= LAPSE_THRESHOLD)
            miss = 0

            # brief blank screen after response
            win.flip()
            core.wait(0.2)

        results.append({
            "participant": exp_info["participant"],
            "session": exp_info["session"],
            "trial": trial,
            "foreperiod_s": round(foreperiod, 6),
            "outcome": outcome,
            "rt_s": round(rt, 6) if rt is not None else "",
            "rt_ms": round(rt_ms, 3) if rt is not None else "",
            "false_start_time_s": "",
            "lapse_500ms": lapse,
            "miss": miss
        })


    # =========================
    # Save CSV send data
    # =========================

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    send_rows(results)

    # =========================
    # End screen
    # =========================

    end_msg.draw()
    win.flip()
    core.wait(2.0)

    win.close()
    core.quit()

if __name__ == "__main__":
    main()