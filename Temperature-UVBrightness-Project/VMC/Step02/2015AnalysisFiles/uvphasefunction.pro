FUNCTION UVPHASEFUNCTION , phase_angle , Br

;---------South Polar campaign only

; Br_model = Br * ( 0.148 * phase_angle * phase_angle - 19.46 * phase_angle + 1076 )


;---------ALL

   Br_model = Br * ( 0.148 * phase_angle * phase_angle - 19.46 * phase_angle + 988 )

 Return,Br_model

End
