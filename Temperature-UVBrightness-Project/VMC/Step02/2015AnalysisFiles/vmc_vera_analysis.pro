Pro VMC_VERA_analysis,name,windfile,phase_file_all,beta_factor


;----------beta_factor is 2.34 for orbit numbers smaller and equal to 2451 (up to EXT3) and 1.0 for EXT4

;----------phase_file_all  contains the full analysis results (B/mu0 - alpha) of the first run on all the images
;----------I added this to compare against the specific orbit

          Readtable,phase_file_all,table,5

          pa_in = table(*,1)
          alb_in = table(*,3)





;----------Determine the number of files in the file "name" containing the list of UV image for this orbit-----------------------

          Get_lun , file_unit

          dump = STRING(5)
          
          Openr , file_unit , name

 ref_1:   Readf , file_unit , dump


          If dump NE 'C_END' Then Goto, ref_1

          n = 0L
         
 ref_2:   Readf , file_unit , dump
          n = n + 1
          If NOT EOF(file_unit) Then Goto, ref_2

          Close , file_unit


;-----------Open three windows: 0 = the image-albedo plot, 1 = the orthographic plot, 2 = the image as is 

          Window , 0 , xsize = 1500 , ysize = 500
          Window , 1 , xsize = 600 , ysize = 600
          Window , 2 , xsize = 512 , ysize = 512
       
       
;-----------Read all the files and plot the image-albedo plot

          n = n-1 

          Openr , file_unit , name

 ref_3:   Readf , file_unit , dump
       
          If dump NE 'C_END' Then Goto, ref_3


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
  
          dump = STRING(90)
 
 
          For i = 0,n-1 Do begin

           dalbedo_nowind(i) = 0
           dalbedo_wind(i) = 0

           Readf, file_unit, dump
           image_name = STRCOMPRESS(dump)

           VMCimage_albedo_extract,image_name,dlat,dlon,lat_sound,lon_sound,T_sound_d,T_sound_h,T_sound_m,'NO_WIND_INFO',$
                                   pa_average_in,lat_site_in,lon_site_in,deltaT_in,albedo_in

          
           albedo_nowind(i) = albedo_in(0)
           dalbedo_nowind(i) = SQRT(albedo_in(1)) 

           lon_site_nowind(i) = lon_site_in
           dlon_site_nowind(i) = dlon

           lat_site_nowind(i) = lat_site_in
           dlat_site_nowind(i) = dlat

           deltaT(i) = deltaT_in

           pa_average(i) = pa_average_in(0)
           pa_stddev(i) = pa_average_in(1)


           If windfile NE 'NO_WIND_INFO' Then Begin

            VMCimage_albedo_extract,image_name,dlat,dlon,lat_sound,lon_sound,T_sound_d,T_sound_h,T_sound_m,windfile,$
              pa_average_in,lat_site_in,lon_site_in,deltaT_in,albedo_in

            albedo_wind(i) = albedo_in(0)
            dalbedo_wind(i) = SQRT(albedo_in(1))

            lon_site_wind(i) = lon_site_in
            dlon_site_wind(i) = dlon

            lat_site_wind(i) = lat_site_in
            dlat_site_wind(i) = dlat

           Endif
    
          Endfor
 
          Close, file_unit


;---------instead of "albedo" use B/mu0  (W/m2/ster/micron) (multiply with  1081 / (0.723 * 0.723 * pi) and apply the beta_factor.

          albedo_nowind = albedo_nowind * beta_factor * 658
          dalbedo_nowind = dalbedo_nowind * beta_factor * 658

          albedo_wind = albedo_wind * beta_factor * 658
          dalbedo_wind = dalbedo_wind * beta_factor * 658

          alb_in = alb_in * 658
          
          nimage = FINDGEN(n)
          image_name_VMC = STRARR(n)
 
          Openr , file_unit , name

ref_4:    Readf , file_unit , dump

          If dump NE 'C_END' Then Goto, ref_4

          Readf , file_unit , lat_sound , lon_sound , T_sound_d , T_sound_h , T_sound_m


          For i = 0,n-1 Do begin

           Readf, file_unit, dump
           image_name_VMC(i) = STRCOMPRESS(dump)

         Endfor

         Close, file_unit
         
         Free_lun , file_unit


;----------------------------------------------------------------------------------
;----------Selection of the image and decision of what to keep and what not to keep

         imagekeep = INTARR(n)
         imagekeep = 0
 
      
         i = 0

ref_5:   nameGEO = image_name_VMC(i) + '.GEO'
         nameIMG = image_name_VMC(i) + '.IMG'
         namePNG = image_name_VMC(i) + '.png'


;---------Read the IMG file------------------------------------------------

         VMCimage = READPDS(nameIMG, /silent)
         VMC = VMCimage.image

;---------Read the header of the image to get to the Radiance Scaling Factor RSF--------------

           head = HEADPDS(nameIMG,/silent)
           j = -1
ref_rhead: j = j + 1
           head_head = STRMID(head(j),0,23)
           If head_head EQ 'RADIANCE_SCALING_FACTOR' Then Goto,ref_head
           Goto,ref_rhead

ref_head:  RSF_string = head(j)
           RSF_in = STRMID(RSF_string,35,8)
           Reads,RSF_in,RSF

;---------The correct units for RSF are  W/m2/micron/ster

           RSF = RSF / 1000000.
           
           print,'RSF ',RSF

;---------Read data from the GEO qubes-------------------------------------------

         Get_lun , geo_file

         Openr, geo_file , nameGEO

         recblock = BYTARR(2048, 8)
         Readu, geo_file , recblock
           
         geocube = FLTARR(512,512,5)
         Readu, geo_file , geocube

         Close, geo_file

         Free_lun , geo_file

         Byteorder, geocube,/xdrtof

         geocube = REVERSE(geocube, 2)

;----------Incidence Angle--------------------------------------------------------

         ia = geocube(*,*,0)


;----------Emission Angle---------------------------------------------------------

         ea = geocube(*,*,1)


;----------Phase Angle------------------------------------------------------------

         pa = geocube(*,*,2)


;---------Coordinates-------------------------------------------------------------

         latitude = geocube(*,*,3)
         longitude = geocube(*,*,4)
         
         lon360 = WHERE(longitude GE -180 AND longitude LT 0)
         longitude(lon360) = longitude(lon360) + 360

;---------Image time---------------------------------------------------------------

          VMClabel = Headpds(nameGEO,/silent)
          VMCtime = Timepds(VMClabel,/doy)
;           print,'T_sound_d,T_sound_h,T_sound_m',T_sound_d,T_sound_h,T_sound_m
;           print,'VMCtime',VMCtime
          VMChour = (VMCtime - FIX(VMCtime)) * 24.
          VMCminute = (VMChour - FIX(VMChour)) * 60.
          VMChour = FIX(VMChour)
          VMCminute = FIX(VMCminute)
          VMCtimestring = STRCOMPRESS(STRING(VMChour)) + 'h:' + STRCOMPRESS(STRING(VMCminute)) + 'm:'




         VMCphotometry,VMC,ia,ea,pa,latitude,longitude,RSF,pa_dump,VMCalb

         longitude(lon360) = longitude(lon360) - 360

;         vmcvalid = WHERE(longitude GE 0 AND longitude LE 360)
         vmcvalid = WHERE(longitude GE -180 AND longitude LE 180)

         VMCalbvalid = VMCalb(vmcvalid)
         latvalid = latitude(vmcvalid)
         lonvalid = longitude(vmcvalid)

         Triangulate,lonvalid,latvalid,tri,fvalue=VMCalbvalid

         VMCtrigrid = TRIGRID(lonvalid,latvalid,VMCalbvalid,tri,$
           [1.0,1.0],xgrid=x,ygrid=y)

         VMCtrigrid = VMCtrigrid * ( 1 + ( VMCtrigrid - min(VMCtrigrid) ) * ( 2. - 1. ) / ( max(VMCtrigrid) - min(VMCtrigrid) ) ) 

         contour_levels = 0.02 + ( (2. - 0.02) / 100 ) * FINDGEN(100)



;----------plot the albedo against the image number, the square is the image currently shown--------------------------------------------

         Wset , 0
         Erase

         !p.multi=[0,2,1]

;----------To plot the B/mu0 against the image-number

         Plot,[-1,n+1],xs=1,[0,1700],ys=1,/NODATA,$
           xtitle='image number',ytitle='B/mu0'
         Plots,nimage(i),albedo_nowind(i),psym=6
         Errplot,nimage(i),albedo_nowind(i) - dalbedo_nowind(i),albedo_nowind(i) + dalbedo_nowind(i)

 

         If i EQ 0 Then Begin
          
          Oplot,nimage(1:n-1),albedo_nowind(1:n-1),psym=1
          Errplot,nimage(1:n-1),albedo_nowind(1:n-1) - dalbedo_nowind(1:n-1),albedo_nowind(1:n-1) + dalbedo_nowind(1:n-1)  
 
         Endif

         If i GT 0 AND i LT n-1 Then Begin

          OPlot,nimage(0:i-1),albedo_nowind(0:i-1),psym=1
          Errplot,nimage(0:i-1),albedo_nowind(0:i-1) - dalbedo_nowind(0:i-1),albedo_nowind(0:i-1) + dalbedo_nowind(0:i-1)

          Oplot,nimage(i+1:n-1),albedo_nowind(i+1:n-1),psym=1
          Errplot,nimage(i+1:n-1),albedo_nowind(i+1:n-1) - dalbedo_nowind(i+1:n-1),albedo_nowind(i+1:n-1) + dalbedo_nowind(i+1:n-1)
 
         Endif
         
        If i EQ n-1 Then Begin
          
          Oplot,nimage(0:n-2),albedo_nowind(0:n-2),psym=1
          Errplot,nimage(0:n-2),albedo_nowind(0:n-2) - dalbedo_nowind(0:n-2),albedo_nowind(0:n-2) + dalbedo_nowind(0:n-2) 

        Endif


;----------Plot extra in case of wind information

        If windfile NE 'NO_WIND_INFO' Then Begin
 
          Plots,nimage(i),albedo_wind(i),psym=5
          Errplot,nimage(i),albedo_wind(i) - dalbedo_wind(i),albedo_wind(i) + dalbedo_wind(i)

          If i EQ 0 Then Begin
                        
            Oplot,nimage(1:n-1),albedo_wind(1:n-1),psym=7
            Errplot,nimage(1:n-1),albedo_wind(1:n-1) - dalbedo_wind(1:n-1),albedo_wind(1:n-1) + dalbedo_wind(1:n-1)

          Endif

          If i GT 0 AND i LT n-1 Then Begin

            OPlot,nimage(0:i-1),albedo_wind(0:i-1),psym=7
            Errplot,nimage(0:i-1),albedo_wind(0:i-1) - dalbedo_wind(0:i-1),albedo_wind(0:i-1) + dalbedo_wind(0:i-1)
            
            Oplot,nimage(i+1:n-1),albedo_wind(i+1:n-1),psym=7
            Errplot,nimage(i+1:n-1),albedo_wind(i+1:n-1) - dalbedo_wind(i+1:n-1),albedo_wind(i+1:n-1) + dalbedo_wind(i+1:n-1)

          Endif

          If i EQ n-1 Then Begin
                        
            Oplot,nimage(0:n-2),albedo_wind(0:n-2),psym=7
            Errplot,nimage(0:n-2),albedo_wind(0:n-2) - dalbedo_wind(0:n-2),albedo_wind(0:n-2) + dalbedo_wind(0:n-2)

          Endif

        Endif

;----------END plot extra


;----------To plot the albedo against the phase angle of the image

         Plot,[20,140],xs=1,[0,1700],ys=1,/NODATA,$
           xtitle='phase angle (degrees)',ytitle='B/mu0'

         Plots,pa_in,alb_in,psym=3

         Plots,pa_average(i),albedo_nowind(i),psym=6
         Errplot,pa_average(i),albedo_nowind(i) - dalbedo_nowind(i),albedo_nowind(i) + dalbedo_nowind(i)

         If i EQ 0 Then Begin
                    
          Oplot,pa_average(1:n-1),albedo_nowind(1:n-1),psym=1
          Errplot,pa_average(1:n-1),albedo_nowind(1:n-1) - dalbedo_nowind(1:n-1),albedo_nowind(1:n-1) + dalbedo_nowind(1:n-1) 

         Endif

         If i GT 0 AND i LT n-1 Then Begin

          OPlot,pa_average(0:i-1),albedo_nowind(0:i-1),psym=1
          Errplot,pa_average(0:i-1),albedo_nowind(0:i-1) - dalbedo_nowind(0:i-1),albedo_nowind(0:i-1) + dalbedo_nowind(0:i-1)

          Oplot,pa_average(i+1:n-1),albedo_nowind(i+1:n-1),psym=1
          Errplot,pa_average(i+1:n-1),albedo_nowind(i+1:n-1) - dalbedo_nowind(i+1:n-1),albedo_nowind(i+1:n-1) + dalbedo_nowind(i+1:n-1)

         Endif

         If i EQ n-1 Then Begin
                    
          Oplot,pa_average(0:n-2),albedo_nowind(0:n-2),psym=1
          Errplot,pa_average(0:n-2),albedo_nowind(0:n-2) - dalbedo_nowind(0:n-2),albedo_nowind(0:n-2) + dalbedo_nowind(0:n-2)

         Endif


;----------Plot extra in case of wind information

         If windfile NE 'NO_WIND_INFO' Then Begin

           Plots,pa_average(i),albedo_wind(i),psym=5
           Errplot,pa_average(i),albedo_wind(i) - dalbedo_wind(i),albedo_wind(i) + dalbedo_wind(i)

           If i EQ 0 Then Begin
            
            Oplot,pa_average(1:n-1),albedo_wind(1:n-1),psym=7
            Errplot,pa_average(1:n-1),albedo_wind(1:n-1) - dalbedo_wind(1:n-1),albedo_wind(1:n-1) + dalbedo_wind(1:n-1) 

           Endif

           If i GT 0 AND i LT n-1 Then Begin

             OPlot,pa_average(0:i-1),albedo_wind(0:i-1),psym=7
             Errplot,pa_average(0:i-1),albedo_wind(0:i-1) - dalbedo_wind(0:i-1),albedo_wind(0:i-1) + dalbedo_wind(0:i-1)

             Oplot,pa_average(i+1:n-1),albedo_wind(i+1:n-1),psym=7
             Errplot,pa_average(i+1:n-1),albedo_wind(i+1:n-1) - dalbedo_wind(i+1:n-1),albedo_wind(i+1:n-1) + dalbedo_wind(i+1:n-1)

           Endif

           If i EQ n-1 Then begin
            
            Oplot,pa_average(0:n-2),albedo_wind(0:n-2),psym=7
            Errplot,pa_average(0:n-2),albedo_wind(0:n-2) - dalbedo_wind(0:n-2),albedo_wind(0:n-2) + dalbedo_wind(0:n-2)

           Endif

         Endif
         
;----------END plot extra

;         xyouts,10,1,'phase angle=' + STRCOMPRESS(FIX(pa_average(i)+0.5)) + ' +/-' + STRCOMPRESS(pa_stddev(i))
         
         !p.multi=0

;----------plot the orthographic map of the image


         Wset , 1
         Erase
         loadct,0

           ;         Map_set, -53., 63, /cylindrical, /isotropic, /grid, /advance, limit=[plothigh_lat,plotlow_lon,plotlow_lat,plothigh_lon], $
           ;           title = string(nameIMG,VMCtimestring),charsize=2.
         Map_set, lat_site_nowind(i), lon_site_nowind(i), /orthographic, /isotropic, /grid, /advance, $
           title = string(nameIMG),charsize=1



         Contour, VMCtrigrid, x, y, /fill, level = contour_levels, /overplot

         Map_set, lat_site_nowind(i), lon_site_nowind(i), /orthographic, /isotropic, /grid, /advance


;---------a square for the predicted site

         plots , lon_site_nowind(i) , lat_site_nowind(i) , psym = 6

         If windfile NE 'NO_WIND_INFO' Then plots , lon_site_wind(i) , lat_site_wind(i) , psym = 5


;---------a diamond for the sounded site

         plots , lon_sound , lat_sound , psym = 4


;----------plot the image

         Wset , 2
         TVSCL,VMCalb


;         plots , lon_site(i) , lat_site(i) , psym = 6
;         plots , lon_sound , lat_sound , psym = 2


         Print,nameIMG + ':'
         Print,'lon,lat,alb: ',lon_site_nowind(i),lat_site_nowind(i),albedo_nowind(i)
         Print,'Time and deltaT',VMCtimestring,deltaT(i)

ref_6:   Read , moveon , prompt = 'Image Number : Stop = -1  '

         If moveon EQ -1 Then Goto,ref_7

         If moveon GT n-1 OR moveon LT -1 Then Goto,ref_6
         
         i = moveon
         Goto,ref_5

ref_7:    Wdelete , 0
          Wdelete , 1
          Wdelete , 2
 
         
         End
          