%==================Control Arudino Shutter with Matlab====================%
% Usage:
%   1. Initialize serial port device: baudrate, 57600
%   2. Send command to serial port to contro shutter:
%       fprintf(serial_object, '%s', '1')  % open shutter
%       fprintf(serial_object, '%s', '0')  % close shutter        
%   3. Close and release serial object
% 
% Ver 0.1 20190905 by H.F
%=========================================================================%


% ser_st = serial('/dev/ttyACM0', 'BaudRate', 57600);
% fopen(ser_st);
% 
fprintf(ser_st, '%s', '1'); % open shutter
fprintf(ser_st, '%s', '0'); % close shutter
% fprintf 的默认格式为 %s\n, �?��将终止符配置为空 �?
% for i = 1:100
%     fprintf(ser_st, '%s', '1');
%     pause(1);s
%     fprintf(ser_st, '%s', '0');
%     pause(1);
% end

t_last = clock;

on = 0.1; % min
off = 0.1; % min

for i = [1:3]
        
    fprintf(ser_st, '%s', '0');
    'Now close shutter'
    while (clock - t_last < 60*off )  % off time
    end
    
    t_last = clock;
    fprintf(ser_st, '%s', '1');    
    'Now open shutter'
    while (clock - t_last < 60*on )  % on time
    end
end