## Zero Overshoot is a way to dampen CLASSIC PID  Kp, Ki, and Kd values

RepRap website has a nice discussion of PID Tuning.  Please see the following URL:

https://reprap.org/wiki/PID_Tuning


A Klipper Extension that allows the Voron User to describe a formula that will recalculate the Classic PID values after a PID_CALIBRATE command is executed.  Only two heaters are presently supported: `heater_bed` and `extruder`.

These new `zero_overshoot PID values` will then be saved to your Klipper's `printer.cfg file`, so they can be used during the heating process for the `heater_bed` and `extruder` heaters.

This Klipper extension adds a command line parameter called `ZERO_OVERSHOOT` that can be used to turn on this extension or turn off this extension via the command line.

If `ZERO_OVERSHOOT` is set to `1` then this Klipper extension will take the Classic PID values generated via the `PID_CALIBRATE` command and recalculate them with the formula the Voron user describes in the config file. Then these new zero_overshoot PID values will be stored in the printer.cfg file.

If `ZERO_OVERSHOOT` is set to `0` then this Klipper extension will **NOT** change the Classic PID values and store the Classic PID values in the printer.cfg file.

Here are the options for Klipper's `PID_CALIBRATE` :

```BASH
PID_CALIBRATE HEATER=heater_bed TARGET=110                      #this will default to the zero_overshoot option from the config file
PID_CALIBRATE HEATER=heater_bed TARGET=110 ZERO_OVERSHOOT=0
PID_CALIBRATE HEATER=heater_bed TARGET=110 ZERO_OVERSHOOT=1
PID_CALIBRATE HEATER=heater_bed TARGET=110 WRITE_FILE=0 ZERO_OVERSHOOT=1
PID_CALIBRATE HEATER=heater_bed TARGET=110 WRITE_FILE=1 ZERO_OVERSHOOT=1

PID_CALIBRATE HEATER=extruder TARGET=240                        #this will default to the zero_overshoot option from the config file
PID_CALIBRATE HEATER=extruder TARGET=240 ZERO_OVERSHOOT=0
PID_CALIBRATE HEATER=extruder TARGET=240 ZERO_OVERSHOOT=1
PID_CALIBRATE HEATER=extruder TARGET=240 WRITE_FILE=0 ZERO_OVERSHOOT=1
PID_CALIBRATE HEATER=extruder TARGET=240 WRITE_FILE=1 ZERO_OVERSHOOT=1

If the WRITE_FILE parameter is enabled, then the file `/tmp/heattest.txt` will be created with a log of all temperature samples taken during the test.

```
---

This Klipper extension can be run on any Klipper 3D Printer.

---
## How to enable ``zero_overshoot`` on your Klipper 3D printer:

To enable the module, add the following to your `printer.cfg` file:

```INI
[zero_overshoot heater_bed]
zero_overshoot:
#   Globally enable the the recalculation of the Classic PID Kp, Ki, and Kd values. Default is 'True'.
#   Setting this to 'True' will enable the formula and the Kp, Ki and Kd values will be changed before they
#   are saved back to the printer.cfg file during the SAVE_CONFIG command. This extension only works with
#   the help of Klipper's PID_CALIBRATE command.
Kp_multiplier:
#    default value is 1.0000000000
Ki_multiplier:
#    default value is 1.0000000000
Kd_multiplier:
#   default value is 1.0000000000
#
[zero_overshoot extruder]
zero_overshoot:
#   Globally enable the the recalculation of the Classic PID Kp, Ki, and Kd values. Default is 'True'.
#   Setting this to 'True' will enable the formula and the Kp, Ki and Kd values will be changed before they
#   are saved back to the printer.cfg file during the SAVE_CONFIG command. This extension only works with
#   the help of Klipper's PID_CALIBRATE command.
Kp_multiplier:
#    default value is 1.0000000000
Ki_multiplier:
#   default value is 1.0000000000
Kd_multiplier:
#   default value is 1.0000000000
#

# The following formulas will be used to recalculate the pid_Kp, pid_Ki, and pid_Kd:
# Kp = Kp_classic * Kp_multiplier
# Ki = Ki_classic * Ki_multiplier
# Kd = Kd_classic * Kd_multiplier
#
# NOTE: if you need to divide, remember that 1/x = 1 * reciprocal of the number;
# The reciprocal is simply: 1/number. To get the reciprocal of a number, we divide 1 by the number. Example: the reciprocal of # 2 is ½
#
# So for example 0.3333333333 is really 1.0 divide by 3.0 or 1./3.
# The number will be calculated to the first 3 significant digits because that is all the significant digits that Klipper will
# store for SAVE_CONFIG command.
#
# NOTE2: for the zero_overshoot calculated values to be done automatically, you must have the following in you printer.cfg file:
# (they can be commented out and located at bottom of the printer.cfg file in the
#*# <---------------------- SAVE_CONFIG ----------------------> section.)
#
# File printer.cfg:
# [heater_bed]
# control = pid
# pid_Kp = 41.135
# pid_Ki = 1.187
# pid_Kd = 356.328
#
# [extruder]
# control = pid
# pid_Kp = 37.787
# pid_Ki = 5.360
# pid_Kd = 66.601
#
# If the above pid_Kp, pid_Ki, and pid_Kd values are located in a seperate `include` file, the software will not
# know where to look to find the classic PID values for Kp, Ki and Kd.
```

>:point_up: NOTE: The default for the option `zero_overshoot` is `True`.  So if you forget to assign `True` or `False` for the option `zero_overshoot` then the extension will load `True` automatically.  But this only applies if you have a `[zero_overshoot heater_bed]` section and/or `[zero_overshoot extruder]` section defined in your printer.cfg file.

I have set the defaults to the option as such so that if you do not know what you want this extension will default to using the `Classic PID values` that Klipper generates.

The module also augments the `PID_CALIBRATE` command with an extra parameter - `ZERO_OVERSHOOT` - which can be used to
control whether the command performs the zero_over shoot recalculation independently of the`zero_overshoot` setting in the configuration section `[zero_overshoot heater_bed]` or `[zero_overshoot extruder]`.

All you will see is a message in your klippy.log file stating the following so that if you need help, the Voron design team will need to know this extension is installed and its current settings:

```
zero_overshoot ::INFO:: [zero_overshoot heater_bed]: zero_overshoot = True
zero_overshoot ::INFO:: [zero_overshoot heater_bed]: Kp_multiplier = 0.3333333333
zero_overshoot ::INFO:: [zero_overshoot heater_bed]: Ki_multiplier = 0.3333333333
zero_overshoot ::INFO:: [zero_overshoot heater_bed]: Kd_multiplier = 0.8800000000
zero_overshoot ::INFO:: [zero_overshoot extruder]: zero_overshoot = True
zero_overshoot ::INFO:: [zero_overshoot extruder]: Kp_multiplier = 0.3333333333
zero_overshoot ::INFO:: [zero_overshoot extruder]: Ki_multiplier = 1.0000000000
zero_overshoot ::INFO:: [zero_overshoot extruder]: Kd_multiplier = 2.6666666667
```
Basically, this extension will document the settings in the klippy.log file.

The above are taken from my klippy.log file.  So these are the setting I am using presently.

I own an LDO 300 Kit Kenovo pad with the following characteristics:

1. Kenovo 280x280mm (600W) & Thermal Fuse (125c) URL: https://keenovo.store/products/keenovo-square-silicone-heater-3d-printer-build-plate-heatbed-heating-pad?variant=12592089268279
2. sensor_type: keenovo ##my user defined type instead of `Generic 3950`
3. My user defined `keenovo` thermistor definition is as follows:
```INI
[thermistor keenovo]
# URL: https://github.com/RealDeuce/Voron-MKS-Monster8/blob/main/keenovo.cfg
# https://www.keenovo.com/NTC-Thermistor-R-T-Table.pdf
temperature1:	25
resistance1:	100000
temperature2:	70
resistance2:	17550
temperature3:	110
resistance3:	5070
```

I am still trying to tweak my E3D Revo Voron heater settings.

I own an E3D Revo Voron with the following characteristics:

1. E3D Voron Revo hot end (40W, 24V heater, USA) URL: https://e3d-online.com/products/revo-voron
2. sensor_type: ATC Semitec 104NT-4-R025H42G
3. `ATC Semitec 104NT-4-R025H42G` is the Klipper definition

>:bulb: **INFO:** Please keep in mind there are many factors that effect the PID tuning process. Like your thermistor definition and
>the option `smooth_time:` in your heater definition.
---

### **Installation:**

You have two ways you can install this `zero_overshoot` extension (manually or via an installation script)

Here is the manual install instruction:

1. Write down the location of the following directories:
    * Klipper Extras: Usually located at `/home/USER/klipper/klippy/extras`.
2. Download  `zero_overshoot.py` file.
3. Download the `ZERO_OVERSHOOT.cfg` and include it into your printer.cfg file.
3. Move `zero_overshoot.py` to your Klipper Extras folder (home/pi/klipper/klippy/extras).
4. Restart Klipper service and do a `FIRMWARE RESTART` command if needed.

>:bulb: NOTE:
> If you install the extension before you create the`[zero_overshoot heater_bed]` and/or `[zero_overshoot extruder]`
> section(s) with the option `zero_overshoot: True`
> Klipper will NOT load the extension when you restart Klipper.

>:bulb: **INFO:** Please restart the Klipper service by using the Mainsail/Fluidd UI (upper right-hand corner Power
>button Symbol) or perform the following command at your Raspberry Pi command prompt (on the Pi that runs Klipper
>for your 3D printer):

```BASH
cd ~
sudo systemctl restart klipper
```

>:point_down: Run the following command:
```BASH
cd ~
```
```BASH
sudo systemctl restart klipper
```

### Here is the installation script method:

Install the `zero_overshoot` extension to Klipper, please run the following commands:

```BASH
cd /home/pi
```
```BASH
git clone https://github.com/GadgetAngel/Zero_Overshoot.git
```
```BASH
./Zero_Overshoot/install_zero_overshoot.sh
```

---
### **Example Usage: An Example of using `[zero_overshoot heater_bed]` section**

First you must create the `[zero_overshoot heater_bed]` section in your printer.cfg file so Klipper knows to load the `zero_overshoot.py` and `zero_overshoots.py` files and include them into the Klipper code running on your Raspberry Pi.

Here are the contents of `ZERO_OVERSHOOT.cfg` file:

```python
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ZERO_OVERSHOOT Setup
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Define the [zero_overshoot heater_bed] and/or [zero_overshoot extruder] section and \
# define the option parameter 'zero_overshoot'.
#  When option parmaeter 'zero_overshoot' is set to True then the printer will automatically change
#  the pid_Kp, pid_Ki, and pid_Kd classical values by the formula you specify to produce a better
#  PID Tune for the specified heater.  There are two heaters this extension will work with
#  'heater_bed' and 'extruder'
#
#  When the option parameter 'zero_overshoot' is set to False then the printer will NOT automatically
#  adjust the pid_Kp, pid_Ki,and pid_Kd values and Classic PID control will be used.
#
# Kp_multiplier default value is 1.0000000000, Ki_multiplier default value is 1.0000000000 and Kd_multiplier
# default value is 1.0000000000
#
# The following formulas will be used:
# Kp = Kp_classic * Kp_multiplier
# Ki = Ki_classic * Ki_multiplier
# Kd = Kd_classic * Kd_multiplier
# NOTE: if you need to divide, remember that 1/x = 1 * reciprocal of the number;
# The reciprocal is simply: 1/number. To get the reciprocal of a number, we divide 1 by the number. Example: the reciprocal of 2 is ½
#
# So for example 0.3333333333 is really 1.0 divide by 3.0 or 1./3.
# The number will be calculated to the first 3 significant digits because that is all the significant digits that Klipper will
# store for SAVE_CONFIG command.
#
# NOTE2: for the zero_overshoot calculated values to be done automatically, you must have the following in you printer.cfg file:
# (they can be commented out and located at bottom of the printer.cfg file in the
#*# <---------------------- SAVE_CONFIG ----------------------> section.)
# File printer.cfg:
# [heater_bed]
# control = pid
# pid_Kp = 41.135
# pid_Ki = 1.187
# pid_Kd = 356.328
#
# [extruder]
# control = pid
# pid_Kp = 37.787
# pid_Ki = 5.360
# pid_Kd = 66.601
#
# If the above pid_Kp, pid_Ki, and pid_Kd values are located in a seperate include file, the software will not
# know where to look to find the classic PID values for Kp, Ki and Kd.
#
# Run a the following to get this extension to redo a PID calibration and recalculate the pid_K values:
#      PID_CALIBRATE HEATER=heater_bed TARGET=110
#      PID_CALIBRATE HEATER=extruder TARGET=240
#
# After the Classic PID calibration is done, the extension will display the classic PID values and also display
# the zero_overshoot PID pid_K values but ONLY SAVE the zero_overshoot PID recaluculated values to the printer.cfg
#
# This way when you heat up your desired heater the 3D printer will use the zero_overshoot PID values instead.
#
# With this extension installed you will no longer have to redo this calculation by hand and manually
# replace the pid_Kp, pid_Ki, and pid_Kp values.

#
# My heater for my bed is a Kenovo (600W, 24V, USA) heater from the LDO 300 Kit
#
[zero_overshoot heater_bed]
zero_overshoot: True
Kp_multiplier: 1.0000000000
Ki_multiplier: 1.0000000000
Kd_multiplier: 1.0000000000
#
# My hotend is an E3D Voron Revo which has an E3D 40W (24V heater, USA) heater
#
[zero_overshoot extruder]
zero_overshoot: True
Kp_multiplier: 1.0000000000
Ki_multiplier: 1.0000000000
Kd_multiplier: 1.0000000000


```
>:point_up: NOTE:
> You can have different equations for the different heaters.  The above example uses the same formula, but this extension allows
>you to create two separate formulas if you want.

Now restart the Klipper service by going to the upper right-hand side corner of Mainsail UI and click on the Power Button symbol.  Take your mouse and click on the curved arrow next to the word `Klipper` to restart the Klipper service.

>:bulb:
>Do a `PID_CALIBRATE` command so that this Klipper extension can do the calculation from the Classic PID Kp, Ki, and Kd values.
>If you choose NOT to do the `SAVE_CONFIG` command after the `PID_CALIBRATE` command completes, then the recalculated PID
>values will not be saved to the `printer.cfg` file and the benefit of this extension will be lost.  If you delete the
>`*# <---------------------- SAVE_CONFIG ----------------------> ` section from your `printer.cfg` file then the benefit of this
>extension will be lost.  But no worries, you will just have to rerun the `PID_CALIBRATE` command again and do a `SAVE_CONFIG`
>after the `PID_CALIBARTE` command finishes to regain the benefit of this extension. This Klipper extension adds to your
>`quality of life` experience.

How often do you do a `PID_CALIBRATE` command? Answer: Not very often.  I tend to forget that I want to change my classic PID
values so that I can dampen the overshoot of the PID control.  So I end up doing a `PID_CALIBRATE` command to achieve my
desired response.  With this extension, I will never have to worry about manually updating the `pid_Kp`, `pid_Ki` and `pid_Kd` values again because now the 3D printer will do it for me automatically as long as I do a `SAVE_CONFIG` command afterwards.

BTW, I have macros that I use to do BED PID Tuning and Nozzle PID Turning that automatically do the `SAVE_CONFIG` command.

Here is my BED PID Tune macro (you can find the _general_Debug macro in this GitHub Repo):

URL to my GitHub Repo for all the other external macros (G32, M117, CURRENT_NORMAL, PARK_UpperRight, _COOL_WAIT, STATUS_READY, TURN_OFF_HEATERS, _USER_VARIABLE, M141, and FILTER): https://github.com/GadgetAngel/Klipperbackup_Voron2.4r2_LDO300kit

```python
#.................................................................................................................
# BED_PID - Optional parameters: BED_TEMP{float_value}, FAN_SPEED{0-1},
#                                ENCLOSURE_TEMP{float_value}, ZERO_OVERSHOOT{0,1},
#                                WRITE_FILE{0,1}
#
#   / Usage:
#           BED_PID,
#           BED_PID BED_TEMP=110 FAN_SPEED=60 ENCLOSURE_TEMP=40
#           BED_PID BED_TEMP=110 FAN_SPEED=60 ENCLOSURE_TEMP=40 WRITE_FILE=1
#           BED_PID BED_TEMP=110 FAN_SPEED=60 ENCLOSURE_TEMP=40 WRITE_FILE=1 ZERO_OVERSHOOT=1
#
#   It performs bed PID tune. If no parameters are specified, BED_TEMP will be [defaultTempBed]
#
#.................................................................................................................
# Required variable(s) to be set. Add the following to your global variable dictionary block as:
#
# [gcode_macro _USER_VARIABLE]
# variable_filament.profile.defaultTempBed
# variable_park.mid.x
# variable_park.mid.y
# variable_hw.chamber.fan
# variable_filament.profile.defaultEnclosure
#
#.................................................................................................................
# Required external macro(s) used by this macro.
#
# _general_Debug
# G32
# M117
# CURRENT_NORMAL
# PARK_UpperRight
# _COOL_WAIT
# STATUS_READY
# TURN_OFF_HEATERS
# _USER_VARIABLE
# M141
# FILTER
#
#.................................................................................................................
#.................................................................................................................
#
## URL Resources: https://github.com/rkolbi/voron2.4/blob/main/MY_V24-350/ACTIVE/MACRO-BED_PID_TUNE.cfg
##
#.................................................................................................................

[gcode_macro BED_PID]
# Usage: BED_PID BED_TEMP=110 FAN_SPEED=40
# Fan speed, from 0 to 255. S255 provides 100% duty cycle; S128 produces 50%
description: Helper: Performs BED PID tune
gcode:
    _general_Debug msg="_BED_PID - entering"
    {% if printer.idle_timeout.state == "Printing" or printer.pause_resume.is_paused %}
        {action_respond_info("Cannot do that while printing")}
    {% else %}
        {% set user = printer['gcode_macro _USER_VARIABLE'] %}
        {% set defaultTB = user.filament.profile.defaultTempBed|float %}
        {% if printer.configfile.config['zero_overshoot heater_bed'].zero_overshoot|string in ['True','true'] %}
            {% set defaultOverShoot = 1 %}
         {% endif %}
        {action_respond_info("defaultOverShoot for heater_bed = %s;" % defaultOverShoot)}
        {% set Z_OVER = params.ZERO_OVERSHOOT|default(defaultOverShoot)|int %}
        {% set WRITE_FILE = params.WRITE_FILE|default(0)|int %}
        {action_respond_info("Z_OVER for heater_bed = %s;" % Z_OVER)}
        # if WRITE_FILE = 1 then file is saved to `/tmp/heattest.txt` on raspberry pi
        {action_respond_info("WRITE_FILE for heater_bed = %s;" % WRITE_FILE)}
        {% set BED_TEMP = params.BED_TEMP|default(defaultTB)|float %}
        {% set FAN_SPEED = params.FAN_SPEED|default(0.40)|float %}
        {% set X_MID =  user.park.mid.x|float %}
        {% set Y_MID =  user.park.mid.y|float %}
        {% set defaultENCLOSURE = user.filament.profile.defaultEnclosure|float %}
        {% set ENCLOSURE_TEMP = params.ENCLOSURE_TEMP|default(defaultENCLOSURE)|float %}
        G90                                                                 ;Absolute Positioning
        {% if user.hw.chamber.fan %} M141 S{ENCLOSURE_TEMP} {% endif %}     ;set chamber temperature for Exhaust fan and Bed fans
        M117 Performing initial homing.
        G32                                                                 ;Clears bed-mesh and performs G28, ATTACH_PROBE, QGL, DOCK_PROBE
        FILTER                                                              ;Toggle Nevermore Filter
        G1 Z5 Y{Y_MID} X{X_MID} F4000                                       ;move to center of bed
        SET_FAN_SPEED FAN=Bedfan_Left SPEED={FAN_SPEED}                     ;set Fan speed for bedfans fan
        SET_FAN_SPEED FAN=Bedfan_Right SPEED={FAN_SPEED}                    ;set Fan speed for bedfans fan
        M117 Starting PID calibration.
        PID_CALIBRATE HEATER=heater_bed TARGET={BED_TEMP} ZERO_OVERSHOOT={Z_OVER} WRITE_FILE={WRITE_FILE}  ;PID tune the heater_bed
        M117 Finished PID calibration.
        TURN_OFF_HEATERS                                                    ;Turn off all heaters and reset the chamber temperature for Exhaust fan
        FILTER                                                              ;Toggle Nevermore Filter
        CURRENT_NORMAL                                                      ;call Macro CURRENT_NORMAL
        PARK_UpperRight                                                     ;Parks nozzle at top front-right
        M18 X Y E                                                           ;Disable Stepper motor
        _COOL_WAIT MINUTES=1                                                ;Cooling cycle waiting routine
		STATUS_READY                                                        ;SB LED status
        SAVE_CONFIG                                                         ;save results of PID tune back in printer.cfg file
    {% endif %}
   _general_Debug msg="_BED_PID - exiting"
```

Here is my Nozzle PID Tune macro(you can find the _general_Debug macro in this GitHub Repo):

URL to my GitHub Repo for all the other external macros (STATUS_HOMING, STATUS_BUSY, STATUS_READY, _COOL_WAIT, _HEAT_WAIT,
PARK_UpperRight, M117, TURN_OFF_HEATERS, G32, M190, M106, _USER_VARIABLE, M141, FILTER): https://github.com/GadgetAngel/Klipperbackup_Voron2.4r2_LDO300kit

```python
#.................................................................................................................
# NZL_PID - Optional parameters: BED_TEMP{float_value}, NZL_TEMP{float_value},
#                                FAN_SPEED{float_value between 0-1}, SOAK_MINUTES{float_value},
#                                ENCLOSURE_TEMP{float_value}, ZERO_OVERSHOOT{0,1},
#                                WRITE_FILE{0,1}
#
#   / Usage:
#           NZL_PID,
#           NZL_PID NZL_TEMP=240 BED_TEMP=110
#           NZL_PID NZL_TEMP=240 BED_TEMP=110.0 FAN_SPEED=0.64 SOAK_MINUTES=12.5 ENCLOSURE_TEMP=40.0
#           NZL_PID NZL_TEMP=240 BED_TEMP=110.0 FAN_SPEED=0.64 SOAK_MINUTES=12.5 ENCLOSURE_TEMP=40.0 WRITE_FILE=1
#           NZL_PID NZL_TEMP=240 BED_TEMP=110.0 FAN_SPEED=0.64 SOAK_MINUTES=12.5 ENCLOSURE_TEMP=40.0 WRITE_FILE=1 ZERO_OVERSHOOT=1
#
#   It performs bed heat soak and then nozzle PID tune. If no parameters are specified, BED_TEMP will be
#   [defaultTempBed], and NZL_TEMP will be [defaultTempNozzle].
#
# Usage: NZL_PID BED_TEMP=95 NZL_TEMP=238
#.................................................................................................................
# Required variable(s) to be set. Add the following to your global variable dictionary block as:
#
# [gcode_macro _USER_VARIABLE]
#  variable_filament.profile.defaultTempNozzle
#  variable_filament.profile.defaultTempBed
#  variable_filament.filament.profile.defaultEnclosure
#  variable_filament.profile.PostPrintParkCool
#  variable_filament.profile.defaultEnclosure
#  variable_hw.chamber.fan
#
#.................................................................................................................
# Required external macro(s) used by this macro.
#
# _general_Debug
# STATUS_HOMING
# STATUS_BUSY
# STATUS_READY
# _COOL_WAIT
# _HEAT_WAIT
# PARK_UpperRight
# M117
# TURN_OFF_HEATERS
# G32
# M190
# M106
# _USER_VARIABLE
# M141
# FILTER
#
#.................................................................................................................

#.................................................................................................................
#
## URL Resources: https://github.com/rkolbi/voron2.4/blob/main/MY_V24-350/ACTIVE/MACRO-NZL_PID_TUNE.cfg
#
#.................................................................................................................
[gcode_macro NZL_PID]
# Usage: NZL_PID BED_TEMP=110 NZL_TEMP=245 FAN_SPEED=85 SOAK_MINUTES=10
# Fan speed, from 0 to 255. S255 provides 100% duty cycle; S128 produces 50%.
description: Helper: Performs NOZZLE PID tune
gcode:
    _general_Debug msg="NZL_PID - entering"
    {% set user = printer['gcode_macro _USER_VARIABLE'] %}
    {% if printer.idle_timeout.state == "Printing" or printer.pause_resume.is_paused %}
        {action_respond_info("Cannot do that while printing")}
    {% else %}
        {% set defaultTN = user.filament.profile.defaultTempNozzle|float %}
        {% set defaultTB = user.filament.profile.defaultTempBed|float %}
        {% if printer.configfile.config['zero_overshoot extruder'].zero_overshoot |string in ['True','true'] %}
            {% set defaultOverShoot = 1 %}
        {% endif %}
        {action_respond_info("defaultOverShoot for extruder = %s;" % defaultOverShoot)}
        {% set Z_OVER = params.ZERO_OVERSHOOT|default(defaultOverShoot)|int %}
        {action_respond_info("Z_OVER for extruder = %s;" % Z_OVER)}
        {% set FAN_SPEED = params.FAN_SPEED|default(0.64)|float %}
        {% set SOAK_MINUTES = params.SOAK_MINUTES|default(12)|float %}
        {% set BED_TEMP = params.BED_TEMP|default(defaultTB)|float %}
        {% set NZL_TEMP = params.NZL_TEMP|default(defaultTN)|float %}
        {% set X_MID = printer.configfile.config.stepper_x.position_max|float / 2.0 %}
        {% set Y_MID = printer.configfile.config.stepper_y.position_max|float / 2.0 %}
        {% set defaultENCLOSURE = user.filament.profile.defaultEnclosure|float %}
        {% set ENCLOSURE_TEMP = params.ENCLOSURE_TEMP|default(defaultENCLOSURE)|float %}
        {% set WRITE_FILE = params.WRITE_FILE|default(0)|int %}
        # if WRITE_FILE = 1 then file is saved to `/tmp/heattest.txt` on raspberry pi
        {action_respond_info("WRITE_FILE for heater_bed = %s;" % WRITE_FILE)}
        G90                                                                                       ;Absolute Positioning
        M117 Performing initial homing.
        G32                                                                                       ;Clears bed-mesh and performs G28, ATTACH_PROBE, QGL, DOCK_PROBE
        G1 Z5 Y{Y_MID} X{X_MID} F4000                                                             ;move to center of bed
        M117 Bringing bed to temperature.
        {% if user.hw.chamber.fan %} M141 S{ENCLOSURE_TEMP} {% endif %}                           ;set chamber temperature for Exhaust fan and Bed fans
        FILTER                                                                                    ;Toggle Nevermore Filter
        M106 S{(FAN_SPEED*255)}                                                                   ;Part Cooling Fan On and start monitoring the tach signal
        M190 S{BED_TEMP}                                                                          ;Wait for bed temp within 5 degrees
        _HEAT_WAIT MINUTES={SOAK_MINUTES} MSG="Pre NZL_PID Soaking..."                            ;Heating cycle waiting routine
        SET_LED LED=sb_leds INDEX=17 RED=.5 GREEN=.5 BLUE=0
        SET_LED LED=sb_leds INDEX=18 RED=.5 GREEN=.5 BLUE=0
        M117 Starting PID calibration.
        PID_CALIBRATE HEATER=extruder TARGET={NZL_TEMP} ZERO_OVERSHOOT={Z_OVER} WRITE_FILE={WRITE_FILE}   ;PID tune the extruder
        M117 Finished PID calibration.
        TURN_OFF_HEATERS                                                                          ;Turn off all heaters and reset the chamber temperature for Exhaust fan
        FILTER                                                                                    ;Toggle Nevermore Filter
        G90                                                                                       ;Absolute Positioning
        PARK_UpperRight                                                                           ;Parks nozzle at top front-right
        M18 X Y E                                                                                 ;Disable Stepper motor
        SET_LED LED=sb_leds INDEX=17 RED=.2 GREEN=.5 BLUE=.2
        SET_LED LED=sb_leds INDEX=18 RED=.2 GREEN=.5 BLUE=.2
        _COOL_WAIT MINUTES={user.filament.profile.PostPrintParkCool|float}                        ;Cooling cycle waiting routine
        STATUS_READY                                                                              ;SB LED status
		SAVE_CONFIG
    {% endif %}
    _general_Debug msg="NZL_PID - exiting"
```
---

```
### Moonraker Update Manager:

It's possible to keep this extension up to date with the Moonraker's update manager by adding this configuration block to the `moonraker.conf` of your printer:

```python
[update_manager zero_overshoot]
type: git_repo
path: ~/Zero_Overshoot
origin: https://github.com/GadgetAngel/Zero_Overshoot.git
install_script: install_zero_overshoot.sh
is_system_service: False
managed_services: klipper
```

After you update `moonraker.conf` file, I rebooted my Raspberry Pi to get it to install (or you could just restart the moonraker service).

This requires this repository to be cloned into your home directory (e.g. /home/pi):

```BASH
git clone https://github.com/GadgetAngel/Zero_Overshoot.git
```

The URL for Moonraker ``[update_manager]`` section can be found [here](https://moonraker.readthedocs.io/en/latest/configuration/#update_manager)

---

Now, you are free to try out the following commands:

```BASH
PID_CALIBRATE HEATER=heater_bed TARGET=110
```

```BASH
PID_CALIBRATE HEATER=heater_bed TARGET=110 ZERO_OVERSHOOT=0
```

```BASH
PID_CALIBRATE HEATER=heater_bed TARGET=110 ZERO_OVERSHOOT=1
```

```BASH
PID_CALIBRATE HEATER=extruder TARGET=240
```

```BASH
PID_CALIBRATE HEATER=extruder TARGET=240 ZERO_OVERSHOOT=0
```

```BASH
PID_CALIBRATE HEATER=extruder TARGET=240 ZERO_OVERSHOOT=1
```

Happy 3D printing!!



























