#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
helical scan
'''
import traceback
import logging
import time
import os
import pickle

from omega_scan import omega_scan

class helical_scan(omega_scan):
    
    actuator_names = ['Omega', 'AlignmentX', 'AlignmentY', 'AlignmentZ', 'CentringX', 'CentringY']
    
    specific_parameter_fields = set(['position_start',
                                    'position_end'])
    
    def __init__(self, 
                 name_pattern='test_$id', 
                 directory='/tmp', 
                 scan_range=180, 
                 scan_exposure_time=18, 
                 scan_start_angle=0, 
                 angle_per_frame=0.1, 
                 image_nr_start=1,
                 position_start=None,
                 position_end=None,
                 photon_energy=None,
                 resolution=None,
                 detector_distance=None,
                 detector_vertical=None,
                 detector_horizontal=None,
                 transmission=None,
                 flux=None,
                 snapshot=False,
                 ntrigger=1,
                 nimages_per_file=100,
                 zoom=None,
                 diagnostic=None,
                 analysis=None,
                 simulation=None):
        
        omega_scan.__init__(self,
                            name_pattern=name_pattern, 
                            directory=directory,
                            scan_range=scan_range, 
                            scan_exposure_time=scan_exposure_time, 
                            scan_start_angle=scan_start_angle,
                            angle_per_frame=angle_per_frame, 
                            image_nr_start=image_nr_start,
                            photon_energy=photon_energy,
                            resolution=resolution,
                            detector_distance=detector_distance,
                            detector_vertical=detector_vertical,
                            detector_horizontal=detector_horizontal,
                            transmission=transmission,
                            flux=flux,
                            snapshot=snapshot,
                            ntrigger=ntrigger,
                            nimages_per_file=nimages_per_file,
                            zoom=zoom,
                            diagnostic=diagnostic,
                            analysis=analysis,
                            simulation=simulation)
            
        self.position_start = self.goniometer.check_position(position_start)
        self.position_end = self.goniometer.check_position(position_end)
        
        self.total_expected_exposure_time = self.scan_exposure_time
        self.total_expected_wedges = 1
        
        self.parameter_fields = self.parameter_fields.union(helical_scan.specific_parameter_fields)
    
    def set_position_start(self, position_start):
        self.position_start = position_start
    def get_position_start(self):
        return self.position_start
    
    def set_position_end(self, position_end):
        self.position_end = position_end
    def get_position_end(self):
        return self.position_end
        
    def run(self, wait=True):
        
        self._start = time.time()
        
        task_id = self.goniometer.helical_scan(self.position_start, self.position_end, self.scan_start_angle, self.scan_range, self.scan_exposure_time, wait=wait)
        
        self.md2_task_info = self.goniometer.get_task_info(task_id)
        
          
def main():
    import optparse
        
    position_start = "{'AlignmentX': -0.10198379516601541, 'AlignmentY': -1.5075817417454083, 'AlignmentZ': -0.14728600084459487, 'CentringX': -0.73496162280701749, 'CentringY': 0.37533442982456139}"
    position_end = "{'AlignmentX': -0.10198379516601541, 'AlignmentY': -1.0274660058923679, 'AlignmentZ': -0.14604777073215836, 'CentringX': -0.41848684210526316, 'CentringY': -0.083777412280701749}"
    
    parser = optparse.OptionParser()
    parser.add_option('-n', '--name_pattern', default='helical_test_$id', type=str, help='Prefix default=%default')
    parser.add_option('-d', '--directory', default='/nfs/data/default', type=str, help='Destination directory default=%default')
    parser.add_option('-r', '--scan_range', default=180, type=float, help='Scan range [deg]')
    parser.add_option('-e', '--scan_exposure_time', default=18, type=float, help='Scan exposure time [s]')
    parser.add_option('-s', '--scan_start_angle', default=0, type=float, help='Scan start angle [deg]')
    parser.add_option('-a', '--angle_per_frame', default=0.1, type=float, help='Angle per frame [deg]')
    parser.add_option('-f', '--image_nr_start', default=1, type=int, help='Start image number [int]')
    parser.add_option('-B', '--position_start', default=position_start, type=str, help='Gonio alignment start position [dict]')
    parser.add_option('-E', '--position_end', default=position_end, type=str, help='Gonio alignment end position [dict]')
    parser.add_option('-p', '--photon_energy', default=None, type=float, help='Photon energy ')
    parser.add_option('-t', '--detector_distance', default=None, type=float, help='Detector distance')
    parser.add_option('-o', '--resolution', default=None, type=float, help='Resolution [Angstroem]')
    parser.add_option('-x', '--flux', default=None, type=float, help='Flux [ph/s]')
    parser.add_option('-m', '--transmission', default=None, type=float, help='Transmission. Number in range between 0 and 1.')
    parser.add_option('-A', '--analysis', action='store_true', help='If set will perform automatic analysis.')
    parser.add_option('-D', '--diagnostic', action='store_true', help='If set will record diagnostic information.')
    parser.add_option('-S', '--simulation', action='store_true', help='If set will record diagnostic information.')
    
    options, args = parser.parse_args()
    print 'options', options
    hs = helical_scan(**vars(options))
    hs.execute()

def test():
    position_start = "{'AlignmentX': -0.10198379516601541, 'AlignmentY': -1.5075817417454083, 'AlignmentZ': -0.14728600084459487, 'CentringX': -0.73496162280701749, 'CentringY': 0.37533442982456139}"
    position_end = "{'AlignmentX': -0.10198379516601541, 'AlignmentY': -1.0274660058923679, 'AlignmentZ': -0.14604777073215836, 'CentringX': -0.41848684210526316, 'CentringY': -0.083777412280701749}"
    
    hs = helical_scan(position_start=eval(position_start), position_end=eval(position_end))
    
if __name__ == '__main__':
    main()