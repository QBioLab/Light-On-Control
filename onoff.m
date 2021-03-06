% ser_st = serial('COM5', 'BaudRate', 57600);
% fopen(ser_st);
% 
% fprintf(ser_st, '%s', '1'); % open shutter
% fprintf(ser_st, '%s', '0'); % close shutter
fprintf(ser_st, '%s', '0'); % close shutter
t_last=clock;
timelabel(1).t0=t_last;
t0=sum(t_last(3:end).*[1440 60 1 1/60]*60)

ton=0:20:140;
toff=ton+5;
t1=t0;
t2=t0;
for i1=1:length(ton)
    % waiting for open
    while t1-t0 <= ton(i1)
        pause(0.1)
        t_next=clock;
        t1=sum(t_next(3:end).*[1440 60 1 1/60]*60);
    end
    timelabel(i1).ton=t_next;
    fprintf(ser_st, '%s', '1'); % open shutter
    [t1-t0 1 t_next(3:end)]
    % waiting for close
    while t1-t0 <= toff(i1)
        pause(0.1)
        t_next=clock;
        t1=sum(t_next(3:end).*[1440 60 1 1/60]*60);
    end
    fprintf(ser_st, '%s', '0'); % close shutter
    timelabel(i1).toff=t_next;
    [t1-t0 0 t_next(3:end)]
end

save ('spinningdisk-onoff-time-label.mat','timelabel','ton','toff');
    