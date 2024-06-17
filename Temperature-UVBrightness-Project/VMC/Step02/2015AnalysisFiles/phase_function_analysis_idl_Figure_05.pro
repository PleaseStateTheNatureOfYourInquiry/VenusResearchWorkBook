; Making the Figure 5 in the paper, the Phase dependance of B0

readtable,'phase_file_SELECTED_ia_ea_20151028',table,5
;readtable,'phase_file_SELECTED',table,5
;readtable,'phase_file_ALL',table,5
;readtable,'phase_file_ALL_no_0955',table,5


orbit_in = table(*,0)
pa_in = table(*,1)
alb_in = table(*,3)
d_alb_in = table(*,4)

factor = 3.141592 * (0.723 * 0.723) / 1081
;plot,pa_in,alb_in/factor,psym=1
;oplot,pa_in(orb_notext4),alb_in(orb_notext4),psym=3

pa_valid = WHERE(pa_in LT 140)

pa = pa_in(pa_valid)
alb = alb_in(pa_valid)
d_alb = d_alb_in(pa_valid)

fit = POLY_FIT(pa,alb/factor,2)
;fit = POLY_FIT(pa,alb/factor,2,MEASURE_ERRORS=d_alb,SIGMA=sigma)

x=25+FINDGEN(115)
y=fit(2)*x*x + fit(1)*x + fit(0)


Set_plot,'ps'
Device,filename='Figure_05 phase_function_SELECTED_20151028.ps',/landscape

functionstring = 'B!I0!N = 0.15 a!E2!N +' + ' 20.2 a + 1029'

 
plot,pa_in(pa_valid),alb_in(pa_valid)/factor,psym=1,xthick=5,ythick=5,$
xrange=[0,160],xs=1,yrange=[0,1700],ys=1,$
xtitle='Phase Angle a (!Eo!N)',ytitle='B!I0!N (W/m!E2!N/ster/micron)',$
title='Lambert only correction  '+ functionstring,xcharsize=1.25,ycharsize=1.25,charthick=2
oplot,x,y,lines=0,thick=3

Device,/close


;Device,filename='phase_function_NOMINAL.ps',/landscape

;orbit = WHERE(orbit_in LE 547)

;functionstring = $
;STRCOMPRESS(STRING(fit(2))) + ' alpha^2 +' + $
;STRCOMPRESS(STRING(fit(1))) + ' alpha +' + $
;STRCOMPRESS(STRING(fit(0)))

;plot,pa_in(orbit),alb_in(orbit)/factor,psym=1,$
;xrange=[0,160],xs=1,yrange=[0,1700],ys=1,$
;xtitle='phase angle',ytitle='B/mu0 (W/m2/ster/micron)',$
;title='NOMINAL: Lambert only'+ functionstring
;oplot,x,y,lines=0

;Device,/close

;Device,filename='phase_function_EXT1.ps',/landscape

;orbit = WHERE(orbit_in GT 547 AND orbit_in LE 1135)

;functionstring = $
;STRCOMPRESS(STRING(fit(2))) + ' alpha^2 +' + $
;STRCOMPRESS(STRING(fit(1))) + ' alpha +' + $
;STRCOMPRESS(STRING(fit(0)))

;plot,pa_in(orbit),alb_in(orbit)/factor,psym=1,$
;xrange=[0,160],xs=1,yrange=[0,1700],ys=1,$
;xtitle='phase angle',ytitle='B/mu0 (W/m2/ster/micron)',$
;title='EXT1: Lambert only'+ functionstring
;oplot,x,y,lines=0

;Device,/close


;Device,filename='phase_function_EXT2.ps',/landscape

;orbit = WHERE(orbit_in GT 1136 AND orbit_in LE 1583)

;functionstring = $
;STRCOMPRESS(STRING(fit(2))) + ' alpha^2 +' + $
;STRCOMPRESS(STRING(fit(1))) + ' alpha +' + $
;STRCOMPRESS(STRING(fit(0)))

;plot,pa_in(orbit),alb_in(orbit)/factor,psym=1,$
;xrange=[0,160],xs=1,yrange=[0,1700],ys=1,$
;xtitle='phase angle',ytitle='B/mu0 (W/m2/ster/micron)',$
;title='EXT2: Lambert only'+ functionstring
;oplot,x,y,lines=0

;Device,/close


;Device,filename='phase_function_EXT3.ps',/landscape

;orbit = WHERE(orbit_in GT 1583 AND orbit_in LE 2451)

;functionstring = $
;STRCOMPRESS(STRING(fit(2))) + ' alpha^2 +' + $
;STRCOMPRESS(STRING(fit(1))) + ' alpha +' + $
;STRCOMPRESS(STRING(fit(0)))

;plot,pa_in(orbit),alb_in(orbit)/factor,psym=1,$
;xrange=[0,160],xs=1,yrange=[0,1700],ys=1,$
;xtitle='phase angle',ytitle='B/mu0 (W/m2/ster/micron)',$
;title='EXT3: Lambert only'+ functionstring
;oplot,x,y,lines=0

;Device,/close


;Device,filename='phase_function_EXT4.ps',/landscape

;orbit = WHERE(orbit_in GT 2451)

;functionstring = $
;STRCOMPRESS(STRING(fit(2))) + ' alpha^2 +' + $
;STRCOMPRESS(STRING(fit(1))) + ' alpha +' + $
;STRCOMPRESS(STRING(fit(0)))

;plot,pa_in(orbit),alb_in(orbit)/factor,psym=1,$
;xrange=[0,160],xs=1,yrange=[0,1700],ys=1,$
;xtitle='phase angle',ytitle='B/mu0 (W/m2/ster/micron)',$
;title='EXT4: Lambert only'+ functionstring
;oplot,x,y,lines=0

;Device,/close




Set_plot,'x'
