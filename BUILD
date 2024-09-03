# prod
west build -d build/left -b nice_nano_v2 -- -DSHIELD=lily58_left -DZMK_CONFIG=~/code/zmk-config/config && mv build/left/zephyr/zmk.uf2 left.lily58.zmk.uf2 && west build -d build/right -b nice_nano_v2 -- -DSHIELD=lily58_right -DZMK_CONFIG=~/code/zmk-config/config && mv build/right/zephyr/zmk.uf2 right.lily58.zmk.uf2

# debug
west build -d build/left -b nice_nano_v2 -S zmk-usb-logging -- -DSHIELD=lily58_left -DZMK_CONFIG=~/code/zmk-config/config && mv build/left/zephyr/zmk.uf2 left.lily58.zmk.uf2 && west build -d build/right -b nice_nano_v2 -S zmk-usb-logging -- -DSHIELD=lily58_right -DZMK_CONFIG=~/code/zmk-config/config && mv build/right/zephyr/zmk.uf2 right.lily58.zmk.uf2 && west build -d build/reset -b nice_nano_v2 -S zmk-usb-logging -- -DSHIELD=settings_reset -DZMK_CONFIG=~/code/zmk-config/config && mv build/reset/zephyr/zmk.uf2 reset.lily58.zmk.uf2
