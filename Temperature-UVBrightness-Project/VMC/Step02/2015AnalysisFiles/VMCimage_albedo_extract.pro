Pro VMCimage_albedo_extract,image_name,dlat,dlon,lat_sound,lon_sound,T_sound_d,T_sound_h,T_sound_m,windfile,pa_average_in,lat_site,lon_site,deltaT,albedo,ia_average,ea_average


;---------extract the value of the albedo of the sounded location at the time of the image in a box of dlat - dlon (degrees) around that position
;---------T_sound_h and _m is the sounding time in hours and in minutes. I assume that the sounding and the image are taken on the same Day of Year!!!
        
;---------the image file names .IMG and .GEO----------------------------------------

           nameGEO = image_name + '.GEO'
           nameIMG = image_name + '.IMG'
;           namePNG = image_name + '.png'
           
          

;----------determine the time of the image in HH:MM:SS----------------------
;----------VMCtime is the time expressed in "Day of Year (DOY)"---------------------------


           VMClabel = Headpds(nameGEO,/silent)
           VMCtime = Timepds(VMClabel,/doy)
;           print,'T_sound_d,T_sound_h,T_sound_m',T_sound_d,T_sound_h,T_sound_m
;           print,'VMCtime',VMCtime
           VMChour = (VMCtime - FIX(VMCtime)) * 24.
           
           deltaT = VMCtime - ( T_sound_d + T_sound_h / 24. + ( T_sound_m / 60. / 24. ) )
           deltaT = deltaT * 24
           
           VMCminute = (VMChour - FIX(VMChour)) * 60.
           VMChour = FIX(VMChour)
           VMCminute = FIX(VMCminute)
           VMCtimestring = STRCOMPRESS(STRING(VMChour)) + 'h:' + STRCOMPRESS(STRING(VMCminute)) + 'm:'
          
 
;---------Read the image from the IMG file------------------------------------------------
 
          VMCimage = READPDS(nameIMG, /silent)
          VMC = VMCimage.image

;---------Read the header of the image to get to the Radiance Scaling Factor RSF--------------

          head = HEADPDS(nameIMG,/silent)          
           i = -1
ref_rhead: i = i + 1
           head_head = STRMID(head(i),0,23)
           If head_head EQ 'RADIANCE_SCALING_FACTOR' Then Goto,ref_head
           Goto,ref_rhead

ref_head:  RSF_string = head(i)
           RSF_in = STRMID(RSF_string,35,8)
           Reads,RSF_in,RSF

;---------The correct units for RSF are  W/m2/micron/ster 

          RSF = RSF / 1000000.


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
 
            
;----------Makes geocube be read in correct direction-----------------------------

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

          
       
          VMCphotometry,VMC,ia,ea,pa,latitude,longitude,RSF,pa_average_in,VMCalb,ia_average,ea_average


;----------See notes of 19-03-2015
;----------the average zonal wind is from Khatuntsev (2013) Fig. 10a and can be parametrized as:

;---------    I.  U(lat) =  -94   + (lat+50) * (65.6/-25)  m/s   for  lat <= -50
;---------   II.  U(lat) = -101.5 + (lat+40) * (7.5/-10)   m/s   for  -40 >= lat > -50 
;---------  III.  U(lat) =  -93   + (lat+15) * (-8.5/-35)  m/s   for  -15 >= lat > -40
;---------   IV.  U(lat) =  -93  m/s  for  lat > -15

;----------the factor 0.0037 is to convert meters to degrees longitude ( 60*60*180/pi/6123000 , with 6123000 the radius of Venus in meters
;----------and deltaT hours), where  deltaT  is the time difference between the image and the sounding in hours


;----------dlon and dlat are the box sizes over which the average is being taken

;----------30-04-2015: instead of dlon and dlat, we are going to take the uncertainties in the wind profiles to calculate dlon and dlat. 
;----------from Khatunstev (2013) section 4.1.1 the sigma in zonal wind is +/- 30m/s, for the meriodinal wind it is +/- 12.5 m/s

;           print,image_name

           If lat_sound LE -50 Then Begin

            lon_site = lon_sound + 0.0337 * ( deltaT * ( -94 - (lat_sound + 50) * (65.6/25) ) ) / COS(3.141592 * lat_sound / 180)
            lon_site_up = lon_sound + 0.0337 * ( deltaT * ( ( -94 - (lat_sound + 50) * (65.6/25) ) + 30 ) ) / COS(3.141592 * lat_sound / 180)
            lon_site_down = lon_sound + 0.0337 * ( deltaT * ( ( -94 - (lat_sound + 50) * (65.6/25) ) - 30 ) ) / COS(3.141592 * lat_sound / 180)

           Endif

           If lat_sound LE -40 AND lat_sound GT -50 Then Begin

            lon_site = lon_sound + 0.0337 * ( deltaT * ( -101.5 - (lat_sound + 40) * (7.5/10) ) ) / COS(3.141592 * lat_sound / 180)
            lon_site_up = lon_sound + 0.0337 * ( deltaT * ( ( -101.5 - (lat_sound + 40) * (7.5/10) ) + 30 ) ) / COS(3.141592 * lat_sound / 180)
            lon_site_down = lon_sound + 0.0337 * ( deltaT * ( ( -101.5 - (lat_sound + 40) * (7.5/10) ) - 30 ) ) / COS(3.141592 * lat_sound / 180)

           Endif

           If lat_sound LE -15 AND lat_sound GT -40 Then Begin

            lon_site = lon_sound + 0.0337 * ( deltaT * ( -93 + (lat_sound + 15) * (8.5/35) ) ) / COS(3.141592 * lat_sound / 180)
            lon_site_up = lon_sound + 0.0337 * ( deltaT * ( ( -93 + (lat_sound + 15) * (8.5/35) ) + 30 ) ) / COS(3.141592 * lat_sound / 180)
            lon_site_down = lon_sound + 0.0337 * ( deltaT * ( ( -93 + (lat_sound + 15) * (8.5/35) ) - 30 ) ) / COS(3.141592 * lat_sound / 180)

           Endif

           If lat_sound GT -15 Then Begin

            lon_site = lon_sound - 0.0337 * ( deltaT * 93 ) / COS(3.141592 * lat_sound / 180)
            lon_site_up = lon_sound - 0.0337 * ( deltaT *  63 ) / COS(3.141592 * lat_sound / 180)
            lon_site_down = lon_sound - 0.0337 * ( deltaT * 123 ) / COS(3.141592 * lat_sound / 180)

           Endif


;----------See notes of 23-04-2015
;----------the average meridional wind is from Khatuntsev (2013) Fig. 10b and can be parametrized as  V(lat) = -10 - (lat+50) * 9 / 25 (m/s).
;----------same conversion factor applies as for the zonal wind: 0.0337 

;---------    I.  V(lat) =  0   m/s   for  lat <= -75
;---------   II.  V(lat) = -9.58 + (lat+50) * (9.38/-25)   m/s   for  -50 >= lat > -75 
;---------  III.  V(lat) = -6.5  + (lat+20) * (-3.08/-30)  m/s   for  -20 >= lat > -50
;---------   IV.  V(lat) = -3.26 + (lat+0)  * (-3.24/-20)  m/s   for  0 >= lat > -20

           If lat_sound LE -75 Then Begin

            lat_site = lat_sound
            lat_site_up = lat_sound + 0.0337 * ( deltaT * 12.5 )
            lat_site_down = lat_sound - 0.0337 * ( deltaT * 12.5 )

           Endif

           If lat_sound LE -50 AND lat_sound GT -75 Then Begin

            lat_site = lat_sound + 0.0337 * ( deltaT * ( -9.58 - (lat_sound + 50) * (9.38/25) ) )
            lat_site_up = lat_sound + 0.0337 * ( deltaT * ( ( -9.58 - (lat_sound + 50) * (9.38/25) ) + 12.5 ) )
            lat_site_down = lat_sound + 0.0337 * ( deltaT * ( ( -9.58 - (lat_sound + 50) * (9.38/25) ) - 12.5 ) )

           Endif

           If lat_sound LE -20 AND lat_sound GT -50 Then Begin

            lat_site = lat_sound + 0.0337 * ( deltaT * ( -6.5 + (lat_sound + 20) * (3.08/30) ) )
            lat_site_up = lat_sound + 0.0337 * ( deltaT * ( ( -6.5 + (lat_sound + 20) * (3.08/30) ) + 12.5 ) )
            lat_site_down = lat_sound + 0.0337 * ( deltaT * ( ( -6.5 + (lat_sound + 20) * (3.08/30) ) - 12.5 ) )

           Endif

           If lat_sound GT -20 Then Begin

            lat_site = lat_sound + 0.0337 * ( deltaT * ( -3.26 + (lat_sound) * (3.24/20) ) )
            lat_site_up = lat_sound + 0.0337 * ( deltaT * ( ( -3.26 + (lat_sound) * (3.24/20) ) + 12.5 ) )
            lat_site_down = lat_sound + 0.0337 * ( deltaT * ( ( -3.26 + (lat_sound) * (3.24/20) ) - 12.5 ) )

           Endif



;           print,'average longitude',lon_site
;           print,'average latitude',lat_site
           
 

;-----------If a wind file is specified, then use the wind profile data in this file: first determine the site location ausing the average
;-----------wind from the two lines before. Next search the wind profile file for wind vectors between this estimated location and the
;-----------sounded location. If there is none or just one, then use the old location. If there is more than one, then average over these
;-----------wind values and re-determine the site location

           If windfile NE 'NO_WIND_INFO' Then Begin
            
            Readtable,windfile,wind,9

; Longitude
            windlon = wind(*,4)

; Latitude
            windlat = wind(*,5)

; Zonal wind
            windzon = wind(*,7)

; Meridional wind
            windmer = wind(*,8)


;----------Define a box in longitude that spans the distance between the sounded location and the average site location based 
;----------on the average wind. In that box, take the measured winds and average them. Now use this new wind to determine the new 
;----------site location. Since the latitude range defined by the meridional wind is always small, I take the maximum range of that
;----------defined by the incertainties in the meridional winds (lat_site_up and lat_site_down)

            windbox_centre_lon = lon_site + 0.5 * (lon_sound - lon_site)
            windbox_width_lon = 0.5 * ABS(lon_site - lon_sound)

            windbox_centre_lat = lat_site + 0.5 * (lat_sound - lat_site)
;            windbox_width_lat = 0.5 * ABS(lat_site - lat_sound)
            windbox_width_lat = ABS(lat_site_up - lat_site_down)
           

;----------Instead of an average of the trajectory from sounded location to site, do a box of +/- 10 drg longitude and +/- 5 drg longitude
;----------around site.

;            windbox_centre_lon = lon_site   
;            windbox_width_lon = 10
;            windbox_centre_lat = lat_site
;            windbox_width_lat = 5


;            print,'lon centre and width',windbox_centre_lon,windbox_width_lon
;            print,'lat centre and width',windbox_centre_lat,windbox_width_lat
            
            windbox = WHERE( windlon GE (windbox_centre_lon - windbox_width_lon) AND $
                             windlon LE (windbox_centre_lon + windbox_width_lon) AND $ 
                             windlat GE (windbox_centre_lat - windbox_width_lat) AND $
                             windlat LE (windbox_centre_lat + windbox_width_lat) $
                           )

            windbox_size = SIZE(windbox)


;            print,'number of point',windbox_size
;            help,windbox
;            print,windbox,windlon(windbox),windlat(windbox)            

;------------At least 5 wind vectors need to be in the box to take this into account

            If windbox_size(0) GT 0 AND windbox_size(1) GT 5 Then Begin
                           
             windzon_in_box = MOMENT(windzon(windbox))
             windmer_in_box = MOMENT(windmer(windbox))


;             print,'________________________________'
;             print,'image',image_name
;             print,'deltaT',deltaT

;             print,'average site lon',lon_site,lon_site_up,lon_site_down 
;             print,'average site lat',lat_site,lat_site_up,lat_site_down

;             print,'winds in box',windzon_in_box(0),SQRT(windzon_in_box(1)),windmer_in_box(0),SQRT(windmer_in_box(1))
;             print,'number of points',windbox_size(1)
;             print,''
;             print,'windzon in box',windzon(windbox)

             lon_site_wind = lon_sound + 0.0337 * ( deltaT * windzon_in_box(0) )  / COS(3.141592 * lat_sound / 180)
             lon_site_wind_up = lon_sound + 0.0337 * ( deltaT * (windzon_in_box(0) + SQRT(windzon_in_box(1))) )  / COS(3.141592 * lat_sound / 180)
             lon_site_wind_down = lon_sound + 0.0337 * ( deltaT * (windzon_in_box(0) - SQRT(windzon_in_box(1))) )  / COS(3.141592 * lat_sound / 180)

             lat_site_wind = lat_sound + 0.0337 * ( deltaT * windmer_in_box(0) )
             lat_site_wind_up = lat_sound + 0.0337 * ( deltaT * (windmer_in_box(0) + SQRT(windmer_in_box(1))) )
             lat_site_wind_down = lat_sound + 0.0337 * ( deltaT * (windmer_in_box(0) - SQRT(windmer_in_box(1))) )
             
;             print,'real site lon',lon_site_wind,lon_site_wind_up,lon_site_wind_down
;             print,'real site lat',lat_site_wind,lat_site_wind_up,lat_site_wind_down


;----------30-04-2015: when there are wind measurement, I decide to take these over the average wind. The differences are not huge
;
             lon_site = lon_site_wind
             lon_site_up = lon_site_wind_up
             lon_site_down = lon_site_wind_down
             
             lat_site = lat_site_wind
             lat_site_up = lat_site_wind_up
             lat_site_down = lat_site_wind_down
;
;             print,'zonal', -95 - (lat_sound + 48) * 2.2 , windzon_in_box(0)
;             print,'meridional', -10 - (lat_sound + 50) * 9 / 25 , windmer_in_box(0)
                          
            Endif

;            print,'wind longitude',lon_site
;            print,'wind latitude',lat_site
            
           Endif

;           print,''
;           print,'____________________________________'
;           print,''
           

           dlon = ABS(lon_site_up - lon_site_down) / 2
           dlat = ABS(lat_site_up - lat_site_down) / 2

           If lon_site GE 360 Then lon_site = lon_site - 360


;----------check the box's valid lons and lats and then only take into account those points that have a positive albedo value!

           site_box = WHERE( longitude GE (lon_site - dlon) and longitude LE (lon_site + dlon) $
             and latitude GE (lat_site - dlat) and latitude LE (lat_site + dlat) )

           VMCalb_site_box = VMCalb(site_box)
           VMCalb_valid = WHERE(VMCalb_site_box GT 0)

           n_site_box = SIZE(site_box)
           n_valid = SIZE(VMCalb_valid)

           If n_valid(1) GT 1 AND (n_valid(1) / n_site_box(1)) EQ 1 Then Begin
            
            albedo = MOMENT(VMCalb_site_box(VMCalb_valid))
            
           Endif Else Begin
            
            albedo = FLTARR(4)
            albedo(*) = 0.
            
           Endelse
            
        End
