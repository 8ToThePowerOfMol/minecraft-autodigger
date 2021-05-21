#!/bin/bash

pickaxe_durability=131
pickaxe_slots=("1" "2" "3" "4")
torch_slot=8
place_torch_after=10
pause_after=10
pause_duration=5

dig_1 () {
    sleep 0.1
    xdotool keydown w
    sleep 0.5
    xdotool keyup w
    sleep 0.1
    xdotool mousedown 1
    sleep 1.35
    xdotool mouseup 1
    sleep 0.1
    xdotool mousemove_relative --sync -- 0 200
    sleep 0.1
    xdotool mousedown 1
    sleep 1.35
    xdotool mouseup 1
    sleep 0.1
    xdotool mousemove_relative --sync -- 0 -200
    sleep 0.1
}

place_torch () {
    prev_slot=$1

    sleep 0.2
    xdotool mousemove_relative --sync -- 700 0
    sleep 0.2
    xdotool key "${torch_slot}"
    sleep 0.3
    xdotool click 3
    sleep 0.3
    xdotool key "${prev_slot}"
    sleep 0.3
    xdotool mousemove_relative --sync -- -700 0
    sleep 0.2
}


echo "10 seconds, in MC, move mouse at the block at the level of your head, where you want to dig."
sleep 10

echo "Started digging..."

# set -x

for slot in "${pickaxe_slots[@]}"; do
    echo "Using item on slot ${slot}"
    
    sleep 0.2
    xdotool key "${slot}"
    sleep 0.2

    for i in `seq "$((${pickaxe_durability}/2))"`; do
        dig_1

        if [ $(("${i}" % "${place_torch_after}")) -eq 0 ]; then
            place_torch "${slot}"
        fi

        if [ $(("${i}" % "${pause_after}")) -eq 0 ]; then
            echo "Taking small break for ${pause_duration} seconds. Chance to stop digging, if you want (CTRL + c)." 
            sleep "${pause_duration}"
            echo "Back to work..."
        fi
    done
done

echo "Jobs done."


