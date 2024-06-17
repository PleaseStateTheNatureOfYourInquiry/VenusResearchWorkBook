Pro VMC_phase_angle_analysis,orb_file_names,phase_angle_file


;----------Determine the number of files in the file "orb_file_names" containing the list of files from each orbit Orbnnnn_full_analysis----------------

          Get_lun , file_unit

          dump = STRING(5)
          
          Openr , file_unit , orb_file_names

 ref_1:   Readf , file_unit , dump


          If dump NE 'C_END' Then Goto, ref_1

          n_orb = 0L
         
 ref_2:   Readf , file_unit , dump
          n_orb = n_orb + 1
          If NOT EOF(file_unit) Then Goto, ref_2

          Close , file_unit

       
;-----------Read all the orb files names

          Openr , file_unit , orb_file_names

ref_3:    Readf , file_unit , dump

          If dump NE 'C_END' Then Goto, ref_3

          orbfiles = STRARR(n_orb)
          dump = STRING(90)

          For i = 0,n_orb-1 Do Begin

           Readf , file_unit , dump

           orbfiles(i) = STRCOMPRESS(dump)
           
          Endfor
      
          Close , file_unit
          Free_lun , file_unit


;----------The file containing all of the information (general file) is  phase_angle_file ------

          Get_lun , phase_file

          Openw , phase_file , phase_angle_file

          Printf , phase_file ,''
          Printf , phase_file ,'File produced by vmc_phase_angle_analysis.pro  (v20151021)'
          Printf , phase_file ,''
          Printf , phase_file ,'   ID    pa(˚) d_pa(˚)  B   dB   ia(˚) d_ia(˚)  ea(˚) d_ea()'
          Printf , phase_file ,'C_END'
          

          For j = 0,n_orb-1 Do Begin

           orbit_dump = orbfiles(j)
           print,j,' : ',orbit_dump
           Reads,STRMID(orbit_dump,3,4),orbit_ID
           orbit_ID = FIX(orbit_ID)


;---------read all images within each orb file, write the general file (phase_angle_file) and the individual orbit files (phase_angle_orbit_file)
             
           name = orbfiles(j)

;---------check if the orbfile(j) has AIX or AEX in it--------


           name_length = STRLEN(name)

           For k = 0,name_length-3 Do Begin
            
            If STRMID(name,k,3) EQ 'AIX' OR STRMID(name,k,3) EQ 'AEX' Then Begin
              
             phase_angle_orbit_file = STRMID(orbit_dump,0,8) + 'phase_lambert_only_' + STRMID(name,k,3)
             phase_angle_orbit_file = STRCOMPRESS(phase_angle_orbit_file,/REMOVE_ALL)
             Goto,ref_moveon
              
            Endif Else Begin
              
             phase_angle_orbit_file = STRMID(orbit_dump,0,8) + 'phase_lambert_only'
             
            Endelse

           Endfor

ref_moveon:

           Get_lun , phase_orbit_file

           Openw  , phase_orbit_file , phase_angle_orbit_file
           Printf , phase_orbit_file ,''
           Printf , phase_orbit_file ,'File produced by vmc_phase_angle_analysis.pro  (v20151021)'
           Printf , phase_orbit_file ,''
           Printf , phase_orbit_file ,'   ID    pa(˚) d_pa(˚)  B   dB   ia(˚) d_ia(˚)  ea(˚) d_ea()'

           Printf , phase_orbit_file ,'C_END'



           Get_lun , file_unit

           dump = STRING(5)

           Openr , file_unit , name

ref_4:     Readf , file_unit , dump

           If dump NE 'C_END' Then Goto, ref_4

           n = 0L

ref_5:     Readf , file_unit , dump
           n = n + 1
           If NOT EOF(file_unit) Then Goto, ref_5

           Close , file_unit

           n = n-1 


           Openr , file_unit , name

ref_6:     Readf , file_unit , dump
       
           If dump NE 'C_END' Then Goto, ref_6


;----------The first line after C_END contains the sounded coordinates and time

           Readf , file_unit , lat_sound , lon_sound , T_sound_d , T_sound_h , T_sound_m


;----------Define some parameters: albedo and stddev albedo, coordinates of the site corrected for wind, the time difference between the 
;----------moment of sounding and the moment of image acquisition, pa_average is the average of the phase angle and its stddev over the valid
;----------pixels (see the routine VMCphotometry)
 
           albedo_nowind = FLTARR(n)
           dalbedo_nowind = FLTARR(n)

           lon_site_nowind = FLTARR(n)
           dlon_site_nowind = FLTARR(n)
           lat_site_nowind = FLTARR(n)
           dlat_site_nowind = FLTARR(n)

           albedo_wind = FLTARR(n)
           dalbedo_wind = FLTARR(n)

           lon_site_wind = FLTARR(n)
           dlon_site_wind = FLTARR(n)
           lat_site_wind = FLTARR(n)
           dlat_site_wind = FLTARR(n)

           deltaT = FLTARR(n)
           pa_average = FLTARR(n)
           pa_stddev = FLTARR(n)

           ia_average = FLTARR(n)
           ia_stddev = FLTARR(n)

           ea_average = FLTARR(n)
           ea_stddev = FLTARR(n)
  
           dump = STRING(90)
 
 
 ;----------number of valid points written to the file----
 
           n_points = 0
 
           For i = 0,n-1 Do begin

            dalbedo_nowind(i) = 0
            dalbedo_wind(i) = 0

            Readf, file_unit, dump
            image_name = STRCOMPRESS(dump)
            
            resultgeo = FILE_TEST(STRCOMPRESS(image_name + '.GEO',/REMOVE_ALL))
            If resultgeo NE 1 Then Goto , ref_nogeo

            VMCimage_albedo_extract,image_name,dlat,dlon,lat_sound,lon_sound,T_sound_d,T_sound_h,T_sound_m,'NO_WIND_INFO',$
                                    pa_average_in,lat_site_in,lon_site_in,deltaT_in,albedo_in,ia_average_in,ea_average_in

          
            albedo_nowind(i) = albedo_in(0)
            dalbedo_nowind(i) = SQRT(albedo_in(1)) 

            lon_site_nowind(i) = lon_site_in
            dlon_site_nowind(i) = dlon

            lat_site_nowind(i) = lat_site_in
            dlat_site_nowind(i) = dlat

            deltaT(i) = deltaT_in

            pa_average(i) = pa_average_in(0)
            pa_stddev(i) = SQRT(pa_average_in(1))

            ia_average(i) = ia_average_in(0)
            ia_stddev(i) = SQRT(ia_average_in(1))

            ea_average(i) = ea_average_in(0)
            ea_stddev(i) = SQRT(ea_average_in(1))


;            If windfile NE 'NO_WIND_INFO' Then Begin

;             VMCimage_albedo_extract,image_name,dlat,dlon,lat_sound,lon_sound,T_sound_d,T_sound_h,T_sound_m,windfile,$
;               pa_average_in,lat_site_in,lon_site_in,deltaT_in,albedo_in

;             albedo_wind(i) = albedo_in(0)
;             dalbedo_wind(i) = SQRT(albedo_in(1))

;             lon_site_wind(i) = lon_site_in
;             dlon_site_wind(i) = dlon

;             lat_site_wind(i) = lat_site_in
;             dlat_site_wind(i) = dlat

;            Endif


;-----------write to both orbit file (phase_orbit_file) and the general file (phase_file), write only positive values, not non-sense values

            If albedo_nowind(i) GT .1 Then Begin

             n_points = n_points + 1

             If orbit_ID GT 2638 Then beta_factor = 1 
             If orbit_ID LE 2638 Then beta_factor = 2.34

             Printf , Format = '(3x,I4,3x,F6.2,2x,F6.4,3x,F5.3,2x,F6.4,3x,F5.2,2x,F5.2,3x,F5.2,2x,F5.2)' , phase_orbit_file , orbit_ID , pa_average(i) , pa_stddev(i) , albedo_nowind(i)*beta_factor , dalbedo_nowind(i)*beta_factor , ia_average(i) , ia_stddev(i) , ea_average(i) , ea_stddev(i)
             Printf , Format = '(3x,I4,3x,F6.2,2x,F6.4,3x,F5.3,2x,F6.4,3x,F5.2,2x,F5.2,3x,F5.2,2x,F5.2)' , phase_file , orbit_ID , pa_average(i) , pa_stddev(i) , albedo_nowind(i)*beta_factor , dalbedo_nowind(i)*beta_factor , ia_average(i) , ia_stddev(i) , ea_average(i) , ea_stddev(i)
    
            Endif

ref_nogeo:
    
           Endfor
 
           Close , phase_orbit_file
           Free_lun , phase_orbit_file

           print,phase_angle_orbit_file,n_points
           
           If n_points LE 2 Then File_Delete,phase_angle_orbit_file 
 
           Close , file_unit
           Free_lun , file_unit

          Endfor 
  
          Close , phase_file
          Free_lun , phase_file

         
         End
          
