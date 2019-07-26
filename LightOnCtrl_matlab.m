% Initalize Hardware
pkg load instrument-control
ser = serial('COM1', 57600);
fopen(ser);

% Send Command
%fprintf(ser,'&ALL_0100_S#'); % All open
%fprintf(ser,'&ALL_0000_S#'); % All close
srl_write(ser,'&ALL_0000_S#'); %ALL close
 

% Close serial port
%fclose(ser);


