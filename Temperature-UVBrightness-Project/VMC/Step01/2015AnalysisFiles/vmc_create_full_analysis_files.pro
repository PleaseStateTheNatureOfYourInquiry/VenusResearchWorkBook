Pro VMC_create_full_analysis_files,VeRafiles


;----------Determine the number of files in "VeRafiles" containing the list of VeRa soundings---------------------


          Get_lun , VeRa_unit

          Openr, VeRa_unit, VeRafiles

          dump = STRARR(1)

          n = 0L

ref_2:    Readf , VeRa_unit , dump
          n = n + 1
          If NOT EOF(VeRa_unit) Then Goto, ref_2

          Close , VeRa_unit

          VeRa_name = STRARR(n)          
          VeRa_doy = INTARR(n)
          orbit = INTARR(n)
          VeRa_lat = FLTARR(n)
          VeRa_lon = FLTARR(n)
          VeRa_time = FLTARR(n)
          
          name_in=STRARR(1)
  
          Openr, VeRa_unit, VeRafiles

          For i = 0 , n-1  Do Begin

           Readf , VeRa_unit , $
            FORMAT='(4x,A31,7X,I3,6X,I4,3x,F12.8,3x,F12.8,4x,F11.4)' , name_in , doy_in , orbit_in , lat_in , lon_in , t_in

           VeRa_name(i) = name_in
           VeRa_doy(i) = doy_in
           orbit(i) = orbit_in
           VeRa_lat(i) = lat_in
           VeRa_lon(i) = lon_in
           VeRa_time(i) = t_in
           
          Endfor 
                                 
 
          Close,VeRa_unit

          Free_lun , VeRa_unit


;----------construct the _full_analysis  files----------

         Get_lun , full_analysis_unit

         For i = 0,n-1 Do Begin
          
          VeRa_name_sub = VeRa_name(i)
          If orbit(i) LT 100 Then $
            name_full_analysis = STRCOMPRESS('Orb00' + STRING(orbit(i)) + '_full_analysis_' + STRMID(VeRa_name_sub,11,3),/REMOVE_ALL)
          If orbit(i) GE 100 AND orbit(i) LT 1000 Then $
            name_full_analysis = STRCOMPRESS('Orb0' + STRING(orbit(i)) + '_full_analysis_' + STRMID(VeRa_name_sub,11,3),/REMOVE_ALL)
          If orbit(i) GE 1000 Then $
            name_full_analysis = STRCOMPRESS('Orb' + STRING(orbit(i)) + '_full_analysis_' + STRMID(VeRa_name_sub,11,3),/REMOVE_ALL)

                  
          Openw , full_analysis_unit , name_full_analysis
          
          Printf , full_analysis_unit , ' '
          Printf , full_analysis_unit , ' File: ' + name_full_analysis 
          Printf , full_analysis_unit , ' '
          Printf , full_analysis_unit , ' This file contains the list of all the UV files in this orbit'
          Printf , full_analysis_unit , ' '
          Printf , full_analysis_unit , ' The numbers on the first line are the latitude, longitude, day of year, hour and minute of the sounding location'
          Printf , full_analysis_unit , ' '
          Printf , full_analysis_unit , 'C_END'

          VeRa_h = FIX(VeRa_time(i))
          VeRa_m = FIX( ( VeRa_time(i) - FIX(VeRa_time(i)) ) * 60 + 0.5)

          If VeRa_lat(i) GE 0 Then Begin
            
            Printf , full_analysis_unit , FIX(VeRa_lat(i)+0.5) , FIX(VeRa_lon(i)+0.5) , VeRa_doy(i) , Vera_h , VeRa_m

          Endif Else Begin
            
            Printf , full_analysis_unit , FIX(VeRa_lat(i)-0.5) , FIX(VeRa_lon(i)+0.5) , VeRa_doy(i) , Vera_h , VeRa_m
            
          Endelse
 
          If orbit(i) LT 100 Then $
            cd_orbit = STRCOMPRESS('~/Venus/data/VMC/Orb00' + STRING(orbit(i)) + '/',/REMOVE_ALL)
          If orbit(i) GE 100 AND orbit(i) LT 1000 Then $
            cd_orbit = STRCOMPRESS('~/Venus/data/VMC/Orb0' + STRING(orbit(i)) + '/',/REMOVE_ALL)
          If orbit(i) GE 1000 Then $
            cd_orbit = STRCOMPRESS('~/Venus/data/VMC/Orb' + STRING(orbit(i)) + '/',/REMOVE_ALL)

          cd,cd_orbit

          Spawn , 'ls *UV2.IMG' , VMCimage_list

          size_VMCimage = SIZE(VMCimage_list)         
          n_VMCimages = size_VMCimage(1)
          
          If n_VMCimages EQ -1 Then Begin
            
            print,'no data in ' + name_full_analysis
            Goto,ref_3

          Endif
          
          For j = 0,n_VMCimages-1 Do Begin
            
           Printf , full_analysis_unit , STRCOMPRESS( cd_orbit + STRMID(VMCimage_list(j),0,14) , /REMOVE_ALL )           
            
          Endfor

ref_3:    cd,'../'
          
          Close , full_analysis_unit
          
         Endfor

         End
          