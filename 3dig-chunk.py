import os
import time


chunk_x = 16
chunk_y = 16
dig_fnt = "dig_4"
pickaxe_durability = 131
pickaxe_slots = [1, 2, 3, 4, 5, 6, 7]
durabilities = None # [69, 104, 111, 131, 131, 131, 131]
dig_duration = 1.35
torch_slot = 8
place_torch_after = 10
pause_after = 10
pause_duration = 5
take_from_inventory = False
stopblock_slot = 9


def switch_to(slot):
    print("Switching to slot {}".format(slot))
    time.sleep(0.3)
    os.system("xdotool key {}".format(slot))
    time.sleep(0.3)


def dig_element(slot, durs, idx):
    time.sleep(0.1)
    os.system("xdotool mousedown 1")
    time.sleep(dig_duration)
    os.system("xdotool mouseup 1")
    time.sleep(0.1)

    # Update durabilities, change pickaxe if necessary
    durs[idx] -= 1
    if durs[idx] <= 1:
        # Take next pickaxe
        idx += 1
        if idx == len(pickaxe_slots):
            # TODO: Try taking from inventory.
            print("All pickaxes broken. Jobs done.")
            exit(0)
        slot = pickaxe_slots[idx]
        switch_to(slot)
    return slot, durs, idx


def turn_left():
    time.sleep(0.2)
    os.system("xdotool mousemove_relative --sync -- -600 0")
    time.sleep(0.2)


def turn_right():
    time.sleep(0.2)
    os.system("xdotool mousemove_relative --sync -- 600 0")
    time.sleep(0.2)


def place():
    time.sleep(0.3)
    os.system("xdotool click 3")
    time.sleep(0.3)


def step_forward(t=0.23):
    time.sleep(0.1)
    os.system("xdotool keydown w")
    time.sleep(t)
    os.system("xdotool keyup w")
    time.sleep(0.1)


def move_forward():
    time.sleep(0.1)
    os.system("xdotool keydown w")
    time.sleep(0.7)
    os.system("xdotool keyup w")
    time.sleep(0.1)


def overprint(*values):
    print("\033[A                             \033[A")
    print(*values, flush=True)


def dig_2(slot, durs, idx):
    step_forward() 
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 200")
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 -200")
    time.sleep(0.1)
    return slot, durs, idx

def dig_3(slot, durs, idx):
    step_forward() 
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 200")
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 -400")
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 200")
    time.sleep(0.1)
    return slot, durs, idx

def dig_4(slot, durs, idx):
    step_forward() 
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 200")
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 -400")
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 -200")
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 400")
    time.sleep(0.1)
    return slot, durs, idx


def place_torch(prev_slot):
    switch_to(torch_slot)
    os.system("xdotool mousemove_relative --sync -- 0 600")
    place()
    os.system("xdotool mousemove_relative --sync -- 0 -600")
    switch_to(prev_slot)

def place_stopblocks(prev_slot):
    time.sleep(0.1)
    os.system("xdotool key {}".format(stopblock_slot))
    time.sleep(0.2)
    os.system("xdotool mousemove_relative --sync -- 0 260")
    place()
    os.system("xdotool mousemove_relative --sync -- 0 -115")
    place()
    os.system("xdotool mousemove_relative --sync -- 0 -145")
    time.sleep(0.2)
    os.system("xdotool key {}".format(prev_slot))
    time.sleep(0.1)


def dig_stopblocks(slot, durs, idx):
    time.sleep(0.1)
    step_forward(0.3)
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 200")
    slot, durs, idx = dig_element(slot, durs, idx)
    os.system("xdotool mousemove_relative --sync -- 0 -200")
    time.sleep(0.1)
    return slot, durs, idx


def is_torch_spot(x, y):
    return ((x % 4) == 1) and ((y % 4) == 1)


iter2x = {k: v for (k,v) in enumerate(list(range(15, -1, -1)))}


def get_info_msg(durs, start_time, est_time):
    if est_time == 0:
        return str(durs)
    curr = round(time.time() - start_time)
    est = round(est_time - start_time)
    return "{}, {}s/{}s".format(durs, curr, est)


def dig_chunk(slot, durs, idx, dig_fnt):
    # Chunk is 16x16 flat
    # Asuming, you start at the left side of the chunk

    #    0 1 2 3 4 5 6 7 8 9101112131415 
    #  0 . . . . . . . . . . . . . . . .
    #  1 . t . . . t . . . t . . . t . .
    #  2 . . . . . . . . . . . . . . . .
    #  3 . . . . . . . . . . . . . . . .
    #  4 . . . . . . . . . . . . . . . .
    #  5 . t . . . t . . . t . . . t . .
    #  6 . . . . . . . . . . . . . . . .
    #  7 . . . . . . . . . . . . . . . .
    #  8 . . . . . . . . . . . . . . . .
    #  9 . t . . . t . . . t . . . t . .
    # 10 . . . . . . . . . . . . . . . .
    # 11 . . . . . . . . . . . . . . . .
    # 12 . . . . . . . . . . . . . . . .
    # 13 . t . . . t . . . t . . . t . .
    # 14 . . . . . . . . . . . . . . . .
    # 15 . . . . . . . . . . . . . . . .

    str2fnt = {
        "dig_2": dig_2,
        "dig_3": dig_3,
        "dig_4": dig_4,
    }
    if isinstance(dig_fnt, str):
        dig_fnt = str2fnt[dig_fnt]

    slot, durs, idx = dig_fnt(slot, durs, idx)
    print(durs)
    
    est_time = start_time = 0

    for x in range(chunk_x):
        if start_time == 0:
            start_time = time.time()
        elif est_time == 0:
            est_time = (chunk_x - 1) * (time.time() - start_time)

        for y in range(chunk_y - 1):
            slot, durs, idx = dig_fnt(slot, durs, idx)
            overprint(get_info_msg(durs, start_time, est_time))
            if is_torch_spot(iter2x[x], y):
                place_torch(slot)
       
        turn_fnt = turn_right if ((x % 2) == 0) else turn_left
        t = 0.1 if ((x % 2) == 0) else 0.3

        if (x % 2) == 1:
            place_stopblocks(slot)
            slot, durs, idx = dig_stopblocks(slot, durs, idx)
        else:
            step_forward(0.3)
        turn_fnt()
        slot, durs, idx = dig_fnt(slot, durs, idx)
        overprint(get_info_msg(durs, start_time, est_time))
        step_forward()
        turn_fnt()
    
    return slot, durs, idx


if __name__ == "__main__":

    print("13 seconds, in MC, make sure you face 90/0 straigh, where you want to dig.")
    time.sleep(13)

    durs = [pickaxe_durability for _ in range(len(pickaxe_slots))] if durabilities is None else durabilities
    idx = 0
    slot = pickaxe_slots[idx]

    slot, durs, idx = dig_chunk(slot, durs, idx, dig_fnt)

    print("Jobs done")
