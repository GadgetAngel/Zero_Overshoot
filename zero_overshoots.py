# Tracking of PWM controlled heaters and their temperature control
#
# Copyright (C) 2016-2020  Kevin O'Connor <kevin@koconnor.net>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging
import configparser
from .pid_calibrate import (
      PIDCalibrate,
      ControlAutoTune
)

ONE_THIRD=1./3.
PERCENT88 =88./100.     
    
######################################################################
# Heater lookup and define new options for PID control
######################################################################
   
class ZeroOvershootHeater:
    def __init__(self, config):
        if len(config.get_name().split()) > 2:
            raise config.error(
                    "Name of section '%s' contains illegal whitespace"
                    % (config.get_name()))
        self.full_section = config.get_name()
        self.heater_name = self.full_section.split()[1]
        self.section = self.full_section.split()[0]
        if not self.heater_name in ['extruder','heater_bed']:
            raise configparser.Error(
                "Invalid name of '%s' for %s section" % (self.heater_name, self.section))    
        self.zero_overshoot = config.getboolean('zero_overshoot', False)
        self.Kp_multiplier = config.getfloat('Kp_multiplier', ONE_THIRD)
        self.Ki_multiplier = config.getfloat('Ki_multiplier', ONE_THIRD)
        self.Kd_multiplier = config.getfloat('Kd_multiplier', PERCENT88)
        # let Log file know this extension is active
        logging.info("zero_overshoot ::INFO:: [zero_overshoot %s]: zero_overshoot = %s" % (self.heater_name, self.zero_overshoot)) 
        logging.info("zero_overshoot ::INFO:: [zero_overshoot %s]: Kp_multiplier = %s" % (self.heater_name, self.Kp_multiplier)) 
        logging.info("zero_overshoot ::INFO:: [zero_overshoot %s]: Ki_multiplier = %s" % (self.heater_name, self.Ki_multiplier)) 
        logging.info("zero_overshoot ::INFO:: [zero_overshoot %s]: Kd_multiplier = %s" % (self.heater_name, self.Kd_multiplier)) 
    def get_K_multiplier_values(self):
        return self.zero_overshoot, self.Kp_multiplier, self.Ki_multiplier, self.Kd_multiplier
        
######################################################################
# ZERO_OVERSHOOTS Klipper extension inherits from pid_calibrate.PIDCalibrate
######################################################################        
class ZeroOvershoots(PIDCalibrate):
    def __init__(self, config):
        self.printer = printer = config.get_printer()
        self.heaters = {}
        self.available_heaters = []
        # Unregister any pre-existing pid_calibrate commands first.
        gcode = self.printer.lookup_object('gcode')
        gcode.register_command('PID_CALIBRATE', None)
        PIDCalibrate.__init__(self, config)
        self.printer.register_event_handler("klippy:ready", self.handle_ready)
                               
    def handle_ready(self):
        # This is the hacky bit:
        # The "klippy:ready" event is sent after all configuration has been
        # read and all objects created. So, we are sure that the 'pid_calibrate'
        # object already exists.
        # So, we can reach into the printer objects and replace the existing 'pid_calibrate'
        # object with this one.
        pid_calibrate_obj = self.printer.objects.pop('pid_calibrate', None)
        self.printer.objects['pid_calibrate'] = self
        del pid_calibrate_obj  
        
    def setup_heater(self, config):
        heater_name = config.get_name().split()[-1]
        if not heater_name in ['extruder','heater_bed']:
            raise config.error("Invalid Heater name: %s" % (heater_name,))
        self.heaters[heater_name] = heater = ZeroOvershootHeater(config)
        return heater        
    def cmd_PID_CALIBRATE(self, gcmd):
        heater_name = gcmd.get('HEATER')
        pheaters = self.printer.lookup_object('heaters')
        try:
            heater = pheaters.lookup_heater(heater_name)
        except self.printer.config_error as e:
            raise gcmd.error(str(e))
        zheater = self.heaters[heater_name]
        zero_overshoot = zheater.get_K_multiplier_values()[0]
        cmdline_param = gcmd.get_int("ZERO_OVERSHOOT", zero_overshoot)
        target = gcmd.get_float('TARGET')
        write_file = gcmd.get_int('WRITE_FILE', 0)
        self.printer.lookup_object('toolhead').get_last_move_time()
        calibrate = ControlAutoTune(heater, target)
        old_control = heater.set_control(calibrate)
        try:
            pheaters.set_temperature(heater, target, True)
        except self.printer.command_error as e:
            heater.set_control(old_control)
            raise
        heater.set_control(old_control)
        if write_file:
            calibrate.write_file('/tmp/heattest.txt')
        if calibrate.check_busy(0., 0., 0.):
            raise gcmd.error("pid_calibrate interrupted")
        Kp, Ki, Kd = calibrate.calc_final_pid()
        logging.info("ClassicPID Autotune: final: Kp=%f Ki=%f Kd=%f" % (Kp, Ki, Kd))
        # gcmd.respond_info("ClassicPID Autotune: final: Kp=%f Ki=%f Kd=%f" % (Kp, Ki, Kd))
        #ZERO_OVERSHOOT zero_overshoot_final_calc func changes Kp, Ki, Kd values
        Kp, Ki, Kd = self.zero_overshoot_final_calc(gcmd, heater_name, Kp, Ki, Kd, cmdline_param)
        # Log and report results
        if cmdline_param == True:
            logging.info("Zero Overshoot Autotune: final: Kp=%f Ki=%f Kd=%f" % (Kp, Ki, Kd))
            # gcmd.respond_info("Zero Overshoot Autotune: final: Kp=%f Ki=%f Kd=%f" % (Kp, Ki, Kd))
            gcmd.respond_info(
                "Zero Overshoot Calculated PID parameters: "
                "    pid_Kp=%.3f pid_Ki=%.3f pid_Kd=%.3f\n"
                "The SAVE_CONFIG command will update the printer config file\n"
                "with these parameters and restart the printer." % (Kp, Ki, Kd))
        else:
            logging.info("Autotune: final: Kp=%f Ki=%f Kd=%f" % (Kp, Ki, Kd))
            # gcmd.respond_info("Autotune: final: Kp=%f Ki=%f Kd=%f" % (Kp, Ki, Kd))
            gcmd.respond_info(
                "PID parameters: pid_Kp=%.3f pid_Ki=%.3f pid_Kd=%.3f\n"
                "The SAVE_CONFIG command will update the printer config file\n"
                "with these parameters and restart the printer." % (Kp, Ki, Kd))        
        # Store results for SAVE_CONFIG
        configfile = self.printer.lookup_object('configfile')
        configfile.set(heater_name, 'control', 'pid')
        configfile.set(heater_name, 'pid_Kp', "%.3f" % (Kp,))
        configfile.set(heater_name, 'pid_Ki', "%.3f" % (Ki,))
        configfile.set(heater_name, 'pid_Kd', "%.3f" % (Kd,))
    def zero_overshoot_final_calc(self, gcmd, heater_name, Kp, Ki, Kd, cmdparam=None):
        if cmdparam == False:
            gcmd.respond_info("Using ClassicPID values...")
            return Kp, Ki, Kd
        gcmd.respond_info("Using Zero_Overshoot Calculated values...")
        zheater = self.heaters[heater_name]
        self.Kp_multiplier, self.Ki_multiplier, self.Kd_multiplier = zheater.get_K_multiplier_values()[1:]
        myKp = round((Kp * self.Kp_multiplier),3)       
        myKi = round((Ki * self.Ki_multiplier),3)       
        myKd = round((Kd * self.Kd_multiplier),3)             
        return myKp, myKi, myKd
        
def load_config(config):
    return ZeroOvershoots(config)