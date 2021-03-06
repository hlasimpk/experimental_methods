#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Object allows to define and carry out a collection of series of wedges of diffraction images of arbitrary slicing parameter and of arbitrary size at arbitrary reference angles.
'''
import traceback
import logging
import time
import os
import pickle

from omega_scan import omega_scan

#class reference_images(scan):
#    def __init__(self,scan_range, scan_exposure_time, scan_start_angles, angle_per_frame, name_pattern, directory, image_nr_start, position=None, photon_energy=None, flux=None, transmission=None ):
#        self.scan_start_angles = scan_start_angles
#        scan_start_angle = scan_start_angles[0]
#        super(self, scan).__init__(scan_range, scan_exposure_time, scan_start_angle, angle_per_frame, name_pattern, directory, image_nr_start, position=None, photon_energy=None, flux=None, transmission=None)
#        self._ntrigger = len(scan_start_angles)
#        
#    def run(self):
#        for scan_start_angle in self.scan_start_angles:
#            self.goniometer.set_scan_start_angle(scan_start_angle)
#            scan_id = self.goniometer.start_scan()
#            while self.goniometer.is_task_running(scan_id):
#                time.sleep(0.1)

class reference_images(omega_scan):
    
    actuator_names = ['Omega']
    
    specific_parameter_fields = set(['scan_start_angles'])

    def __init__(self, 
                 name_pattern='ref-test_$id', 
                 directory='/tmp', 
                 scan_range=1, 
                 scan_exposure_time=1, 
                 scan_start_angles='[0, 90, 180, 270]', 
                 angle_per_frame=0.1, 
                 image_nr_start=1,
                 position=None,
                 photon_energy=None,
                 resolution=None,
                 detector_distance=None,
                 detector_vertical=None,
                 detector_horizontal=None,
                 transmission=None,
                 flux=None,
                 snapshot=None,
                 diagnostic=None,
                 analysis=None,
                 simulation=None): 
        
        self.scan_start_angles = eval(scan_start_angles)
        self.scan_range = scan_range
        self.angle_per_frame = angle_per_frame
        
        ntrigger = len(self.scan_start_angles)
        nimages_per_file = int(self.scan_range/self.angle_per_frame)
        
        omega_scan.__init__(self,
                            name_pattern, 
                            directory, 
                            scan_range=scan_range, 
                            scan_exposure_time=scan_exposure_time, 
                            angle_per_frame=angle_per_frame, 
                            image_nr_start=image_nr_start,
                            position=position, 
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
                            diagnostic=diagnostic,
                            analysis=analysis,
                            simulation=simulation)
        
        self.ntrigger = ntrigger
        
        self.total_expected_exposure_time = self.scan_exposure_time * ntrigger
        self.total_expected_wedges = ntrigger
        
        self.parameter_fields = self.parameter_fields.union(reference_images.specific_parameter_fields)
        
    def set_scan_start_angles(self, scan_start_angles):
        self.scan_start_angles = scan_start_angles
        
    def get_scan_start_angles(self):
        return self.scan_start_angles
    
    def get_nimages_per_file(self):
        return int(self.scan_range/self.angle_per_frame)
        
    def run(self, wait=True):
        self._start = time.time()
        task_ids = []
        self.md2_task_info = []
        for scan_start_angle in self.scan_start_angles:
            print 'scan_start_angle', scan_start_angle
            task_id = self.goniometer.omega_scan(scan_start_angle, self.scan_range, self.scan_exposure_time, wait=wait)
            task_ids.append(task_id)
            self.md2_task_info.append(self.goniometer.get_task_info(task_id))
    
def main():
    import optparse
        
    parser = optparse.OptionParser()
    parser.add_option('-n', '--name_pattern', default='ref-test_$id', type=str, help='Prefix default=%default')
    parser.add_option('-d', '--directory', default='/nfs/data/default', type=str, help='Destination directory default=%default')
    parser.add_option('-r', '--scan_range', default=1, type=float, help='Scan range [deg]')
    parser.add_option('-e', '--scan_exposure_time', default=0.25, type=float, help='Scan exposure time [s]')
    parser.add_option('-s', '--scan_start_angles', default='[0, 90, 180, 270]', type=str, help='Scan start angles [deg]')
    parser.add_option('-a', '--angle_per_frame', default=0.1, type=float, help='Angle per frame [deg]')
    parser.add_option('-f', '--image_nr_start', default=1, type=int, help='Start image number [int]')
    parser.add_option('-i', '--position', default=None, type=str, help='Gonio alignment position [dict]')
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
    ri = reference_images(**vars(options))
    ri.execute()
    
if __name__ == '__main__':
    main()
