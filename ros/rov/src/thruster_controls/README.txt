Welcome to thruster_controls.


This package processes input from the surface. This does any necessary thrust vectoring.


Nodes:
  * thruster_controls:
      subs: surface_command, current_sense, thruster_proc
      pubs: control_tx 
   
