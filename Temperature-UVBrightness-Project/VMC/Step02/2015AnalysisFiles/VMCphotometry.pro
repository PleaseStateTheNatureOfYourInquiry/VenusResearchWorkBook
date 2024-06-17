Pro VMCphotometry,VMCobs,ia,ea,pa,lat,lon,RSF,pa_average_in,VMCalb,ia_average_in,ea_average_in

    pi = 3.141592
    ia_rad = ia * pi / 180
    ea_rad = ea * pi / 180

    VMCalb = FLTARR(512,512)

    lon360 = WHERE(lon GE -180 AND lon LT 0)
    lon(lon360) = lon(lon360) + 360

    vmcvalid = WHERE(lon GE 0 AND lon LE 360 AND ia LE 89)
    vmcinvalid = WHERE(lon LT 0 OR lon GT 360 OR ia GT 89)

        
    pa_average_in = MOMENT(pa(vmcvalid))
    pa_average = pa_average_in(0)

    ia_average_in = MOMENT(ia(vmcvalid))
    ia_average = ia_average_in(0)

    ea_average_in = MOMENT(ea(vmcvalid))
    ea_average = ea_average_in(0)


;    print,pa_average

;---------This is Equation (2) from Lee et al.: 0.723 is the distance Venus-Sun in AU, 1081 is the solar irradiation in the VMC UV filter 
;---------at Earth's distance in W/m2/micron (Equation (1) in Lee et al.) I determined this using VMCUVsun.pro 
;---------0.077381 is the correction factor that has to be applied to the image cube numbers. This INCLUDES the beta from Eq. (2) for the data from
;---------EXT4 (orbit number 2452 and higher), but NOT for the other orbits!!!
    
;--------include the Radiance Scaling Factor RSF in the right units (W/m2/ster/micron)
;    
    
    VMCalb(vmcinvalid) = 0
    VMCalb(vmcvalid) = RSF * VMCobs(vmcvalid) * pi * (0.723 * 0.723) / 1081 


;---------29 april 2015: we are going to use the Lambertian law only

     VMCalb(vmcvalid) = VMCalb(vmcvalid) / COS(ia_rad(vmcvalid))  


;---------This is the "best" law as determined by Lee et al.: Lambert and Lommel-Seeliger law Eq. (7) with k_LLS(alpha) Eq. (11)
;---------In fact, the dependance on the phase angle alpha is small.

;    If (pa_average LE 90) Then Begin

;     VMCalb(vmcvalid) = VMCalb(vmcvalid) / COS(ia_rad(vmcvalid))     

;    Endif
  
    
;    If (pa_average GT 90) Then Begin
    
;     k_LLS = 0.0077956 * (pa_average - 90)
;     VMCalb(vmcvalid) = VMCalb(vmcvalid) / $
;                        (  k_LLS * 2 * COS(ia_rad(vmcvalid)) / ( COS(ia_rad(vmcvalid)) + COS(ea_rad(vmcvalid)) ) $
;                           + ( 1 - k_LLS ) * COS(ia_rad(vmcvalid))  )
  
;    Endif    



;----------some checking with Lee's paper, reproducing some of the figures

;    print,MAX(VMCalb(vmcvalid)),MIN(VMCalb(vmcvalid)),MEAN(VMCalb(vmcvalid))
;    mu0 = COS(ia_rad)
;    mu = COS(ea_rad)
;    mu1 = COS( 0.5 * (ia_rad + ea_rad) )
;    mu2 = COS( 0.5 * (ia_rad - ea_rad) )
;    mu12 = mu1*mu2

;----------similar to the fig. 3(b) in Lee's paper, units in Obs are x10.000 though.

;    plot,VMCobs(vmcvalid),mu0(vmcvalid),psym=1

;----------similar to the fig. 3(a) in Lee's paper!

;    plot,ALOG(mu(vmcvalid)*mu0(vmcvalid)),ALOG(mu(vmcvalid)*VMCalb(vmcvalid) * mu0(vmcvalid)),psym=2

;    plot,mu0(vmcvalid),VMCalb(vmcvalid),psym=3
    
;----------similar to Lee's fig. 4(a) IF beta correction factor = 1

;    plot,(1 - mu12(vmcvalid))/mu12(vmcvalid),VMCalb(vmcvalid),psym=3,xrange=[0,8],xs=1,yrange=[0,1.4],ys=1
    
End
