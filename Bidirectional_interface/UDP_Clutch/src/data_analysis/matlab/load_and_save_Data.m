%%import data
% clear all;
% close all;
% clc;
cd('Archive')

flightstyle = {'torso_' ;
               'torso_arm_'};

phase_exp = {'s3_closedloop_' 's3_';
         's4_evaluation_' 's4_'};
         
measure = {'waypointDistTime_1.txt' 'wpdt';
           'TimeAngleRatePosRot_1.txt' 'arpr';
           'manoeuvreList_1.txt' 'manl'};
       
subject = struct([]);

for i = 1:35 % for all subjects
    for j = 1:2 % for all flight style
        for k = 1:2 % for all phases 
            for l = 1:3 % for all measures
                
                %create the name of the file
                subject_name = sprintf('subject_%d',i);
                file_name = strjoin([subject_name, '_', flightstyle(j), phase_exp(k,1), measure(l,1)],'');

                %test if the file exist
                if exist(file_name,'file') > 0
                    varname = genvarname(strjoin([flightstyle(j), phase(k,2), measure(l,2)],''));
                    subject(i).(varname) = importdata(file_name);
                    
                    %delete line with '-1' in WPdt files (mainly at the end of the file)
                    if(l == 1)
                        if(~all(all(subject(i).(varname).data(1:end,:)>-0.5)))
                            subject(i).(varname).data = subject(i).(varname).data(1:end-1,:);
                        end
                    end
                end
                
            end
        end
    end
end

clearvars file_name flightstyle i j k l measure phase subject_name varname

%save data
save('closed_loop_data.mat','subject');

%clear all;
