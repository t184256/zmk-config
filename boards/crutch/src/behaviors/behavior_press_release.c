/*
 * Copyright (c) 2020 The ZMK Contributors
 *
 * SPDX-License-Identifier: MIT
 */

#define DT_DRV_COMPAT zmk_behavior_press_release

#include <zephyr/device.h>
#include <drivers/behavior.h>
#include <zephyr/logging/log.h>

#include <zmk/behavior.h>
#include <zmk/event_manager.h>
#include <zmk/events/position_state_changed.h>

LOG_MODULE_DECLARE(zmk, CONFIG_ZMK_LOG_LEVEL);

#if DT_HAS_COMPAT_STATUS_OKAY(DT_DRV_COMPAT)

struct behavior_press_release_config {
    struct zmk_behavior_binding press_binding;
    struct zmk_behavior_binding release_binding;
};

static int on_press_release_binding_pressed(struct zmk_behavior_binding *binding,
                                             struct zmk_behavior_binding_event event) {
    const struct device *dev = zmk_behavior_get_binding(binding->behavior_dev);
    const struct behavior_press_release_config *cfg = dev->config;

    LOG_DBG("Press binding triggered at position %d", event.position);

    // Invoke the press binding
    return zmk_behavior_invoke_binding(&cfg->press_binding, event, true);
}

static int on_press_release_binding_released(struct zmk_behavior_binding *binding,
                                              struct zmk_behavior_binding_event event) {
    const struct device *dev = zmk_behavior_get_binding(binding->behavior_dev);
    const struct behavior_press_release_config *cfg = dev->config;

    LOG_DBG("Release binding triggered at position %d", event.position);

    // Invoke the release binding
    return zmk_behavior_invoke_binding(&cfg->release_binding, event, false);
}

static const struct behavior_driver_api behavior_press_release_driver_api = {
    .binding_pressed = on_press_release_binding_pressed,
    .binding_released = on_press_release_binding_released,
};

static int behavior_press_release_init(const struct device *dev) {
    return 0;
}

#define PRESS_RELEASE_INST(n)                                                                      \
    static struct behavior_press_release_config behavior_press_release_config_##n = {             \
        .press_binding = ZMK_KEYMAP_EXTRACT_BINDING(0, DT_DRV_INST(n)),                          \
        .release_binding = ZMK_KEYMAP_EXTRACT_BINDING(1, DT_DRV_INST(n)),                        \
    };                                                                                             \
    BEHAVIOR_DT_INST_DEFINE(n, behavior_press_release_init, NULL, NULL,                           \
                            &behavior_press_release_config_##n, POST_KERNEL,                       \
                            CONFIG_KERNEL_INIT_PRIORITY_DEFAULT,                                   \
                            &behavior_press_release_driver_api);

DT_INST_FOREACH_STATUS_OKAY(PRESS_RELEASE_INST)

#endif
